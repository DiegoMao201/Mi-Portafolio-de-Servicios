'use client';

import { useRef, useState } from 'react';
import ArchGraph, { GraphEdge, GraphNode } from './ArchGraph';

type Msg = { role: 'user' | 'assistant'; content: string };
type Arch = { titulo?: string; nodos: GraphNode[]; conexiones: GraphEdge[]; fases?: { titulo: string; detalle: string }[] };

function visible(text: string): string {
  return text
    .replace(/<lead>[\s\S]*?(<\/lead>|$)/g, '')
    .replace(/<arquitectura>[\s\S]*?(<\/arquitectura>|$)/g, '')
    .trim();
}

function extractArch(text: string): Arch | null {
  const m = text.match(/<arquitectura>([\s\S]*?)<\/arquitectura>/);
  if (!m) return null;
  try {
    const j = JSON.parse(m[1]);
    if (Array.isArray(j.nodos) && Array.isArray(j.conexiones) && j.nodos.length >= 2) return j as Arch;
  } catch { /* json inválido: se ignora */ }
  return null;
}

const SUGERENCIAS = [
  'Se me pierde el inventario entre bodegas',
  'Pago a proveedores cruzando Excels a mano',
  'Quiero vender en línea sin depender de nadie',
  'Necesito saber mi margen real por producto',
];

export default function Diagnosticador() {
  const [msgs, setMsgs] = useState<Msg[]>([]);
  const [input, setInput] = useState('');
  const [busy, setBusy] = useState(false);
  const [off, setOff] = useState<string | null>(null);
  const [arch, setArch] = useState<Arch | null>(null);
  const listRef = useRef<HTMLDivElement>(null);
  const sessionRef = useRef<string>(Math.random().toString(36).slice(2));

  async function send(text: string) {
    const q = text.trim();
    if (!q || busy) return;
    const history: Msg[] = [...msgs, { role: 'user', content: q }];
    setMsgs([...history, { role: 'assistant', content: '' }]);
    setInput('');
    setBusy(true);
    try {
      const res = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ messages: history, session: sessionRef.current }),
      });
      if (!res.ok) {
        const j = await res.json().catch(() => ({}));
        const why =
          j.error === 'rate_limit' || j.error === 'session_limit'
            ? 'Llegamos al límite de esta conversación. Sigamos por WhatsApp: +57 320 504 6277, o déjame tus datos en el formulario de contacto.'
            : 'El asistente está descansando un momento. Escríbeme directo por WhatsApp +57 320 504 6277 o usa el formulario de contacto.';
        setOff(why);
        setMsgs(history);
        return;
      }
      const reader = res.body!.getReader();
      const dec = new TextDecoder();
      let acc = '';
      for (;;) {
        const { done, value } = await reader.read();
        if (done) break;
        acc += dec.decode(value, { stream: true });
        const shown = visible(acc);
        setMsgs([...history, { role: 'assistant', content: shown }]);
        const a = extractArch(acc);
        if (a) setArch(a);
        listRef.current?.scrollTo({ top: 1e6 });
      }
      const finalArch = extractArch(acc);
      if (finalArch) setArch(finalArch);
      setMsgs([...history, { role: 'assistant', content: visible(acc) || '…' }]);
    } catch {
      setOff('Se cortó la conexión. Escríbeme por WhatsApp +57 320 504 6277 y seguimos allá.');
      setMsgs(history);
    } finally {
      setBusy(false);
      listRef.current?.scrollTo({ top: 1e6 });
    }
  }

  return (
    <div className="diag" id="diagnosticador">
      <div className="diag-chat">
        <div className="diag-head">
          <span className="label">El Diagnosticador</span>
          <span className="label" style={{ color: 'var(--machine-dim)' }}>IA · respuestas sobre casos reales</span>
        </div>
        <div className="diag-msgs" ref={listRef}>
          {msgs.length === 0 ? (
            <>
              <div className="msg a">
                <p>Cuéntame qué proceso te está costando tiempo o plata — con tus palabras, sin tecnicismos.</p>
                <p>Te muestro aquí mismo, dibujado, cómo se resolvería.</p>
              </div>
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8 }}>
                {SUGERENCIAS.map((s) => (
                  <button
                    key={s}
                    onClick={() => send(s)}
                    style={{
                      background: 'transparent', border: '1px solid var(--machine-line)',
                      color: 'var(--machine-dim)', padding: '7px 12px', cursor: 'pointer',
                      fontSize: 13, fontFamily: 'var(--font-serif), Georgia, serif',
                    }}
                  >
                    {s}
                  </button>
                ))}
              </div>
            </>
          ) : (
            msgs.map((m, i) => (
              <div key={i} className={`msg ${m.role === 'user' ? 'u' : 'a'}`}>
                {m.content ? (
                  m.content.split('\n').filter(Boolean).map((p, k) => <p key={k}>{p}</p>)
                ) : (
                  <span className="typing"><i /><i /><i /></span>
                )}
              </div>
            ))
          )}
          {off ? <div className="msg a"><p>{off}</p></div> : null}
        </div>
        <form
          className="diag-form"
          onSubmit={(e) => { e.preventDefault(); send(input); }}
        >
          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Describe tu cuello de botella…"
            maxLength={1200}
            aria-label="Describe tu problema"
            disabled={busy || !!off}
          />
          <button type="submit" disabled={busy || !input.trim() || !!off}>Enviar</button>
        </form>
      </div>
      <div className="diag-canvas">
        <span className="label">Boceto de tu solución — se dibuja en vivo</span>
        {arch ? (
          <>
            {arch.titulo ? (
              <div style={{ fontFamily: 'var(--font-archivo), sans-serif', fontWeight: 600, fontSize: 15, margin: '2px 0 8px', color: 'var(--machine-ink)' }}>
                {arch.titulo}
              </div>
            ) : null}
            <ArchGraph nodos={arch.nodos} conexiones={arch.conexiones} dark />
            {arch.fases?.length ? (
              <div className="fases">
                {arch.fases.slice(0, 4).map((f, i) => (
                  <div className="fase" key={i}><b>F{i + 1} · {f.titulo}</b>{f.detalle}</div>
                ))}
              </div>
            ) : null}
            <p style={{ fontSize: 12, color: 'var(--machine-dim)', marginTop: 12 }}>
              Boceto preliminar generado por IA. El diagnóstico formal lo confirma con tus datos reales.
            </p>
          </>
        ) : (
          <div className="diag-empty">
            <p>
              Aquí aparecerá el diagrama de tu solución:<br />
              qué sistemas se conectan, qué datos viajan y en qué fases.
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
