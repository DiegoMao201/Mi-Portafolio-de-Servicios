import type { Metadata } from 'next';
import Link from 'next/link';
import { notFound } from 'next/navigation';
import { CASOS, getCaso } from '@/content/casos';
import ArchGraph from '@/components/ArchGraph';
import { SITE, waLink } from '@/lib/site';

export function generateStaticParams() {
  return CASOS.map((c) => ({ slug: c.slug }));
}

export async function generateMetadata({ params }: { params: Promise<{ slug: string }> }): Promise<Metadata> {
  const { slug } = await params;
  const c = getCaso(slug);
  if (!c) return {};
  return {
    title: `${c.codigo} · ${c.titulo}`,
    description: c.resumen.slice(0, 155),
    alternates: { canonical: `/casos/${c.slug}` },
  };
}

export default async function CasoPage({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  const c = getCaso(slug);
  if (!c) notFound();

  const jsonld = {
    '@context': 'https://schema.org',
    '@type': 'BreadcrumbList',
    itemListElement: [
      { '@type': 'ListItem', position: 1, name: 'Casos', item: `${SITE.url}/casos` },
      { '@type': 'ListItem', position: 2, name: c.titulo, item: `${SITE.url}/casos/${c.slug}` },
    ],
  };

  return (
    <main className="sec">
      <div className="wrap">
        <p className="label sec-kicker">
          <Link href="/casos" style={{ color: 'inherit' }}>Casos</Link> / {c.codigo}
        </p>
        <h1 style={{ fontSize: 'clamp(30px,4.4vw,48px)', maxWidth: '24ch' }}>{c.titulo}</h1>
        <div className="exp-meta">
          <span className="pill">{c.codigo}</span>
          <span className="pill">{c.cliente}</span>
          <span className="pill pill-ok">En operación</span>
        </div>

        <div className="exp-block">
          <span className="label">Contexto</span>
          {c.contexto.map((p, i) => <p key={i}>{p}</p>)}
        </div>

        <div className="callout">
          <p><strong>La restricción.</strong> {c.restriccion}</p>
        </div>

        <div className="exp-block">
          <span className="label">Arquitectura</span>
          <ul className="clean">
            {c.arquitectura.map((a, i) => <li key={i}>{a}</li>)}
          </ul>
          <ArchGraph
            nodos={c.diagrama.nodos}
            conexiones={c.diagrama.conexiones}
            caption={`Fig. — ${c.codigo}. El diagrama se traza como se diseñó el sistema; los pulsos marcan el flujo del dato.`}
          />
        </div>

        <div className="exp-block">
          <span className="label">Resultado</span>
          <ul className="clean">
            {c.resultado.map((r, i) => <li key={i}><strong>{r}</strong></li>)}
          </ul>
        </div>

        <div className="exp-block">
          <span className="label">Stack</span>
          <p className="mono" style={{ fontSize: 14, color: 'var(--ink-2)' }}>{c.stack.join(' · ')}</p>
        </div>

        <div className="hero-actions">
          <Link className="btn btn-signal" href="/contacto">Mi operación tiene algo parecido</Link>
          <a className="btn btn-line" href={waLink(`Hola Diego, leí el caso "${c.titulo}" y tengo una situación parecida.`)} target="_blank" rel="noopener">Contar mi caso por WhatsApp</a>
        </div>
      </div>
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonld) }} />
    </main>
  );
}
