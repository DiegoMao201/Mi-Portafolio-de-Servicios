'use client';

import { useEffect } from 'react';

type Gtag = (...a: unknown[]) => void;
/** Envía un evento a Google Analytics si está cargado; si lo bloquearon, no pasa nada. */
export function evento(nombre: string, datos: Record<string, unknown> = {}) {
  const g = (window as unknown as { gtag?: Gtag }).gtag;
  if (g) g('event', nombre, datos);
}

/** Cuenta cada clic a WhatsApp, venga del botón flotante o de cualquier enlace del sitio. */
export default function Medicion() {
  useEffect(() => {
    const clic = (e: MouseEvent) => {
      const a = (e.target as HTMLElement | null)?.closest('a');
      if (a && /wa\.me\//.test(a.getAttribute('href') ?? '')) evento('contacto_whatsapp', { ubicacion: location.pathname });
    };
    document.addEventListener('click', clic, { capture: true });
    return () => document.removeEventListener('click', clic, { capture: true });
  }, []);
  return null;
}
