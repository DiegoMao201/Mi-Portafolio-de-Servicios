import Link from 'next/link';

export default function Header() {
  return (
    <header className="site-header">
      <div className="wrap">
        <Link href="/" className="brand" aria-label="Inicio">
          <b>DIEGO MAURICIO GARCÍA R.</b>
          <span>DATOVATE NEXUS PRO</span>
        </Link>
        <nav className="nav" aria-label="Principal">
          <Link href="/servicios">Servicios</Link>
          <Link href="/casos">Casos</Link>
          <Link href="/metodo">Método</Link>
          <Link href="/notas">Notas</Link>
          <Link href="/diego">Diego</Link>
          <Link href="/contacto" className="cta">Hablemos</Link>
        </nav>
      </div>
    </header>
  );
}
