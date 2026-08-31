const API = 'https://api.sendgrid.com/v3/mail/send';

export async function sendMail(args: {
  to: string;
  subject: string;
  text: string;
  replyTo?: string;
}): Promise<boolean> {
  const key = process.env.SENDGRID_API_KEY;
  const from = process.env.MAIL_FROM || 'contacto@datovatenexuspro.com';
  if (!key) {
    console.warn('[mail] SENDGRID_API_KEY ausente; correo no enviado:', args.subject);
    return false;
  }
  try {
    const res = await fetch(API, {
      method: 'POST',
      headers: { Authorization: `Bearer ${key}`, 'Content-Type': 'application/json' },
      body: JSON.stringify({
        personalizations: [{ to: [{ email: args.to }] }],
        from: { email: from, name: 'Datovate Nexus Pro' },
        ...(args.replyTo ? { reply_to: { email: args.replyTo } } : {}),
        subject: args.subject,
        content: [{ type: 'text/plain', value: args.text }],
      }),
    });
    if (!res.ok) console.error('[mail] SendGrid respondió', res.status, await res.text());
    return res.ok;
  } catch (e) {
    console.error('[mail] Error enviando:', e);
    return false;
  }
}

export async function notifyLead(lead: Record<string, unknown>, transcript?: string) {
  const to = process.env.MAIL_TO || 'contacto@datovatenexuspro.com';
  const lines = Object.entries(lead)
    .filter(([, v]) => v !== undefined && v !== null && v !== '')
    .map(([k, v]) => `${k}: ${v}`)
    .join('\n');
  const text = `Nuevo lead en datovatenexuspro.com\n\n${lines}\n${transcript ? `\n--- Conversación ---\n${transcript}` : ''}`;
  await sendMail({ to, subject: `Lead: ${lead.nombre || lead.email || lead.telefono || 'sin nombre'}`, text });
  const email = typeof lead.email === 'string' ? lead.email : '';
  if (email && email.includes('@')) {
    await sendMail({
      to: email,
      subject: 'Recibí tu mensaje — Diego Mauricio García R.',
      text: `Hola${lead.nombre ? ` ${lead.nombre}` : ''},\n\nRecibí tu mensaje y lo voy a leer personalmente. Te escribo en el transcurso del día.\n\nSi es urgente: WhatsApp +57 320 504 6277.\n\nDiego Mauricio García R.\nDatovate Nexus Pro · datovatenexuspro.com`,
    });
  }
}
