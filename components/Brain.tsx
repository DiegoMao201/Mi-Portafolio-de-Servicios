'use client';

import { useEffect, useRef } from 'react';

/**
 * El cerebro. No es un adorno: es la pieza que tiene que dejar sin aire al
 * visitante en el primer segundo.
 *
 * Cómo está hecho:
 *  · La silueta —lóbulos, circunvoluciones, cerebelo y tronco— se muestrea
 *    sobre trazados SVG, así que es un cerebro de verdad y no una mancha.
 *  · Se dibuja con mezcla aditiva sobre una estela: cada cuadro tiñe el lienzo
 *    en vez de borrarlo, de modo que la luz deja rastro y los cruces de
 *    sinapsis se suman hasta el blanco. Eso produce el resplandor.
 *  · No parpadea al azar: PIENSA. Cada cierto tiempo nace un pensamiento en
 *    una neurona y se propaga por la red respetando la distancia real entre
 *    nodos, así que se ve viajar la idea.
 *  · Tiene profundidad: cada nodo se desplaza distinto con el cursor.
 *  · Baja de intensidad cuando el hero sale de la vista, para no gastar
 *    batería dibujando algo que nadie está mirando.
 */
type Kind = 'brain' | 'axon';
type Node = {
  x: number; y: number; ox: number; oy: number;
  r: number; glow: number; hue: 'a' | 'b'; ph: number;
  kind: Kind; z: number;
};
type Edge = { i: number; j: number; d: number; kind: Kind };
type Onda = { t: number; vel: number; hue: 'a' | 'b'; alcance: number; dist: Float32Array };

const GLOW_A = { r: 255, g: 116, b: 64 };
const GLOW_B = { r: 63, g: 216, b: 206 };
const FONDO = { r: 7, g: 11, b: 14 };

const BRAIN_OUTLINE =
  'M18 44 C10 40 10 30 18 26 C18 17 27 12 35 16 C38 8 48 7 53 13 ' +
  'C58 6 68 7 72 14 C80 12 89 18 88 27 C96 30 96 40 88 44 ' +
  'C92 50 86 57 78 56 C76 63 66 66 60 61 C54 65 46 64 43 58 ' +
  'C36 62 26 60 24 53 C18 52 16 48 18 44 Z';
const BRAIN_FOLDS = [
  'M22 38 C30 32 32 44 40 38 C48 32 50 44 58 38 C66 32 68 42 76 37',
  'M24 30 C32 25 36 34 44 29 C52 24 56 33 64 28 C72 23 76 30 82 27',
  'M26 47 C34 42 38 51 46 46 C54 41 58 50 66 46 C74 42 78 48 84 45',
  'M30 20 C38 16 44 23 52 19 C60 15 66 21 73 18',
  'M34 55 C42 51 48 58 56 54 C64 50 70 55 76 52',
  'M84 22 C90 26 92 34 86 39',
];
const BRAIN_STEM = [
  'M22 54 C28 52 33 57 31 62 C28 67 21 65 20 59 Z',
  'M30 63 C31 68 33 72 36 75',
];

