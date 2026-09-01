import Link from 'next/link';
import { SITE, waLink } from '@/lib/site';

export default function Footer() {
  return (
    <footer className="site-footer">
      <div className="wrap">
        <div>
          <div className="f-sign">Diego Mauricio García R.</div>
          <div className="f-sub">DATOVATE NEXUS PRO</div>
          {/* --machine-dim es tinta de zona oscura. Aqui el fondo es claro (--void):
              daba 2.47:1, muy por debajo de AA. */}
          <p style={{ color: 'var(--ink-2)', fontSize: 14.5, maxWidth: '42ch' }}>
            Automatización, sistemas e inteligencia artificial construidos y operados desde
            Pereira, Colombia, para empresas de todo el país. La tecnología que vendo es la que
            uso todos los días en mis propias operaciones.
          </p>
          <p style={{ fontSize: 14.5 }}>
            <a href={`mailto:${SITE.email}`}>{SITE.email}</a>
            <a href={waLink('Hola Diego, quiero hablar sobre un proyecto.')} target="_blank" rel="noopener">
              WhatsApp +57 320 504 6277
            </a>
          </p>
        </div>
        <div>
          <h4>Servicios</h4>
          <Link href="/servicios/automatizacion-de-procesos">Automatización</Link>
          <Link href="/servicios/integracion-de-sistemas-y-apis">Integraciones y APIs</Link>
          <Link href="/servicios/aplicaciones-web-a-la-medida">Apps web a la medida</Link>
          <Link href="/servicios/agentes-de-ia-conversacional">Agentes de IA</Link>
          <Link href="/servicios">Todos los servicios</Link>
        </div>
        <div>
          <h4>Sitio</h4>
          <Link href="/casos">Casos reales</Link>
          <Link href="/metodo">Método de trabajo</Link>
          <Link href="/notas">Notas técnicas</Link>
          <Link href="/diego">Quién está detrás</Link>
          <Link href="/contacto">Contacto</Link>
        </div>
      </div>
      <div className="f-legal">
        <span>© {new Date().getFullYear()} Datovate Nexus Pro · Pereira, Colombia</span>
        <span>
          <Link href="/privacidad">Privacidad</Link> · <Link href="/habeas-data">Habeas data</Link> ·{' '}
          <Link href="/terminos">Términos</Link>
        </span>
      </div>
    </footer>
  );
}
