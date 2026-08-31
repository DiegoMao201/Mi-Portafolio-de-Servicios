import type { Metadata } from 'next';
import Link from 'next/link';
import { SERVICIOS } from '@/content/servicios';

export const metadata: Metadata = {
  title: 'Servicios de automatización e IA',
  description:
    'Automatización de procesos, integración de sistemas y APIs, apps web y móviles, bases de datos, agentes de IA y dashboards. Pereira, todo el país.',
  alternates: { canonical: '/servicios' },
};

export default function ServiciosPage() {
  return (
    <main className="sec">
      <div className="wrap">
        <p className="label sec-kicker">Servicios</p>
        <h1 style={{ fontSize: 'clamp(30px,4.4vw,48px)' }}>Ocho frentes, una sola disciplina</h1>
        <p className="lede">
          Todo lo que construyo comparte el mismo estándar: datos ordenados en PostgreSQL,
          sistemas que no tocan tu operación crítica, y registro auditable de cada cosa que pasa.
          El frente cambia; la ingeniería no.
        </p>
        <div className="grid g-servicios" style={{ marginTop: 30 }}>
          {SERVICIOS.map((s) => (
            <Link key={s.slug} href={`/servicios/${s.slug}`} className="card">
              <h3>{s.titulo}</h3>
              <p>{s.corto}</p>
              <span className="go">Ver el servicio →</span>
            </Link>
          ))}
        </div>
      </div>
    </main>
  );
}
