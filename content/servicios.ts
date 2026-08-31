export type Servicio = {
  slug: string;
  titulo: string;
  /** Título corto para <title> cuando el titular visible pasa de 39 caracteres. */
  tituloSeo?: string;
  corto: string;
  respuesta: string;
  problema: string[];
  metodo: string[];
  entregables: string[];
  tecnologias: string[];
  faq: { q: string; a: string }[];
  casoSlug: string;
};

export const SERVICIOS: Servicio[] = [
  {
    slug: 'automatizacion-de-procesos',
    titulo: 'Automatización de procesos operativos',
    corto: 'El trabajo repetitivo que hoy hace una persona con Excel y paciencia, hecho por un sistema que no se cansa ni se equivoca.',
    respuesta: 'Automatizar un proceso operativo es reemplazar los pasos manuales repetitivos —copiar datos, cruzar archivos, calcular, notificar— por un sistema que los ejecuta solo, con registro de cada acción. El criterio de decisión sigue siendo humano; lo que se elimina es el trabajo mecánico.',
    problema: [
      'En la mayoría de las empresas hay al menos un proceso que consume horas de una persona valiosa haciendo trabajo mecánico: cruzar el reporte del ERP con un archivo del banco, armar el consolidado de pagos, pasar pedidos de un formato a otro, perseguir facturas por correo. Ese proceso funciona, pero se cae cuando la persona se enferma, se equivoca cuando está cansada, y no escala cuando el negocio crece.',
      'Lo he vivido del lado del dueño: administro empresas donde esos procesos existían, y los automaticé porque el costo real no era el tiempo — era el error silencioso y la dependencia de una sola persona.',
    ],
    metodo: [
      'Primero levanto el proceso como es, no como debería ser: quién lo hace, con qué archivos, cuánto se demora, dónde se equivoca. De ahí sale un mapa honesto.',
      'Después diseño la automatización respetando una regla: los sistemas fuente no se tocan. Se extrae de ellos sin intervenirlos, se procesa en una base intermedia, y la decisión final —qué se paga, qué se aprueba— sigue siendo de quien debe tomarla.',
      'Se construye por fases cortas con resultados verificables: cada semana algo que antes era manual deja de serlo.',
    ],
    entregables: [
      'Mapa del proceso actual con tiempos y puntos de error',
      'Sistema en producción corriendo en tu infraestructura o en la mía',
      'Registro auditable de cada ejecución',
      'Capacitación a tu equipo y documentación de operación',
    ],
    tecnologias: ['Python', 'PostgreSQL', 'Next.js', 'Docker', 'integraciones con ERP, correo, Dropbox y bancos'],
    faq: [
      { q: '¿Tengo que cambiar mi ERP o mi software actual?', a: 'No. La regla de diseño es no tocar los sistemas fuente: se extrae la información sin intervenirlos. Tu operación sigue igual mientras la automatización se construye al lado.' },
      { q: '¿Qué pasa si el proceso tiene excepciones que solo maneja una persona?', a: 'Las excepciones se enrutan a esa persona. Una buena automatización resuelve el 90% mecánico y le entrega a la persona solo los casos que de verdad necesitan criterio.' },
      { q: '¿Cuánto se demora?', a: 'El diagnóstico toma 5 días hábiles. Una automatización típica de un proceso administrativo está en producción entre 3 y 8 semanas, por fases con entregas verificables.' },
      { q: '¿Cómo sé que está funcionando bien?', a: 'Todo queda registrado: cada ejecución, cada dato movido, cada error. Puedes auditar lo que el sistema hizo, cosa que con el proceso manual casi nunca es posible.' },
    ],
    casoSlug: 'tesoreria-que-se-armaba-a-mano',
  },
  {
    slug: 'integracion-de-sistemas-y-apis',
    titulo: 'Integración de sistemas y APIs',
    corto: 'Tu ERP, tu banco, tu pasarela de pagos, tu e-commerce y tu contabilidad hablando entre ellos sin recurrir a un humano con dos pantallas.',
    respuesta: 'Integrar sistemas es hacer que las plataformas que ya usas —ERP, pasarela de pagos, e-commerce, mensajería, bancos— intercambien datos automáticamente mediante sus APIs, con una base intermedia que garantiza que nada se pierda ni se duplique.',
    problema: [
      'Cada software de tu empresa funciona bien solo. El problema es el espacio entre ellos: alguien exporta de uno e importa en otro, re-digita, concilia a mano. Cada frontera entre sistemas es un costo fijo mensual en horas y una fuente de errores.',
      'He conectado ERPs con bases de datos modernas, pasarelas de pago con contabilidad, catálogos con Meta y Google, mensajería con CRMs. La lección de todas esas integraciones: el patrón correcto casi nunca es conectar A con B directo, sino pasar por una base intermedia que absorba los caprichos de cada lado.',
    ],
    metodo: [
      'Inventario de sistemas y del dato que viaja: qué sale de dónde, hacia dónde, con qué frecuencia y qué pasa si llega tarde o repetido.',
      'Diseño con desacople: colas de salida, claves de idempotencia y reintentos. Si una parte se cae, el resto sigue y nada se duplica.',
      'Pruebas contra datos reales antes de conectar producción. Nunca se estrena una integración con datos vivos.',
    ],
    entregables: [
      'Integración en producción con monitoreo y alertas',
      'Base intermedia con el histórico del dato intercambiado',
      'Semáforos de salud: sabes si algo se atascó antes de que duela',
      'Documentación del flujo y plan de contingencia',
    ],
    tecnologias: ['APIs REST', 'PostgreSQL', 'Python', 'FastAPI', 'webhooks', 'SQL Server', 'pasarelas de pago', 'SendGrid'],
    faq: [
      { q: 'Mi ERP es viejo y no tiene API. ¿Se puede integrar?', a: 'Casi siempre sí. Un ERP sin API suele tener base de datos consultable o exportaciones programables; con eso se construye una extracción periódica sin tocar el sistema. Es exactamente como he integrado ERPs de escritorio con plataformas modernas.' },
      { q: '¿Qué pasa si la integración se cae un día?', a: 'Se diseña para eso: lo pendiente queda en cola y se procesa al volver, sin duplicados. Además recibes una alerta cuando algo lleva demasiado tiempo atascado, no cuando ya es un problema.' },
      { q: '¿Los datos quedan en manos de terceros?', a: 'No. La base intermedia vive en tu infraestructura o en un servidor dedicado bajo tu control. No dependo de plataformas de integración por suscripción que cobran por registro.' },
      { q: '¿Cuánto cuesta mantenerla?', a: 'Una integración bien construida requiere poco: el plan de operación mensual cubre monitoreo, ajustes cuando un sistema cambia y mejoras. Muchos meses no requiere intervención alguna.' },
    ],
    casoSlug: 'recaudo-digital-sin-friccion',
  },
  {
    slug: 'aplicaciones-web-a-la-medida',
    titulo: 'Aplicaciones web a la medida',
    corto: 'Cuando el software genérico te obliga a trabajar como él quiere, se construye uno que trabaja como tu operación necesita.',
    respuesta: 'Una aplicación web a la medida es un sistema construido para tu proceso exacto —con tus reglas, tus roles y tus datos— accesible desde cualquier navegador sin instalar nada, y alojado en infraestructura que controlas.',
    problema: [
      'El software genérico cubre el 70% de lo que necesitas y te deja peleando con el 30% restante: campos que no existen, reglas que no aplican, reportes que no dicen lo que necesitas saber. Ese 30% es donde vive tu diferencia competitiva.',
      'Construyo aplicaciones que son de la empresa: el código, los datos y el servidor quedan bajo tu control. Sin licencias por usuario que crecen con tu equipo, sin depender de que un proveedor decida subir precios.',
    ],
    metodo: [
      'Se parte del proceso, no de las pantallas: qué decisión toma cada rol y qué información necesita para tomarla bien.',
      'Interfaz rápida y directa: la app correcta es la que un empleado nuevo aprende en una tarde.',
      'Cada aplicación sale a producción con despliegue automatizado, respaldos y registro de actividad desde el día uno.',
    ],
    entregables: [
      'Aplicación en producción bajo tu dominio',
      'Panel de administración y control de roles',
      'Código fuente de tu propiedad en tu repositorio',
      'Despliegue automatizado y respaldos configurados',
    ],
    tecnologias: ['Next.js', 'React', 'TypeScript', 'PostgreSQL', 'FastAPI', 'Docker', 'Coolify'],
    faq: [
      { q: '¿El código queda mío?', a: 'Sí, completo y en tu repositorio. Si mañana quieres seguir con otro desarrollador, puede hacerlo. Estoy tan seguro de la calidad de lo que entrego que no necesito amarrarte.' },
      { q: '¿Web o instalada?', a: 'Web. Se usa desde cualquier navegador, celular incluido, sin instalar nada y con actualizaciones instantáneas para todos. Cuando hace falta funcionar sin internet o en tienda de aplicaciones, ese es otro servicio: apps móviles.' },
      { q: '¿Qué pasa cuando necesite cambios?', a: 'El plan de operación mensual los cubre. Y como el sistema se construye por módulos, agregar una función no implica reescribir lo existente.' },
      { q: '¿En cuánto tiempo está lista?', a: 'Una primera versión útil en producción: 4 a 8 semanas según el alcance. Prefiero entregar un núcleo que ya trabaje y crecer sobre él, que desaparecer seis meses.' },
    ],
    casoSlug: 'bigotes-y-paticas',
  },
  {
    slug: 'apps-moviles-play-store',
    titulo: 'Aplicaciones móviles en Play Store',
    corto: 'Tu operación o tu servicio en el bolsillo de tus clientes o tu equipo, publicado en Google Play.',
    respuesta: 'Desarrollo aplicaciones móviles publicadas en Google Play Store, y también PWAs —aplicaciones web que se instalan en el celular sin pasar por la tienda— cuando esa vía es más rápida y económica para el objetivo.',
    problema: [
      'Hay operaciones que suceden lejos del escritorio: el vendedor en la calle, el cliente que quiere pedir desde el sofá, el técnico en campo. Para ellas el navegador de escritorio no basta.',
      'La decisión honesta que casi nadie te cuenta: muchas veces no necesitas una app nativa de tienda. Una PWA bien construida se instala en el celular, funciona sin conexión, manda notificaciones y cuesta una fracción. He construido ambas y te recomiendo la que tu caso necesita, no la más cara.',
    ],
    metodo: [
      'Primero se define el trabajo que la app hace en el celular y qué debe funcionar sin señal.',
      'Se elige la vía con criterio de costo total: PWA instalable o app publicada en Play Store.',
      'Diseño para dedos y para afán: pantallas que se operan con una mano y flujos de tres toques.',
    ],
    entregables: [
      'App publicada en Google Play o PWA instalable bajo tu dominio',
      'Funcionamiento offline donde el flujo lo exige',
      'Backend y panel de administración incluidos',
      'Actualizaciones sin fricción para los usuarios',
    ],
    tecnologias: ['PWA', 'Next.js', 'React', 'Capacitor', 'notificaciones push', 'PostgreSQL'],
    faq: [
      { q: '¿PWA o app de tienda? ¿Cuál me conviene?', a: 'Si tu objetivo es que clientes o empleados usen el sistema desde el celular, una PWA suele bastar y sale a producción en semanas. La tienda vale la pena cuando necesitas presencia en Play Store como canal de descubrimiento o funciones profundas del teléfono.' },
      { q: '¿Funciona sin internet?', a: 'Los flujos críticos se diseñan para operar sin señal y sincronizar al volver la conexión. Se define contigo qué debe funcionar offline, porque cada cosa que lo hace tiene costo de complejidad.' },
      { q: '¿Ustedes publican la app en Play Store?', a: 'Sí, el servicio incluye la publicación completa: cuenta de desarrollador, fichas, revisiones de Google y las actualizaciones posteriores.' },
      { q: '¿La app necesita su propio servidor?', a: 'Usa un backend que queda en infraestructura tuya o administrada por mí, el mismo criterio de todo lo que construyo: control y propiedad para ti.' },
    ],
    casoSlug: 'bigotes-y-paticas',
  },
  {
    slug: 'bases-de-datos-y-arquitectura',
    titulo: 'Bases de datos y arquitectura de información',
    tituloSeo: 'Bases de datos y arquitectura',
    corto: 'Que el dato de tu empresa viva en un solo lugar confiable, y no repartido entre Excels, correos y la memoria de alguien.',
    respuesta: 'Diseño bases de datos PostgreSQL que se vuelven la fuente única de verdad de la empresa: modelan el negocio real, absorben los datos dispersos en archivos y sistemas, y quedan listas para reportes, aplicaciones e inteligencia artificial.',
    problema: [
      'La información existe, pero está repartida: una parte en el ERP, otra en Excels con versiones infinitas, otra en correos. Nadie confía del todo en ningún número porque hay tres versiones de cada uno. Sin una fuente única de verdad, cada reporte es una negociación.',
      'Todo lo que construyo se apoya en este servicio: una base bien diseñada es la diferencia entre un sistema que crece y uno que se enreda. Es el trabajo menos visible y el más determinante.',
    ],
    metodo: [
      'Modelado desde el negocio: clientes, productos, pedidos, pagos — el modelo refleja cómo opera tu empresa de verdad, con sus excepciones.',
      'Migración con verificación: los datos históricos se cargan y se cuadran contra la fuente. Ningún dato se da por migrado sin verificarse.',
      'Se deja lista para lo que sigue: reportes, aplicaciones encima, y estructuras que la IA pueda consumir.',
    ],
    entregables: [
      'Base PostgreSQL en producción con respaldos automáticos',
      'Migración verificada de tus datos históricos',
      'Diccionario de datos: qué significa cada cosa y de dónde sale',
      'Accesos por rol y auditoría de cambios',
    ],
    tecnologias: ['PostgreSQL', 'SQL Server', 'Python', 'modelado dimensional', 'respaldos automatizados'],
    faq: [
      { q: '¿Por qué PostgreSQL?', a: 'Es la base de datos de código abierto más sólida que existe: sin costo de licencia, escalable, y con capacidades modernas como JSON y búsqueda vectorial para IA. Es la que uso en todos mis sistemas en producción.' },
      { q: 'Mis datos están en un caos de Excels. ¿Por dónde se empieza?', a: 'Por el inventario: qué archivos existen, quién los alimenta y cuál es la versión confiable de cada dato. El caos casi siempre tiene menos fuentes reales de las que parece.' },
      { q: '¿Puedo seguir usando Excel?', a: 'Sí, pero como ventana y no como bodega: Excel sirve para analizar datos que salen de la base, no para almacenarlos. Ese solo cambio elimina el problema de versiones.' },
      { q: '¿Qué pasa con mi información? ¿Es confidencial?', a: 'Totalmente. Trabajo con acuerdos de confidencialidad, los datos quedan en servidores bajo tu control y mi política pública es no revelar jamás detalles internos de un cliente.' },
    ],
    casoSlug: 'tesoreria-que-se-armaba-a-mano',
  },
  {
    slug: 'agentes-de-ia-conversacional',
    titulo: 'Agentes de IA conversacional',
    corto: 'Un agente que atiende, responde con la información de tu negocio y captura al cliente — sin inventar y sin tumbar tus sistemas.',
    respuesta: 'Un agente de IA conversacional es un sistema que atiende a tus clientes en lenguaje natural —en tu web o por chat— respondiendo solo con la información verificada de tu negocio, capturando datos del interesado y escalando a un humano cuando corresponde.',
    problema: [
      'Los clientes escriben a toda hora y la capacidad de respuesta humana tiene horario. Cada mensaje sin responder en los primeros minutos es una venta que se enfría.',
      'El riesgo real de la IA conversacional no es técnico, es de confianza: un agente que inventa precios o promete lo que no existe hace más daño que no tener ninguno. Por eso mis agentes responden únicamente sobre un corpus verificado del negocio, nunca consultan tus sistemas críticos en medio de una conversación, y saben decir "eso lo confirma un humano".',
    ],
    metodo: [
      'Se construye el corpus: qué sabe el agente, con qué límites, qué tiene prohibido decir.',
      'Arquitectura desacoplada: el agente trabaja contra una base propia sincronizada, jamás en línea directa contra tu sistema transaccional. Si el agente se satura, tu operación ni se entera.',
      'Control de costos desde el diseño: límites por conversación, tope de gasto mensual y modelos elegidos por relación calidad/precio, con ruta de mejora cuando el volumen lo justifique.',
    ],
    entregables: [
      'Agente en producción en tu web o canal de chat',
      'Corpus de conocimiento del negocio, editable',
      'Captura y calificación automática de interesados, con aviso inmediato',
      'Registro completo de conversaciones y costos',
    ],
    tecnologias: ['LLMs (Claude, GPT, modelos abiertos)', 'OpenRouter', 'LangGraph', 'PostgreSQL', 'streaming', 'SendGrid'],
    faq: [
      { q: '¿El agente puede inventar cosas y quedar mal con mis clientes?', a: 'Ese riesgo se controla con diseño: responde solo sobre información verificada de tu negocio, con reglas duras de lo que no puede afirmar, y cuando no sabe lo dice y escala a un humano. Además todo queda registrado para auditar.' },
      { q: '¿Cuánto cuesta mantener la IA funcionando?', a: 'Menos de lo que se cree: con modelos bien elegidos, cientos de conversaciones al mes cuestan pocos dólares. Se configura un tope de gasto duro para que nunca haya sorpresas.' },
      { q: '¿Se conecta a WhatsApp?', a: 'Sí, es un canal habitual. Recomiendo empezar por la web —donde el control es total— y sumar WhatsApp cuando el corpus ya demostró calidad de respuestas.' },
      { q: '¿Reemplaza a mi equipo de atención?', a: 'Lo multiplica. El agente resuelve lo repetitivo y captura el dato a cualquier hora; tu equipo recibe conversaciones ya contextualizadas donde el humano sí agrega valor.' },
    ],
    casoSlug: 'agente-que-toma-pedidos',
  },
  {
    slug: 'dashboards-y-bi',
    titulo: 'Dashboards y BI accionable',
    corto: 'Indicadores que provocan decisiones — no un tablero bonito que nadie abre después de la segunda semana.',
    respuesta: 'Construyo tableros de indicadores conectados directamente a los datos reales de la empresa, diseñados alrededor de decisiones concretas: qué comprar, a quién cobrar, qué producto empuja el margen y cuál lo destruye.',
    problema: [
      'La mayoría de los dashboards fracasan por la misma razón: muestran datos en lugar de provocar decisiones. Un tablero con 40 gráficas que nadie consulta vale menos que una lista de cinco números que alguien revisa cada mañana porque le cambian el día.',
      'Diseño los indicadores desde la pregunta del negocio: margen real por producto, ventas por debajo de costo, clientes en riesgo de no volver, capital atrapado en inventario que no rota. Los mismos que uso para administrar mis propias operaciones.',
    ],
    metodo: [
      'Se parte de las decisiones, no de los datos: qué decide cada rol cada semana y qué número necesitaría para decidir mejor.',
      'Conexión directa a la fuente: el tablero lee de la base de datos, no de un Excel que alguien alimenta. Si requiere alimentación manual, ya nació muerto.',
      'Comparaciones honestas: mes contra el mismo corte del mes anterior, no contra el mes completo. Los indicadores mal calculados son peores que no tener ninguno.',
    ],
    entregables: [
      'Tablero web en producción, accesible desde cualquier dispositivo',
      'Indicadores accionables definidos contigo, con su ficha de cálculo',
      'Alertas cuando un indicador cruza el umbral que definas',
      'Fuente de datos automatizada, sin alimentación manual',
    ],
    tecnologias: ['Next.js', 'PostgreSQL', 'Python', 'visualización a la medida', 'GA4'],
    faq: [
      { q: '¿En qué se diferencia de Power BI?', a: 'Power BI es una gran herramienta si tienes quién modele los datos y mantenga los reportes. Lo que yo entrego es la solución completa: el dato ordenado, el indicador bien calculado y el tablero en tu dominio, sin licencias por usuario.' },
      { q: '¿Qué indicadores debería medir?', a: 'Depende de las decisiones que tomas. En distribución y retail, los que más plata mueven suelen ser margen real por producto, rotación de inventario, recompra de clientes y cartera por vencer. El diagnóstico define los tuyos.' },
      { q: '¿Cada cuánto se actualizan los datos?', a: 'Según la decisión que alimentan: los operativos cada pocos minutos, los gerenciales una vez al día. Actualizar más de lo necesario solo agrega costo.' },
      { q: '¿Sirve si mis datos están regados?', a: 'Ese es el caso típico. La primera fase ordena la fuente (ver bases de datos y arquitectura); el tablero llega cuando el dato es confiable, nunca antes.' },
    ],
    casoSlug: 'bigotes-y-paticas',
  },
  {
    slug: 'sistemas-de-decision-en-tiempo-real',
    titulo: 'Sistemas de decisión en tiempo real',
    corto: 'Sistemas que leen flujos continuos de datos, evalúan reglas y modelos, y actúan en milisegundos — con cada decisión registrada y auditable.',
    respuesta: 'Un sistema de decisión en tiempo real consume un flujo continuo de datos, lo evalúa contra reglas y modelos —incluida IA— y ejecuta o veta acciones en milisegundos, dejando registro auditable de cada decisión y su motivo.',
    problema: [
      'Hay decisiones que no pueden esperar al reporte de mañana: el precio que cambió, el nivel de inventario que cruzó el mínimo, la operación que hay que aprobar o frenar ya. Cuando la ventana de decisión se mide en segundos, un humano mirando pantallas no alcanza.',
      'He construido y operado motores que procesan flujos de datos de mercado en vivo y deciden en milisegundos, combinando reglas duras con modelos de IA que pueden vetar una acción. La exigencia de ese entorno —latencia, tolerancia a fallos, auditoría de cada decisión— es el estándar de ingeniería que aplico a cualquier dominio: inventarios, precios, alertas operativas, monitoreo.',
    ],
    metodo: [
      'Se define la decisión y su costo de error: qué se decide, con qué datos, qué pasa si el sistema se equivoca o se cae. De ahí salen los límites y las reglas de veto.',
      'Arquitectura de flujo: ingesta continua, evaluación por capas (reglas duras primero, modelos después) y ejecución con confirmación.',
      'Auditoría total: cada decisión queda registrada con sus datos de entrada y su motivo. Si algo sale raro, se reconstruye exactamente qué vio el sistema y por qué actuó.',
    ],
    entregables: [
      'Motor de decisión en producción con monitoreo continuo',
      'Reglas y límites definidos contigo, modificables sin reescribir código',
      'Bitácora auditable de cada decisión',
      'Alertas inmediatas ante comportamiento anómalo',
    ],
    tecnologias: ['Python', 'websockets y flujos en tiempo real', 'PostgreSQL', 'modelos de IA como capa de veto', 'Docker'],
    faq: [
      { q: '¿Esto aplica a un negocio normal o es solo para cosas exóticas?', a: 'Aplica a cualquier decisión repetitiva con ventana corta: reponer inventario cuando cruza el mínimo, ajustar precios ante cambios de costo, frenar un pedido con riesgo, alertar cuando una métrica se sale de rango. Lo exótico es la exigencia de ingeniería, no el uso.' },
      { q: '¿La IA decide sola?', a: 'Decide dentro de límites que tú defines, y las reglas duras siempre están por encima del modelo. En mis sistemas la IA puede vetar acciones, pero nunca saltarse un límite. El diseño responde a una pregunta: ¿cuál es el error que no te puedes permitir?' },
      { q: '¿Qué pasa si el sistema se cae?', a: 'Se diseña la caída antes que el vuelo: estados seguros, reconexión automática y alertas. Un sistema de tiempo real sin plan de caída es una bomba de tiempo, y eso se resuelve en arquitectura, no en parches.' },
      { q: '¿Puedo ver por qué tomó cada decisión?', a: 'Sí, esa es la regla de oro: bitácora completa de entradas, evaluación y motivo. La confianza en un sistema autónomo se construye pudiendo auditarlo.' },
    ],
    casoSlug: 'motores-de-decision-en-tiempo-real',
  },
];

export function getServicio(slug: string): Servicio | undefined {
  return SERVICIOS.find((s) => s.slug === slug);
}
