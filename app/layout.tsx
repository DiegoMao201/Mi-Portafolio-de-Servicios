import type { Metadata, Viewport } from 'next';
import Script from 'next/script';
import '@fontsource/archivo/latin-500.css';
import '@fontsource/archivo/latin-600.css';
import '@fontsource/archivo/latin-700.css';
import '@fontsource/source-serif-4/latin-400.css';
import '@fontsource/source-serif-4/latin-600.css';
import '@fontsource/ibm-plex-mono/latin-400.css';
import '@fontsource/ibm-plex-mono/latin-500.css';
import './globals.css';
import { SITE, JSONLD_BASE, waLink } from '@/lib/site';
import Header from '@/components/Header';
import Footer from '@/components/Footer';
import Fx from '@/components/Fx';

export const metadata: Metadata = {
  metadataBase: new URL(SITE.url),
  title: {
    default: `${SITE.person} — ${SITE.title}`,
    template: `%s · ${SITE.shortName}`,
  },
  description: SITE.description,
  alternates: { canonical: '/' },
  openGraph: {
    type: 'website',
    locale: 'es_CO',
    url: SITE.url,
    siteName: SITE.shortName,
    title: `${SITE.person} — ${SITE.title}`,
    description: SITE.description,
  },
  robots: { index: true, follow: true },
};

export const viewport: Viewport = {
  themeColor: '#070B0E',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  const ga = process.env.NEXT_PUBLIC_GA_ID;
  return (
    <html lang="es-CO">
      <body>
        <Header />
        {children}
        <Footer />
        <Fx />
        <a
          className="wa-float"
          href={waLink('Hola Diego, vengo de datovatenexuspro.com y quiero hablar sobre un proyecto.')}
          target="_blank"
          rel="noopener"
          aria-label="Escribir por WhatsApp"
        >
          <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm0 18.2a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2Zm4.6-6.1c-.3-.1-1.5-.8-1.8-.9s-.4-.1-.6.1-.7.9-.8 1-.3.2-.6.1a6.7 6.7 0 0 1-2-1.2 7.4 7.4 0 0 1-1.4-1.7c-.1-.3 0-.4.1-.6l.4-.5c.1-.2.2-.3.3-.5a.6.6 0 0 0 0-.5c0-.1-.6-1.4-.8-1.9s-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3A2.9 2.9 0 0 0 6.7 9a5 5 0 0 0 1 2.7A11.4 11.4 0 0 0 12 15.5a14 14 0 0 0 1.5.5 3.6 3.6 0 0 0 1.6.1 2.7 2.7 0 0 0 1.8-1.2 2.2 2.2 0 0 0 .1-1.3c0-.1-.2-.2-.4-.3Z"/></svg>
          WhatsApp directo
        </a>
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(JSONLD_BASE) }}
        />
        {ga ? (
          <>
            <Script src={`https://www.googletagmanager.com/gtag/js?id=${ga}`} strategy="afterInteractive" />
            <Script id="ga4" strategy="afterInteractive">
              {`window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag('js',new Date());gtag('config','${ga}');`}
            </Script>
          </>
        ) : null}
      </body>
    </html>
  );
}
