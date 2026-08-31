import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Tratamiento de datos personales',
  description: 'Política de tratamiento de datos personales de Datovate Nexus Pro conforme a la Ley 1581 de 2012 y el Decreto 1377 de 2013 (Colombia).',
  alternates: { canonical: '/habeas-data' },
};

export default function HabeasDataPage() {
  return (
    <main className="sec">
      <div className="wrap prose">
        <p className="label sec-kicker">Legal</p>
        <h1 style={{ fontSize: 'clamp(26px,3.6vw,38px)' }}>Política de tratamiento de datos personales</h1>
        <p className="lede">Conforme a la Ley 1581 de 2012 y el Decreto 1377 de 2013 de la República de Colombia.</p>

        <h2>Responsable del tratamiento</h2>
        <p>
          Datovate Nexus Pro (Diego Mauricio García R.), con domicilio en Pereira, Risaralda,
          Colombia. Correo: diegomao.201@gmail.com. Teléfono: +57 320 504 6277.
        </p>

        <h2>Datos que se recogen y para qué</h2>
        <p>
          A través del formulario de contacto y del asistente conversacional de este sitio se
          recogen los datos que tú decides compartir: nombre, empresa, teléfono, correo
          electrónico y la descripción del proceso o necesidad que quieres resolver. Estos datos
          se usan exclusivamente para: responder tu solicitud, preparar propuestas de servicios,
          y mantener comunicación comercial contigo sobre los servicios de este sitio.
        </p>

        <h2>Tratamiento del asistente conversacional</h2>
        <p>
          Las conversaciones con el asistente de este sitio se procesan mediante proveedores de
          modelos de inteligencia artificial y pueden almacenarse para atender tu solicitud y
          mejorar el servicio. No incluyas en el chat información sensible: no es necesaria para
          atenderte.
        </p>

        <h2>Tus derechos</h2>
        <p>
          Como titular de los datos puedes: conocer, actualizar y rectificar tus datos; solicitar
          prueba de la autorización otorgada; ser informado sobre el uso que se les ha dado;
          presentar quejas ante la Superintendencia de Industria y Comercio; revocar la
          autorización y solicitar la supresión de tus datos cuando no exista un deber legal o
          contractual que lo impida.
        </p>

        <h2>Cómo ejercerlos</h2>
        <p>
          Escribe a diegomao.201@gmail.com indicando tu solicitud. Las consultas se
          atienden en un máximo de diez (10) días hábiles y los reclamos en un máximo de quince
          (15) días hábiles, conforme a la ley.
        </p>

        <h2>Conservación y seguridad</h2>
        <p>
          Los datos se almacenan en bases de datos con acceso restringido, se conservan mientras
          exista una relación comercial o interés legítimo de contacto, y se suprimen a solicitud
          del titular. No se venden ni se comparten con terceros con fines comerciales.
        </p>

        <p style={{ color: 'var(--ink-3)', fontSize: 14 }}>
          Vigente desde agosto de 2026. Esta política puede actualizarse; la versión publicada en
          esta página es la vigente.
        </p>
      </div>
    </main>
  );
}
