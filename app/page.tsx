import Link from 'next/link';
import Brain from '@/components/Brain';
import Wordmark from '@/components/Wordmark';
import Console from '@/components/Console';
import Ticker from '@/components/Ticker';
import Diagnosticador from '@/components/Diagnosticador';
import Vena from '@/components/Vena';
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
          {/* La frase se queda por su fuerza, pero no puede ser TODO el h1: no
              lleva un solo término por el que alguien busque. La línea
              descriptiva —que ya existía debajo— pasa a vivir dentro del h1.
              Se ve exactamente igual; lo que cambia es qué entiende un
              buscador o un asistente al leer el encabezado de la página. */}
          <h1>
            <span className="h1-frase">
              No vendo software.
              <br />
              <em>Opero con él.</em>
            </span>
            <span className="hero-sub h1-clave">
              Automatización de procesos, integración de sistemas y análisis de datos con IA
              para empresas colombianas. Los mismos sistemas que construyo llevan años
              operando mi propia compañía, todos los días, sin interrupciones.
            </span>
          </h1>
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

      {/* 01 · El Diagnosticador — apretada arriba, y el panel sale a sangre */}
      <section className="sec sec--tight" id="diag-sec">
        <span className="sec-num" aria-hidden="true">01</span>
        <div className="wrap">
          <div className="sec-head">
            <p className="label sec-kicker">El Diagnosticador</p>
            <h2>Cuéntale tu problema.<br />Mira cómo se resuelve, dibujado en vivo.</h2>
          </div>
          <p className="lede">
            No te pido que imagines lo que hago: descríbele tu cuello de botella al asistente y
            te devuelve, en segundos, el boceto de la arquitectura que lo resolvería.
          </p>
        </div>
      </section>

      <Vena de={13} a={13} />

      <div className="banda">
        <div className="wrap wrap--ancho">
          <Diagnosticador />
        </div>
      </div>

      <Vena de={13} a={26} />

      {/* 02 · Servicios — la columna izquierda se queda fija, las tarjetas corren */}
      <section className="sec sec--split">
        <span className="sec-num" aria-hidden="true">02</span>
        <div className="wrap">
          <div className="riel-fijo">
            <div className="sec-head">
              <p className="label sec-kicker">Ocho frentes, una sola disciplina</p>
              <h2>Qué construyo</h2>
            </div>
            <p className="lede">
              El frente cambia; la ingeniería no. Datos ordenados, sistemas que no tocan tu
              operación crítica y registro auditable de todo.
            </p>
            <p style={{ marginTop: 20 }}>
              <Link href="/servicios">Ver los ocho servicios →</Link>
            </p>
          </div>
          <div className="grid g2 grid--escalonada">
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

      <Vena de={26} a={12} />

      {/* 03 · Casos — mucho aire, y el carril se sale por la derecha */}
      <section className="sec sec--air sec--colgada">
        <span className="sec-num" aria-hidden="true">03</span>
        <div className="wrap">
          <div className="sec-head">
            <p className="label sec-kicker">Expedientes técnicos, no testimonios</p>
            <h2>Sistemas que ya están trabajando</h2>
          </div>
          <p className="lede bloque--angosto">
            Cada caso cuenta el problema, la restricción, la arquitectura y el resultado medible.
            Sin capturas de clientes y sin revelar cómo funciona nada por dentro.
          </p>
        </div>
        <div className="carril">
          {CASOS.map((c) => (
            <Link key={c.slug} href={`/casos/${c.slug}`} className="card">
              <span className="label">{c.codigo} · {c.cliente.split('·')[0].split('—')[0]}</span>
              <h3>{c.titulo}</h3>
              <p>{c.resumen}</p>
              <span className="go">Abrir expediente →</span>
            </Link>
          ))}
        </div>
        <div className="wrap">
          <p className="carril-pie">Los cinco expedientes · desliza →</p>
        </div>
      </section>

      <Vena de={12} a={88} />

      {/* 04 · Oferta — anclada a la derecha, el numeral sangra por ese lado */}
      <section className="sec sec--derecha sec--linea">
        <span className="sec-num" aria-hidden="true">04</span>
        <div className="wrap">
          <div className="bloque--derecha">
            <div className="sec-head">
              <p className="label sec-kicker">Sin letra pequeña</p>
              <h2>Cómo se empieza</h2>
            </div>
            <div className="scroll-x">
              <table>
                <thead>
                  <tr><th>Paso</th><th>Qué recibes</th><th>Inversión</th></tr>
                </thead>
                <tbody>
                  <tr>
                    <td><strong>Llamada de 30 minutos</strong></td>
                    <td data-col="Qué recibes">Conversación técnica sobre tu operación. Sin compromiso y sin libreto de ventas.</td>
                    <td className="mono tnum" data-col="Inversión">Gratis</td>
                  </tr>
                  <tr>
                    <td><strong>Diagnóstico de operación</strong></td>
                    <td data-col="Qué recibes">En 5 días hábiles: mapa de tu proceso, dónde se pierde tiempo y plata, arquitectura propuesta, plan por fases y estimado de inversión. <strong>Se abona el 100% al proyecto</strong> si contratas dentro de los 30 días.</td>
                    <td className="mono tnum" data-col="Inversión">COP $300.000</td>
                  </tr>
                  <tr>
                    <td><strong>Construcción</strong></td>
                    <td data-col="Qué recibes">El sistema completo en producción: datos, integraciones, aplicación, despliegue y capacitación. Por hitos verificables.</td>
                    <td className="mono tnum" data-col="Inversión">$2.000.000 a $5.000.000</td>
                  </tr>
                  <tr>
                    <td><strong>Operación y evolución</strong></td>
                    <td data-col="Qué recibes">El sistema vivo: monitoreo, soporte, mejoras y nuevas automatizaciones cada mes. El valor depende de la complejidad de lo que hay que vigilar.</td>
                    <td className="mono tnum" data-col="Inversión">desde $150.000/mes</td>
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
        </div>
      </section>
    </main>
  );
}
