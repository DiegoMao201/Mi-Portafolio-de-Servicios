import { ImageResponse } from 'next/og';

export const runtime = 'nodejs';
export const alt = 'Diego Mauricio García R. — Datovate Nexus Pro';
export const size = { width: 1200, height: 630 };
export const contentType = 'image/png';

// La marca DV, la misma del favicon, dibujada para la tarjeta social.
function Mark({ s = 92 }: { s?: number }) {
  return (
    <svg width={s} height={s} viewBox="0 0 64 64">
      <rect width="64" height="64" rx="13" fill="#0D1418" />
      <path
        d="M11 13h13c9.9 0 17 7.6 17 19s-7.1 19-17 19H11V13zm9 8.5v21h4.2c5.1 0 8.4-4 8.4-10.5S29.3 21.5 24.2 21.5H20z"
        fill="#FF7440"
      />
      <path
        d="M25.5 17.5l10.8 27.2 10.8-27.2"
        fill="none"
        stroke="#3FD8CE"
        strokeWidth="7.4"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
      <circle cx="47.5" cy="16" r="6.2" fill="#0D1418" stroke="#3FD8CE" strokeWidth="4" />
    </svg>
  );
}

export default function OgImage() {
  return new ImageResponse(
    (
      <div
        style={{
          width: '100%',
          height: '100%',
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'space-between',
          background: '#090D10',
          padding: 68,
          color: '#E9EDEE',
          fontFamily: 'sans-serif',
          position: 'relative',
        }}
      >
        {/* filo de señal superior */}
        <div
          style={{
            position: 'absolute',
            top: 0,
            left: 0,
            width: 1200,
            height: 4,
            display: 'flex',
            background: 'linear-gradient(90deg, #FF7440 0%, #3FD8CE 60%, rgba(63,216,206,0) 100%)',
          }}
        />

        <div style={{ display: 'flex', alignItems: 'center', gap: 22 }}>
          <Mark s={82} />
          <div style={{ display: 'flex', flexDirection: 'column' }}>
            <span style={{ fontSize: 30, fontWeight: 700, letterSpacing: -0.5 }}>
              Diego Mauricio García R.
            </span>
            <span style={{ fontSize: 17, color: '#FF7440', letterSpacing: 7 }}>DATOVATE NEXUS PRO</span>
          </div>
        </div>

        <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
          <div style={{ fontSize: 82, fontWeight: 700, lineHeight: 1.04, display: 'flex', flexDirection: 'column' }}>
            <span>No vendo software.</span>
            <span style={{ color: '#FF7440' }}>Opero con él.</span>
          </div>
          <span style={{ fontSize: 26, color: '#9FADB4', maxWidth: 900 }}>
            Automatización, integración de sistemas y agentes de IA que ya operan empresas reales.
          </span>
        </div>

        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <span style={{ fontSize: 21, color: '#3FD8CE', letterSpacing: 5 }}>
            PEREIRA, COLOMBIA · OPERACIÓN CONTINUA
          </span>
          <span style={{ fontSize: 24, color: '#E9EDEE' }}>datovatenexuspro.com</span>
        </div>
      </div>
    ),
    size
  );
}
