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
      '@type': 'Person',
      '@id': `${SITE.url}/#diego`,
      name: 'Diego Mauricio García R.',
      jobTitle: 'Ingeniero industrial · Inteligencia de negocios y automatización',
      email: SITE.email,
      telephone: '+57 320 504 6277',
      url: `${SITE.url}/diego`,
      // Una entidad con rostro es mucho más fácil de reconciliar: Google y los
      // asistentes usan la imagen para confirmar que es la misma persona.
      image: `${SITE.url}/diego.png`,
      address: { '@type': 'PostalAddress', addressLocality: 'Pereira', addressRegion: 'Risaralda', addressCountry: 'CO' },
      alumniOf: {
        '@type': 'CollegeOrUniversity',
        name: 'Universidad Tecnológica de Pereira',
        sameAs: 'https://es.wikipedia.org/wiki/Universidad_Tecnológica_de_Pereira',
      },
      worksFor: { '@id': `${SITE.url}/#org` },
      knowsAbout: [
        'Ingeniería industrial', 'Inteligencia de negocios', 'Business Intelligence',
        'Automatización de procesos', 'Integración de sistemas y APIs', 'Analítica de datos',
        'PostgreSQL', 'SQL Server', 'Python', 'FastAPI', 'Next.js', 'Streamlit',
        'Agentes conversacionales', 'Retrieval-Augmented Generation', 'WhatsApp Cloud API',
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
      sameAs: ['https://github.com/DiegoMao201'] as string[],
    },
    {
      /* ProfessionalService en vez de solo Organization: le dice a un buscador
         y a un asistente QUÉ se vende, DÓNDE y POR CUÁNTO. Los precios son los
         mismos que ya están publicados en la página; no hay cifra nueva. */
      '@type': ['Organization', 'ProfessionalService'],
      '@id': `${SITE.url}/#org`,
      name: 'Datovate Nexus Pro',
      url: SITE.url,
      email: SITE.email,
      telephone: '+57 320 504 6277',
      founder: { '@id': `${SITE.url}/#diego` },
      sameAs: ['https://github.com/DiegoMao201'],
      description:
        'Automatización de procesos operativos, integración de sistemas y APIs, análisis ' +
        'de datos e inteligencia de negocios, bases de datos, agentes de IA conversacional ' +
        'y aplicaciones a la medida para empresas colombianas. Opera desde Pereira para ' +
        'todo el país, de forma remota.',
      knowsLanguage: 'es-CO',
      // El rango arranca en el plan mensual, que es la puerta de entrada real
      // para una pyme, no en el diagnóstico.
      priceRange: 'COP $150.000 – $3.900.000+',
      currenciesAccepted: 'COP',
      areaServed: { '@type': 'Country', name: 'Colombia' },
      serviceArea: { '@type': 'Country', name: 'Colombia' },
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
            price: '690000',
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
              minPrice: '3900000',
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
