'use client';

import { useEffect, useRef } from 'react';

/**
 * La red que piensa. Ocupa el panel del Diagnosticador mientras no hay
 * arquitectura que dibujar: en reposo late despacio, y mientras el modelo
 * responde se activa — ondas de señal cruzando las capas de izquierda a
 * derecha, neuronas que se encienden al recibir y conexiones que se calientan
 * por donde pasó la señal.
 *
 * No es una barra de progreso disfrazada: la actividad refleja el estado real
 * (`activa` es true solo mientras hay respuesta en curso), y el rótulo dice lo
 * que de verdad está pasando, no un guion inventado.
 */

const CAPAS = [4, 6, 6, 3];
const CYAN = { r: 63, g: 216, b: 206 };
const SIGNAL = { r: 255, g: 116, b: 64 };

type N = { x: number; y: number; capa: number; carga: number };

export default function RedPensando({ activa = false }: { activa?: boolean }) {
  const ref = useRef<HTMLCanvasElement>(null);
  const activaRef = useRef(activa);
  activaRef.current = activa;

  useEffect(() => {
    const canvas = ref.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;
    const reducido = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    let W = 0, H = 0, dpr = 1, raf = 0, vivo = true, ultimo = 0;
    let nodos: N[] = [];
    let ondas: { capa: number; t: number; calor: number }[] = [];
    let desdeOnda = 0;

    function medir() {
      const r = canvas!.getBoundingClientRect();
      dpr = Math.min(window.devicePixelRatio || 1, 2);
      W = Math.max(160, r.width);
      H = Math.max(120, r.height);
      canvas!.width = Math.round(W * dpr);
      canvas!.height = Math.round(H * dpr);
      ctx!.setTransform(dpr, 0, 0, dpr, 0, 0);

      nodos = [];
      const padX = Math.min(46, W * 0.11), padY = Math.min(30, H * 0.13);
      const anchoCapa = (W - padX * 2) / (CAPAS.length - 1);
      CAPAS.forEach((cuantas, c) => {
        const alto = (H - padY * 2) / Math.max(1, cuantas - 1);
        for (let i = 0; i < cuantas; i++) {
          nodos.push({
            x: padX + anchoCapa * c,
            y: cuantas === 1 ? H / 2 : padY + alto * i,
            capa: c,
            carga: 0,
          });
        }
      });
    }

    function pintar() {
      ctx!.clearRect(0, 0, W, H);

      // conexiones entre capas contiguas
      for (let c = 0; c < CAPAS.length - 1; c++) {
        const izq = nodos.filter((n) => n.capa === c);
        const der = nodos.filter((n) => n.capa === c + 1);
        for (const a of izq) {
          for (const b of der) {
            const viva = Math.min(a.carga, 1) * Math.min(b.carga + 0.35, 1);
            const alfa = 0.055 + viva * 0.5;
            const col = viva > 0.28 ? SIGNAL : CYAN;
            ctx!.strokeStyle = `rgba(${col.r},${col.g},${col.b},${alfa})`;
            ctx!.lineWidth = 0.7 + viva * 1.1;
            ctx!.beginPath();
            ctx!.moveTo(a.x, a.y);
            ctx!.lineTo(b.x, b.y);
            ctx!.stroke();
          }
        }
      }

      // neuronas
      for (const n of nodos) {
        const q = n.carga;
        if (q > 0.04) {
          const col = q > 0.55 ? SIGNAL : CYAN;
          const g = ctx!.createRadialGradient(n.x, n.y, 0, n.x, n.y, 4 + q * 15);
          g.addColorStop(0, `rgba(${col.r},${col.g},${col.b},${q * 0.55})`);
          g.addColorStop(1, `rgba(${col.r},${col.g},${col.b},0)`);
          ctx!.fillStyle = g;
          ctx!.beginPath();
          ctx!.arc(n.x, n.y, 4 + q * 15, 0, Math.PI * 2);
          ctx!.fill();
        }
        const col = q > 0.55 ? SIGNAL : CYAN;
        ctx!.fillStyle = `rgba(${col.r},${col.g},${col.b},${0.34 + q * 0.66})`;
        ctx!.beginPath();
        ctx!.arc(n.x, n.y, 2.1 + q * 2.4, 0, Math.PI * 2);
        ctx!.fill();
      }
    }

    function paso(ahora: number) {
      if (!vivo) return;
      const dt = Math.min(48, ahora - (ultimo || ahora));
      ultimo = ahora;
      const enMarcha = activaRef.current;

      // Una onda nueva cada 260ms si está respondiendo; cada 1.7s en reposo.
      desdeOnda += dt;
      const cada = enMarcha ? 260 : 1700;
      if (desdeOnda > cada && ondas.length < 7) {
        desdeOnda = 0;
        ondas.push({ capa: 0, t: 0, calor: Math.random() < (enMarcha ? 0.6 : 0.25) ? 1 : 0 });
      }

      for (let i = ondas.length - 1; i >= 0; i--) {
        const o = ondas[i];
        o.t += dt / (enMarcha ? 190 : 420);
        if (o.t >= 1) {
          o.capa += 1;
          o.t = 0;
          if (o.capa >= CAPAS.length) { ondas.splice(i, 1); continue; }
          // al llegar a una capa, enciende sus neuronas
          for (const n of nodos) {
            if (n.capa === o.capa) n.carga = Math.min(1, n.carga + (o.calor ? 1 : 0.7));
          }
        }
      }

      const caida = enMarcha ? 0.9955 : 0.9975;
      for (const n of nodos) n.carga *= Math.pow(caida, dt);

      pintar();
      raf = requestAnimationFrame(paso);
    }

    medir();
    if (reducido) {
      for (const n of nodos) n.carga = 0.35;
      pintar();
      const ro = new ResizeObserver(() => { medir(); for (const n of nodos) n.carga = 0.35; pintar(); });
      ro.observe(canvas);
      return () => ro.disconnect();
    }

    raf = requestAnimationFrame(paso);
    const ro = new ResizeObserver(() => medir());
    ro.observe(canvas);

    // El panel pasa la mayor parte del tiempo fuera de pantalla: pintarlo
    // mientras nadie lo ve es batería regalada. Mismo criterio que el cerebro.
    let enPantalla = true;
    const arrancar = () => {
      if (vivo || !enPantalla || document.hidden) return;
      vivo = true; ultimo = 0; raf = requestAnimationFrame(paso);
    };
    const parar = () => { vivo = false; cancelAnimationFrame(raf); };
    const io = new IntersectionObserver(
      ([e]) => { enPantalla = e.isIntersecting; enPantalla ? arrancar() : parar(); },
      { threshold: 0 }
    );
    io.observe(canvas);
    const alVisibilidad = () => { document.hidden ? parar() : arrancar(); };
    document.addEventListener('visibilitychange', alVisibilidad);
    return () => {
      parar();
      ro.disconnect();
      io.disconnect();
      document.removeEventListener('visibilitychange', alVisibilidad);
    };
  }, []);

  return <canvas ref={ref} className="red-pensando" aria-hidden="true" />;
}
