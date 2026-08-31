import type { Metadata } from 'next';
import Link from 'next/link';
import { NOTAS } from '@/content/notas';

export const metadata: Metadata = {
  title: 'Notas técnicas',
  description:
    'Notas de ingeniería desde la trinchera: migrar Streamlit a producción, conectar SQL Server con PostgreSQL, agentes de IA que no tumban la operación.',
  alternates: { canonical: '/notas' },
};

export default function NotasPage() {
  return (
    <main className="sec">
      <div className="wrap">
        <p className="label sec-kicker">Notas</p>
        <h1 style={{ fontSize: 'clamp(30px,4.4vw,48px)' }}>Ingeniería desde la trinchera</h1>
        <p className="lede">
          Lo que aprendo construyendo y operando sistemas reales, escrito para que te sirva
          aunque nunca me contrates.
        </p>
        <div className="grid" style={{ marginTop: 26, maxWidth: 760 }}>
          {NOTAS.map((n) => (
            <Link key={n.slug} href={`/notas/${n.slug}`} className="card">
              <span className="label">{new Date(n.fecha + 'T12:00:00Z').toLocaleDateString('es-CO', { year: 'numeric', month: 'long' })}</span>
              <h3>{n.titulo}</h3>
              <p>{n.descripcion}</p>
              <span className="go">Leer la nota →</span>
            </Link>
          ))}
        </div>
      </div>
    </main>
  );
}
