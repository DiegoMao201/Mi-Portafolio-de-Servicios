import type { MetadataRoute } from 'next';
import { SITE } from '@/lib/site';

export default function robots(): MetadataRoute.Robots {
  // Mientras el sitio viva en el dominio temporal, poner NOINDEX=1 en Coolify.
  if (process.env.NOINDEX === '1') {
    return { rules: { userAgent: '*', disallow: '/' } };
  }
  return {
    rules: { userAgent: '*', allow: '/', disallow: ['/api/'] },
    sitemap: `${SITE.url}/sitemap.xml`,
  };
}
