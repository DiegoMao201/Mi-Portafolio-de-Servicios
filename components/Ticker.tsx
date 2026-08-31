const ITEMS = [
  'Automatización de procesos',
  'Integración de sistemas y APIs',
  'Aplicaciones web a la medida',
  'Apps en Play Store',
  'PostgreSQL · arquitectura de datos',
  'Agentes de IA conversacional',
  'Dashboards accionables',
  'Decisión en tiempo real',
  'Pereira → toda Colombia',
];

/** Cinta de capacidades en movimiento continuo. */
export default function Ticker() {
  const row = ITEMS.map((t, i) => <span key={i}>{t}</span>);
  const row2 = ITEMS.map((t, i) => <span key={`b${i}`} aria-hidden="true">{t}</span>);
  return (
    <div className="ticker" aria-label="Capacidades">
      <div className="ticker-track">{row}{row2}</div>
    </div>
  );
}
