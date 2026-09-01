'use client';

import { useEffect, useRef } from 'react';

/**
 * La corriente: el sustrato eléctrico del sitio.
 *
 * Una red neuronal dispersa que vive detrás de TODAS las vistas. En reposo es
 * casi invisible — textura, no ruido. Lo que se ve es la actividad: cargas que
 * nacen en un nodo y caminan por las conexiones saltando de nodo en nodo,
 * destellos ocasionales, y el cursor, que electrifica lo que tiene cerca.
 *
 * Reglas que me impuse para que no sobrepoble:
 *  - Pocos nodos y solo dos vecinos por nodo: se lee como circuito, no como
 *    telaraña. Un grafo denso es ruido visual.
 *  - Los nodos se siembran en una cuadrícula con desorden, no al azar puro:
 *    el azar puro hace grumos y deja zonas muertas.
 *  - Nada se dibuja por encima del texto: el lienzo va detrás de todo y las
 *    intensidades máximas están calibradas para no tocar el contraste.
 *  - Con prefers-reduced-motion se dibuja UNA vez, quieta. La red sigue ahí;
 *    lo que desaparece es el movimiento.
 */

const CYAN = { r: 11, g: 106, b: 99 };     // --cyan-ink
const SIGNAL = { r: 188, g: 65, b: 23 };   // --signal-ink

type Nodo = { x: number; y: number; carga: number; fase: number };
type Arista = { a: number; b: number; largo: number };
type Carga = { arista: number; t: number; dir: 1 | -1; saltos: number; calor: number };
/** Destello: el chispazo al llegar la carga a un nodo. Anillo que se abre y
 *  filamentos cortos, como un arco eléctrico. Dura menos de medio segundo. */
type Destello = { x: number; y: number; t: number; calor: number; ramas: number[] };
/** Estrellas: puntos diminutos que titilan. No están conectadas a nada; su
 *  único trabajo es que el fondo nunca esté del todo quieto. */
type Estrella = { x: number; y: number; r: number; fase: number; vel: number; calor: number };

