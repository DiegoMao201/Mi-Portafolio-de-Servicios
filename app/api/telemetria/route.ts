import { getMetricas } from '@/lib/db';

export const runtime = 'nodejs';
export const revalidate = 60;

// Semilla verificable: se usa mientras la tabla web.metricas no exista.
// Cada cifra tiene su nota de origen — nada de contadores inventados.
const SEED = [
  { clave: 'sistemas_operando', etiqueta: 'Sistemas construidos y operando', valor: 25, unidad: null, nota: 'Proyectos con historial de desarrollo propio, en operación o entregados' },
  { clave: 'clientes_gestionados', etiqueta: 'Clientes atendidos por sus sistemas', valor: 434, unidad: null, nota: 'Base de clientes de Bigotes y Paticas administrada por sistemas construidos por Diego' },
  { clave: 'pedidos_procesados', etiqueta: 'Pedidos procesados sin digitar a mano', valor: 1456, unidad: null, nota: 'Pedidos históricos gestionados por la plataforma de Bigotes y Paticas' },
  { clave: 'skus_sincronizados', etiqueta: 'Productos que se actualizan solos', valor: 467, unidad: null, nota: 'Catálogo publicado y sincronizado automáticamente con Meta' },
  { clave: 'meses_continuos', etiqueta: 'Meses construyendo sin parar', valor: 15, unidad: null, nota: 'Desarrollo continuo desde junio de 2025, verificable en el historial de los repositorios' },
];

export async function GET() {
  const fromDb = await getMetricas();
  return Response.json({ metricas: fromDb ?? SEED, fuente: fromDb ? 'db' : 'seed' });
}
