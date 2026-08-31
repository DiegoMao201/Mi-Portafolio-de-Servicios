import type { Metadata } from 'next';
import LeadForm from '@/components/LeadForm';
import { SITE, waLink } from '@/lib/site';

export const metadata: Metadata = {
  title: 'Contacto',
  description:
    'Hablemos de tu operación: WhatsApp +57 320 504 6277, diegomao.201@gmail.com o el formulario. Llamada de 30 minutos gratis, sin libreto de ventas.',
  alternates: { canonical: '/contacto' },
};

export default function ContactoPage() {
  return (
    <main className="sec">
      <div className="wrap">
        <p className="label sec-kicker">Contacto</p>
        <h1 style={{ fontSize: 'clamp(30px,4.4vw,48px)' }}>Cuéntame qué te duele</h1>
        <p className="lede">
          Empezamos con una llamada de 30 minutos, gratis y sin libreto de ventas: tú me cuentas
          tu operación, yo te digo con franqueza qué se puede resolver y qué no vale la pena.
        </p>

        <div className="grid g3" style={{ margin: '26px 0 34px' }}>
          <a className="card" href={waLink('Hola Diego, quiero agendar la llamada de 30 minutos.')} target="_blank" rel="noopener">
            <span className="label">La vía rápida</span>
            <h3>WhatsApp</h3>
            <p>+57 320 504 6277 — respondo personalmente.</p>
            <span className="go">Abrir chat →</span>
          </a>
          <a className="card" href={`mailto:${SITE.email}`}>
            <span className="label">Para propuestas y documentos</span>
            <h3>Correo</h3>
            <p>{SITE.email}</p>
            <span className="go">Escribir →</span>
          </a>
          <a className="card" href="/#diagnosticador">
            <span className="label">¿Aún explorando?</span>
            <h3>El Diagnosticador</h3>
            <p>Descríbele tu problema a la IA y mira el boceto de la solución.</p>
            <span className="go">Probar →</span>
          </a>
        </div>

        <h2 style={{ marginBottom: 16 }}>O deja el mensaje aquí</h2>
        <LeadForm />
      </div>
    </main>
  );
}
