'use client';

/**
 * El letrero DVNP electrificado: las letras se recortan sobre una malla de
 * circuitos que se mueve, de modo que la corriente parece correr por dentro
 * de la tipografía. Puramente decorativo — el nombre real lo lleva el <h1>
 * y el texto accesible va en el aria-label.
 *
 * No usa canvas: es SVG con animación CSS, así que sale en el HTML del
 * servidor y funciona aunque el JavaScript no cargue.
 */
export default function Wordmark() {
  return (
    <div className="wordmark" aria-label="Datovate Nexus Pro">
      <svg viewBox="0 0 420 96" role="img" aria-hidden="true" preserveAspectRatio="xMinYMid meet">
        <defs>
          <clipPath id="wm-letters">
            <text
              x="0"
              y="74"
              fontFamily="var(--font-archivo), system-ui, sans-serif"
              fontSize="92"
              fontWeight="800"
              letterSpacing="-3"
            >
              DVNP
            </text>
          </clipPath>

          {/* La corriente: una banda de luz que barre las letras de izquierda a derecha */}
          <linearGradient id="wm-current" x1="0" y1="0" x2="1" y2="0">
            <stop offset="0%" stopColor="var(--glow-a)" stopOpacity="0" />
            <stop offset="42%" stopColor="var(--glow-a)" stopOpacity="0.95" />
            <stop offset="50%" stopColor="#FFFFFF" stopOpacity="1" />
            <stop offset="58%" stopColor="var(--glow-b)" stopOpacity="0.95" />
            <stop offset="100%" stopColor="var(--glow-b)" stopOpacity="0" />
          </linearGradient>

          <linearGradient id="wm-body" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stopColor="#16242A" />
            <stop offset="100%" stopColor="#0A1216" />
          </linearGradient>

          <filter id="wm-glow" x="-20%" y="-40%" width="140%" height="180%">
            <feGaussianBlur stdDeviation="3.2" result="b" />
            <feMerge>
              <feMergeNode in="b" />
              <feMergeNode in="SourceGraphic" />
            </feMerge>
          </filter>
        </defs>

        <g clipPath="url(#wm-letters)">
          {/* cuerpo de las letras: metal oscuro con volumen */}
          <rect x="0" y="0" width="420" height="96" fill="url(#wm-body)" />

          {/* placa de circuito impresa dentro de las letras */}
          <g stroke="var(--glow-b)" strokeWidth="1.5" opacity="0.8" fill="none">
            <path d="M-10 20 H60 V44 H130 V16 H210 V52 H300 V26 H430" />
            <path d="M-10 62 H40 V38 H120 V70 V70 H240 V46 H330 V72 H430" />
            <path d="M-10 82 H90 V60 H180 V86 H280 V58 H370 V84 H430" />
            <path d="M30 -10 V30 M150 -10 V22 M260 -10 V40 M350 -10 V18" />
            <path d="M80 106 V70 M200 106 V78 M310 106 V64 M395 106 V72" />
          </g>
          <g fill="var(--glow-a)" opacity="1">
            <circle cx="60" cy="44" r="2.6" /><circle cx="130" cy="16" r="2.6" />
            <circle cx="210" cy="52" r="2.6" /><circle cx="300" cy="26" r="2.6" />
            <circle cx="120" cy="70" r="2.6" /><circle cx="240" cy="46" r="2.6" />
            <circle cx="330" cy="72" r="2.6" /><circle cx="180" cy="86" r="2.6" />
            <circle cx="280" cy="58" r="2.6" /><circle cx="370" cy="84" r="2.6" />
          </g>

          {/* la corriente que recorre las letras */}
          <rect className="wm-sweep" x="-420" y="0" width="420" height="96" fill="url(#wm-current)" opacity="1" />
        </g>

        {/* contorno luminoso de las letras */}
        <text
          className="wm-stroke"
          x="0"
          y="74"
          fontFamily="var(--font-archivo), system-ui, sans-serif"
          fontSize="92"
          fontWeight="800"
          letterSpacing="-3"
          fill="none"
          stroke="var(--glow-b)"
          strokeWidth="2.1"
          filter="url(#wm-glow)"
        >
          DVNP
        </text>
      </svg>
      <span className="wordmark-dom">datovatenexuspro.com</span>
    </div>
  );
}
