'use client';

import { useEffect, useRef } from 'react';

/**
 * El cerebro de luces: una silueta de cerebro dibujada con nodos y sinapsis,
 * compacta arriba a la derecha del hero. Los pulsos nacen dentro del cerebro,
 * recorren sus circunvoluciones y salen por axones —trazas tipo circuito— que
 * llevan la luz hacia el resto de la página. El cursor excita la zona cercana.
 */
type Kind = 'brain' | 'axon';
type Node = { x: number; y: number; ox: number; oy: number; r: number; glow: number; hue: 'a' | 'b'; ph: number; kind: Kind };
type Edge = { i: number; j: number; d: number; kind: Kind };
type Pulse = { e: number; t: number; v: number; dir: 1 | -1; hue: 'a' | 'b' };

const GLOW_A = { r: 255, g: 116, b: 64 };   // naranja señal
const GLOW_B = { r: 63, g: 216, b: 206 };   // cian sináptico

// Silueta del cerebro, en una caja de 100 x 80, mirando a la derecha.
// El contorno lleva los lóbulos marcados; los pliegues son las circunvoluciones;
// el cerebelo y el tronco son lo que lo vuelve inconfundible.
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
// Cerebelo (abajo a la izquierda) y tronco encefálico
const BRAIN_STEM = [
  'M22 54 C28 52 33 57 31 62 C28 67 21 65 20 59 Z',
  'M30 63 C31 68 33 72 36 75',
];

