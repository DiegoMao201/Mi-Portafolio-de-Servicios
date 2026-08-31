export type CasoDiagrama = {
  nodos: { id: string; label: string; sub?: string; capa: number; acento?: boolean }[];
  conexiones: { de: string; a: string; dato?: string }[];
};

export type Caso = {
  slug: string;
  codigo: string;
  titulo: string;
  cliente: string;
  resumen: string;
  contexto: string[];
  restriccion: string;
  arquitectura: string[];
  resultado: string[];
  stack: string[];
  diagrama: CasoDiagrama;
};

export const CASOS: Caso[] = [
  {
    slug: 'tesoreria-que-se-armaba-a-mano',
    codigo: 'E-01',
    titulo: 'La tesorería que se armaba a mano',
    cliente: 'Distribuidora ferretera del Eje Cafetero',
    resumen: 'El pago a proveedores se calculaba manualmente cruzando el ERP, correos y archivos sueltos. Hoy un sistema arma los lotes en minutos y la decisión sigue siendo humana.',
    contexto: [
      'Una distribuidora ferretera con múltiples sedes pagaba a decenas de proveedores cada semana. El proceso: exportar del ERP, cruzar con correos de proveedores, calcular descuentos por pronto pago y retenciones, armar el archivo del banco. Horas de trabajo experto, cada semana, con el riesgo de que un error se convirtiera en plata perdida o en una relación comercial dañada.',
    ],
    restriccion: 'Prohibido tocar el ERP. El sistema contable de la empresa no se podía modificar ni intervenir: cualquier solución tenía que construirse alrededor, sin riesgo para la operación.',
    arquitectura: [
      'Extracción periódica del ERP sin intervenirlo, hacia una base de datos intermedia que se convirtió en la fuente de verdad de cuentas por pagar.',
      'Lista blanca de proveedores: solo aparece lo que el administrador registra explícitamente, con detección de proveedores nuevos para registrarlos en un clic.',
      'Escritorio de pagos: facturas agrupadas por proveedor, lotes consolidados, exportador en el formato exacto que exige el banco y notificación automática a cada proveedor pagado.',
    ],
    resultado: [
      'El armado de un lote de pagos pasó de horas de trabajo manual a minutos.',
      'La decisión de qué pagar sigue siendo humana, con criterio de flujo de caja: el sistema eliminó el cálculo, no el criterio.',
      'Cada pago queda trazado desde la factura de origen hasta la notificación al proveedor.',
    ],
    stack: ['Python', 'PostgreSQL', 'Next.js', 'SendGrid', 'exportadores bancarios'],
    diagrama: {
      nodos: [
        { id: 'erp', label: 'ERP contable', sub: 'no se toca', capa: 0 },
        { id: 'ext', label: 'Extracción periódica', capa: 1 },
        { id: 'db', label: 'Base intermedia', sub: 'fuente de verdad', capa: 2, acento: true },
        { id: 'desk', label: 'Escritorio de pagos', capa: 3 },
        { id: 'banco', label: 'Archivo del banco', capa: 4 },
        { id: 'prov', label: 'Aviso a proveedores', capa: 4 },
      ],
      conexiones: [
        { de: 'erp', a: 'ext', dato: 'cuentas por pagar' },
        { de: 'ext', a: 'db' },
        { de: 'db', a: 'desk', dato: 'facturas filtradas' },
        { de: 'desk', a: 'banco', dato: 'lote consolidado' },
        { de: 'desk', a: 'prov', dato: 'notificación' },
      ],
    },
  },
  {
    slug: 'recaudo-digital-sin-friccion',
    codigo: 'E-02',
    titulo: 'Recaudo digital sin fricción',
    cliente: 'Distribuidora ferretera del Eje Cafetero',
    resumen: 'Dos portales de pago sobre pasarela, servidos por una misma base de código y ruteados por dominio, cada uno con su marco legal exacto.',
    contexto: [
      'La empresa necesitaba recibir pagos en línea en dos contextos distintos: cobros empresariales abiertos y aportes a un proyecto específico. Dos públicos, dos lenguajes, dos marcos legales — y un solo equipo para mantenerlo todo.',
    ],
    restriccion: 'Cada portal respondía a un marco legal distinto, y el lenguaje público tenía que reflejarlo con exactitud: una palabra mal usada podía tener consecuencias tributarias. La redacción final pasó por revisión contable.',
    arquitectura: [
      'Un solo servicio web sirviendo dos portales, ruteados por dominio mediante middleware: una base de código, dos experiencias completas.',
      'Integración con la pasarela de pagos resolviendo las exigencias no documentadas de su API — el tipo de detalle que consume días si no se ha hecho antes.',
      'Persistencia de cada transacción con panel administrativo: listado, filtros y exportación para conciliación contable.',
    ],
    resultado: [
      'Cobro en línea operativo con trazabilidad completa de cada transacción.',
      'Una sola base de código que mantener: la mitad del costo de mantenimiento de por vida.',
      'Lenguaje legal exacto en cada portal, validado por el equipo contable.',
    ],
    stack: ['Next.js 15', 'PostgreSQL', 'pasarela de pagos', 'middleware por dominio', 'Coolify'],
    diagrama: {
      nodos: [
        { id: 'c1', label: 'Cliente empresarial', capa: 0 },
        { id: 'c2', label: 'Aportante del proyecto', capa: 0 },
        { id: 'mw', label: 'Middleware por dominio', capa: 1, acento: true },
        { id: 'app', label: 'Un solo servicio web', capa: 2 },
        { id: 'pas', label: 'Pasarela de pagos', capa: 3 },
        { id: 'db', label: 'PostgreSQL + panel admin', capa: 3 },
      ],
      conexiones: [
        { de: 'c1', a: 'mw', dato: 'dominio A' },
        { de: 'c2', a: 'mw', dato: 'dominio B' },
        { de: 'mw', a: 'app' },
        { de: 'app', a: 'pas', dato: 'sesión de pago' },
        { de: 'app', a: 'db', dato: 'transacción' },
      ],
    },
  },
  {
    slug: 'bigotes-y-paticas',
    codigo: 'E-03',
    titulo: 'Bigotes y Paticas: retail completo',
    cliente: 'Bigotes y Paticas · Dosquebradas — empresa propia',
    resumen: 'E-commerce, portal de fidelización instalable, catálogo sincronizado y programa de puntos, sobre un monorepo con tienda, administración y API.',
    contexto: [
      'Bigotes y Paticas es mi tienda de mascotas en Dosquebradas. Es el caso donde no tengo que pedirte que me creas: puedes ver el resultado funcionando en vivo, porque el cliente soy yo y las consecuencias de cada decisión técnica las pago yo.',
      'La necesidad: competir en digital con las cadenas grandes sin el presupuesto de una cadena grande. Vender en línea, fidelizar con puntos y referidos, agendar servicios y administrar todo desde un solo panel.',
    ],
    restriccion: 'Presupuesto y equipo de una pyme real: cada componente tenía que pagarse solo. Nada de arquitectura de startup financiada — ingeniería de negocio que factura.',
    arquitectura: [
      'Monorepo con tres aplicaciones — tienda, administración y API — compartiendo un solo modelo de datos en PostgreSQL con contextos separados para CRM, catálogo y ventas.',
      'Portal de fidelización como aplicación web instalable (PWA): puntos por compra, referidos con recompensa en dos etapas, mascotas, citas e historial.',
      'Catálogo sincronizado automáticamente con Meta (467 productos) y SEO técnico completo: más de 1.000 URLs indexables, datos estructurados válidos y sitemap vivo.',
    ],
    resultado: [
      '434 clientes y 1.456 pedidos gestionados por el sistema.',
      'Programa de puntos y referidos operando solo: registra, acumula y premia sin intervención manual.',
      'Cierre de caja diario sistematizado y agendamiento de servicios en línea.',
    ],
    stack: ['Next.js 14', 'FastAPI', 'PostgreSQL', 'Turborepo', 'PWA', 'Meta Commerce', 'Coolify'],
    diagrama: {
      nodos: [
        { id: 'cli', label: 'Clientes', capa: 0 },
        { id: 'store', label: 'Tienda en línea', capa: 1 },
        { id: 'portal', label: 'Portal de fidelización', sub: 'PWA instalable', capa: 1, acento: true },
        { id: 'api', label: 'API central', capa: 2 },
        { id: 'db', label: 'PostgreSQL', sub: 'CRM · catálogo · ventas', capa: 3 },
        { id: 'meta', label: 'Catálogo Meta', sub: '467 productos', capa: 3 },
        { id: 'admin', label: 'Panel administrativo', capa: 2 },
      ],
      conexiones: [
        { de: 'cli', a: 'store' },
        { de: 'cli', a: 'portal', dato: 'puntos · citas' },
        { de: 'store', a: 'api' },
        { de: 'portal', a: 'api' },
        { de: 'api', a: 'db' },
        { de: 'db', a: 'meta', dato: 'sincronización' },
        { de: 'admin', a: 'db' },
      ],
    },
  },
  {
    slug: 'motores-de-decision-en-tiempo-real',
    codigo: 'E-04',
    titulo: 'Motores de decisión en tiempo real',
    cliente: 'Sistemas propios en operación continua',
    resumen: 'Sistemas que consumen flujos continuos de datos, evalúan reglas y modelos de IA, y ejecutan o vetan decisiones en milisegundos, con registro auditable de cada una.',
    contexto: [
      'Opero sistemas que procesan flujos de datos de mercado en vivo, las 24 horas: cada segundo llegan datos nuevos, y el sistema debe decidir —actuar, esperar o vetar— en milisegundos, sin supervisión humana continua.',
      'Este es el entorno de ingeniería más exigente en el que he trabajado: la latencia importa, las caídas cuestan dinero real y cada decisión tiene que poder explicarse después.',
    ],
    restriccion: 'Cero margen para el error silencioso: una decisión equivocada cuesta dinero propio en minutos. El sistema tenía que ser capaz de frenarse solo antes que equivocarse rápido.',
    arquitectura: [
      'Ingesta continua por websockets con reconexión automática y estados seguros ante cualquier caída.',
      'Evaluación por capas: reglas duras primero —los límites que nada puede saltarse—, modelos de IA después, con poder de veto sobre las acciones pero nunca sobre los límites.',
      'Bitácora total: cada decisión registra sus datos de entrada, su evaluación y su motivo. Cualquier comportamiento se puede reconstruir y auditar después.',
    ],
    resultado: [
      'Operación autónoma continua con supervisión por excepción: el sistema avisa cuando algo se sale de rango, no al revés.',
      'Un estándar de ingeniería —latencia, tolerancia a fallos, auditoría— que aplico a todo lo demás que construyo.',
      'La disciplina empírica como método: ninguna hipótesis sobrevive sin verificarse contra datos reales.',
    ],
    stack: ['Python', 'websockets', 'PostgreSQL', 'modelos de IA como capa de veto', 'Docker'],
    diagrama: {
      nodos: [
        { id: 'feed', label: 'Flujo de datos en vivo', sub: '24/7', capa: 0 },
        { id: 'rules', label: 'Reglas duras', sub: 'límites inviolables', capa: 1 },
        { id: 'ai', label: 'Modelos de IA', sub: 'pueden vetar', capa: 1, acento: true },
        { id: 'exec', label: 'Ejecución', capa: 2 },
        { id: 'log', label: 'Bitácora auditable', capa: 3 },
        { id: 'alert', label: 'Alertas', capa: 3 },
      ],
      conexiones: [
        { de: 'feed', a: 'rules', dato: 'cada tick' },
        { de: 'feed', a: 'ai' },
        { de: 'rules', a: 'exec', dato: 'permitir / frenar' },
        { de: 'ai', a: 'exec', dato: 'veto' },
        { de: 'exec', a: 'log', dato: 'decisión + motivo' },
        { de: 'exec', a: 'alert', dato: 'anomalías' },
      ],
    },
  },
  {
    slug: 'agente-que-toma-pedidos',
    codigo: 'E-05',
    titulo: 'El agente que toma pedidos',
    cliente: 'Plataforma interna de pedidos conversacionales',
    resumen: 'Agente conversacional que atiende pedidos, valida contra una base propia y alimenta un CRM con segmentación por valor — sin tocar jamás el sistema transaccional en vivo.',
    contexto: [
      'Diseñé y construí una plataforma donde un agente de IA toma pedidos conversando: entiende lo que el cliente quiere, valida productos y cantidades, y deja el pedido listo, alimentando de paso un CRM con segmentación por recencia, frecuencia y valor.',
    ],
    restriccion: 'El agente jamás puede bloquear ni saturar el sistema transaccional del negocio. Una conversación de IA no puede tumbar la facturación: el aislamiento era la condición número uno del diseño.',
    arquitectura: [
      'El agente conversa únicamente contra una base de datos propia, sincronizada periódicamente — nunca consulta el sistema del negocio en medio de una conversación.',
      'Doble modelo por costo: un modelo liviano clasifica la intención de cada mensaje; el modelo potente solo entra cuando el razonamiento lo exige. La cuenta de IA baja a una fracción.',
      'Salida por cola con claves de idempotencia: los pedidos viajan al sistema del negocio de forma asíncrona y sin posibilidad de duplicarse.',
    ],
    resultado: [
      'Pedidos conversacionales sin riesgo operativo para el negocio: el transaccional ni se entera de que la IA existe.',
      'CRM con segmentación RFM alimentado automáticamente por cada conversación.',
      'Patrón de arquitectura reutilizable: es el mismo aislamiento que aplico en cada agente que construyo.',
    ],
    stack: ['LangGraph', 'doble modelo LLM', 'PostgreSQL', 'patrón outbox', 'idempotencia', 'TypeScript'],
    diagrama: {
      nodos: [
        { id: 'cli', label: 'Cliente conversando', capa: 0 },
        { id: 'intent', label: 'Clasificador liviano', sub: 'intención', capa: 1 },
        { id: 'llm', label: 'Modelo potente', sub: 'solo si hace falta', capa: 1, acento: true },
        { id: 'db', label: 'Base propia sincronizada', capa: 2 },
        { id: 'queue', label: 'Cola de salida', sub: 'idempotente', capa: 3 },
        { id: 'crm', label: 'CRM · segmentación RFM', capa: 3 },
        { id: 'core', label: 'Sistema del negocio', sub: 'aislado y a salvo', capa: 4 },
      ],
      conexiones: [
        { de: 'cli', a: 'intent' },
        { de: 'intent', a: 'llm', dato: 'casos complejos' },
        { de: 'llm', a: 'db', dato: 'validación' },
        { de: 'intent', a: 'db' },
        { de: 'db', a: 'queue', dato: 'pedido listo' },
        { de: 'db', a: 'crm' },
        { de: 'queue', a: 'core', dato: 'asíncrono' },
      ],
    },
  },
];

export function getCaso(slug: string): Caso | undefined {
  return CASOS.find((c) => c.slug === slug);
}
