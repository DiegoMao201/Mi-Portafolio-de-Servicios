'use client';

import { useEffect, useRef } from 'react';

export type GraphNode = { id: string; label: string; sub?: string; capa?: number; acento?: boolean };
export type GraphEdge = { de: string; a: string; dato?: string };

/**
 * Circuito de arquitectura: los trazos se dibujan al entrar en pantalla,
 * los nodos encienden en cascada y por cada conexión corren pulsos de luz.
 */
export default function ArchGraph({
  nodos, conexiones, caption, dark = false, eje = 'vertical',
}: {
  nodos: GraphNode[];
  conexiones: GraphEdge[];
  caption?: string;
  dark?: boolean;
  /** Una cadena lineal (una fase tras otra) se lee mejor en horizontal, y
   *  ademas llena el ancho: en vertical quedaba una columna flaca en el centro
   *  de una banda enorme. */
  eje?: 'vertical' | 'horizontal';
}) {
  const ref = useRef<HTMLDivElement>(null);

  // Capas: sin entradas = 0; el resto, máx(capa origen)+1
  const layers = new Map<string, number>();
  for (const n of nodos) if (typeof n.capa === 'number') layers.set(n.id, n.capa);
  let guard = 0;
  while (layers.size < nodos.length && guard++ < 20) {
    for (const n of nodos) {
      if (layers.has(n.id)) continue;
      const inc = conexiones.filter((e) => e.a === n.id);
      if (!inc.length) { layers.set(n.id, 0); continue; }
      if (inc.every((e) => layers.has(e.de))) {
        layers.set(n.id, Math.max(...inc.map((e) => layers.get(e.de)!)) + 1);
      }
    }
  }
  for (const n of nodos) if (!layers.has(n.id)) layers.set(n.id, 0);

  const horiz = eje === 'horizontal';
  const BW = 182, BH = 54, PADX = 24, PADY = 26;
  const ROW = 118;          // separacion entre capas en vertical
  // El hueco entre columnas lo manda la etiqueta de cable mas larga: con un
  // valor fijo, 'sistema en produccion' se montaba encima de las cajas.
  const anchoChip = (t: string) => t.length * 6.4 + 18;
  const chipMax = conexiones.reduce((m, e) => Math.max(m, e.dato ? anchoChip(e.dato) : 0), 0);
  const COL = BW + Math.max(80, Math.ceil(chipMax) + 34);
  const byLayer = new Map<number, GraphNode[]>();
  for (const n of nodos) {
    const l = layers.get(n.id)!;
    if (!byLayer.has(l)) byLayer.set(l, []);
    byLayer.get(l)!.push(n);
  }
  const maxLayer = Math.max(...Array.from(byLayer.keys()));
  const anchoGrupo = Math.max(...Array.from(byLayer.values()).map((g) => g.length));

  const W = horiz ? PADX * 2 + (maxLayer + 1) * BW + maxLayer * (COL - BW) : 900;
  const H = horiz
    ? PADY * 2 + anchoGrupo * BH + (anchoGrupo - 1) * 64
    : PADY * 2 + (maxLayer + 1) * BH + maxLayer * (ROW - BH);

  const pos = new Map<string, { x: number; y: number }>();
  for (const [l, group] of byLayer) {
    if (horiz) {
      const slot = (H - PADY * 2) / group.length;
      group.forEach((n, i) => {
        pos.set(n.id, { x: PADX + l * COL, y: PADY + slot * i + (slot - BH) / 2 });
      });
    } else {
      const slot = (W - PADX * 2) / group.length;
      group.forEach((n, i) => {
        pos.set(n.id, { x: PADX + slot * i + (slot - BW) / 2, y: PADY + l * ROW });
      });
    }
  }

  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    el.querySelectorAll<SVGPathElement>('path.draw').forEach((p, i) => {
      const len = p.getTotalLength();
      p.style.setProperty('--len', String(len));
      p.style.setProperty('--d', `${i * 110}ms`);
    });
    el.querySelectorAll<SVGGElement>('g.n-g').forEach((g, i) => {
      g.style.setProperty('--nd', `${i * 130}ms`);
    });
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
      el.classList.add('on');
      return;
    }
    const io = new IntersectionObserver(
      (es) => es.forEach((e) => { if (e.isIntersecting) { el.classList.add('on'); io.disconnect(); } }),
      { threshold: 0.3 }
    );
    io.observe(el);
    return () => io.disconnect();
  }, [nodos.length]);

  type EdgeGeo = { d: string; lx: number; ly: number; x1: number; y1: number; x2: number; y2: number };
  function edgeGeo(e: GraphEdge): EdgeGeo | null {
    const a = pos.get(e.de), b = pos.get(e.a);
    if (!a || !b) return null;
    // En horizontal el cable sale por el costado derecho y entra por el izquierdo.
    const x1 = horiz ? a.x + BW : a.x + BW / 2;
    const y1 = horiz ? a.y + BH / 2 : a.y + BH;
    const x2 = horiz ? b.x : b.x + BW / 2;
    const y2 = horiz ? b.y + BH / 2 : b.y;
    const dx = Math.max(28, (x2 - x1) * 0.55);
    const dy = Math.max(28, (y2 - y1) * 0.55);
    const d = horiz
      ? `M${x1} ${y1} C ${x1 + dx} ${y1}, ${x2 - dx} ${y2}, ${x2} ${y2}`
      : `M${x1} ${y1} C ${x1} ${y1 + dy}, ${x2} ${y2 - dy}, ${x2} ${y2}`;
    const lx = (x1 + x2) / 2;
    const ly = (y1 + y2) / 2;
    return { d, lx, ly, x1, y1, x2, y2 };
  }

  return (
    <div ref={ref} className={`${dark ? 'arch diag-arch' : 'arch'}${horiz ? ' arch--h' : ''}`}>
      {/* El lienzo se separa del pie: en pantallas estrechas un diagrama
          horizontal se desplaza en lugar de aplastarse hasta ser ilegible,
          y el pie de figura se queda quieto. */}
      <div className="arch-lienzo">
      <svg viewBox={`0 0 ${W} ${H}`} role="img" aria-label="Diagrama de arquitectura del sistema">
        {/* conexiones */}
        {conexiones.map((e, i) => {
          const g = edgeGeo(e);
          if (!g) return null;
          const chipW = e.dato ? e.dato.length * 6.4 + 18 : 0;
          return (
            <g key={`e${i}`}>
              <path className="e-glow" d={g.d} fill="none" />
              <path className="e-line draw" d={g.d} fill="none" />
              <path className={`e-flow ${i % 2 ? 'b' : ''}`} d={g.d} fill="none" style={{ animationDelay: `${i * 0.5}s` }} />
              <path className={`e-flow ${i % 2 ? '' : 'b'}`} d={g.d} fill="none" style={{ animationDelay: `${i * 0.5 + 1.3}s` }} />
              <circle className="port out" cx={g.x1} cy={g.y1} r={3.2} />
              <circle className="port" cx={g.x2} cy={g.y2} r={3.2} />
              {e.dato ? (
                <g>
                  <rect className="lbl-box" x={g.lx - chipW / 2} y={g.ly - 9} width={chipW} height={16} rx={2} />
                  <text className="e-label" x={g.lx} y={g.ly + 3} textAnchor="middle">{e.dato.toUpperCase()}</text>
                </g>
              ) : null}
            </g>
          );
        })}
        {/* nodos */}
        {nodos.map((n) => {
          const p = pos.get(n.id)!;
          return (
            <g key={n.id} className="n-g">
              <rect className={n.acento ? 'n-box acc' : 'n-box'} x={p.x} y={p.y} width={BW} height={BH} />
              {/* marcas de esquina técnicas */}
              <path className="n-tick" d={`M${p.x} ${p.y + 10} V${p.y} H${p.x + 10}`} fill="none" />
              <path className="n-tick" d={`M${p.x + BW - 10} ${p.y + BH} H${p.x + BW} V${p.y + BH - 10}`} fill="none" />
              <text className="n-t" x={p.x + 13} y={p.y + (n.sub ? 23 : 32)}>{n.label}</text>
              {n.sub ? <text className="n-s" x={p.x + 13} y={p.y + 41}>{n.sub.toUpperCase()}</text> : null}
            </g>
          );
        })}
      </svg>
      </div>
      {caption ? <div className="arch-cap">{caption}</div> : null}
    </div>
  );
}
