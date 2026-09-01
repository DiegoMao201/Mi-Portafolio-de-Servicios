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
      // de la misma persona. Pendiente: agregar LinkedIn y GitHub.
      sameAs: [] as string[],
    },
    {
      '@type': 'Organization',
      '@id': `${SITE.url}/#org`,
      name: 'Datovate Nexus Pro',
      url: SITE.url,
      email: SITE.email,
      telephone: '+57 320 504 6277',
      founder: { '@id': `${SITE.url}/#diego` },
      areaServed: 'CO',
      address: { '@type': 'PostalAddress', addressLocality: 'Pereira', addressRegion: 'Risaralda', addressCountry: 'CO' },
    },
  ],
};