export default function Brain() {
  const ref = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = ref.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d', { alpha: false });
    if (!ctx) return;

    const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    let W = 0, H = 0, dpr = 1;
    let nodes: Node[] = [];
    let edges: Edge[] = [];
    let vecinos: number[][] = [];
    let ondas: Onda[] = [];
    let raf = 0;
    let running = true;
    let small = false;
    let intensidad = 1;
    const mouse = { x: -9999, y: -9999, px: 0, py: 0 };

    /** El halo se pre-dibuja una sola vez por color y después solo se estampa
     *  escalado. Crear un degradado radial por neurona y por cuadro costaba
     *  ~200 degradados por fotograma; esto lo baja a dos imágenes. */
    function haloSprite(c: { r: number; g: number; b: number }) {
      const S = 128;
      const off = document.createElement('canvas');
      off.width = off.height = S;
      const o = off.getContext('2d')!;
      const g = o.createRadialGradient(S / 2, S / 2, 0, S / 2, S / 2, S / 2);
      g.addColorStop(0, 'rgba(' + c.r + ',' + c.g + ',' + c.b + ',1)');
      g.addColorStop(0.42, 'rgba(' + c.r + ',' + c.g + ',' + c.b + ',0.26)');
      g.addColorStop(1, 'rgba(' + c.r + ',' + c.g + ',' + c.b + ',0)');
      o.fillStyle = g;
      o.fillRect(0, 0, S, S);
      return off;
    }
    const SPRITE_A = haloSprite(GLOW_A);
    const SPRITE_B = haloSprite(GLOW_B);

    function samplePath(d: string, count: number) {
      const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
      svg.setAttribute('width', '0'); svg.setAttribute('height', '0');
      svg.style.cssText = 'position:absolute;opacity:0;pointer-events:none';
      const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
      path.setAttribute('d', d);
      svg.appendChild(path);
      document.body.appendChild(svg);
      const out: { x: number; y: number }[] = [];
      try {
        const len = path.getTotalLength();
        for (let i = 0; i < count; i++) {
          const p = path.getPointAtLength((len * i) / count);
          out.push({ x: p.x, y: p.y });
        }
      } catch { /* sin soporte: el cerebro queda vacío */ }
      document.body.removeChild(svg);
      return out;
    }

    function seed() {
      nodes = []; edges = []; ondas = [];
      small = W < 760;

      const bw = Math.min(small ? W * 0.58 : W * 0.34, 460);
      const bh = bw * 0.8;
      const bx = small ? W - bw * 0.9 : W - bw - W * 0.055;
      const by = small ? H * 0.03 : H * 0.1;
      const toHero = (p: { x: number; y: number }) => ({
        x: bx + (p.x / 100) * bw,
        y: by + (p.y / 80) * bh,
      });

      const dens = small ? 0.72 : 1;
      const push = (p: { x: number; y: number }, kind: Kind, hueBias: number, r: number) => {
        nodes.push({
          x: p.x, y: p.y, ox: p.x, oy: p.y,
          r, glow: 0,
          hue: Math.random() < hueBias ? 'a' : 'b',
          ph: Math.random() * Math.PI * 2,
          kind, z: Math.random(),
        });
      };

      for (const p of samplePath(BRAIN_OUTLINE, Math.round(70 * dens))) push(toHero(p), 'brain', 0.16, 1.5 + Math.random() * 1.6);
      for (const d of BRAIN_FOLDS) for (const p of samplePath(d, Math.round(17 * dens))) push(toHero(p), 'brain', 0.3, 1.1 + Math.random() * 1.4);
      for (const d of BRAIN_STEM) for (const p of samplePath(d, Math.round(12 * dens))) push(toHero(p), 'brain', 0.22, 1.1 + Math.random() * 1.2);
      const nCerebro = nodes.length;

      const vistos = new Set<string>();
      const maxLink = bw * 0.1;
      for (let i = 0; i < nCerebro; i++) {
        const cerca = nodes.slice(0, nCerebro)
          .map((m, j) => ({ j, d: Math.hypot(m.x - nodes[i].x, m.y - nodes[i].y) }))
          .filter((o) => o.j !== i).sort((a, b) => a.d - b.d).slice(0, 3);
        for (const { j, d } of cerca) {
          const k = i < j ? i + '-' + j : j + '-' + i;
          if (!vistos.has(k) && d < maxLink) { vistos.add(k); edges.push({ i: Math.min(i, j), j: Math.max(i, j), d, kind: 'brain' }); }
        }
      }

      const anclas = nodes.slice(0, nCerebro)
        .map((n, i) => ({ i, s: n.x - n.y * 0.55 }))
        .sort((a, b) => a.s - b.s).slice(0, small ? 3 : 6);
      for (const a of anclas) {
        let from = a.i; let x = nodes[from].x, y = nodes[from].y;
        let horiz = true;
        const tramos = 2 + Math.floor(Math.random() * 2);
        for (let l = 0; l < tramos; l++) {
          const largo = (horiz ? W : H) * (0.09 + Math.random() * 0.14);
          const tx = horiz ? x - largo : x;
          const ty = horiz ? y : y + largo * 0.7;
          if (tx < W * 0.03 || ty > H * 0.95) break;
          const pasos = Math.max(1, Math.round(Math.hypot(tx - x, ty - y) / 42));
          for (let s = 1; s <= pasos; s++) {
            const px = x + ((tx - x) * s) / pasos, py = y + ((ty - y) * s) / pasos;
            push({ x: px, y: py }, 'axon', 0.35, s === pasos && l === tramos - 1 ? 2.6 : 1.1);
            const to = nodes.length - 1;
            edges.push({ i: from, j: to, d: Math.hypot(px - x, py - y) / pasos, kind: 'axon' });
            from = to;
          }
          x = tx; y = ty; horiz = !horiz;
        }
      }

      vecinos = nodes.map(() => [] as number[]);
      for (const e of edges) { vecinos[e.i].push(e.j); vecinos[e.j].push(e.i); }
    }

    /** Nace un pensamiento: recorrido por anchura desde una neurona, guardando
     *  la distancia real a cada una. Después la onda avanza sobre esa distancia
     *  y por eso se ve VIAJAR la idea por la red. */
    function pensar() {
      if (!nodes.length || ondas.length > 3) return;
      const origen = Math.floor(Math.random() * nodes.length);
      const dist = new Float32Array(nodes.length).fill(-1);
      dist[origen] = 0;
      const cola = [origen];
      let max = 0;
      for (let h = 0; h < cola.length; h++) {
        const u = cola[h];
        for (const v of vecinos[u]) {
          if (dist[v] >= 0) continue;
          const d = dist[u] + Math.hypot(nodes[v].x - nodes[u].x, nodes[v].y - nodes[u].y);
          dist[v] = d; if (d > max) max = d;
          cola.push(v);
        }
      }
      ondas.push({
        t: 0,
        vel: 260 + Math.random() * 260,
        hue: Math.random() < 0.32 ? 'a' : 'b',
        alcance: max || 1,
        dist,
      });
    }

    function resize() {
      const rect = canvas!.parentElement!.getBoundingClientRect();
      dpr = Math.min(window.devicePixelRatio || 1, 2);
      W = rect.width; H = rect.height;
      canvas!.width = Math.round(W * dpr);
      canvas!.height = Math.round(H * dpr);
      ctx!.setTransform(dpr, 0, 0, dpr, 0, 0);
      ctx!.fillStyle = 'rgb(' + FONDO.r + ',' + FONDO.g + ',' + FONDO.b + ')';
      ctx!.fillRect(0, 0, W, H);
      seed();
      if (reduced) { pensar(); draw(0); draw(16); }
    }

    let last = 0;
    function draw(time: number) {
      const dt = Math.min(0.05, (time - last) / 1000) || 0.016;
      last = time;
      const t = time * 0.001;

      // Estela: teñir en vez de borrar. La luz deja rastro.
      ctx!.globalCompositeOperation = 'source-over';
      ctx!.fillStyle = 'rgba(' + FONDO.r + ',' + FONDO.g + ',' + FONDO.b + ',' + (reduced ? 1 : 0.26) + ')';
      ctx!.fillRect(0, 0, W, H);

      mouse.px += ((mouse.x > -9000 ? (mouse.x - W / 2) * 0.016 : 0) - mouse.px) * 0.05;
      mouse.py += ((mouse.y > -9000 ? (mouse.y - H / 2) * 0.016 : 0) - mouse.py) * 0.05;

      for (let k = ondas.length - 1; k >= 0; k--) {
        const o = ondas[k];
        o.t += o.vel * dt;
        if (o.t > o.alcance + 220) ondas.splice(k, 1);
      }

      for (const n of nodes) {
        const amp = n.kind === 'brain' ? 2.4 : 0.9;
        const par = 0.4 + n.z * 1.6;
        n.x = n.ox + (reduced ? 0 : Math.sin(t * 0.55 + n.ph) * amp) + mouse.px * par;
        n.y = n.oy + (reduced ? 0 : Math.cos(t * 0.47 + n.ph * 1.3) * amp) + mouse.py * par;
      }

      for (let i = 0; i < nodes.length; i++) {
        const n = nodes[i];
        n.glow *= 0.94;
        for (const o of ondas) {
          const d = o.dist[i];
          if (d < 0) continue;
          const frente = Math.abs(o.t - d);
          if (frente < 90) { const v = 1 - frente / 90; if (v * v > n.glow) n.glow = v * v; }
        }
        const dm = Math.hypot(n.x - mouse.x, n.y - mouse.y);
        if (dm < 150) { const v = Math.pow(1 - dm / 150, 1.5); if (v > n.glow) n.glow = v; }
      }

      // Mezcla aditiva: los cruces se suman y florecen.
      ctx!.globalCompositeOperation = 'lighter';
      const I = intensidad;

      for (const e of edges) {
        const a = nodes[e.i], b = nodes[e.j];
        const ex = Math.max(a.glow, b.glow);
        if (ex < 0.02 && e.kind === 'axon') continue;
        const c = (a.hue === 'a' || b.hue === 'a') ? GLOW_A : GLOW_B;
        const base = e.kind === 'axon' ? 0.05 : 0.1;
        const al = (base + ex * 0.62) * I;
        ctx!.strokeStyle = 'rgba(' + c.r + ',' + c.g + ',' + c.b + ',' + al + ')';
        ctx!.lineWidth = 0.9 + ex * 1.9;
        ctx!.beginPath(); ctx!.moveTo(a.x, a.y); ctx!.lineTo(b.x, b.y); ctx!.stroke();
      }

      for (const n of nodes) {
        const c = n.hue === 'a' ? GLOW_A : GLOW_B;
        const g = n.glow;
        if (g > 0.04) {
          const R = 8 + g * 36;
          ctx!.globalAlpha = 0.55 * g * I;
          ctx!.drawImage(n.hue === 'a' ? SPRITE_A : SPRITE_B, n.x - R, n.y - R, R * 2, R * 2);
          ctx!.globalAlpha = 1;
        }
        const nuc = (n.kind === 'brain' ? 0.3 : 0.16) + g * 0.7;
        const rr = Math.min(255, c.r + g * 120), gg = Math.min(255, c.g + g * 90), bb = Math.min(255, c.b + g * 90);
        ctx!.fillStyle = 'rgba(' + rr + ',' + gg + ',' + bb + ',' + (nuc * I) + ')';
        ctx!.beginPath(); ctx!.arc(n.x, n.y, n.r + g * 2.2, 0, Math.PI * 2); ctx!.fill();
      }
      ctx!.globalCompositeOperation = 'source-over';
    }

    let acumulado = 0;
    function loop(time: number) {
      if (!running) return;
      draw(time);
      acumulado += 16;
      if (acumulado > (small ? 1500 : 950)) { acumulado = 0; pensar(); }
      raf = requestAnimationFrame(loop);
    }

    function onMove(ev: PointerEvent) {
      const r = canvas!.getBoundingClientRect();
      mouse.x = ev.clientX - r.left; mouse.y = ev.clientY - r.top;
    }
    function onLeave() { mouse.x = -9999; mouse.y = -9999; }
    function onVis() {
      running = document.visibilityState === 'visible';
      if (running && !reduced) { last = performance.now(); raf = requestAnimationFrame(loop); }
    }

    resize();
    const ro = new ResizeObserver(resize);
    ro.observe(canvas.parentElement!);
    const io = new IntersectionObserver(
      function (entries) { intensidad = entries[0].isIntersecting ? 1 : 0.35; },
      { threshold: 0.05 }
    );
    io.observe(canvas.parentElement!);
    canvas.parentElement!.addEventListener('pointermove', onMove);
    canvas.parentElement!.addEventListener('pointerleave', onLeave);
    document.addEventListener('visibilitychange', onVis);
    if (!reduced) { pensar(); raf = requestAnimationFrame(loop); }

    return () => {
      running = false;
      cancelAnimationFrame(raf);
      ro.disconnect(); io.disconnect();
      canvas.parentElement?.removeEventListener('pointermove', onMove);
      canvas.parentElement?.removeEventListener('pointerleave', onLeave);
      document.removeEventListener('visibilitychange', onVis);
    };
  }, []);

  return <canvas ref={ref} aria-hidden="true" />;
}
