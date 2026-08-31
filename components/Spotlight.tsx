'use client';

import { useEffect } from 'react';

/**
 * La firma de la casa: la misma luz que enciende el cerebro del hero, ahora en
 * las tarjetas. Al pasar el cursor sobre una rejilla, la tarjeta bajo el cursor
 * se ilumina desde el punto exacto donde está, y las demás de esa rejilla se
 * atenúan. En reposo no se ve nada: la página queda limpia y el efecto solo
 * aparece cuando alguien explora.
 *
 * El trabajo pesado lo hace el CSS: aquí solo se publica la posición del cursor
 * en dos variables (--mx, --my) y se marca la rejilla como activa.
 */
export default function Spotlight() {
  useEffect(() => {
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
    // En pantallas táctiles no hay cursor que seguir: no vale la pena el trabajo.
    if (!window.matchMedia('(hover: hover) and (pointer: fine)').matches) return;

    let frame = 0;
    let pending: { card: HTMLElement; x: number; y: number } | null = null;

    function flush() {
      frame = 0;
      if (!pending) return;
      const { card, x, y } = pending;
      card.style.setProperty('--mx', `${x}px`);
      card.style.setProperty('--my', `${y}px`);
      pending = null;
    }

    function onMove(ev: PointerEvent) {
      const target = ev.target as HTMLElement | null;
      const card = target?.closest<HTMLElement>('.card');
      const grid = target?.closest<HTMLElement>('.grid');
      if (!grid) return;

      if (card) {
        const r = card.getBoundingClientRect();
        pending = { card, x: ev.clientX - r.left, y: ev.clientY - r.top };
        if (!frame) frame = requestAnimationFrame(flush);
        if (!grid.classList.contains('lit')) grid.classList.add('lit');
        if (!card.classList.contains('on')) {
          grid.querySelectorAll('.card.on').forEach((c) => c.classList.remove('on'));
          card.classList.add('on');
        }
      } else {
        // dentro de la rejilla pero entre tarjetas: se apagan todas
        grid.classList.remove('lit');
        grid.querySelectorAll('.card.on').forEach((c) => c.classList.remove('on'));
      }
    }

    function onLeave(ev: PointerEvent) {
      const grid = (ev.target as HTMLElement | null)?.closest<HTMLElement>('.grid');
      if (!grid) return;
      grid.classList.remove('lit');
      grid.querySelectorAll('.card.on').forEach((c) => c.classList.remove('on'));
    }

    document.addEventListener('pointermove', onMove, { passive: true });
    document.addEventListener('pointerout', onLeave, { passive: true });
    return () => {
      if (frame) cancelAnimationFrame(frame);
      document.removeEventListener('pointermove', onMove);
      document.removeEventListener('pointerout', onLeave);
    };
  }, []);

  return null;
}
