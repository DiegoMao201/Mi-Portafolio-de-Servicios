/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'standalone',
  images: { unoptimized: true },
  poweredByHeader: false,

  async redirects() {
    return [
      {
        /* Sin www respondia 200 igual que con www, asi que Google indexo las
           dos versiones como si fueran dos sitios distintos: en los resultados
           una salia con el logo y la otra con un icono generico. La canonica
           apunta a www, pero eso es una sugerencia — una redireccion 301 no.
           Consolida enlaces, autoridad y favicon en un solo dominio. */
        source: '/:path*',
        has: [{ type: 'host', value: 'datovatenexuspro.com' }],
        destination: 'https://www.datovatenexuspro.com/:path*',
        permanent: true,
      },
    ];
  },
};

export default nextConfig;
