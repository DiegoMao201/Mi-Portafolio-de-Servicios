import { getMetricas } from '@/lib/db';

export const runtime = 'nodejs';
export const revalidate = 60;

// Semilla verificable: se usa mientras la tabla web.metricas no exista.
// Cada cifra tiene su nota de origen — nada de contadores inventados.
const SEED = [
  { clave: 'clientes_gestionados', etiqueta: 'Clientes en sistemas propios', valor: 434, unidad: null, nota: 'Base de clientes de Bigotes y Paticas administrada por sistemas construidos por Diego' },
  { clave: 'pedidos_procesados', etiqueta: 'Pedidos procesados', valor: 1456, unidad: null, nota: 'Pedidos históricos gestionados por la plataforma de Bigotes y Paticas' },
  { clave: 'skus_sincronizados', etiqueta: 'Productos sincronizados', valor: 467, unidad: null, nota: 'Catálogo publicado y sincronizado automáticamente con Meta' },
  { clave: 'urls_indexables', etiqueta: 'URLs indexables generadas', valor: 1027, unidad: null, nota: 'Sitemap de un e-commerce construido y posicionado por Diego' },
  { clave: 'decision_ms', etiqueta: 'Latencia de decisión', valor: 40, unidad: 'ms', nota: 'Orden de magnitud de los motores de decisión en tiempo real que Diego opera' },
];

export async function GET() {
  const fromDb = await getMetricas();
  return Response.json({ metricas: fromDb ?? SEED, fuente: fromDb ? 'db' : 'seed' });
}
