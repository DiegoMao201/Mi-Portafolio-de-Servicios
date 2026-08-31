'use client';

import { useState } from 'react';

export default function LeadForm() {
  const [state, setState] = useState<'idle' | 'busy' | 'ok' | 'err'>('idle');

  async function onSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const form = e.currentTarget;
    const data = Object.fromEntries(new FormData(form).entries());
    setState('busy');
    try {
      const res = await fetch('/api/lead', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ...data, origen: window.location.href }),
      });
      if (res.ok) { setState('ok'); form.reset(); }
      else setState('err');
    } catch {
      setState('err');
    }
  }

  if (state === 'ok') {
    return (
      <div className="callout">
        <p><strong>Recibido.</strong> Leo cada mensaje personalmente y te escribo en el transcurso del día. Si es urgente: WhatsApp +57 320 504 6277.</p>
      </div>
    );
  }

  return (
    <form className="form" onSubmit={onSubmit}>
      <label>
        <span className="lb">Tu nombre</span>
        <input name="nombre" maxLength={120} autoComplete="name" />
      </label>
      <label>
        <span className="lb">Empresa (opcional)</span>
        <input name="empresa" maxLength={160} autoComplete="organization" />
      </label>
      <label>
        <span className="lb">WhatsApp o teléfono</span>
        <input name="telefono" maxLength={40} inputMode="tel" autoComplete="tel" />
      </label>
      <label>
        <span className="lb">Correo</span>
        <input name="email" type="email" maxLength={160} autoComplete="email" />
      </label>
      <label>
        <span className="lb">¿Qué proceso te está doliendo?</span>
        <textarea name="mensaje" required maxLength={2000} placeholder="Con tus palabras: qué se hace a mano, qué se pierde, qué quieres lograr." />
      </label>
      <label className="hp" aria-hidden="true" tabIndex={-1}>
        Sitio web
        <input name="web" tabIndex={-1} autoComplete="off" />
      </label>
      <p style={{ fontSize: 13, color: 'var(--ink-3)' }}>
        Al enviar aceptas la <a href="/habeas-data">política de tratamiento de datos</a>. Deja al menos un teléfono o un correo.
      </p>
      {state === 'err' ? (
        <p style={{ color: 'var(--signal)', fontSize: 14.5 }}>
          No se pudo enviar. Intenta de nuevo o escríbeme directo: WhatsApp +57 320 504 6277.
        </p>
      ) : null}
      <button className="btn btn-signal" type="submit" disabled={state === 'busy'}>
        {state === 'busy' ? 'Enviando…' : 'Enviar mensaje'}
      </button>
    </form>
  );
}
