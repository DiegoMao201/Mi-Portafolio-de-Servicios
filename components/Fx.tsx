'use client';

import { useEffect } from 'react';
import { usePathname } from 'next/navigation';

const SELECTOR = [
  '.card', '.sec-head', '.exp-block', '.callout', '.scroll-x',
  '.arch', '.diag', '.form', 'ul.clean', '.exp-meta', '.lede',
].join(',');

/** Hace que el contenido entre en escena al hacer scroll, con escalonado. */
export default function Fx() {
  const path = usePathname();

  useEffect(() => {
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
    const els = Array.from(document.querySelectorAll<HTMLElement>(SELECTOR));
    const io = new IntersectionObserver(
      (entries) => {
        entries.forEach((en) => {
          if (en.isIntersecting) {
            en.target.classList.add('fx-in');
            io.unobserve(en.target);
          }
        });
      },
      { threshold: 0.12, rootMargin: '0px 0px -6% 0px' }
    );
    els.forEach((el, i) => {
      if (el.classList.contains('fx-in')) return;
      el.classList.add('fx');
      el.style.transitionDelay = `${(i % 5) * 70}ms`;
      io.observe(el);
    });
    return () => io.disconnect();
  }, [path]);

  return null;
}
