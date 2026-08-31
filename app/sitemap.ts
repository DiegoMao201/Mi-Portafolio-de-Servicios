import type { MetadataRoute } from 'next';
import { SITE } from '@/lib/site';
import { SERVICIOS } from '@/content/servicios';
import { CASOS } from '@/content/casos';
import { NOTAS } from '@/content/notas';

export default function sitemap(): MetadataRoute.Sitemap {
  const now = new Date();
  const base: MetadataRoute.Sitemap = [
    { url: `${SITE.url}/`, lastModified: now, changeFrequency: 'weekly', priority: 1 },
    { url: `${SITE.url}/servicios`, lastModified: now, changeFrequency: 'monthly', priority: 0.9 },
    { url: `${SITE.url}/casos`, lastModified: now, changeFrequency: 'monthly', priority: 0.9 },
    { url: `${SITE.url}/metodo`, lastModified: now, changeFrequency: 'monthly', priority: 0.7 },
    { url: `${SITE.url}/diego`, lastModified: now, changeFrequency: 'monthly', priority: 0.8 },
    { url: `${SITE.url}/notas`, lastModified: now, changeFrequency: 'weekly', priority: 0.7 },
    { url: `${SITE.url}/contacto`, lastModified: now, changeFrequency: 'yearly', priority: 0.8 },
    { url: `${SITE.url}/privacidad`, lastModified: now, changeFrequency: 'yearly', priority: 0.1 },
    { url: `${SITE.url}/habeas-data`, lastModified: now, changeFrequency: 'yearly', priority: 0.1 },
    { url: `${SITE.url}/terminos`, lastModified: now, changeFrequency: 'yearly', priority: 0.1 },
  ];
  const servicios = SERVICIOS.map((s) => ({
    url: `${SITE.url}/servicios/${s.slug}`,
    lastModified: now,
    changeFrequency: 'monthly' as const,
    priority: 0.9,
  }));
  const casos = CASOS.map((c) => ({
    url: `${SITE.url}/casos/${c.slug}`,
    lastModified: now,
    changeFrequency: 'monthly' as const,
    priority: 0.8,
  }));
  const notas = NOTAS.map((n) => ({
    url: `${SITE.url}/notas/${n.slug}`,
    lastModified: new Date(n.fecha),
    changeFrequency: 'yearly' as const,
    priority: 0.6,
  }));
  return [...base, ...servicios, ...casos, ...notas];
}
