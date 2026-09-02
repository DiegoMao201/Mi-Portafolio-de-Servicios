export const SITE = {
  url: process.env.SITE_URL || 'https://www.datovatenexuspro.com',
  name: 'Diego Mauricio García R.',
  shortName: 'Diego García',
  /* Datovate Nexus Pro sigue siendo la firma comercial, pero en segundo plano:
     en consultoría se contrata a una persona, y una persona también es una
     entidad mucho más fácil de reconocer para los buscadores y las IA. */
  firma: 'Datovate Nexus Pro',
  person: 'Diego Mauricio García R.',
  title: 'Automatización, sistemas e IA que operan empresas reales',
  description:
    'Ingeniero industrial en Pereira. Automatización, integración de sistemas, inteligencia de negocios e IA aplicada para empresas colombianas.',
  email: 'diegomao.201@gmail.com',
  whatsapp: process.env.WHATSAPP_NUMBER || '573205046277',
  city: 'Pereira',
  region: 'Risaralda',
  country: 'CO',
} as const;

export function waLink(text: string): string {
  return `https://wa.me/${SITE.whatsapp}?text=${encodeURIComponent(text)}`;
}

export const JSONLD_BASE = {
  '@context': 'https://schema.org',
  '@graph': [
    {
      /* El nodo del sitio: da un ancla al grafo entero y deja explicito quien
         publica y en que idioma. Sin el, cada pagina es un grafo suelto. */
      '@type': 'WebSite',
      '@id': `${SITE.url}/#sitio`,
      url: SITE.url,
      /* El nombre del sitio que Google muestra encima de la URL en los
         resultados. Antes decia una cosa aqui y otra en og:site_name, y ante
         señales contradictorias Google se queda con el dominio pelado.
         Va la persona por delante: "Nexus Pro" colisiona con productos
         establecidos —Sonatype, Nexus Data— y el nombre propio no colisiona
         con nada. alternateName deja las otras formas por si Google prefiere
         alguna. */
      name: 'Diego Mauricio García R.',
      alternateName: ['Datovate Nexus Pro', 'Diego García', 'Datovate'],
      inLanguage: 'es-CO',
      publisher: { '@id': `${SITE.url}/#org` },
      about: { '@id': `${SITE.url}/#diego` },
    },
    {
      '@type': ['Organization', 'PetStore'],
      '@id': 'https://bigotesypaticas.com/#organization',
      name: 'Bigotes y Paticas',
      legalName: 'Diego Mauricio García — Bigotes y Paticas',
      url: 'https://bigotesypaticas.com',
      founder: { '@id': `${SITE.url}/#diego` },
      address: {
        '@type': 'PostalAddress',
        streetAddress: 'Mall Zamara Plaza, Cl. 15 #3A-07 Local 2',
        addressLocality: 'Dosquebradas',
        addressRegion: 'Risaralda',
        addressCountry: 'CO',
      },
      sameAs: ['https://www.instagram.com/bigotesypaticas/'],
    },
    {
      '@type': 'Person',
      '@id': `${SITE.url}/#diego`,
      name: 'Diego Mauricio García R.',
      jobTitle: 'Ingeniero industrial · Inteligencia de negocios y automatización',
      email: SITE.email,
      telephone: '+57 320 504 6277',
      /* El identificador va en la persona, que es quien esta registrada.
         Datovate Nexus Pro es la marca comercial bajo la que opera; la empresa
         como tal todavia no esta matriculada, asi que declararla como entidad
         legal seria exactamente la afirmacion no comprobable que se busca
         eliminar. Este NIT si es publico y consultable en el registro
         mercantil colombiano. */
      taxID: '1088266407',
      identifier: {
        '@type': 'PropertyValue',
        propertyID: 'NIT',
        value: '1088266407',
        description: 'Registro mercantil de Colombia (persona natural)',
      },
      url: `${SITE.url}/diego`,
      // Una entidad con rostro es mucho más fácil de reconciliar: Google y los
      // asistentes usan la imagen para confirmar que es la misma persona.
      image: `${SITE.url}/diego-6c8f3375.png`,
      address: { '@type': 'PostalAddress', addressLocality: 'Pereira', addressRegion: 'Risaralda', addressCountry: 'CO' },
      alumniOf: {
        '@type': 'CollegeOrUniversity',
        name: 'Universidad Tecnológica de Pereira',
        sameAs: [
          'https://es.wikipedia.org/wiki/Universidad_Tecnológica_de_Pereira',
          'https://www.wikidata.org/wiki/Q2441962',
        ],
      },
      workLocation: {
        '@type': 'City',
        name: 'Pereira',
        sameAs: 'https://www.wikidata.org/wiki/Q51111',
        containedInPlace: {
          '@type': 'AdministrativeArea',
          name: 'Risaralda',
          sameAs: 'https://www.wikidata.org/wiki/Q13993',
        },
      },
      nationality: { '@type': 'Country', name: 'Colombia', sameAs: 'https://www.wikidata.org/wiki/Q739' },
      worksFor: { '@id': `${SITE.url}/#org` },
      /* El vinculo con la otra empresa, declarado en las dos direcciones.
         Bigotes y Paticas es un negocio real, con local fisico, NIT publico y
         Perfil de Empresa de Google verificado, y esta legalmente a su nombre.
         Es la corroboracion externa que le faltaba a esta identidad: hasta
         ahora todo lo que se afirmaba aqui solo se podia comprobar aqui. */
      affiliation: { '@id': 'https://bigotesypaticas.com/#organization' },
      /* knowsAbout con entidades, no con cadenas de texto.
         Una lista de strings obliga a la maquina a adivinar: buscando "Python"
         en Wikidata el primer resultado es un genero de reptiles, "Pereira" es
         un apellido y "Risaralda" es un municipio de Caldas. Enlazando a la
         entidad canonica no queda nada que adivinar — es lo que permite que un
         buscador o un asistente resuelvan de que hablamos. */
      knowsAbout: [
        { '@type': 'Thing', name: 'Ingeniería industrial', sameAs: 'https://www.wikidata.org/wiki/Q4489420' },
        { '@type': 'Thing', name: 'Automatización de procesos de negocio', sameAs: 'https://www.wikidata.org/wiki/Q5001911' },
        { '@type': 'Thing', name: 'Inteligencia empresarial', sameAs: 'https://www.wikidata.org/wiki/Q3353185' },
        { '@type': 'Thing', name: 'Análisis de datos', sameAs: 'https://www.wikidata.org/wiki/Q1988917' },
        { '@type': 'Thing', name: 'Ciencia de datos', sameAs: 'https://www.wikidata.org/wiki/Q2374463' },
        { '@type': 'Thing', name: 'Inteligencia artificial', sameAs: 'https://www.wikidata.org/wiki/Q11660' },
        { '@type': 'Thing', name: 'Aprendizaje automático', sameAs: 'https://www.wikidata.org/wiki/Q2539' },
        { '@type': 'Thing', name: 'Generación aumentada por recuperación (RAG)', sameAs: 'https://www.wikidata.org/wiki/Q121362277' },
        { '@type': 'Thing', name: 'Integración de sistemas', sameAs: 'https://www.wikidata.org/wiki/Q1665453' },
        { '@type': 'Thing', name: 'Planificación de recursos empresariales (ERP)', sameAs: 'https://www.wikidata.org/wiki/Q131508' },
        { '@type': 'Thing', name: 'Agentes conversacionales', sameAs: 'https://www.wikidata.org/wiki/Q870780' },
        { '@type': 'Thing', name: 'PostgreSQL', sameAs: 'https://www.wikidata.org/wiki/Q192490' },
        { '@type': 'Thing', name: 'Python', sameAs: 'https://www.wikidata.org/wiki/Q28865' },
        { '@type': 'Thing', name: 'TypeScript', sameAs: 'https://www.wikidata.org/wiki/Q978185' },
        { '@type': 'Thing', name: 'Next.js', sameAs: 'https://www.wikidata.org/wiki/Q56062435' },
        { '@type': 'Thing', name: 'FastAPI', sameAs: 'https://www.wikidata.org/wiki/Q101119404' },
        'Control de inventarios', 'Optimización de compras', 'Análisis financiero',
      ],
      description:
        'Ingeniero industrial de la Universidad Tecnológica de Pereira y desarrollador de ' +
        'software. Integra analítica de datos, desarrollo web e inteligencia artificial para ' +
        'optimizar procesos comerciales, logísticos y empresariales. Con experiencia previa en ' +
        'liderazgo de compras y gestión comercial en el sector de recubrimientos, adhesivos y ' +
        'suministros industriales.',
      // sameAs: enlaza esta página con los perfiles públicos de Diego. Es la
      // señal con la que buscadores y asistentes de IA confirman que se trata
      // de la misma persona en todas partes.
      sameAs: [
        'https://github.com/DiegoMao201',
        'https://www.linkedin.com/in/diegomauriciogarcia',
      ] as string[],
    },
    {
      /* ProfessionalService en vez de solo Organization: le dice a un buscador
         y a un asistente QUÉ se vende, DÓNDE y POR CUÁNTO. Los precios son los
         mismos que ya están publicados en la página; no hay cifra nueva. */
      '@type': ['Organization', 'ProfessionalService'],
      '@id': `${SITE.url}/#org`,
      name: 'Datovate Nexus Pro',
      /* Marca comercial bajo la que opera Diego como persona natural. Cuando la
         empresa quede matriculada, aqui entran legalName y su propio NIT. */
      brand: { '@type': 'Brand', name: 'Datovate Nexus Pro' },
      url: SITE.url,
      email: SITE.email,
      telephone: '+57 320 504 6277',
      founder: { '@id': `${SITE.url}/#diego` },
      sameAs: [
        'https://github.com/DiegoMao201',
        'https://www.linkedin.com/in/diegomauriciogarcia',
        'https://www.google.com/search?kgmid=/g/11zxd85728',
      ],
      /* KGMID: el identificador que Google asigno a esta entidad en su
         Knowledge Graph. Declararlo cierra el circulo — el sitio afirma ser la
         misma entidad que Google ya reconocio, y deja de depender de que Google
         lo deduzca solo. */
      identifier: {
        '@type': 'PropertyValue',
        propertyID: 'Google Knowledge Graph',
        value: '/g/11zxd85728',
      },
      description:
        'Automatización de procesos operativos, integración de sistemas y APIs, análisis ' +
        'de datos e inteligencia de negocios, bases de datos, agentes de IA conversacional ' +
        'y aplicaciones a la medida para empresas colombianas. Opera desde Pereira para ' +
        'todo el país, de forma remota.',
      knowsLanguage: 'es-CO',
      // El rango arranca en el plan mensual, que es la puerta de entrada real
      // para una pyme, no en el diagnóstico.
      priceRange: 'COP $150.000 – $5.000.000',
      currenciesAccepted: 'COP',
      areaServed: { '@type': 'Country', name: 'Colombia', sameAs: 'https://www.wikidata.org/wiki/Q739' },
      serviceArea: { '@type': 'Country', name: 'Colombia', sameAs: 'https://www.wikidata.org/wiki/Q739' },
      hasOfferCatalog: {
        '@type': 'OfferCatalog',
        name: 'Servicios de automatización e IA aplicada',
        itemListElement: [
          {
            '@type': 'Offer',
            name: 'Llamada de diagnóstico inicial',
            description: 'Conversación técnica de 30 minutos sobre tu operación, sin compromiso.',
            price: '0',
            priceCurrency: 'COP',
          },
          {
            '@type': 'Offer',
            name: 'Diagnóstico de operación',
            description:
              'Cinco días hábiles: mapa del proceso, dónde se pierde tiempo y dinero, ' +
              'arquitectura propuesta, plan por fases y estimado de inversión. Se abona el ' +
              '100% al proyecto si se contrata dentro de 30 días.',
            price: '300000',
            priceCurrency: 'COP',
          },
          {
            '@type': 'Offer',
            name: 'Construcción del sistema',
            description:
              'Sistema completo en producción: datos, integraciones, aplicación, despliegue ' +
              'y capacitación. Por hitos verificables (40/30/30).',
            priceCurrency: 'COP',
            priceSpecification: {
              '@type': 'PriceSpecification',
              minPrice: '2000000',
              maxPrice: '5000000',
              priceCurrency: 'COP',
            },
          },
          {
            '@type': 'Offer',
            name: 'Operación y evolución',
            description: 'Monitoreo, soporte, ajustes y nuevas automatizaciones cada mes.',
            priceCurrency: 'COP',
            priceSpecification: {
              '@type': 'PriceSpecification',
              minPrice: '150000',
              priceCurrency: 'COP',
              billingDuration: 1,
              billingIncrement: 1,
            },
          },
        ],
      },
      address: { '@type': 'PostalAddress', addressLocality: 'Pereira', addressRegion: 'Risaralda', addressCountry: 'CO' },
    },
  ],
};
