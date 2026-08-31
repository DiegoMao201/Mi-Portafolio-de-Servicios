import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Términos de uso',
  description: 'Términos de uso del sitio datovatenexuspro.com.',
  alternates: { canonical: '/terminos' },
};

export default function TerminosPage() {
  return (
    <main className="sec">
      <div className="wrap prose">
        <p className="label sec-kicker">Legal</p>
        <h1 style={{ fontSize: 'clamp(26px,3.6vw,38px)' }}>Términos de uso</h1>
        <h2>El sitio y su contenido</h2>
        <p>
          Este sitio presenta los servicios profesionales de Datovate Nexus Pro (Diego Mauricio
          García R.). Los contenidos —textos, casos, diagramas y cifras— son informativos y de
          propiedad de su autor; puedes citarlos con enlace a la fuente.
        </p>
        <h2>El asistente conversacional</h2>
        <p>
          Las respuestas del asistente de este sitio son generadas por inteligencia artificial
          sobre información verificada del negocio y constituyen orientación preliminar, no una
          propuesta comercial ni asesoría profesional. Los bocetos de arquitectura que produce
          son preliminares: el alcance real de cualquier proyecto se define en el diagnóstico
          formal.
        </p>
        <h2>Precios y propuestas</h2>
        <p>
          Los valores publicados son de referencia en pesos colombianos y pueden ajustarse según
          el alcance de cada caso. Toda contratación se formaliza con una propuesta escrita
          aceptada por ambas partes.
        </p>
        <h2>Limitación</h2>
        <p>
          El sitio se ofrece &ldquo;tal cual&rdquo;. Se hace un esfuerzo razonable por mantener la
          información exacta y el servicio disponible, sin garantizar disponibilidad
          ininterrumpida.
        </p>
        <p style={{ color: 'var(--ink-3)', fontSize: 14 }}>Vigentes desde agosto de 2026.</p>
      </div>
    </main>
  );
}
