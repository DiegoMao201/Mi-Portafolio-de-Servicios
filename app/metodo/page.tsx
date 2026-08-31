import type { Metadata } from 'next';
import Link from 'next/link';
import ArchGraph from '@/components/ArchGraph';

export const metadata: Metadata = {
  title: 'Método de trabajo',
  description:
    'Cómo trabajo: diagnóstico con datos reales, arquitectura antes que código, construcción por fases verificables y operación continua. Método empírico: nada se afirma sin verificarse.',
  alternates: { canonical: '/metodo' },
};

export default function MetodoPage() {
  return (
    <main className="sec">
      <div className="wrap">
        <p className="label sec-kicker">Método</p>
        <h1 style={{ fontSize: 'clamp(30px,4.4vw,48px)' }}>Empírico, por fases, sin humo</h1>
        <p className="lede">
          Mi método viene de operar sistemas donde equivocarse cuesta dinero propio en minutos.
          De ahí sale una regla que aplico a todo: <strong>nada se afirma sin verificarse contra
          datos reales.</strong> Ni un diagnóstico, ni una estimación, ni un &ldquo;ya quedó&rdquo;.
        </p>

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
          caption="Fig. — Las cuatro fases. Ninguna se salta; el tamaño de cada una depende de tu caso."
        />

        <div className="exp-block">
          <span className="label">1 · Diagnóstico</span>
          <p>
            Cinco días hábiles trabajando con tu proceso real: quién hace qué, con qué archivos y
            sistemas, cuánto se demora, dónde se equivoca. El entregable es un documento que vale
            por sí solo — mapa del proceso, dónde se pierde tiempo y plata, la arquitectura
            propuesta y el estimado por fases — y es tuyo aunque no sigas conmigo.
          </p>
        </div>
        <div className="exp-block">
          <span className="label">2 · Arquitectura</span>
          <p>
            El diseño se decide antes de escribir código, con tres reglas que no negocio: los
            sistemas fuente no se tocan (se lee de ellos sin intervenirlos), toda pieza crítica
            queda aislada de los experimentos, y cada acción del sistema deja registro auditable.
          </p>
        </div>
        <div className="exp-block">
          <span className="label">3 · Construcción por fases</span>
          <p>
            Hitos de una a tres semanas, cada uno con algo funcionando que puedes verificar.
            Pago por hitos (40/30/30): nunca pagas por promesas, pagas por software que ya
            puedes usar. Si en algún hito decides parar, lo construido queda tuyo y operando.
          </p>
        </div>
        <div className="exp-block">
          <span className="label">4 · Operación</span>
          <p>
            Un sistema sin monitoreo es una promesa sin testigos. El plan mensual cubre
            vigilancia, soporte, ajustes y nuevas automatizaciones — y como administro empresas
            que dependen de mis propios sistemas, la operación no es un anexo del contrato:
            es donde vivo.
          </p>
        </div>

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
    </main>
  );
}