export default function Brain() {
  const ref = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = ref.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    let W = 0, H = 0, dpr = 1;
    let nodes: Node[] = [];
    let edges: Edge[] = [];
    let axonEdges: number[] = [];
    let pulses: Pulse[] = [];
    let raf = 0;
    let running = true;
    let small = false;
    const mouse = { x: -9999, y: -9999 };

    // Muestrea puntos equiespaciados a lo largo de un path SVG.
    function samplePath(d: string, count: number): { x: number; y: number }[] {
      const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
      svg.setAttribute('width', '0');
      svg.setAttribute('height', '0');
      svg.style.position = 'absolute';
      svg.style.opacity = '0';
      svg.style.pointerEvents = 'none';
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
      } catch {
        /* navegador sin soporte: el cerebro simplemente queda vacío */
      }
      document.body.removeChild(svg);
      return out;
    }

    function seed() {
      nodes = [];
      edges = [];
      axonEdges = [];
      pulses = [];

      small = W < 760;
      // El cerebro: pequeño y compacto, arriba a la derecha. Nunca domina el titular.
      // En móvil se recuesta contra el borde derecho para no montarse sobre el letrero.
      const bw = Math.min(small ? W * 0.46 : W * 0.25, 330);
      const bh = bw * 0.8;
      const bx = small ? W - bw * 0.88 : W - bw - W * 0.09;
      const by = small ? H * 0.03 : H * 0.13;
      const toHero = (p: { x: number; y: number }) => ({
        x: bx + (p.x / 100) * bw,
        y: by + (p.y / 80) * bh,
      });

      const density = small ? 0.7 : 1;
      const push = (p: { x: number; y: number }, kind: Kind, hueBias: number, r: number) => {
        nodes.push({
          x: p.x, y: p.y, ox: p.x, oy: p.y,
          r, glow: Math.random() * 0.25,
          hue: Math.random() < hueBias ? 'a' : 'b',
          ph: Math.random() * Math.PI * 2,
          kind,
        });
      };

      // 1. Contorno del cerebro
      for (const p of samplePath(BRAIN_OUTLINE, Math.round(58 * density))) {
        push(toHero(p), 'brain', 0.18, 1.5 + Math.random() * 1.5);
      }
      // 2. Circunvoluciones internas
      for (const d of BRAIN_FOLDS) {
        for (const p of samplePath(d, Math.round(14 * density))) {
          push(toHero(p), 'brain', 0.3, 1.1 + Math.random() * 1.3);
        }
      }
      // 3. Cerebelo y tronco: lo que lo vuelve inconfundible
      for (const d of BRAIN_STEM) {
        for (const p of samplePath(d, Math.round(10 * density))) {
          push(toHero(p), 'brain', 0.22, 1.1 + Math.random() * 1.1);
        }
      }
      const brainCount = nodes.length;

      // Sinapsis del cerebro: k vecinos más cercanos, para que sigan los pliegues
      const seen = new Set<string>();
      const maxLink = bw * 0.105;
      for (let i = 0; i < brainCount; i++) {
        const near = nodes
          .slice(0, brainCount)
          .map((m, j) => ({ j, d: Math.hypot(m.x - nodes[i].x, m.y - nodes[i].y) }))
          .filter((o) => o.j !== i)
          .sort((a, b) => a.d - b.d)
          .slice(0, 3);
        for (const { j, d } of near) {
          const key = i < j ? `${i}-${j}` : `${j}-${i}`;
          if (!seen.has(key) && d < maxLink) {
            seen.add(key);
            edges.push({ i: Math.min(i, j), j: Math.max(i, j), d, kind: 'brain' });
          }
        }
      }

      // 3. Axones: trazas tipo circuito que salen del cerebro hacia la página.
      //    Nacen en los nodos más a la izquierda/abajo y avanzan en ángulo recto.
      const anchors = nodes
        .slice(0, brainCount)
        .map((n, i) => ({ i, score: n.x - n.y * 0.55 }))
        .sort((a, b) => a.score - b.score)
        .slice(0, small ? 3 : 5);

      for (const a of anchors) {
        let from = a.i;
        let { x, y } = nodes[from];
        const legs = 2 + Math.floor(Math.random() * 2);
        let horizontal = true;
        for (let l = 0; l < legs; l++) {
          const reach = (horizontal ? W : H) * (0.09 + Math.random() * 0.13);
          const tx = horizontal ? x - reach : x;
          const ty = horizontal ? y : y + reach * 0.7;
          if (tx < W * 0.04 || ty > H * 0.94) break;
          // nodos intermedios cada ~46px para que el pulso tenga por dónde viajar
          const steps = Math.max(1, Math.round(Math.hypot(tx - x, ty - y) / 46));
          for (let s = 1; s <= steps; s++) {
            const px = x + ((tx - x) * s) / steps;
            const py = y + ((ty - y) * s) / steps;
            push({ x: px, y: py }, 'axon', 0.35, s === steps && l === legs - 1 ? 2.4 : 1.1);
            const to = nodes.length - 1;
            axonEdges.push(edges.length);
            edges.push({ i: from, j: to, d: Math.hypot(px - x, py - y) / steps, kind: 'axon' });
            from = to;
          }
          x = tx; y = ty;
          horizontal = !horizontal;
        }
      }
    }

    function resize() {
      const rect = canvas!.parentElement!.getBoundingClientRect();
      dpr = Math.min(window.devicePixelRatio || 1, 2);
      W = rect.width; H = rect.height;
      canvas!.width = Math.round(W * dpr);
      canvas!.height = Math.round(H * dpr);
      ctx!.setTransform(dpr, 0, 0, dpr, 0, 0);
      seed();
      if (reduced) drawFrame(0); // un solo cuadro estático
    }

    function spawnPulse() {
      if (!edges.length) return;
      // 45% de los pulsos salen por los axones: es la luz que va hacia la página
      const useAxon = axonEdges.length > 0 && Math.random() < 0.45;
      const e = useAxon
        ? axonEdges[Math.floor(Math.random() * axonEdges.length)]
        : Math.floor(Math.random() * edges.length);
      pulses.push({
        e, t: 0,
        v: 0.008 + Math.random() * 0.016,
        dir: useAxon ? 1 : (Math.random() < 0.5 ? 1 : -1),
        hue: Math.random() < 0.3 ? 'a' : 'b',
      });
    }

    // Cascada: cuando un pulso llega, la señal se propaga por las otras sinapsis
    function cascade(fromNode: number, hue: 'a' | 'b') {
      if (pulses.length > 60) return;
      for (let k = 0; k < edges.length; k++) {
        const e = edges[k];
        if (e.i !== fromNode && e.j !== fromNode) continue;
        if (Math.random() > 0.45) continue;
        pulses.push({
          e: k, t: 0,
          v: 0.012 + Math.random() * 0.014,
          dir: e.i === fromNode ? 1 : -1,
          hue,
        });
      }
    }

    function drawFrame(time: number) {
      ctx!.clearRect(0, 0, W, H);
      const t = time * 0.001;
      ctx!.globalAlpha = small ? 0.55 : 1; // en móvil el cerebro no compite con el texto

      // sinapsis y trazas (se iluminan cuando sus nodos están excitados)
      for (const e of edges) {
        const a = nodes[e.i], b = nodes[e.j];
        const excite = Math.max(a.glow, b.glow);
        const axon = e.kind === 'axon';
        const alpha = (axon ? 0.13 : Math.max(0.16, 0.34 - e.d / (W * 0.9))) + excite * 0.34;
        if (excite > 0.25) {
          const c = (a.hue === 'a' || b.hue === 'a') ? GLOW_A : GLOW_B;
          ctx!.strokeStyle = `rgba(${c.r},${c.g},${c.b},${Math.min(0.55, alpha)})`;
          ctx!.lineWidth = axon ? 1.2 : 1.4;
        } else {
          ctx!.strokeStyle = `rgba(135,168,176,${alpha})`;
          ctx!.lineWidth = 1;
        }
        ctx!.beginPath();
        ctx!.moveTo(a.x, a.y);
        ctx!.lineTo(b.x, b.y);
        ctx!.stroke();
      }

      // pulsos viajando
      for (let p = pulses.length - 1; p >= 0; p--) {
        const pu = pulses[p];
        pu.t += pu.v;
        if (pu.t >= 1) {
          const edge = edges[pu.e];
          const ti = pu.dir === 1 ? edge.j : edge.i;
          nodes[ti].glow = 1; // el nodo se enciende al recibir el pulso
          if (Math.random() < 0.5) cascade(ti, pu.hue); // y la señal se propaga
          pulses.splice(p, 1);
          continue;
        }
        const edge = edges[pu.e];
        const a = pu.dir === 1 ? nodes[edge.i] : nodes[edge.j];
        const b = pu.dir === 1 ? nodes[edge.j] : nodes[edge.i];
        const x = a.x + (b.x - a.x) * pu.t;
        const y = a.y + (b.y - a.y) * pu.t;
        const c = pu.hue === 'a' ? GLOW_A : GLOW_B;
        const g = ctx!.createRadialGradient(x, y, 0, x, y, 7);
        g.addColorStop(0, `rgba(${c.r},${c.g},${c.b},0.95)`);
        g.addColorStop(1, `rgba(${c.r},${c.g},${c.b},0)`);
        ctx!.fillStyle = g;
        ctx!.beginPath();
        ctx!.arc(x, y, 7, 0, Math.PI * 2);
        ctx!.fill();
        // estela sobre la sinapsis
        ctx!.strokeStyle = `rgba(${c.r},${c.g},${c.b},0.35)`;
        ctx!.lineWidth = 1.2;
        ctx!.beginPath();
        ctx!.moveTo(a.x + (b.x - a.x) * Math.max(0, pu.t - 0.12), a.y + (b.y - a.y) * Math.max(0, pu.t - 0.12));
        ctx!.lineTo(x, y);
        ctx!.stroke();
      }

      // nodos
      for (const nd of nodes) {
        // deriva orgánica: el cerebro respira, los axones casi no se mueven
        if (!reduced) {
          const amp = nd.kind === 'brain' ? 2.2 : 0.8;
          nd.x = nd.ox + Math.sin(t * 0.6 + nd.ph) * amp + Math.sin(t * 0.23 + nd.ph * 2.1) * amp * 0.5;
          nd.y = nd.oy + Math.cos(t * 0.5 + nd.ph * 1.3) * amp + Math.cos(t * 0.19 + nd.ph) * amp * 0.5;
        }
        // excitación por cercanía del cursor
        const dm = Math.hypot(nd.x - mouse.x, nd.y - mouse.y);
        if (dm < 130) nd.glow = Math.max(nd.glow, 1 - dm / 130);
        nd.glow *= 0.965; // decaimiento

        const c = nd.hue === 'a' ? GLOW_A : GLOW_B;
        const base = (nd.kind === 'brain' ? 0.6 : 0.3) + nd.glow * 0.4;
        if (nd.glow > 0.06) {
          const halo = ctx!.createRadialGradient(nd.x, nd.y, 0, nd.x, nd.y, 16 * nd.glow + 4);
          halo.addColorStop(0, `rgba(${c.r},${c.g},${c.b},${0.5 * nd.glow})`);
          halo.addColorStop(1, `rgba(${c.r},${c.g},${c.b},0)`);
          ctx!.fillStyle = halo;
          ctx!.beginPath();
          ctx!.arc(nd.x, nd.y, 16 * nd.glow + 4, 0, Math.PI * 2);
          ctx!.fill();
        }
        ctx!.fillStyle = `rgba(${c.r},${c.g},${c.b},${base})`;
        ctx!.beginPath();
        ctx!.arc(nd.x, nd.y, nd.r + nd.glow * 1.5, 0, Math.PI * 2);
        ctx!.fill();
      }
    }

    let last = 0;
    function loop(time: number) {
      if (!running) return;
      if (time - last > 1000 / 60) {
        last = time;
        if (Math.random() < 0.5) spawnPulse();
        if (pulses.length > 70) pulses.splice(0, pulses.length - 70);
        drawFrame(time);
      }
      raf = requestAnimationFrame(loop);
    }

    function onMove(ev: PointerEvent) {
      const r = canvas!.getBoundingClientRect();
      mouse.x = ev.clientX - r.left;
      mouse.y = ev.clientY - r.top;
    }
    function onLeave() { mouse.x = -9999; mouse.y = -9999; }
    function onVis() {
      running = document.visibilityState === 'visible';
      if (running && !reduced) raf = requestAnimationFrame(loop);
    }

    resize();
    const ro = new ResizeObserver(resize);
    ro.observe(canvas.parentElement!);
    canvas.parentElement!.addEventListener('pointermove', onMove);
    canvas.parentElement!.addEventListener('pointerleave', onLeave);
    document.addEventListener('visibilitychange', onVis);
    if (!reduced) raf = requestAnimationFrame(loop);

    return () => {
      running = false;
      cancelAnimationFrame(raf);
      ro.disconnect();
      canvas.parentElement?.removeEventListener('pointermove', onMove);
      canvas.parentElement?.removeEventListener('pointerleave', onLeave);
      document.removeEventListener('visibilitychange', onVis);
    };
  }, []);

  return <canvas ref={ref} aria-hidden="true" />;
}
