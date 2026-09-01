import type { Metadata } from 'next';
import Link from 'next/link';
import ArchGraph from '@/components/ArchGraph';
import FasesMetodo from '@/components/FasesMetodo';

export const metadata: Metadata = {
  title: 'Método de trabajo',
  description:
    'Cómo trabajo: diagnóstico con datos reales, arquitectura antes que código, construcción por fases verificables y operación continua.',
  alternates: { canonical: '/metodo' },
  // Sin esto, al compartir cualquier página salía el título de la portada.
  openGraph: { title: 'Método de trabajo', description: 'Cómo trabajo: diagnóstico con datos reales, arquitectura antes que código, construcción por fases verificables y operación continua.' },
};

const FASES = [
  {
    n: '01',
    titulo: 'Diagnóstico',
    texto: (
      <>
        Cinco días hábiles trabajando con tu proceso real: quién hace qué, con qué archivos y
        sistemas, cuánto se demora, dónde se equivoca. El entregable es un documento que vale
        por sí solo — mapa del proceso, dónde se pierde tiempo y plata, la arquitectura
        propuesta y el estimado por fases — y es tuyo aunque no sigas conmigo.
      </>
    ),
  },
  {
    n: '02',
    titulo: 'Arquitectura',
    texto: (
      <>
        El diseño se decide antes de escribir código, con tres reglas que no negocio: los
        sistemas fuente no se tocan (se lee de ellos sin intervenirlos), toda pieza crítica
        queda aislada de los experimentos, y cada acción del sistema deja registro auditable.
      </>
    ),
  },
  {
    n: '03',
    titulo: 'Construcción por fases',
    texto: (
      <>
        Hitos de una a tres semanas, cada uno con algo funcionando que puedes verificar.
        Pago por hitos (40/30/30): nunca pagas por promesas, pagas por software que ya
        puedes usar. Si en algún hito decides parar, lo construido queda tuyo y operando.
      </>
    ),
  },
  {
    n: '04',
    titulo: 'Operación',
    texto: (
      <>
        Un sistema sin monitoreo es una promesa sin testigos. El plan mensual cubre
        vigilancia, soporte, ajustes y nuevas automatizaciones — y como administro empresas
        que dependen de mis propios sistemas, la operación no es un anexo del contrato:
        es donde vivo.
      </>
    ),
  },
];

export default function MetodoPage() {
  return (
    <main>
      <section className="sec sec--air">
        <div className="wrap">
          <p className="label sec-kicker">Método</p>
          <h1>Empírico, por fases,<br />sin humo</h1>
          <p className="lede bloque--angosto">
            Mi método viene de operar sistemas donde equivocarse cuesta dinero propio en minutos.
            De ahí sale una regla que aplico a todo: <strong>nada se afirma sin verificarse contra
            datos reales.</strong> Ni un diagnóstico, ni una estimación, ni un &ldquo;ya quedó&rdquo;.
          </p>
        </div>
      </section>

      {/* El diagrama deja de ser una cajita centrada: ocupa todo el ancho */}
      <div className="banda">
        <div className="wrap wrap--ancho">
          <ArchGraph
            nodos={[
              { id: 'diag', label: 'Diagnóstico', sub: '5 días · con tus datos', capa: 0 },
              { id: 'arq', label: 'Arquitectura', sub: 'antes que el código', capa: 1, acento: true },
              { id: 'build', label: 'Construcción por fases', sub: 'entregas verificables', capa: 2 },
              { id: 'op', label: 'Operación', sub: 'monitoreo y evolución', capa: 3 },
            ]}
            conexiones={[
              { de: 'diag', a: 'arq', dato: 'mapa del proceso' },
              { de: 'arq', a: 'build', dato: 'plan por fases' },
              { de: 'build', a: 'op', dato: 'sistema en producción' },
            ]}
            eje="horizontal"
            caption="Fig. — Las cuatro fases. Ninguna se salta; el tamaño de cada una depende de tu caso."
          />
        </div>
      </div>

      <section className="sec sec--split">
        <FasesMetodo fases={FASES} />
      </section>

      <section className="sec sec--tight sec--linea">
        <div className="wrap">
          <div className="bloque--derecha">
            <div className="callout">
              <p>
                <strong>Una cosa más:</strong> el código que construyo para ti es tuyo, en tu
                repositorio, con tu servidor. La continuidad conmigo se gana con resultados,
                no con candados.
              </p>
            </div>
            <div className="hero-actions">
              <Link className="btn btn-signal" href="/contacto">Empezar por la llamada gratis</Link>
            </div>
          </div>
        </div>
      </section>
    </main>
  );
}
