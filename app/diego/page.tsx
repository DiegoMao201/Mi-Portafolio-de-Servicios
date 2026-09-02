import type { Metadata } from 'next';
import Link from 'next/link';
import { waLink } from '@/lib/site';

export const metadata: Metadata = {
  title: 'Ingeniero industrial en automatización e IA',
  description:
    'Ingeniero industrial de la Universidad Tecnológica de Pereira. Inteligencia de negocios, automatización e IA aplicada a operaciones reales.',
  alternates: { canonical: '/diego' },
  // Sin esto, al compartir cualquier página salía el título de la portada.
  openGraph: { title: 'Ingeniero industrial en automatización e IA', description: 'Ingeniero industrial de la Universidad Tecnológica de Pereira. Inteligencia de negocios, automatización e IA aplicada a operaciones reales.' },
};

export default function DiegoPage() {
  return (
    <main>
      <section className="sec sec--air sec--retrato">
        <div className="wrap">
          <div>
            <p className="label sec-kicker">Quién está detrás</p>
            <h1>
              <span className="h1-frase" style={{ maxWidth: '13ch' }}>Diego Mauricio García R.</span>
              <span className="h1-clave">Ingeniero industrial de la UTP. Automatización de procesos, inteligencia de negocios e IA aplicada en Pereira, Colombia</span>
            </h1>
            <p className="lede">
              Ingeniero industrial de la Universidad Tecnológica de Pereira y desarrollador de
              software. Vengo del liderazgo de compras y la gestión comercial en el sector de
              recubrimientos, adhesivos y suministros industriales — es decir, conozco por dentro
              la operación que hoy automatizo. Esa combinación, entender el negocio y además
              construir el sistema, define cómo trabajo.
            </p>
          </div>

          {/* Sin recuadro: el sujeto va recortado y la sombra sigue su silueta,
              que es lo que lo despega de la página. Detrás, el halo de la casa y
              una línea de horizonte que él tapa — ahí nace la profundidad. */}
          <figure className="retrato">
            {/* El nombre del archivo lleva la huella del contenido: si la foto cambia,
                  cambia la URL. Reemplazar un archivo conservando el nombre deja a los
                  navegadores sirviendo la version vieja durante horas. */}
            <span className="retrato-halo" aria-hidden="true" />
            <picture>
              <source srcSet="/diego-6c8f3375.webp" type="image/webp" />
              <img
                src="/diego-6c8f3375.png"
                width={644}
                height={744}
                alt="Diego Mauricio García R., ingeniero industrial, en Pereira, Colombia"
                loading="eager"
                decoding="async"
              />
            </picture>
            <figcaption>Pereira · Risaralda · Colombia</figcaption>
          </figure>
        </div>
      </section>

      {/* La ficha se queda fija a la derecha mientras se lee la historia */}
      <section className="sec sec--tight sec--split sec--invertida">
        <div className="wrap">
          <div>
            <div className="exp-block">
              <span className="label">De dónde vengo</span>
              <ul className="clean">
                <li><strong>Ingeniería y gestión comercial.</strong> Egresado de la Universidad Tecnológica de Pereira. Años liderando compras y gestión comercial en el sector de recubrimientos, adhesivos y suministros industriales: presupuestos, proveedores, inventario y margen, vistos desde adentro.</li>
                <li><strong>Inteligencia de negocios y desarrollo.</strong> Construyo herramientas de análisis y plataformas web con Python, FastAPI, Next.js, PostgreSQL y SQL Server, orientadas al control de inventarios, la optimización de compras y el análisis financiero.</li>
                <li><strong>Inteligencia artificial aplicada.</strong> Diseño y orquestación de agentes conversacionales: recuperación sobre bases propias, integración de modelos de lenguaje y automatizaciones sobre WhatsApp Cloud API.</li>
                <li><strong>Emprendimiento digital.</strong> Fundador de Bigotes y Paticas, una plataforma de gestión y servicios para mascotas que opera sobre sistemas construidos por mí.</li>
              </ul>
            </div>

            <div className="exp-block">
              <span className="label">Por qué soy distinto a una agencia</span>
              <p>
                Una agencia te entrega el software y factura. Yo administro empresas que funcionan
                sobre mis propios desarrollos: la tesorería que paga proveedores, el e-commerce que
                factura, el programa de puntos que fideliza, los motores que deciden en milisegundos.
                Esos sistemas llevan años funcionando todos los días, y yo dependo de ellos igual
                que mis clientes. Operarlos a diario produce un tipo de ingeniería que no se aprende
                haciendo demostraciones: sistemas aburridos de tan confiables, con registro de todo,
                que avisan solos cuando algo se sale de rango.
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
          </div>

          <aside className="riel-fijo">
            <div className="ficha">
              <div>
                <span className="label">Stack de todos los días</span>
                <p>Python · PostgreSQL · Next.js · TypeScript · FastAPI · Docker · IA aplicada (Claude, GPT, modelos abiertos) · despliegue propio en la nube</p>
              </div>
              <div>
                <span className="label">Datos formales</span>
                <p>
                  Diego Mauricio García R. — Pereira, Risaralda, Colombia.<br />
                  <strong>NIT 1088266407</strong>, consultable en el registro mercantil.<br />
                  Datovate Nexus Pro es la marca comercial bajo la que opero.
                </p>
              </div>
            </div>
          </aside>
        </div>
      </section>

      <section className="sec sec--tight sec--linea">
        <div className="wrap">
          <div className="bloque--angosto">
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
        </div>
      </section>
    </main>
  );
}
