'use client';

import { useEffect, useRef, useState } from 'react';

type Metrica = { clave: string; etiqueta: string; valor: number; unidad: string | null; nota: string };

/** Consola de telemetría: cifras reales que suben hasta su valor al entrar en pantalla. */
export default function Console() {
  const [metricas, setMetricas] = useState<Metrica[]>([]);
  const [shown, setShown] = useState<number[]>([]);
  const ref = useRef<HTMLDivElement>(null);
  const started = useRef(false);

  useEffect(() => {
    fetch('/api/telemetria')
      .then((r) => r.json())
      .then((j) => {
        const m: Metrica[] = j.metricas || [];
        setMetricas(m);
        setShown(m.map(() => 0));
      })
      .catch(() => {});
  }, []);

  useEffect(() => {
    if (!metricas.length || started.current) return;
    const el = ref.current;
    if (!el) return;
    const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    const run = () => {
      if (started.current) return;
      started.current = true;
      if (reduced) { setShown(metricas.map((m) => m.valor)); return; }
      const t0 = performance.now();
      const dur = 1400;
      const tick = (t: number) => {
        const p = Math.min(1, (t - t0) / dur);
        const ease = 1 - Math.pow(1 - p, 3);
        setShown(metricas.map((m) => Math.round(m.valor * ease)));
        if (p < 1) requestAnimationFrame(tick);
      };
      requestAnimationFrame(tick);
    };
    const io = new IntersectionObserver((es) => es.forEach((e) => e.isIntersecting && run()), { threshold: 0.4 });
    io.observe(el);
    return () => io.disconnect();
  }, [metricas]);

  if (!metricas.length) return null;

  return (
    <div className="console" ref={ref} role="group" aria-label="Telemetría de sistemas en operación">
      {metricas.map((m, i) => (
        <div className="c-cell" key={m.clave} title={m.nota} style={{ ['--cd' as string]: `${i * 0.9}s` }}>
          <span className="c-dot" aria-hidden="true" />
          <span className="c-v tnum">
            {(shown[i] ?? 0).toLocaleString('es-CO')}
            {m.unidad ? <small>{m.unidad}</small> : null}
          </span>
          <span className="c-k">{m.etiqueta}</span>
        </div>
      ))}
    </div>
  );
}
