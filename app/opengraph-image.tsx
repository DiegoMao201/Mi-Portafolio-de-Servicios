import { ImageResponse } from 'next/og';

export const runtime = 'nodejs';
export const alt = 'Diego Mauricio García R. — Datovate Nexus Pro';
export const size = { width: 1200, height: 630 };
export const contentType = 'image/png';

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
          padding: 72,
          color: '#E9EDEE',
          fontFamily: 'sans-serif',
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: 14, color: '#3FD8CE', fontSize: 22, letterSpacing: 6 }}>
          <div style={{ width: 40, height: 2, background: '#3FD8CE', display: 'flex' }} />
          PEREIRA, COLOMBIA · SISTEMAS EN OPERACIÓN CONTINUA
        </div>
        <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
          <div style={{ fontSize: 84, fontWeight: 700, lineHeight: 1.05, display: 'flex', flexDirection: 'column' }}>
            <span>No vendo software.</span>
            <span style={{ color: '#FF7440' }}>Opero con él.</span>
          </div>
        </div>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-end' }}>
          <div style={{ display: 'flex', flexDirection: 'column' }}>
            <span style={{ fontSize: 30, fontWeight: 700 }}>Diego Mauricio García R.</span>
            <span style={{ fontSize: 18, color: '#FF7440', letterSpacing: 6 }}>DATOVATE NEXUS PRO</span>
          </div>
          <span style={{ fontSize: 22, color: '#8FA0A8' }}>datovatenexuspro.com</span>
        </div>
      </div>
    ),
    size
  );
}
