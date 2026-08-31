import type { Metadata } from 'next';
import Link from 'next/link';

export const metadata: Metadata = {
  title: 'Aviso de privacidad',
  description: 'Aviso de privacidad del sitio datovatenexuspro.com: qué datos se recogen, con qué finalidad y cómo ejercer tus derechos.',
  alternates: { canonical: '/privacidad' },
};

export default function PrivacidadPage() {
  return (
    <main className="sec">
      <div className="wrap prose">
        <p className="label sec-kicker">Legal</p>
        <h1 style={{ fontSize: 'clamp(26px,3.6vw,38px)' }}>Aviso de privacidad</h1>
        <p className="lede">
          Este sitio recoge únicamente los datos que tú decides compartir para que pueda
          responderte: nombre, contacto y la descripción de tu necesidad.
        </p>
        <h2>Lo esencial</h2>
        <p>
          El responsable del tratamiento es Datovate Nexus Pro (Diego Mauricio García R.),
          Pereira, Colombia. Los datos se usan para responder tu solicitud y mantener
          comunicación comercial contigo; no se venden ni se comparten con terceros con fines
          comerciales. Puedes conocer, actualizar, rectificar o suprimir tus datos escribiendo a
          diegomao.201@gmail.com.
        </p>
        <h2>Medición del sitio</h2>
        <p>
          Este sitio puede usar Google Analytics para medir visitas de forma agregada. Puedes
          bloquear estas mediciones con las herramientas de tu navegador sin que el sitio deje de
          funcionar.
        </p>
        <p>
          El detalle completo está en la <Link href="/habeas-data">política de tratamiento de
          datos personales</Link>, conforme a la Ley 1581 de 2012.
        </p>
      </div>
    </main>
  );
}
