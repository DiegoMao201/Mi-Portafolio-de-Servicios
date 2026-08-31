import { NextRequest } from 'next/server';
import { allow, clientIp, ipHash } from '@/lib/ratelimit';
import { saveLead } from '@/lib/db';
import { notifyLead } from '@/lib/sendgrid';

export const runtime = 'nodejs';
export const dynamic = 'force-dynamic';

export async function POST(req: NextRequest) {
  const ip = clientIp(req);
  const hash = ipHash(ip);
  if (!allow(`lead:${hash}`, 5, 60 * 60 * 1000)) {
    return Response.json({ error: 'rate_limit' }, { status: 429 });
  }

  let body: Record<string, string>;
  try {
    body = await req.json();
  } catch {
    return Response.json({ error: 'bad_request' }, { status: 400 });
  }

  // Honeypot anti-spam: campo invisible que los humanos dejan vacío
  if (body.web) return Response.json({ ok: true });

  const clean = (v: unknown, max = 300) => (typeof v === 'string' ? v.trim().slice(0, max) : '');
  const nombre = clean(body.nombre, 120);
  const telefono = clean(body.telefono, 40);
  const email = clean(body.email, 160);
  const empresa = clean(body.empresa, 160);
  const mensaje = clean(body.mensaje, 2000);

  if (!mensaje || (!telefono && !email)) {
    return Response.json({ error: 'faltan_datos' }, { status: 400 });
  }

  await saveLead({ nombre, empresa, telefono, email, canal: 'formulario', mensaje, ip_hash: hash, origen_url: clean(body.origen, 300) });
  await notifyLead({ nombre, empresa, telefono, email, mensaje, canal: 'formulario' });
  return Response.json({ ok: true });
}
