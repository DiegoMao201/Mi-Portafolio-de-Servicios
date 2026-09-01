/**
 * La vena entre secciones: un cable que sale de donde terminó una sección y
 * entra por donde arranca la siguiente, con dos pulsos corriendo a distinta
 * velocidad. No es un adorno centrado: los extremos se dan por parámetro para
 * que el cable siga la composición asimétrica de la página — si el 03 sangra
 * por la izquierda y el 04 por la derecha, el cable cruza.
 *
 * Va en el flujo del documento, así que ocupa alto real y separa. Con
 * prefers-reduced-motion el cable queda, los pulsos no.
 */
export default function Vena({ de = 22, a = 22 }: { de?: number; a?: number }) {
  // Curva en S: sale vertical, cruza, entra vertical. Con preserveAspectRatio
  // "none" el trazo se estira, por eso el grosor va con vector-effect.
  const d = `M${de} 0 C ${de} 38, ${a} 58, ${a} 96`;
  return (
    <div className="vena" aria-hidden="true">
      <svg viewBox="0 0 100 96" preserveAspectRatio="none">
        <path d={d} fill="none" vectorEffect="non-scaling-stroke" />
        <path className="flow" d={d} fill="none" vectorEffect="non-scaling-stroke" />
        <path className="flow2" d={d} fill="none" vectorEffect="non-scaling-stroke" />
      </svg>
      <span className="vena-nodo" style={{ left: `${a}%` }} />
    </div>
  );
}
