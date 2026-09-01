'use client';

import { useEffect, useRef, useState } from 'react';

export type Fase = { n: string; titulo: string; texto: React.ReactNode };

/**
 * El momento anclado al scroll: el índice de fases se queda fijo a la izquierda
 * mientras las fases pasan por la derecha, y la fase que cruza el centro de la
 * pantalla se enciende. Es el único recurso de la casa que "se transforma
 * mientras bajas".
 *
 * Sin JavaScript se ve completo igual: las cuatro fases están en el HTML y el
 * índice sale con la primera marcada. La banda de deteccion es una franja
 * delgada en mitad del viewport (-45% arriba y abajo), no el viewport entero:
 * asi solo hay una fase activa a la vez y el cambio ocurre donde el ojo mira.
 */
export default function FasesMetodo({ fases }: { fases: Fase[] }) {
  const [activa, setActiva] = useState(0);
  const bloques = useRef<(HTMLDivElement | null)[]>([]);

  useEffect(() => {
    // El observador solo sirve de disparador: la fase activa se decide siempre
    // midiendo cual bloque tiene su centro mas cerca del centro de la pantalla.
    // Con la version anterior (marcar la que entra) el indice se quedaba en la
    // ultima fase vista al volver arriba del todo.
    const recalcular = () => {
      const centro = window.innerHeight / 2;
      let mejor = 0, min = Infinity;
      bloques.current.forEach((el, i) => {
        if (!el) return;
        const r = el.getBoundingClientRect();
        const d = Math.abs(r.top + r.height / 2 - centro);
        if (d < min) { min = d; mejor = i; }
      });
      setActiva(mejor);
    };
    // El scroll dispara muchas veces por segundo: se agrupa en un fotograma
    // para no medir el layout mas de lo necesario.
    let frame = 0;
    const alScroll = () => {
      if (frame) return;
      frame = requestAnimationFrame(() => { frame = 0; recalcular(); });
    };
    const io = new IntersectionObserver(recalcular, { rootMargin: '-30% 0px -30% 0px', threshold: 0 });
    bloques.current.forEach((el) => el && io.observe(el));
    window.addEventListener('scroll', alScroll, { passive: true });
    recalcular();
    return () => {
      io.disconnect();
      window.removeEventListener('scroll', alScroll);
      if (frame) cancelAnimationFrame(frame);
    };
  }, []);

  return (
    <div className="wrap">
      <div className="riel-fijo indice-fases" aria-hidden="true">
        <p className="label sec-kicker">Las cuatro fases</p>
        <ol>
          {fases.map((f, i) => (
            <li key={f.n} className={i === activa ? 'activa' : undefined}>
              <span className="if-n">{f.n}</span>
              <span className="if-t">{f.titulo}</span>
            </li>
          ))}
        </ol>
        <p className="if-pie">Ninguna se salta. El tamaño de cada una depende de tu caso.</p>
      </div>

      <div className="fases-cuerpo">
        {fases.map((f, i) => (
          <div
            key={f.n}
            className={`fase-bloque${i === activa ? ' activa' : ''}`}
            ref={(el) => { bloques.current[i] = el; }}
          >
            <span className="fb-n" aria-hidden="true">{f.n}</span>
            <h2>{f.titulo}</h2>
            <p>{f.texto}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
