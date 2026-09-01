import type { Metadata } from 'next';
import Link from 'next/link';
import { CASOS } from '@/content/casos';

export const metadata: Metadata = {
  title: 'Casos reales: sistemas en operación',
  description:
    'Expedientes técnicos de sistemas en operación: tesorería automatizada, recaudo digital, e-commerce, motores de decisión y agentes de IA.',
  alternates: { canonical: '/casos' },
};

export default function CasosPage() {
  return (
    <main>
      <section className="sec sec--air">
        <div className="wrap">
          <p className="label sec-kicker">Casos</p>
          <h1>Expedientes<br />técnicos</h1>
          <p className="lede bloque--angosto">
            Aquí no hay testimonios con foto de banco de imágenes. Hay cinco sistemas reales,
            contados como se diseñaron: el problema, la restricción que lo hacía difícil,
            la arquitectura que lo resolvió y el resultado que se puede medir.
          </p>
          <p className="lede bloque--angosto" style={{ marginTop: 12 }}>
            Lo que no vas a encontrar: URLs de clientes ni el mecanismo interno de nada — esa
            misma discreción te cubre a ti cuando trabajemos juntos.
          </p>
        </div>
      </section>

      <section className="sec sec--tight">
        <div className="wrap">
          <div className="grid expedientes">
            {CASOS.map((c) => (
              <Link key={c.slug} href={`/casos/${c.slug}`} className="card card--exp">
                <span className="exp-cod" aria-hidden="true">{c.codigo}</span>
                <span className="label">{c.codigo} · {c.cliente}</span>
                <h3>{c.titulo}</h3>
                <p>{c.resumen}</p>
                <span className="go">Abrir expediente →</span>
              </Link>
            ))}
          </div>
        </div>
      </section>
    </main>
  );
}
