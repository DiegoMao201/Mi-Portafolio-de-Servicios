/** Línea conductora entre secciones: una vena del sistema con un pulso corriendo. */
export default function Conduit({ x = 50 }: { x?: number }) {
  const d = `M${x} 0 V56`;
  return (
    <div className="conduit" aria-hidden="true">
      <svg viewBox="0 0 100 56" preserveAspectRatio="none">
        <path d={d} fill="none" vectorEffect="non-scaling-stroke" />
        <path className="flow" d={d} fill="none" vectorEffect="non-scaling-stroke" />
        <path className="flow2" d={d} fill="none" vectorEffect="non-scaling-stroke" />
      </svg>
    </div>
  );
}
