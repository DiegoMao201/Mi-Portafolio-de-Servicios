export type Nota = {
  slug: string;
  titulo: string;
  descripcion: string;
  fecha: string; // ISO
  parrafos: { h?: string; t: string }[];
};

export const NOTAS: Nota[] = [
  {
    slug: 'migrar-streamlit-a-produccion',
    titulo: 'Migrar una app de Streamlit a producción: cuándo y cómo hacerlo',
    descripcion: 'Streamlit es excelente para prototipar y malo para ser tu producto. Cómo saber cuándo migrar y qué arquitectura usar sin botar lo aprendido.',
    fecha: '2026-08-31',
    parrafos: [
      { t: 'Streamlit es una de las mejores herramientas que existen para convertir un análisis de Python en una interfaz usable en horas. Y precisamente por eso muchas empresas terminan con Streamlit en producción sin haberlo decidido nunca: el prototipo funcionó, la gente lo empezó a usar, y un año después esa "prueba" es el sistema del que depende un proceso del negocio. Lo sé de primera mano: la primera versión de este mismo sitio fue una app de Streamlit.' },
      { h: 'Las señales de que ya toca migrar', t: 'Hay cuatro síntomas claros. Primero, Google no te ve: Streamlit entrega una página vacía que se pinta con JavaScript, así que tu contenido no existe para los buscadores. Segundo, la sesión se reinicia y los usuarios pierden trabajo. Tercero, cada usuario concurrente cuesta memoria del servidor de forma desproporcionada. Cuarto, quieres control fino de la interfaz —marca, velocidad, móvil— y peleas contra el framework en vez de trabajar con él.' },
      { h: 'Qué conservar de la app original', t: 'La lógica de Python casi siempre se salva completa. El error típico de la migración es reescribir todo; lo correcto es separar: la lógica de negocio y de datos se convierte en una API (FastAPI es la ruta natural, porque el código ya es Python), y solo la capa visual se reescribe en un framework web de verdad, como Next.js, que entrega HTML completo al navegador y a los buscadores.' },
      { h: 'La arquitectura de llegada', t: 'El patrón que uso: FastAPI sirviendo la lógica existente, Next.js sirviendo la interfaz con renderizado en servidor, PostgreSQL como fuente de datos, y todo desplegado con Docker detrás de un proxy con TLS automático. Con esa base, la app gana lo que Streamlit no puede dar: posicionamiento en Google, sesiones estables, control total del diseño y costos de servidor predecibles.' },
      { h: 'El error a evitar', t: 'No migres en caliente. Deja la app de Streamlit corriendo mientras la nueva versión se construye y se valida en un dominio temporal, y solo entonces cambia el dominio principal. La migración correcta es aburrida: el día del cambio no debería pasar nada visible, excepto que todo funciona mejor.' },
    ],
  },
  {
    slug: 'conectar-sql-server-con-postgresql-sin-tocar-el-erp',
    titulo: 'Conectar SQL Server con PostgreSQL sin tocar el ERP',
    descripcion: 'Cómo sacarle los datos a un ERP que no se puede modificar, construir una base intermedia confiable y automatizar procesos encima — sin poner en riesgo la operación.',
    fecha: '2026-08-31',
    parrafos: [
      { t: 'El escenario más común en las pymes colombianas que quieren automatizar: el ERP funciona, el contador lo domina, el proveedor del ERP no ofrece API y nadie en su sano juicio quiere tocarlo. La conclusión equivocada es "entonces no podemos automatizar". La correcta es: el ERP no se toca, y aun así se automatiza casi todo.' },
      { h: 'El principio: leer sin intervenir', t: 'Un ERP sobre SQL Server se puede consultar sin modificarlo: una extracción periódica de solo lectura, en horarios de baja carga, que copia lo necesario —facturas, cartera, inventario— hacia una base PostgreSQL aparte. El ERP ni se entera. Ese es el contrato de confianza con el negocio: pase lo que pase con la automatización, la operación contable sigue intacta.' },
      { h: 'Por qué una base intermedia y no consultas directas', t: 'Consultar el ERP directamente desde cada nueva herramienta multiplica el riesgo y acopla todo a un esquema que no controlas. La base intermedia invierte la ecuación: una sola extracción bien hecha, y encima de ella todas las aplicaciones, reportes y automatizaciones que quieras, con un modelo de datos limpio que sí controlas. Cuando el ERP cambie de versión, solo se ajusta la extracción.' },
      { h: 'Los detalles que cuestan días', t: 'Tres trampas típicas: filtros heredados en las consultas que excluyen registros legítimos sin que nadie recuerde por qué; cortes históricos mal definidos que duplican o pierden facturas al arrancar; y confiar en el correo como fuente de datos, cuando el correo es respaldo documental lleno de ruido — la fuente de verdad debe ser el dato estructurado. Cada una de estas me ha costado horas de diagnóstico en sistemas reales; por eso ahora se revisan primero.' },
      { h: 'Qué se vuelve posible después', t: 'Con la base intermedia estable, lo demás es rápido: escritorios de pago que arman lotes bancarios, tableros de cartera en tiempo real, alertas de inventario, conciliaciones automáticas. La inversión en la tubería se paga con la primera automatización y las siguientes salen casi gratis.' },
    ],
  },
  {
    slug: 'agente-de-ia-que-no-tumba-tu-sistema',
    titulo: 'Un agente de IA que atiende clientes sin poner en riesgo tu operación',
    descripcion: 'El diseño que separa al agente conversacional de tus sistemas críticos: base propia sincronizada, doble modelo por costo y salida idempotente.',
    fecha: '2026-08-31',
    parrafos: [
      { t: 'El miedo razonable de cualquier empresario ante un agente de IA no es que responda feo: es que un experimento conversacional termine afectando la facturación, el inventario o la base de clientes. Ese miedo tiene fundamento cuando el agente se conecta directo a los sistemas del negocio. La solución no es evitar la IA: es aislarla bien.' },
      { h: 'Regla uno: el agente nunca toca el transaccional en vivo', t: 'El agente conversa contra una base de datos propia, sincronizada periódicamente con el negocio. Si mil personas le escriben al mismo tiempo, se satura el agente — no tu facturación. Y cuando la conversación produce algo que el negocio debe procesar (un pedido, un dato de cliente), viaja de forma asíncrona por una cola con claves de idempotencia: llega cuando el sistema puede recibirlo y es imposible que se duplique.' },
      { h: 'Regla dos: dos modelos, no uno', t: 'La mayoría de los mensajes de una conversación comercial son simples: saludos, confirmaciones, preguntas frecuentes. Pagar un modelo de razonamiento potente por cada "sí, gracias" es regalar plata. El patrón correcto usa un modelo liviano para clasificar la intención de cada mensaje y reserva el modelo potente para donde hay razonamiento real. La cuenta mensual baja a una fracción sin que el cliente note diferencia.' },
      { h: 'Regla tres: el agente sabe lo que sabe', t: 'Un agente confiable responde solo sobre un corpus verificado del negocio, tiene reglas duras sobre lo que no puede afirmar ni prometer, y cuando no sabe, lo dice y escala a un humano. Todo queda registrado: cada conversación se puede auditar después. La confianza en la IA no se pide — se construye con arquitectura.' },
      { h: 'Por dónde empezar', t: 'Por el canal que controlas: tu propia web. Ahí se afina el corpus, se miden costos reales y se ajustan las reglas con riesgo cero. WhatsApp y otros canales llegan después, cuando el agente ya demostró la calidad de sus respuestas con datos, no con promesas.' },
    ],
  },
];

export function getNota(slug: string): Nota | undefined {
  return NOTAS.find((n) => n.slug === slug);
}
