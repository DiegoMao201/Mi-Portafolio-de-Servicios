import type { MetadataRoute } from 'next';
import { SITE } from '@/lib/site';

/* Los robots de los asistentes de IA van nombrados uno por uno: para ellos la
   invitación explícita pesa más que el comodín, y así queda escrito que este
   sitio quiere ser leído y citado. */
const IA = ['GPTBot', 'OAI-SearchBot', 'ChatGPT-User', 'ClaudeBot', 'Claude-SearchBot', 'Claude-User', 'PerplexityBot', 'Perplexity-User', 'Google-Extended', 'Applebot-Extended', 'Bingbot', 'CCBot', 'meta-externalagent'];

export default function robots(): MetadataRoute.Robots {
  // Mientras el sitio viva en el dominio temporal, poner NOINDEX=1 en Coolify.
  if (process.env.NOINDEX === '1') {
    return { rules: { userAgent: '*', disallow: '/' } };
  }
  return {
    rules: [{ userAgent: '*', allow: '/', disallow: ['/api/'] }, ...IA.map((userAgent) => ({ userAgent, allow: '/', disallow: ['/api/'] }))],
    sitemap: `${SITE.url}/sitemap.xml`,
  };
}
