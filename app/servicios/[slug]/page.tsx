import type { Metadata } from 'next';
import Link from 'next/link';
import { notFound } from 'next/navigation';
import { SERVICIOS, getServicio } from '@/content/servicios';
import { getCaso } from '@/content/casos';
import ArchGraph from '@/components/ArchGraph';
import { SITE, waLink } from '@/lib/site';

export function generateStaticParams() {
  return SERVICIOS.map((s) => ({ slug: s.slug }));
}

export async function generateMetadata({ params }: { params: Promise<{ slug: string }> }): Promise<Metadata> {
  const { slug } = await params;
  const s = getServicio(slug);
  if (!s) return {};
  return {
    title: s.tituloSeo || s.titulo,
    description: s.respuesta.slice(0, 155),
    alternates: { canonical: `/servicios/${s.slug}` },
  };
}

export default async function ServicioPage({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  const s = getServicio(slug);
  if (!s) notFound();
  const caso = getCaso(s.casoSlug);

  const jsonld = {
    '@context': 'https://schema.org',
    '@graph': [
      {
        '@type': 'Service',
        name: s.titulo,
        description: s.respuesta,
        provider: { '@id': `${SITE.url}/#org` },
        areaServed: 'CO',
        url: `${SITE.url}/servicios/${s.slug}`,
      },
      {
        '@type': 'FAQPage',
        mainEntity: s.faq.map((f) => ({
          '@type': 'Question',
          name: f.q,
          acceptedAnswer: { '@type': 'Answer', text: f.a },
        })),
      },
      {
        '@type': 'BreadcrumbList',
        itemListElement: [
          { '@type': 'ListItem', position: 1, name: 'Servicios', item: `${SITE.url}/servicios` },
          { '@type': 'ListItem', position: 2, name: s.titulo, item: `${SITE.url}/servicios/${s.slug}` },
        ],
      },
    ],
  };

  return (
    <main className="sec">
      <div className="wrap">
        <p className="label sec-kicker">
          <Link href="/servicios" style={{ color: 'inherit' }}>Servicios</Link> / {s.titulo}
        </p>
        <h1 style={{ fontSize: 'clamp(30px,4.4vw,48px)', maxWidth: '22ch' }}>{s.titulo}</h1>
        <p className="lede"><strong>{s.respuesta}</strong></p>

        <div className="exp-block">
          <span className="label">El problema</span>
          {s.problema.map((p, i) => <p key={i}>{p}</p>)}
        </div>

        <div className="exp-block">
          <span className="label">Cómo lo abordo</span>
          <ul className="clean">
            {s.metodo.map((m, i) => <li key={i}>{m}</li>)}
          </ul>
        </div>

        <div className="grid g2" style={{ margin: '26px 0' }}>
          <div className="card">
            <span className="label">Qué recibes</span>
            <ul className="clean" style={{ margin: 0 }}>
              {s.entregables.map((e, i) => <li key={i} style={{ fontSize: 15 }}>{e}</li>)}
            </ul>
          </div>
          <div className="card">
            <span className="label">Tecnologías</span>
            <p>{s.tecnologias.join(' · ')}</p>
            <span className="label" style={{ marginTop: 14 }}>Cómo se empieza</span>
            <p>
              Llamada de 30 minutos gratis. Después, diagnóstico de operación por COP $690.000
              (5 días hábiles) que se abona completo al proyecto si contratas en 30 días.
            </p>
          </div>
        </div>

        {caso ? (
          <div className="exp-block">
            <span className="label">Caso real relacionado — {caso.codigo}</span>
            <h3 style={{ marginBottom: 6 }}>
              <Link href={`/casos/${caso.slug}`} style={{ color: 'inherit' }}>{caso.titulo}</Link>
            </h3>
            <p>{caso.resumen}</p>
            <ArchGraph nodos={caso.diagrama.nodos} conexiones={caso.diagrama.conexiones} caption={`Fig. — Arquitectura del caso ${caso.codigo}, dibujada como se diseñó.`} />
          </div>
        ) : null}

        <div className="exp-block">
          <span className="label">Preguntas frecuentes</span>
          {s.faq.map((f, i) => (
            <div key={i} style={{ marginBottom: 18, maxWidth: '70ch' }}>
              <h3 style={{ fontSize: 16.5, marginBottom: 6 }}>{f.q}</h3>
              <p style={{ color: 'var(--ink-2)' }}>{f.a}</p>
            </div>
          ))}
        </div>

        <div className="callout">
          <p>
            <strong>¿Este es tu caso?</strong> Cuéntamelo con tus palabras y te digo, sin humo,
            si se puede resolver y cuánto costaría averiguarlo con certeza.
          </p>
        </div>
        <div className="hero-actions">
          <Link className="btn btn-signal" href="/contacto">Agendar la llamada gratis</Link>
          <a className="btn btn-line" href={waLink(`Hola Diego, me interesa el servicio de ${s.titulo}.`)} target="_blank" rel="noopener">WhatsApp directo</a>
        </div>
      </div>
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonld) }} />
    </main>
  );
}
