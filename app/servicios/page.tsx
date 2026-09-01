import type { Metadata } from 'next';
import Link from 'next/link';
import { SERVICIOS } from '@/content/servicios';

export const metadata: Metadata = {
  title: 'Servicios de automatización e IA',
  description:
    'Automatización de procesos, integración de sistemas y APIs, apps web y móviles, bases de datos, agentes de IA y dashboards. Pereira, todo el país.',
  alternates: { canonical: '/servicios' },
  // Sin esto, al compartir cualquier página salía el título de la portada.
  openGraph: { title: 'Servicios de automatización e IA', description: 'Automatización de procesos, integración de sistemas y APIs, apps web y móviles, bases de datos, agentes de IA y dashboards. Pereira, todo el país.' },
};

export default function ServiciosPage() {
  return (
    <main>
      <section className="sec sec--air">
        <div className="wrap">
          <p className="label sec-kicker">Servicios</p>
          <h1>
            <span className="h1-frase">Ocho frentes,<br />una sola disciplina</span>
            <span className="h1-clave">Servicios de automatización de procesos, integración de sistemas, análisis de datos e inteligencia artificial en Colombia</span>
          </h1>
          <p className="lede bloque--angosto">
            Todo lo que construyo comparte el mismo estándar: datos ordenados en PostgreSQL,
            sistemas que no tocan tu operación crítica, y registro auditable de cada cosa que pasa.
            El frente cambia; la ingeniería no.
          </p>
        </div>
      </section>

      <section className="sec sec--tight">
        <div className="wrap">
          <div className="lista">
            {SERVICIOS.map((s, i) => (
              <Link key={s.slug} href={`/servicios/${s.slug}`} className="card card--fila">
                <span className="fila-num" aria-hidden="true">{String(i + 1).padStart(2, '0')}</span>
                <span>
                  <h3>{s.titulo}</h3>
                  <p>{s.corto}</p>
                </span>
                <span className="go">Ver el servicio →</span>
              </Link>
            ))}
          </div>
        </div>
      </section>
    </main>
  );
}
