import { ImageResponse } from 'next/og';

export const runtime = 'nodejs';
export const size = { width: 180, height: 180 };
export const contentType = 'image/png';

/** Ícono para iOS/Android al guardar el sitio en la pantalla de inicio. */
export default function AppleIcon() {
  return new ImageResponse(
    (
      <div
        style={{
          width: '100%',
          height: '100%',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          background: '#090D10',
        }}
      >
        <svg width="150" height="150" viewBox="0 0 64 64">
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
          <circle cx="47.5" cy="16" r="6.2" fill="#090D10" stroke="#3FD8CE" strokeWidth="4" />
        </svg>
      </div>
    ),
    size
  );
}
