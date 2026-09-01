import { NextRequest } from 'next/server';
import { systemPrompt } from '@/agent/prompt';
import { allow, clientIp, ipHash } from '@/lib/ratelimit';
import { monthSpendUSD, saveLead, logConversation } from '@/lib/db';
import { notifyLead } from '@/lib/sendgrid';

export const runtime = 'nodejs';
export const dynamic = 'force-dynamic';

const MAX_TURNS = 12;
const MAX_LEN = 1200;

type Msg = { role: 'user' | 'assistant'; content: string };

export async function POST(req: NextRequest) {
  const apiKey = process.env.OPENROUTER_API_KEY;
  if (!apiKey) return Response.json({ error: 'chat_off' }, { status: 503 });

  const ip = clientIp(req);
  const hash = ipHash(ip);
  if (!allow(`chat:${hash}`, 40, 24 * 60 * 60 * 1000) || !allow(`chatmin:${hash}`, 8, 60 * 1000)) {
    return Response.json({ error: 'rate_limit' }, { status: 429 });
  }

  const budget = parseFloat(process.env.LLM_BUDGET_USD || '25');
  if ((await monthSpendUSD()) >= budget) {
    return Response.json({ error: 'budget' }, { status: 503 });
  }

  let body: { messages?: Msg[]; session?: string };
  try {
    body = await req.json();
  } catch {
    return Response.json({ error: 'bad_request' }, { status: 400 });
  }
  const messages = (body.messages || [])
    .filter((m) => m && (m.role === 'user' || m.role === 'assistant') && typeof m.content === 'string')
    .slice(-MAX_TURNS * 2)
    .map((m) => ({ role: m.role, content: m.content.slice(0, MAX_LEN) }));
  if (!messages.length || messages[messages.length - 1].role !== 'user') {
    return Response.json({ error: 'bad_request' }, { status: 400 });
  }
  const userTurns = messages.filter((m) => m.role === 'user').length;
  if (userTurns > MAX_TURNS) return Response.json({ error: 'session_limit' }, { status: 429 });

  // 'openrouter/auto' enruta a lo que esté barato en ese momento: por eso el
  // Diagnosticador respondía flojo y con el mismo esquema siempre. El modelo se
  // fija; la variable de entorno sigue mandando si Diego quiere cambiarlo.
  const model = process.env.OPENROUTER_MODEL || 'anthropic/claude-opus-5';

  // El corpus (servicios, casos, precios) es el mismo en cada turno y es la
  // mayor parte del prompt. En los modelos de Anthropic se marca como cacheable
  // y se cobra a una fracción a partir del segundo turno. Solo se manda esta
  // forma cuando el modelo la entiende: en otros proveedores rompería.
  const sistema = systemPrompt();
  const anthropic = model.startsWith('anthropic/');
  const mensajeSistema = anthropic
    ? { role: 'system', content: [{ type: 'text', text: sistema, cache_control: { type: 'ephemeral' } }] }
    : { role: 'system', content: sistema };
  const upstream = await fetch('https://openrouter.ai/api/v1/chat/completions', {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${apiKey}`,
      'Content-Type': 'application/json',
      'HTTP-Referer': process.env.SITE_URL || 'https://www.datovatenexuspro.com',
      'X-Title': 'Datovate Nexus Pro',
    },
    body: JSON.stringify({
      model,
      stream: true,
      usage: { include: true },
      // 900 no alcanzaba: la respuesta lleva el texto, el bloque de
      // arquitectura (hasta 8 nodos) y a veces el de lead. Se truncaba el JSON
      // y el diagrama no llegaba a dibujarse.
      max_tokens: 2400,
      temperature: 0.4,
      messages: [mensajeSistema, ...messages],
    }),
  });

  if (!upstream.ok || !upstream.body) {
    console.error('[chat] OpenRouter error', upstream.status, await upstream.text().catch(() => ''));
    return Response.json({ error: 'upstream' }, { status: 502 });
  }

  let full = '';
  let cost = 0;
  let tokensIn = 0;
  let tokensOut = 0;
  const decoder = new TextDecoder();
  let carry = '';

  const session = (body.session || '').slice(0, 64) || 'anon';

  const stream = new ReadableStream<Uint8Array>({
    async start(controller) {
      const encoder = new TextEncoder();
      const reader = upstream.body!.getReader();
      try {
        for (;;) {
          const { done, value } = await reader.read();
          if (done) break;
          carry += decoder.decode(value, { stream: true });
          const lines = carry.split('\n');
          carry = lines.pop() || '';
          for (const line of lines) {
            const t = line.trim();
            if (!t.startsWith('data:')) continue;
            const data = t.slice(5).trim();
            if (data === '[DONE]') continue;
            try {
              const j = JSON.parse(data);
              const delta = j.choices?.[0]?.delta?.content;
              if (typeof delta === 'string' && delta) {
                full += delta;
                controller.enqueue(encoder.encode(delta));
              }
              if (j.usage) {
                cost = j.usage.cost ?? cost;
                tokensIn = j.usage.prompt_tokens ?? tokensIn;
                tokensOut = j.usage.completion_tokens ?? tokensOut;
              }
            } catch {
              /* línea parcial, se ignora */
            }
          }
        }
      } catch (e) {
        console.error('[chat] stream error', e);
      } finally {
        controller.close();
        // Efectos secundarios después de cerrar el stream (servidor persistente)
        void (async () => {
          try {
            const convId = await logConversation({
              session_id: session,
              ip_hash: hash,
              modelo: model,
              tokens_in: tokensIn,
              tokens_out: tokensOut,
              costo_usd: cost,
              mensajes: [...messages, { rol: 'assistant', contenido: full }].map((m) => ({
                rol: 'role' in m ? (m as Msg).role : (m as { rol: string }).rol,
                contenido: 'content' in m ? (m as Msg).content : (m as { contenido: string }).contenido,
              })),
            });
            const m = full.match(/<lead>([\s\S]*?)<\/lead>/);
            if (m) {
              const lead = JSON.parse(m[1]);
              // Candado: sin teléfono ni correo el lead no sirve (no hay a quién
              // responderle). El modelo a veces emite el bloque antes de tiempo.
              const contacto = String(lead.telefono || '').trim() || String(lead.email || '').trim();
              if (!contacto) {
                console.warn('[chat] lead descartado: sin teléfono ni correo', { session });
                return;
              }
              const transcript = messages.map((x) => `${x.role}: ${x.content}`).join('\n');
              await saveLead({
                nombre: lead.nombre || undefined,
                empresa: lead.empresa || undefined,
                telefono: lead.telefono || undefined,
                email: lead.email || undefined,
                canal: 'chat',
                proceso_dolor: lead.proceso_dolor || undefined,
                sistemas_actuales: lead.sistemas_actuales || undefined,
                urgencia: lead.urgencia || undefined,
                calificacion: typeof lead.calificacion === 'number' ? lead.calificacion : undefined,
                resumen_agente: lead.resumen || undefined,
                ip_hash: hash,
                conversation_id: convId,
              });
              await notifyLead(lead, transcript);
            }
          } catch (e) {
            console.error('[chat] post-proceso falló', e);
          }
        })();
      }
    },
  });

  return new Response(stream, {
    headers: {
      'Content-Type': 'text/plain; charset=utf-8',
      'Cache-Control': 'no-store',
      'X-Accel-Buffering': 'no',
    },
  });
}
