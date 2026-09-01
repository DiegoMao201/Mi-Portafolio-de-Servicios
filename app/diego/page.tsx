import type { Metadata } from 'next';
import Link from 'next/link';
import { waLink } from '@/lib/site';

export const metadata: Metadata = {
  title: 'Diego Mauricio García R.',
  description:
    'Ingeniero industrial de la Universidad Tecnológica de Pereira. Inteligencia de negocios, automatización e IA aplicada a operaciones reales.',
  alternates: { canonical: '/diego' },
};

export default function DiegoPage() {
  return (
    <main className="sec">
      <div className="wrap">
        <p className="label sec-kicker">Quién está detrás</p>
        <h1 style={{ fontSize: 'clamp(30px,4.4vw,48px)', maxWidth: '18ch' }}>
          Diego Mauricio García R.
        </h1>
        <p className="lede">
          Ingeniero industrial de la Universidad Tecnológica de Pereira, dedicado a la
          inteligencia de negocios y la automatización. Administro empresas que funcionan
          sobre los sistemas que yo mismo construyo: esa combinación —diseñar la solución y
          además operarla a diario— define cómo trabajo.
        </p>

        <div className="exp-block">
          <span className="label">Por qué soy distinto a una agencia</span>
          <p>
            Una agencia te entrega el software y factura. Yo administro empresas que funcionan
            sobre mis propios desarrollos: la tesorería que paga proveedores, el e-commerce que
            factura, el programa de puntos que fideliza, los motores que deciden en milisegundos.
            Cuando un sistema mío falla, no pierde &ldquo;el cliente&rdquo; — pierdo yo, esa misma tarde.
            Esa presión, sostenida durante años, produce un tipo de ingeniería que no se aprende
            haciendo demos: sistemas aburridos de tan confiables, con registro de todo, que se
            avisan solos cuando algo se sale de rango.
          </p>
        </div>

        <div className="exp-block">
          <span className="label">Cómo pienso</span>
          <ul className="clean">
            <li><strong>Empírico primero.</strong> Ninguna hipótesis sobrevive sin datos. Si un número no se puede verificar, no se afirma — ni en un diagnóstico, ni en este sitio.</li>
            <li><strong>Lo crítico se aísla.</strong> Ningún experimento, ninguna IA, ningún proceso nuevo puede poner en riesgo la operación que factura. Es la regla número uno de todas mis arquitecturas.</li>
            <li><strong>El criterio es humano.</strong> Automatizo el cálculo, el cruce, el trámite. La decisión de negocio —qué pagar, qué comprar, a quién— sigue siendo de quien debe tomarla, con mejor información.</li>
            <li><strong>Tu código es tuyo.</strong> Repositorio tuyo, servidor tuyo, datos tuyos. Trabajo para que quieras seguir conmigo, no para que no puedas irte.</li>
          </ul>
        </div>

        <div className="grid g2" style={{ margin: '10px 0 26px' }}>
          <div className="card">
            <span className="label">Stack de todos los días</span>
            <p>Python · PostgreSQL · Next.js · TypeScript · FastAPI · Docker · IA aplicada (Claude, GPT, modelos abiertos) · despliegue propio en la nube</p>
          </div>
          <div className="card">
            <span className="label">Datos formales</span>
            <p>
              Datovate Nexus Pro — Pereira, Risaralda, Colombia.<br />
              Facturación como empresa o como persona natural, según convenga a tu contabilidad.
            </p>
          </div>
        </div>

        <div className="callout">
          <p>
            <strong>Atiendo toda Colombia desde Pereira.</strong> Mis clientes casi nunca me ven
            la cara y sus sistemas funcionan igual: esto es tecnología, la distancia no es una
            limitante.
          </p>
        </div>

        <div className="hero-actions">
          <Link className="btn btn-signal" href="/contacto">Hablemos de tu operación</Link>
          <a className="btn btn-line" href={waLink('Hola Diego, leí tu página y quiero conversar.')} target="_blank" rel="noopener">WhatsApp +57 320 504 6277</a>
        </div>
      </div>
    </main>
  );
}
