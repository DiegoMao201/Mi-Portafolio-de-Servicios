export type Nota = {
  slug: string;
  titulo: string;
  /** Título corto para <title> cuando el titular visible pasa de 39 caracteres. */
  tituloSeo?: string;
  descripcion: string;
  fecha: string; // ISO
  parrafos: { h?: string; t: string }[];
};

export const NOTAS: Nota[] = [
  {
    slug: 'cuanto-cuesta-automatizar-un-proceso-en-colombia',
    titulo: 'Cuánto cuesta automatizar un proceso en una empresa colombiana',
    tituloSeo: 'Cuánto cuesta automatizar un proceso',
    descripcion: 'La respuesta honesta depende de la complejidad del proceso y del estado de los datos. Aquí están los rangos reales, qué los mueve y qué se paga después.',
    fecha: '2026-09-01',
    parrafos: [
      { t: 'Es la primera pregunta que me hacen y casi nadie la responde con números. Voy a responderla, con la advertencia que va por delante: el precio depende de dos cosas —la complejidad del proceso y el estado en el que estén tus datos— y quien te dé una cifra cerrada sin haber visto ninguna de las dos te está adivinando el bolsillo, no el proyecto.' },
      { h: 'Primero la radiografía, no la cotización', t: 'Nadie opera a un paciente sin verlo. Antes de cualquier desarrollo hago una radiografía de la operación: quién hace qué, con qué archivos y sistemas, cuánto se demora, dónde se equivoca y dónde exactamente se está yendo la plata. Cuesta COP $300.000 y su entregable vale por sí solo — el mapa del proceso, el punto de fuga y la arquitectura propuesta son tuyos aunque no sigas conmigo. Sin ese paso, todo lo demás es una estimación con los ojos vendados.' },
      { h: 'El rango real de una implementación', t: 'Con la radiografía hecha, una automatización completa —que quede corriendo sola, no un script que alguien tenga que ejecutar— está entre COP $2.000.000 y $5.000.000. Ese rango no es capricho: lo mueven el número de sistemas que hay que conectar, si esos sistemas tienen forma de entregar datos o hay que sacárselos a la fuerza, cuántas excepciones tiene el proceso, y qué tan sucio esté el dato de origen. Un proceso de un solo sistema con datos limpios va al piso del rango. Tres sistemas que no se hablan y un Excel que cada quien llena a su manera, al techo.' },
      { h: 'Qué se paga después, y qué no', t: 'Aquí está la diferencia con un software que se arrienda: cuando el sistema queda automatizado y corriendo solo, no hay una licencia mensual que pagar por usarlo. Lo que sigue son auditorías periódicas — revisar que siga haciendo lo que debe, ajustar cuando el negocio cambia y agregar lo nuevo que aparezca. Nada más. El sistema es tuyo, en tu repositorio y en tu servidor.' },
      { h: 'Cómo saber si te conviene, en una cuenta de servilleta', t: 'Toma el proceso que quieres automatizar y calcula cuántas horas al mes consume de la persona que lo hace. Multiplica por lo que vale esa hora. Súmale lo que te ha costado el error más caro que ese proceso produjo el año pasado. Si el resultado anual se acerca al rango de arriba, la automatización se paga sola en meses, no en años. Y si no se acerca, te lo digo yo mismo antes de cobrarte nada: hay procesos que no vale la pena automatizar, y decirlo es parte del trabajo.' },
      { h: 'La advertencia que casi nadie da', t: 'El costo más alto de un proyecto de automatización no suele ser el desarrollo: es el dato sucio. Si tu inventario tiene el mismo producto con tres códigos distintos, o tus clientes están duplicados en dos sistemas, ningún software arregla eso solo — y ordenar ese desorden es trabajo que hay que presupuestar. Por eso la radiografía va primero: para que la sorpresa aparezca antes de la factura y no después.' },
    ],
  },
  {
    slug: 'cuanto-dinero-tienes-atrapado-en-tu-inventario',
    titulo: 'Cuánto dinero tienes atrapado en tu inventario (y cómo saberlo)',
    tituloSeo: 'Dinero atrapado en el inventario',
    descripcion: 'Un inventario quieto es capital congelado. Con qué datos se calcula cuánto tienes atrapado, y por qué la venta perdida es la fuga que nadie mide.',
    fecha: '2026-09-01',
    parrafos: [
      { t: 'Un inventario atrapado es capital que estás dejando quieto. No es una metáfora contable: es plata tuya, que ya pagaste, parada en una estantería en vez de estar circulando. Y la mayoría de las empresas no sabe cuánta tiene ahí, porque el inventario se mide en unidades y en el balance, no en el costo de la oportunidad perdida.' },
      { h: 'Con qué datos se calcula, y no hace falta un sistema nuevo', t: 'Para saber cuánto tienes atrapado no necesitas comprar software. Necesitas cruzar cinco cosas que tu operación ya genera: el flujo de ventas de cada producto, su rotación real, qué clientes lo compran, la estacionalidad de la demanda y la demanda promedio. Con eso sale la cuenta: cuánto de lo que tienes en bodega corresponde a demanda real y cuánto es un pedido que alguien hizo por costumbre, por miedo a quedarse corto o porque el proveedor daba descuento por volumen.' },
      { h: 'Lo que pasa cuando liberas ese capital', t: 'La conclusión del análisis no es "vende lo que no rota" y ya. Es más útil que eso: liberas ese capital y con esa misma plata compras producto que sí se vende. No estás pidiendo un préstamo ni inyectando dinero nuevo — estás moviendo el que ya tenías, de un producto muerto a uno vivo. Es la única mejora de flujo de caja que no le cuesta nada al dueño.' },
      { h: 'La venta perdida: la fuga que nadie mide', t: 'Y aquí está la mitad que casi siempre se ignora. Todo el mundo mira el exceso de inventario, porque se ve: está ahí ocupando espacio. Nadie mira lo contrario — la venta perdida, el pedido que no pudiste despachar porque no tenías el producto. Ese cliente no te reclama: simplemente compra en otro lado, y muchas veces no vuelve. No aparece en ningún informe, no deja rastro en el sistema y por eso no se gestiona. Es una fuga de ingresos importante y completamente invisible.' },
      { h: 'Un solo análisis resuelve las dos', t: 'Lo interesante es que el exceso y la venta perdida no son dos problemas: son el mismo problema mal repartido. Tienes demasiado de lo que no rota y muy poco de lo que sí. Los mismos datos que te dicen cuánto capital está atrapado te dicen dónde te estás quedando corto. Un análisis de inventarios bien hecho te soluciona las dos al tiempo, y por eso es de los trabajos con mejor retorno que existen en una operación comercial.' },
      { h: 'Por dónde empezar mañana', t: 'Empieza por lo más simple: exporta las ventas de los últimos doce meses y el inventario actual, y ordena los productos por rotación. Los que llevan meses sin moverse son tu capital atrapado. Los que se agotaron y tardaste en reponer son tu venta perdida. Esa lista, hecha una sola vez a mano, ya te dice si el problema es grande. Si lo es, entonces sí vale la pena automatizar el cálculo para que se actualice solo y avise antes de que ocurra, en vez de contarte lo que ya pasó.' },
    ],
  },
  {
    slug: 'como-sacar-los-datos-de-tu-erp-para-analizarlos',
    titulo: 'Cómo sacar los datos de tu ERP para analizarlos',
    tituloSeo: 'Sacar datos del ERP para analizar',
    descripcion: 'Tres formas de extraer información de tu ERP, de la más sencilla a la más confiable: informes manuales, conexión directa a la base de datos y APIs en vivo.',
    fecha: '2026-09-01',
    parrafos: [
      { t: 'Antes de analizar cualquier cosa hay que sacar el dato de donde vive, y ahí es donde se atascan la mayoría de los proyectos. La buena noticia: hay varias formas, y no todas requieren tocar el ERP. La regla que aplico en todas es la misma — los sistemas fuente no se tocan. Se lee de ellos sin intervenirlos, porque el sistema que factura no se pone en riesgo por un análisis.' },
      { h: '1. Informes exportados, tal como el ERP los entregue', t: 'La forma más sencilla y la que sirve para empezar hoy mismo: sacas del ERP los informes que necesitas para el análisis, en el formato que sea — CSV, Excel, o incluso texto plano. No importa que salgan feos ni que el formato sea raro: se procesan tal como el sistema los entregue. Ventaja: no requiere permisos especiales ni tocar nada. Desventaja: alguien tiene que acordarse de exportarlos, y ese alguien algún día se enferma o se va de vacaciones.' },
      { h: '2. Conexión directa a la base de datos', t: 'El siguiente escalón, y es más sencillo de lo que la gente cree: se conecta directamente a la base de datos del ERP en modo lectura y se extrae lo necesario de forma automatizada. Con una tarea programada de Windows corriendo cada noche, ya no depende de que alguien se acuerde. El dato llega solo. Es la opción que más rendimiento da por el esfuerzo que cuesta, y funciona incluso con ERP viejos que no tienen ninguna interfaz moderna.' },
      { h: '3. Conexión por API: en vivo', t: 'Cuando el ERP la ofrece, la conexión por API es más rápida y más confiable, y sobre todo trae el dato en vivo en vez de la foto de anoche. Deja de haber ventana ciega: si algo cambió hace diez minutos, el análisis ya lo sabe. Es lo que permite pasar de un informe que cuenta lo que pasó a un sistema que avisa mientras está pasando — y esa diferencia, en inventario o en cartera, es la que se traduce en plata.' },
      { h: 'Cuál elegir', t: 'No hay una respuesta única y tampoco hay que escoger para siempre. Lo normal es empezar por el informe exportado para validar que el análisis sirve, pasar a la conexión a base de datos cuando ya se usa de verdad, y llegar a la API cuando el negocio necesita reaccionar en el momento. Escalar así tiene una ventaja concreta: en cada paso ya tienes algo funcionando, y nunca pagas por una integración compleja antes de saber si el análisis vale la pena.' },
      { h: 'Lo que no se negocia', t: 'Sea cual sea la vía, tres reglas: se lee del sistema fuente sin intervenirlo, el dato extraído aterriza en una base intermedia que se vuelve la única versión de la verdad, y cada extracción deja registro de qué se trajo y cuándo. La tercera parece burocracia hasta el día en que un número no cuadra y hay que saber si el problema es del análisis o del origen.' },
    ],
  },
  {
    slug: 'migrar-streamlit-a-produccion',
    titulo: 'Migrar una app de Streamlit a producción: cuándo y cómo hacerlo',
    tituloSeo: 'Migrar de Streamlit a producción',
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
    tituloSeo: 'Conectar SQL Server con PostgreSQL',
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
    tituloSeo: 'Agentes de IA sin riesgo operativo',
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
