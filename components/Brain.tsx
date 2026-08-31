'use client';

import { useEffect, useRef } from 'react';

/**
 * El cerebro de luces: red neuronal viva dibujada en canvas.
 * Nodos orgánicos conectados por sinapsis; pulsos de luz viajan por las
 * conexiones y encienden los nodos al llegar. El cursor excita la zona cercana.
 */
type Node = { x: number; y: number; ox: number; oy: number; r: number; glow: number; hue: 'a' | 'b'; ph: number };
type Edge = { i: number; j: number; d: number };
type Pulse = { e: number; t: number; v: number; dir: 1 | -1; hue: 'a' | 'b' };

const GLOW_A = { r: 255, g: 116, b: 64 };   // naranja señal
const GLOW_B = { r: 63, g: 216, b: 206 };   // cian técnico

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
    let pulses: Pulse[] = [];
    let raf = 0;
    let running = true;
    const mouse = { x: -9999, y: -9999 };

    function seed() {
      const n = W < 700 ? 64 : 110;
      nodes = [];
      // Nubes orgánicas: tres cúmulos con densidad hacia la derecha del hero
      const clusters = [
        { cx: W * 0.68, cy: H * 0.42, rx: W * 0.26, ry: H * 0.36, w: 0.55 },
        { cx: W * 0.88, cy: H * 0.68, rx: W * 0.18, ry: H * 0.26, w: 0.25 },
        { cx: W * 0.30, cy: H * 0.78, rx: W * 0.30, ry: H * 0.22, w: 0.20 },
      ];
      for (let i = 0; i < n; i++) {
        let c = clusters[0];
        const p = Math.random();
        if (p > clusters[0].w && p <= clusters[0].w + clusters[1].w) c = clusters[1];
        else if (p > clusters[0].w + clusters[1].w) c = clusters[2];
        const ang = Math.random() * Math.PI * 2;
        const rad = Math.sqrt(Math.random());
        const x = c.cx + Math.cos(ang) * c.rx * rad;
        const y = c.cy + Math.sin(ang) * c.ry * rad;
        nodes.push({
          x, y, ox: x, oy: y,
          r: 1 + Math.random() * 1.8,
          glow: Math.random() * 0.3,
          hue: Math.random() < 0.24 ? 'a' : 'b',
          ph: Math.random() * Math.PI * 2,
        });
      }
      // Sinapsis: k vecinos más cercanos
      edges = [];
      const seen = new Set<string>();
      for (let i = 0; i < nodes.length; i++) {
        const dists = nodes
          .map((m, j) => ({ j, d: (m.x - nodes[i].x) ** 2 + (m.y - nodes[i].y) ** 2 }))
          .filter((o) => o.j !== i)
          .sort((a, b) => a.d - b.d)
          .slice(0, 3);
        for (const { j, d } of dists) {
          const key = i < j ? `${i}-${j}` : `${j}-${i}`;
          if (!seen.has(key) && Math.sqrt(d) < W * 0.16) {
            seen.add(key);
            edges.push({ i: Math.min(i, j), j: Math.max(i, j), d: Math.sqrt(d) });
          }
        }
      }
      pulses = [];
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
      const e = Math.floor(Math.random() * edges.length);
      pulses.push({
        e, t: 0,
        v: 0.008 + Math.random() * 0.016,
        dir: Math.random() < 0.5 ? 1 : -1,
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

      // sinapsis (se iluminan cuando sus nodos están excitados)
      for (const e of edges) {
        const a = nodes[e.i], b = nodes[e.j];
        const excite = Math.max(a.glow, b.glow);
        const alpha = Math.max(0.06, 0.17 - e.d / (W * 1.4)) + excite * 0.3;
        if (excite > 0.25) {
          const c = (a.hue === 'a' || b.hue === 'a') ? GLOW_A : GLOW_B;
          ctx!.strokeStyle = `rgba(${c.r},${c.g},${c.b},${Math.min(0.55, alpha)})`;
          ctx!.lineWidth = 1.4;
        } else {
          ctx!.strokeStyle = `rgba(120,150,158,${alpha})`;
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
        // deriva orgánica visible
        if (!reduced) {
          nd.x = nd.ox + Math.sin(t * 0.6 + nd.ph) * 9 + Math.sin(t * 0.23 + nd.ph * 2.1) * 5;
          nd.y = nd.oy + Math.cos(t * 0.5 + nd.ph * 1.3) * 9 + Math.cos(t * 0.19 + nd.ph) * 5;
        }
        // excitación por cercanía del cursor
        const dm = Math.hypot(nd.x - mouse.x, nd.y - mouse.y);
        if (dm < 130) nd.glow = Math.max(nd.glow, 1 - dm / 130);
        nd.glow *= 0.965; // decaimiento

        const c = nd.hue === 'a' ? GLOW_A : GLOW_B;
        const base = 0.35 + nd.glow * 0.65;
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
        if (Math.random() < 0.45) spawnPulse();
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
