import Link from 'next/link';
import Brain from '@/components/Brain';
import Wordmark from '@/components/Wordmark';
import Console from '@/components/Console';
import Conduit from '@/components/Conduit';
import Ticker from '@/components/Ticker';
import Diagnosticador from '@/components/Diagnosticador';
import { SERVICIOS } from '@/content/servicios';
import { CASOS } from '@/content/casos';
import { waLink } from '@/lib/site';

export default function Home() {
  return (
    <main>
      {/* Sala de máquinas */}
      <section className="machine">
        <Brain />
        <div className="wrap">
          <Wordmark />
          <p className="hero-eyebrow">Pereira, Colombia · Sistemas en operación continua</p>
          <h1>
            No vendo software.
            <br />
            <em>Opero con él.</em>
          </h1>
          <p className="hero-sub">
            Automatizo tesorería, inventario y ventas para empresas colombianas. Los mismos
            sistemas que construyo llevan años operando mi propia compañía, todos los días,
            sin interrupciones.
          </p>
          <div className="hero-actions">
            <a className="btn btn-signal" href="#diagnosticador">Diagnostica tu proceso con IA</a>
            <Link className="btn btn-ghost" href="/casos">Ver los sistemas en operación</Link>
          </div>
          <Console />
          <p style={{ fontFamily: 'var(--font-mono), monospace', fontSize: 10.5, color: 'var(--machine-dim)', letterSpacing: '.06em', margin: '10px 2px 0' }}>
            CIFRAS REALES DE SISTEMAS CONSTRUIDOS Y OPERADOS POR DIEGO — PASA EL CURSOR POR CADA UNA PARA VER SU ORIGEN
          </p>
        </div>
      </section>

      <Ticker />

      {/* El Diagnosticador */}
      <section className="sec" id="diag-sec">
        <div className="wrap">
          <div className="sec-head">
            <span className="sec-num">01</span>
            <div>
              <p className="label sec-kicker">El Diagnosticador</p>
              <h2>Cuéntale tu problema. Mira cómo se resuelve, dibujado en vivo.</h2>
            </div>
          </div>
          <p className="lede">
            No te pido que imagines lo que hago: descríbele tu cuello de botella al asistente y
            te devuelve, en segundos, el boceto de la arquitectura que lo resolvería. Te vas de
            esta página con algo en la mano.
          </p>
          <Diagnosticador />
        </div>
      </section>

      <Conduit x={22} />

      {/* Servicios */}
      <section className="sec">
        <div className="wrap">
          <div className="sec-head">
            <span className="sec-num">02</span>
            <div>
              <p className="label sec-kicker">Ocho frentes, una sola disciplina</p>
              <h2>Qué construyo</h2>
            </div>
          </div>
          <div className="grid g3" style={{ marginTop: 26 }}>
            {SERVICIOS.map((s) => (
              <Link key={s.slug} href={`/servicios/${s.slug}`} className="card">
                <h3>{s.titulo}</h3>
                <p>{s.corto}</p>
                <span className="go">Ver el servicio →</span>
              </Link>
            ))}
          </div>
        </div>
      </section>

      <Conduit x={78} />

      {/* Casos */}
      <section className="sec">
        <div className="wrap">
          <div className="sec-head">
            <span className="sec-num">03</span>
            <div>
              <p className="label sec-kicker">Expedientes técnicos, no testimonios</p>
              <h2>Sistemas que ya están trabajando</h2>
            </div>
          </div>
          <p className="lede">
            Cada caso cuenta el problema, la restricción, la arquitectura y el resultado medible.
            Sin capturas de pantalla de clientes y sin revelar cómo funciona nada por dentro:
            la confianza se construye con resultados, no regalando ingeniería.
          </p>
          <div className="grid g3" style={{ marginTop: 22 }}>
            {CASOS.slice(0, 3).map((c) => (
              <Link key={c.slug} href={`/casos/${c.slug}`} className="card">
                <span className="label">{c.codigo} · {c.cliente.split('·')[0].split('—')[0]}</span>
                <h3>{c.titulo}</h3>
                <p>{c.resumen}</p>
                <span className="go">Abrir expediente →</span>
              </Link>
            ))}
          </div>
          <p style={{ marginTop: 18 }}>
            <Link href="/casos">Ver los cinco expedientes →</Link>
          </p>
        </div>
      </section>

      <Conduit x={40} />

      {/* Oferta */}
      <section className="sec">
        <div className="wrap">
          <div className="sec-head">
            <span className="sec-num">04</span>
            <div>
              <p className="label sec-kicker">Sin letra pequeña</p>
              <h2>Cómo se empieza</h2>
            </div>
          </div>
          <div className="scroll-x">
            <table>
              <thead>
                <tr><th>Paso</th><th>Qué recibes</th><th>Inversión</th></tr>
              </thead>
              <tbody>
                <tr>
                  <td><strong>Llamada de 30 minutos</strong></td>
                  <td>Conversación técnica sobre tu operación. Sin compromiso y sin libreto de ventas.</td>
                  <td className="mono tnum">Gratis</td>
                </tr>
                <tr>
                  <td><strong>Diagnóstico de operación</strong></td>
                  <td>En 5 días hábiles: mapa de tu proceso, dónde se pierde tiempo y plata, arquitectura propuesta, plan por fases y estimado de inversión. <strong>Se abona el 100% al proyecto</strong> si contratas dentro de los 30 días.</td>
                  <td className="mono tnum">COP $690.000</td>
                </tr>
                <tr>
                  <td><strong>Construcción</strong></td>
                  <td>El sistema completo en producción: datos, integraciones, aplicación, despliegue y capacitación. Por hitos verificables.</td>
                  <td className="mono tnum">desde $3.900.000</td>
                </tr>
                <tr>
                  <td><strong>Operación y evolución</strong></td>
                  <td>El sistema vivo: monitoreo, soporte, mejoras y nuevas automatizaciones cada mes.</td>
                  <td className="mono tnum">desde $890.000/mes</td>
                </tr>
              </tbody>
            </table>
          </div>
          <div className="callout">
            <p>
              <strong>Cobertura nacional.</strong> Opero desde Pereira para empresas de todo el país.
              El trabajo es remoto por diseño: los sistemas se monitorean, se corrigen y se
              actualizan en línea, sin depender de visitas presenciales.
            </p>
          </div>
          <div className="hero-actions" style={{ marginTop: 8 }}>
            <Link className="btn btn-signal" href="/contacto">Agendar la llamada gratis</Link>
            <a className="btn btn-line" href={waLink('Hola Diego, quiero agendar la llamada de 30 minutos.')} target="_blank" rel="noopener">
              Escribir por WhatsApp
            </a>
          </div>
        </div>
      </section>
    </main>
  );
}