export default function Corriente() {
  const ref = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = ref.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const reducido = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    const fino = window.matchMedia('(hover: hover) and (pointer: fine)').matches;

    let W = 0, H = 0, dpr = 1;
    let nodos: Nodo[] = [];
    let aristas: Arista[] = [];
    let salidas: number[][] = [];   // aristas que salen de cada nodo
    let cargas: Carga[] = [];
    let destellos: Destello[] = [];
    let estrellas: Estrella[] = [];
    let raf = 0;
    let vivo = true;
    let ultimo = 0;
    let acumulador = 0;
    const raton = { x: -9999, y: -9999 };

    /** El halo se pre-dibuja una vez por color y luego solo se estampa: crear
     *  un degradado radial por nodo y por cuadro es lo que mata el rendimiento. */
    function halo(c: { r: number; g: number; b: number }) {
      const S = 96;
      const off = document.createElement('canvas');
      off.width = off.height = S;
      const o = off.getContext('2d')!;
      const g = o.createRadialGradient(S / 2, S / 2, 0, S / 2, S / 2, S / 2);
      g.addColorStop(0, `rgba(${c.r},${c.g},${c.b},0.85)`);
      g.addColorStop(0.35, `rgba(${c.r},${c.g},${c.b},0.22)`);
      g.addColorStop(1, `rgba(${c.r},${c.g},${c.b},0)`);
      o.fillStyle = g;
      o.fillRect(0, 0, S, S);
      return off;
    }
    const HALO_CYAN = halo(CYAN);
    const HALO_SIGNAL = halo(SIGNAL);

    function sembrar() {
      // Cuadrícula con desorden: reparte sin grumos y sin zonas muertas.
      const objetivo = W < 700 ? 26 : W < 1200 ? 42 : 58;
      const cols = Math.max(3, Math.round(Math.sqrt(objetivo * (W / H))));
      const filas = Math.max(3, Math.ceil(objetivo / cols));
      const celdaX = W / cols, celdaY = H / filas;
      nodos = [];
      for (let f = 0; f < filas; f++) {
        for (let c = 0; c < cols; c++) {
          nodos.push({
            x: celdaX * (c + 0.5) + (Math.random() - 0.5) * celdaX * 0.72,
            y: celdaY * (f + 0.5) + (Math.random() - 0.5) * celdaY * 0.72,
            carga: 0,
            fase: Math.random() * Math.PI * 2,
          });
        }
      }
      // Cada nodo se une a sus dos vecinos más cercanos. Sin duplicar aristas.
      const vistas = new Set<string>();
      aristas = [];
      nodos.forEach((n, i) => {
        const cerca = nodos
          .map((m, j) => ({ j, d: (m.x - n.x) ** 2 + (m.y - n.y) ** 2 }))
          .filter((o) => o.j !== i)
          .sort((a, b) => a.d - b.d)
          .slice(0, 2);
        for (const { j, d } of cerca) {
          const clave = i < j ? `${i}-${j}` : `${j}-${i}`;
          if (vistas.has(clave)) continue;
          vistas.add(clave);
          aristas.push({ a: i, b: j, largo: Math.sqrt(d) });
        }
      });
      salidas = nodos.map(() => []);
      aristas.forEach((e, k) => { salidas[e.a].push(k); salidas[e.b].push(k); });
      cargas = []; destellos = [];
      const cuantas = W < 700 ? 34 : 62;
      estrellas = Array.from({ length: cuantas }, () => ({
        x: Math.random() * W, y: Math.random() * H,
        r: 0.5 + Math.random() * 0.7,
        fase: Math.random() * Math.PI * 2,
        vel: 0.0012 + Math.random() * 0.0022,
        calor: Math.random() < 0.34 ? 1 : 0,
      }));
    }

    function medir() {
      dpr = Math.min(window.devicePixelRatio || 1, 2);
      W = window.innerWidth;
      H = window.innerHeight;
      canvas!.width = Math.round(W * dpr);
      canvas!.height = Math.round(H * dpr);
      canvas!.style.width = W + 'px';
      canvas!.style.height = H + 'px';
      ctx!.setTransform(dpr, 0, 0, dpr, 0, 0);
      sembrar();
    }

    function nacerCarga() {
      if (cargas.length > 13 || !aristas.length) return;
      const nodo = Math.floor(Math.random() * nodos.length);
      const salidasNodo = salidas[nodo];
      if (!salidasNodo.length) return;
      const arista = salidasNodo[Math.floor(Math.random() * salidasNodo.length)];
      cargas.push({
        arista,
        t: aristas[arista].a === nodo ? 0 : 1,
        dir: aristas[arista].a === nodo ? 1 : -1,
        saltos: 2 + Math.floor(Math.random() * 4),
        calor: Math.random() < 0.5 ? 0 : 1,
      });
    }

    function pintar(dt: number) {
      ctx!.clearRect(0, 0, W, H);

      // ── estrellas ────────────────────────────────────────────────────────
      for (const s of estrellas) {
        const t = 0.5 + 0.5 * Math.sin(s.fase);
        const c = s.calor ? SIGNAL : CYAN;
        ctx!.fillStyle = `rgba(${c.r},${c.g},${c.b},${0.05 + t * 0.26})`;
        ctx!.beginPath();
        ctx!.arc(s.x, s.y, s.r, 0, Math.PI * 2);
        ctx!.fill();
      }

      // ── conexiones ───────────────────────────────────────────────────────
      ctx!.lineWidth = 1;
      for (const e of aristas) {
        const a = nodos[e.a], b = nodos[e.b];
        const viva = Math.max(a.carga, b.carga);
        const alfa = 0.075 + viva * 0.42;
        const c = viva > 0.25 ? SIGNAL : CYAN;
        ctx!.strokeStyle = `rgba(${c.r},${c.g},${c.b},${alfa})`;
        ctx!.beginPath();
        ctx!.moveTo(a.x, a.y);
        ctx!.lineTo(b.x, b.y);
        ctx!.stroke();
      }

      // ── cargas viajando ──────────────────────────────────────────────────
      for (let i = cargas.length - 1; i >= 0; i--) {
        const p = cargas[i];
        const e = aristas[p.arista];
        const a = nodos[e.a], b = nodos[e.b];
        p.t += (p.dir * dt * 0.42) / Math.max(60, e.largo);
        const llegó = p.dir === 1 ? p.t >= 1 : p.t <= 0;
        const tt = Math.min(1, Math.max(0, p.t));
        const x = a.x + (b.x - a.x) * tt;
        const y = a.y + (b.y - a.y) * tt;
        const c = p.calor ? SIGNAL : CYAN;
        const sprite = p.calor ? HALO_SIGNAL : HALO_CYAN;
        ctx!.globalAlpha = 0.5;
        ctx!.drawImage(sprite, x - 13, y - 13, 26, 26);
        ctx!.globalAlpha = 1;
        ctx!.fillStyle = `rgba(${c.r},${c.g},${c.b},0.85)`;
        ctx!.beginPath();
        ctx!.arc(x, y, 1.7, 0, Math.PI * 2);
        ctx!.fill();

        if (llegó) {
          const destino = p.dir === 1 ? e.b : e.a;
          nodos[destino].carga = 1;                 // el nodo se enciende al recibir
          if (destellos.length < 9) {
            destellos.push({
              x: nodos[destino].x, y: nodos[destino].y, t: 0, calor: p.calor,
              ramas: [Math.random() * 6.283, Math.random() * 6.283, Math.random() * 6.283,
                      Math.random(), Math.random(), Math.random()],
            });
          }
          cargas.splice(i, 1);
          if (p.saltos > 0) {
            // salta a otra conexión de ese nodo: la corriente camina la red
            const opciones = salidas[destino].filter((k) => k !== p.arista);
            if (opciones.length) {
              const sig = opciones[Math.floor(Math.random() * opciones.length)];
              const ea = aristas[sig];
              cargas.push({
                arista: sig,
                t: ea.a === destino ? 0 : 1,
                dir: ea.a === destino ? 1 : -1,
                saltos: p.saltos - 1,
                calor: p.calor,
              });
            }
          }
        }
      }

      // ── nodos ────────────────────────────────────────────────────────────
      for (const n of nodos) {
        const respiro = 0.5 + 0.5 * Math.sin(n.fase);
        const base = 0.15 + respiro * 0.07;
        const q = n.carga;
        if (q > 0.02) {
          const sprite = q > 0.5 ? HALO_SIGNAL : HALO_CYAN;
          const r = 10 + q * 22;
          ctx!.globalAlpha = q * 0.42;
          ctx!.drawImage(sprite, n.x - r, n.y - r, r * 2, r * 2);
          ctx!.globalAlpha = 1;
        }
        const c = q > 0.5 ? SIGNAL : CYAN;
        ctx!.fillStyle = `rgba(${c.r},${c.g},${c.b},${base + q * 0.62})`;
        ctx!.beginPath();
        ctx!.arc(n.x, n.y, 1.15 + q * 2.1, 0, Math.PI * 2);
        ctx!.fill();
      }

      // ── destellos: el chispazo ───────────────────────────────────────────
      for (let i = destellos.length - 1; i >= 0; i--) {
        const d = destellos[i];
        d.t += dt / 430;
        if (d.t >= 1) { destellos.splice(i, 1); continue; }
        const c = d.calor ? SIGNAL : CYAN;
        const desvanece = 1 - d.t;
        // anillo que se abre
        ctx!.strokeStyle = `rgba(${c.r},${c.g},${c.b},${desvanece * 0.5})`;
        ctx!.lineWidth = 1.2 * desvanece;
        ctx!.beginPath();
        ctx!.arc(d.x, d.y, 3 + d.t * 26, 0, Math.PI * 2);
        ctx!.stroke();
        // filamentos: tres latigazos cortos con un quiebre, como un arco
        ctx!.strokeStyle = `rgba(${c.r},${c.g},${c.b},${desvanece * 0.75})`;
        ctx!.lineWidth = 1;
        for (let k = 0; k < 3; k++) {
          const ang = d.ramas[k];
          const largo = (9 + d.ramas[k + 3] * 15) * (0.4 + d.t);
          const mx = d.x + Math.cos(ang) * largo * 0.55 + Math.cos(ang + 1.6) * 4;
          const my = d.y + Math.sin(ang) * largo * 0.55 + Math.sin(ang + 1.6) * 4;
          ctx!.beginPath();
          ctx!.moveTo(d.x, d.y);
          ctx!.lineTo(mx, my);
          ctx!.lineTo(d.x + Math.cos(ang) * largo, d.y + Math.sin(ang) * largo);
          ctx!.stroke();
        }
      }
    }

    function paso(ahora: number) {
      if (!vivo) return;
      const dt = Math.min(48, ahora - (ultimo || ahora));
      ultimo = ahora;

      // El cursor electrifica lo que tiene cerca.
      if (fino && raton.x > -9000) {
        for (const n of nodos) {
          const d = Math.hypot(n.x - raton.x, n.y - raton.y);
          if (d < 170) n.carga = Math.max(n.carga, (1 - d / 170) * 0.85);
        }
      }
      for (const n of nodos) {
        n.carga *= Math.pow(0.9975, dt);
        n.fase += dt * 0.0011;
      }
      for (const s of estrellas) s.fase += dt * s.vel;

      acumulador += dt;
      // Una carga nueva cada ~560ms: suficiente para que siempre esté pasando
      // algo en pantalla, poco para que nunca parezca una feria.
      while (acumulador > 560) { acumulador -= 560; nacerCarga(); }

      pintar(dt);
      raf = requestAnimationFrame(paso);
    }

    medir();

    if (reducido) {
      // Quieta: la red se ve, no se mueve.
      pintar(0);
      const alRedimensionar = () => { medir(); pintar(0); };
      window.addEventListener('resize', alRedimensionar);
      return () => window.removeEventListener('resize', alRedimensionar);
    }

    // Arranca con la red ya poblada de actividad, no vacía.
    for (let i = 0; i < 7; i++) nacerCarga();
    raf = requestAnimationFrame(paso);

    const alMover = (e: PointerEvent) => { raton.x = e.clientX; raton.y = e.clientY; };
    const alSalir = () => { raton.x = raton.y = -9999; };
    const alRedimensionar = () => medir();
    const alVisibilidad = () => {
      // En pestaña oculta no se gasta batería.
      if (document.hidden) { vivo = false; cancelAnimationFrame(raf); }
      else if (!vivo) { vivo = true; ultimo = 0; raf = requestAnimationFrame(paso); }
    };

    window.addEventListener('pointermove', alMover, { passive: true });
    window.addEventListener('pointerleave', alSalir);
    window.addEventListener('resize', alRedimensionar);
    document.addEventListener('visibilitychange', alVisibilidad);

    return () => {
      vivo = false;
      cancelAnimationFrame(raf);
      window.removeEventListener('pointermove', alMover);
      window.removeEventListener('pointerleave', alSalir);
      window.removeEventListener('resize', alRedimensionar);
      document.removeEventListener('visibilitychange', alVisibilidad);
    };
  }, []);

  return <canvas ref={ref} className="corriente" aria-hidden="true" />;
}
