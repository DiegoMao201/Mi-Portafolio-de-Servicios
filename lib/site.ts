export const SITE = {
  url: process.env.SITE_URL || 'https://www.datovatenexuspro.com',
  name: 'Diego Mauricio García R. · Datovate Nexus Pro',
  shortName: 'Datovate Nexus Pro',
  person: 'Diego Mauricio García R.',
  title: 'Automatización, sistemas e IA que operan empresas reales',
  description:
    'Ingeniero de software en Pereira. Construyo automatizaciones, integraciones, apps a la medida y agentes de IA que ya operan empresas reales.',
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
      jobTitle: 'Ingeniero de software y arquitecto de sistemas',
      email: SITE.email,
      telephone: '+57 320 504 6277',
      url: `${SITE.url}/diego`,
      address: { '@type': 'PostalAddress', addressLocality: 'Pereira', addressRegion: 'Risaralda', addressCountry: 'CO' },
      knowsAbout: [
        'Automatización de procesos', 'Integración de sistemas y APIs', 'PostgreSQL',
        'Aplicaciones web', 'Aplicaciones móviles', 'Agentes de IA', 'Inteligencia de negocios',
      ],
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
