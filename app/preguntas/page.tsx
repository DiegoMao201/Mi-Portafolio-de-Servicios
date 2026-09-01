import type { Metadata } from 'next';
import Link from 'next/link';
import { SERVICIOS } from '@/content/servicios';
import { SITE, waLink } from '@/lib/site';

export const metadata: Metadata = {
  title: 'Preguntas frecuentes sobre automatización e IA',
  description:
    'Respuestas directas: si hay que cambiar el ERP, qué pasa con los datos, cuánto cuesta, cuánto se demora, si el código queda tuyo y si la IA puede inventar. Colombia.',
  alternates: { canonical: '/preguntas' },
  // Sin esto, al compartir cualquier página salía el título de la portada.
  openGraph: { title: 'Preguntas frecuentes sobre automatización e IA', description: 'Respuestas directas: si hay que cambiar el ERP, qué pasa con los datos, cuánto cuesta, cuánto se demora, si el código queda tuyo y si la IA puede inventar. Colombia.' },
};

/**
 * Las 32 preguntas vivían enterradas dentro de cada página de servicio: solo las
 * veía quien ya había llegado hasta allí. Aquí quedan todas en un solo sitio
 * indexable, con FAQPage — que es el formato que un asistente de IA cita cuando
 * la pregunta del usuario coincide casi literalmente con el encabezado.
 *
 * Ni una palabra nueva: son las mismas respuestas de content/servicios.ts.
 */
/** Ancla estable y legible por persona: /preguntas#cambiar-mi-erp-o-software.
 *  Sin ancla, lo único citable es la página entera; con ancla, la respuesta. */
function ancla(q: string): string {
  return q
    .normalize('NFD').replace(/[\u0300-\u036f]/g, '')
    .toLowerCase()
    .replace(/[¿?¡!.,:;""'()]/g, '')
    .trim().split(/\s+/).slice(0, 7).join('-');
}

export default function PreguntasPage() {
  const grupos = SERVICIOS.filter((s) => s.faq.length > 0);
  const todas = grupos.flatMap((s) => s.faq);

  const jsonld = {
    '@context': 'https://schema.org',
    '@type': 'FAQPage',
    '@id': `${SITE.url}/preguntas#faq`,
    inLanguage: 'es-CO',
    about: { '@id': `${SITE.url}/#diego` },
    mainEntity: todas.map((f) => ({
      '@type': 'Question',
      '@id': `${SITE.url}/preguntas#${ancla(f.q)}`,
      url: `${SITE.url}/preguntas#${ancla(f.q)}`,
      name: f.q,
      inLanguage: 'es-CO',
      answerCount: 1,
      acceptedAnswer: {
        '@type': 'Answer',
        text: f.a,
        url: `${SITE.url}/preguntas#${ancla(f.q)}`,
        author: { '@id': `${SITE.url}/#diego` },
      },
    })),
  };

  return (
    <main>
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonld) }} />

      <section className="sec sec--air">
        <div className="wrap">
          <p className="label sec-kicker">Preguntas frecuentes</p>
          <h1>Lo que me preguntan<br />antes de contratar</h1>
          <p className="lede bloque--angosto">
            {todas.length} preguntas reales, respondidas sin rodeos: si hay que cambiar el ERP,
            qué pasa con los datos, cuánto cuesta mantenerlo, de quién es el código y qué
            ocurre el día que algo se cae.
          </p>
        </div>
      </section>

      {grupos.map((s, i) => (
        <section key={s.slug} className={`sec sec--tight${i === grupos.length - 1 ? ' sec--linea' : ''}`}>
          <div className="wrap">
            <div className="sec-head">
              <p className="label sec-kicker">
                <Link href={`/servicios/${s.slug}`} style={{ color: 'inherit' }}>{s.titulo}</Link>
              </p>
            </div>
            <div className="preguntas">
              {s.faq.map((f) => (
                <article key={f.q} id={ancla(f.q)} className="pregunta">
                  <h2>
                    <a href={`#${ancla(f.q)}`} className="pregunta-enlace">{f.q}</a>
                  </h2>
                  <p>{f.a}</p>
                </article>
              ))}
            </div>
          </div>
        </section>
      ))}

      <section className="sec sec--tight">
        <div className="wrap">
          <div className="bloque--angosto">
            <div className="callout">
              <p>
                <strong>¿Tu pregunta no está aquí?</strong> Escríbeme y te respondo yo mismo,
                con franqueza — incluso si la respuesta es que lo que necesitas no vale la pena.
              </p>
            </div>
            <div className="hero-actions">
              <Link className="btn btn-signal" href="/contacto">Hacer mi pregunta</Link>
              <a className="btn btn-line" href={waLink('Hola Diego, tengo una pregunta sobre mi operación.')} target="_blank" rel="noopener">
                Preguntar por WhatsApp
              </a>
            </div>
          </div>
        </div>
      </section>
    </main>
  );
}
