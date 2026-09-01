'use client';

/**
 * El letrero: DIEGO GARCÍA con un universo dentro de las letras.
 *
 * Las letras funcionan como una ventana recortada sobre un cielo profundo:
 * nebulosas que derivan lentamente, un campo de estrellas que titila, la
 * placa de circuito de la marca y una corriente que barre de izquierda a
 * derecha. Al lado, la firma DVNP en pequeño.
 *
 * Todo es SVG con animación CSS: sale en el HTML del servidor, no depende de
 * JavaScript y no cuesta un solo byte de librería. Las estrellas se generan
 * con un generador pseudoaleatorio de semilla fija para que el servidor y el
 * navegador dibujen exactamente lo mismo (si no, React se queja de hidratación).
 */

/** Mulberry32: mismo resultado en servidor y navegador con la misma semilla. */
function prng(seed: number) {
  return () => {
    seed |= 0;
    seed = (seed + 0x6d2b79f5) | 0;
    let t = Math.imul(seed ^ (seed >>> 15), 1 | seed);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

const W = 760;
const H = 132;

const rand = prng(20260901);
const ESTRELLAS = Array.from({ length: 78 }, () => ({
  x: +(rand() * W).toFixed(1),
  y: +(rand() * H).toFixed(1),
  r: +(0.5 + rand() * 1.5).toFixed(2),
  d: +(rand() * 4).toFixed(2),      // desfase del titileo
  c: rand() < 0.22 ? 'a' : 'b',     // algunas naranjas, la mayoría frías
}));

export default function Wordmark() {
  return (
    <div className="wordmark">
      <svg
        viewBox={`0 0 ${W} ${H}`}
        role="img"
        aria-label="Diego García · Datovate Nexus Pro"
        preserveAspectRatio="xMinYMid meet"
      >
        <defs>
          {/* Las letras recortan todo lo que va dentro */}
          <clipPath id="wm-clip">
            <text
              x="0"
              y="86"
              fontFamily="var(--font-archivo), system-ui, sans-serif"
              fontSize="82"
              fontWeight="800"
              letterSpacing="-2"
            >
              DIEGO GARCÍA
            </text>
            <text
              x="612"
              y="46"
              fontFamily="var(--font-archivo), system-ui, sans-serif"
              fontSize="30"
              fontWeight="800"
              letterSpacing="1"
            >
              DVNP
            </text>
          </clipPath>

          {/* Cielo profundo */}
          <linearGradient id="wm-cielo" x1="0" y1="0" x2="0.4" y2="1">
            <stop offset="0%" stopColor="#0B1A2A" />
            <stop offset="55%" stopColor="#080F18" />
            <stop offset="100%" stopColor="#0A0708" />
          </linearGradient>

          {/* Nebulosas: tres nubes de color que derivan */}
          <radialGradient id="wm-neb-a" cx="0.5" cy="0.5" r="0.5">
            <stop offset="0%" stopColor="#3FD8CE" stopOpacity="0.62" />
            <stop offset="100%" stopColor="#3FD8CE" stopOpacity="0" />
          </radialGradient>
          <radialGradient id="wm-neb-b" cx="0.5" cy="0.5" r="0.5">
            <stop offset="0%" stopColor="#FF7440" stopOpacity="0.55" />
            <stop offset="100%" stopColor="#FF7440" stopOpacity="0" />
          </radialGradient>
          <radialGradient id="wm-neb-c" cx="0.5" cy="0.5" r="0.5">
            <stop offset="0%" stopColor="#7B5CFF" stopOpacity="0.5" />
            <stop offset="100%" stopColor="#7B5CFF" stopOpacity="0" />
          </radialGradient>

          {/* La corriente que recorre las letras */}
          <linearGradient id="wm-corriente" x1="0" y1="0" x2="1" y2="0">
            <stop offset="0%" stopColor="#FF7440" stopOpacity="0" />
            <stop offset="44%" stopColor="#FF7440" stopOpacity="0.85" />
            <stop offset="50%" stopColor="#FFFFFF" stopOpacity="1" />
            <stop offset="56%" stopColor="#3FD8CE" stopOpacity="0.85" />
            <stop offset="100%" stopColor="#3FD8CE" stopOpacity="0" />
          </linearGradient>

          <filter id="wm-halo" x="-15%" y="-40%" width="130%" height="180%">
            <feGaussianBlur stdDeviation="3" result="b" />
            <feMerge>
              <feMergeNode in="b" />
              <feMergeNode in="SourceGraphic" />
            </feMerge>
          </filter>
        </defs>

        <g clipPath="url(#wm-clip)">
          {/* 1. el vacío */}
          <rect x="0" y="0" width={W} height={H} fill="url(#wm-cielo)" />

          {/* 2. nebulosas a la deriva */}
          <g className="wm-neb">
            <ellipse className="wm-n1" cx="150" cy="70" rx="230" ry="110" fill="url(#wm-neb-a)" />
            <ellipse className="wm-n2" cx="470" cy="52" rx="250" ry="105" fill="url(#wm-neb-b)" />
            <ellipse className="wm-n3" cx="330" cy="96" rx="200" ry="95" fill="url(#wm-neb-c)" />
          </g>

          {/* 3. campo de estrellas */}
          <g className="wm-stars">
            {ESTRELLAS.map((s, i) => (
              <circle
                key={i}
                cx={s.x}
                cy={s.y}
                r={s.r}
                fill={s.c === 'a' ? '#FFC9A8' : '#DFF7F5'}
                style={{ animationDelay: `${s.d}s` }}
              />
            ))}
          </g>

          {/* 4. la placa de circuito de la marca, tenue sobre el cielo */}
          <g stroke="#3FD8CE" strokeWidth="1.1" opacity="0.3" fill="none">
            <path d="M-10 26 H110 V58 H240 V22 H380 V70 H540 V34 H780" />
            <path d="M-10 86 H70 V50 H210 V100 H430 V62 H600 V104 H780" />
            <path d="M60 -10 V38 M270 -10 V28 M470 -10 V54 M640 -10 V24" />
            <path d="M150 142 V96 M350 142 V108 M560 142 V88 M700 142 V100" />
          </g>

          {/* 5. la corriente */}
          <rect className="wm-sweep" x={-W} y="0" width={W} height={H} fill="url(#wm-corriente)" />
        </g>

        {/* contorno luminoso: define las letras contra el fondo */}
        <g filter="url(#wm-halo)" fill="none" strokeWidth="1.6">
          <text
            className="wm-stroke"
            x="0"
            y="86"
            fontFamily="var(--font-archivo), system-ui, sans-serif"
            fontSize="82"
            fontWeight="800"
            letterSpacing="-2"
            stroke="#5FE4DB"
          >
            DIEGO GARCÍA
          </text>
          <text
            className="wm-stroke wm-firma"
            x="612"
            y="46"
            fontFamily="var(--font-archivo), system-ui, sans-serif"
            fontSize="30"
            fontWeight="800"
            letterSpacing="1"
            stroke="#FF9166"
          >
            DVNP
          </text>
        </g>
      </svg>
      <span className="wordmark-dom">datovatenexuspro.com</span>
    </div>
  );
}
