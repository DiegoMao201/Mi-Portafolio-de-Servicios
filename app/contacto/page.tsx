import type { Metadata } from 'next';
import LeadForm from '@/components/LeadForm';
import { SITE, waLink } from '@/lib/site';

export const metadata: Metadata = {
  title: 'Hablemos de automatizar tu operación',
  description:
    'Hablemos de tu operación: WhatsApp +57 320 504 6277, diegomao.201@gmail.com o el formulario. Llamada de 30 minutos gratis, sin libreto de ventas.',
  alternates: { canonical: '/contacto' },
  // Sin esto, al compartir cualquier página salía el título de la portada.
  openGraph: { title: 'Hablemos de automatizar tu operación', description: 'Hablemos de tu operación: WhatsApp +57 320 504 6277, diegomao.201@gmail.com o el formulario. Llamada de 30 minutos gratis, sin libreto de ventas.' },
};

export default function ContactoPage() {
  return (
    <main>
      <section className="sec sec--air">
        <div className="wrap">
          <p className="label sec-kicker">Contacto</p>
          <h1>
            <span className="h1-frase">Cuéntame<br />qué te duele</span>
            <span className="h1-clave">Hablemos de automatizar tu operación: procesos, inventario, tesorería y análisis de datos</span>
          </h1>
          <p className="lede bloque--angosto">
            Empezamos con una llamada de 30 minutos, gratis y sin libreto de ventas: tú me cuentas
            tu operación, yo te digo con franqueza qué se puede resolver y qué no vale la pena.
          </p>
        </div>
      </section>

      {/* Las tres vías quedan fijas a la izquierda mientras se llena el formulario */}
      <section className="sec sec--tight sec--split">
        <div className="wrap">
          <div className="riel-fijo">
            <p className="label sec-kicker">Por dónde prefieras</p>
            <div className="lista" style={{ marginTop: 14 }}>
              <a className="card card--fila card--via" href={waLink('Hola Diego, quiero agendar la llamada de 30 minutos.')} target="_blank" rel="noopener">
                <span>
                  <h3>WhatsApp</h3>
                  <p>+57 320 504 6277 — respondo personalmente.</p>
                </span>
                <span className="go">Abrir chat →</span>
              </a>
              <a className="card card--fila card--via" href={`mailto:${SITE.email}`}>
                <span>
                  <h3>Correo</h3>
                  <p>{SITE.email}</p>
                </span>
                <span className="go">Escribir →</span>
              </a>
              <a className="card card--fila card--via" href="/#diagnosticador">
                <span>
                  <h3>El Diagnosticador</h3>
                  <p>Descríbele tu problema a la IA y mira el boceto de la solución.</p>
                </span>
                <span className="go">Probar →</span>
              </a>
            </div>
          </div>

          <div>
            <h2 style={{ marginBottom: 20 }}>O deja el mensaje aquí</h2>
            <LeadForm />
          </div>
        </div>
      </section>
    </main>
  );
}
