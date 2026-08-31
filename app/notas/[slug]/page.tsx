import type { Metadata } from 'next';
import Link from 'next/link';
import { notFound } from 'next/navigation';
import { NOTAS, getNota } from '@/content/notas';
import { SITE } from '@/lib/site';

export function generateStaticParams() {
  return NOTAS.map((n) => ({ slug: n.slug }));
}

export async function generateMetadata({ params }: { params: Promise<{ slug: string }> }): Promise<Metadata> {
  const { slug } = await params;
  const n = getNota(slug);
  if (!n) return {};
  return {
    title: n.titulo,
    description: n.descripcion.slice(0, 155),
    alternates: { canonical: `/notas/${n.slug}` },
  };
}

export default async function NotaPage({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  const n = getNota(slug);
  if (!n) notFound();

  const jsonld = {
    '@context': 'https://schema.org',
    '@type': 'Article',
    headline: n.titulo,
    description: n.descripcion,
    datePublished: n.fecha,
    inLanguage: 'es-CO',
    author: { '@id': `${SITE.url}/#diego` },
    publisher: { '@id': `${SITE.url}/#org` },
    mainEntityOfPage: `${SITE.url}/notas/${n.slug}`,
  };

  return (
    <main className="sec">
      <div className="wrap">
        <p className="label sec-kicker">
          <Link href="/notas" style={{ color: 'inherit' }}>Notas</Link> · {new Date(n.fecha + 'T12:00:00Z').toLocaleDateString('es-CO', { year: 'numeric', month: 'long', day: 'numeric' })}
        </p>
        <article className="prose">
          <h1 style={{ fontSize: 'clamp(28px,4vw,42px)', marginBottom: 14 }}>{n.titulo}</h1>
          <p className="lede">{n.descripcion}</p>
          {n.parrafos.map((p, i) => (
            <div key={i}>
              {p.h ? <h2>{p.h}</h2> : null}
              <p>{p.t}</p>
            </div>
          ))}
        </article>
        <div className="callout" style={{ maxWidth: '70ch' }}>
          <p>
            <strong>¿Estás en esta situación?</strong> Escríbeme y te digo sin compromiso si tu
            caso se resuelve así o de otra forma: <Link href="/contacto">contacto</Link>.
          </p>
        </div>
      </div>
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonld) }} />
    </main>
  );
}
