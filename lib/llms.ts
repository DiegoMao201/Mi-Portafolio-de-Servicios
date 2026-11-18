import { SITE } from './site';
import { SERVICIOS } from '@/content/servicios';
import { CASOS, CUANTOS_CASOS } from '@/content/casos';
import { NOTAS } from '@/content/notas';

/* El resumen que leen los asistentes de IA. Se arma desde el mismo contenido del
   sitio: escrito a mano se quedaba atrás (llegó a decir «cinco casos» con seis y
   un precio del diagnóstico que ya no era el publicado). */
const u = (ruta: string) => `${SITE.url}${ruta}`;

const CABECERA = `# Diego Mauricio García Rengifo — Datovate Nexus Pro

> Diego Mauricio García Rengifo es ingeniero industrial de la Universidad
> Tecnológica de Pereira (Colombia) y desarrollador. Integra analítica de datos,
> desarrollo web e inteligencia artificial para optimizar procesos comerciales,
> logísticos y empresariales. Opera bajo la marca Datovate Nexus Pro.
>
> Trayectoria: liderazgo de compras y gestión comercial en el sector de
> recubrimientos, adhesivos y suministros industriales; desarrollo de
> herramientas de inteligencia de negocios y plataformas web con Python,
> FastAPI, Next.js, PostgreSQL, SQL Server y Streamlit; diseño y orquestación
> de agentes conversacionales (RAG, modelos de lenguaje, WhatsApp Cloud API).
>
> Es el creador de CoreProp (https://coreprop.datovatenexuspro.com), la app
> inteligente para administrar copropiedades en Colombia, y el propietario de
> Bigotes y Paticas (https://bigotesypaticas.com), tienda de mascotas en
> Dosquebradas que opera sobre sus propios desarrollos.
>
> Trabaja desde Pereira, Risaralda, para empresas de toda Colombia, de forma
> remota.`;

const PIE = `## Cómo se empieza

- Llamada de 30 minutos: gratis, sin libreto de ventas.
- Diagnóstico de operación: COP $300.000, 5 días hábiles. Entrega mapa del proceso, dónde se pierde tiempo y dinero, arquitectura propuesta, plan por fases y estimado de inversión. Se abona el 100% al proyecto si se contrata dentro de 30 días.
- [Contacto y formulario](${u('/contacto')})

## Contacto

- WhatsApp: +57 320 504 6277
- Correo: ${SITE.email}
- LinkedIn: https://www.linkedin.com/in/diegomauriciogarcia
- GitHub: https://github.com/DiegoMao201
- Ubicación: Pereira, Risaralda, Colombia. Atiende todo el país de forma remota.`;

export function llmsCorto() {
  return `${CABECERA}

## Servicios

${SERVICIOS.map((s) => `- [${s.titulo}](${u(`/servicios/${s.slug}`)}): ${s.corto}`).join('\n')}

## Casos reales

- [Expedientes técnicos](${u('/casos')}): ${CUANTOS_CASOS} sistemas en operación, contados como se diseñaron — problema, restricción, arquitectura y resultado medible.
${CASOS.map((c) => `- [${c.titulo}](${u(`/casos/${c.slug}`)}): ${c.resumen}`).join('\n')}

## Cómo trabaja

- [Método de trabajo](${u('/metodo')}): diagnóstico con datos reales, arquitectura antes que código, construcción por fases verificables y operación continua.
- [Quién está detrás](${u('/diego')}): ingeniero industrial y administrador de empresas reales en Pereira.
- [Preguntas frecuentes](${u('/preguntas')})

## Notas

${NOTAS.map((n) => `- [${n.titulo}](${u(`/notas/${n.slug}`)}): ${n.descripcion}`).join('\n')}

${PIE}

## Opcional

- [Versión completa de este resumen](${u('/llms-full.txt')})
- [Política de privacidad](${u('/privacidad')})
- [Tratamiento de datos personales](${u('/habeas-data')})
- [Términos de servicio](${u('/terminos')})
`;
}

export function llmsCompleto() {
  const lista = (t: string, xs: string[]) => (xs.length ? `${t}\n${xs.map((x) => `- ${x}`).join('\n')}` : '');
  return `${CABECERA}

## Servicios

${SERVICIOS.map((s) => [`### ${s.titulo}`, u(`/servicios/${s.slug}`), s.respuesta, lista('El problema:', s.problema), lista('Cómo se hace:', s.metodo), lista('Qué se entrega:', s.entregables), `Tecnologías: ${s.tecnologias.join(', ')}`, ...s.faq.map((f) => `P: ${f.q}\nR: ${f.a}`)].filter(Boolean).join('\n\n')).join('\n\n')}

## Casos reales

${CASOS.map((c) => [`### ${c.codigo} · ${c.titulo}`, u(`/casos/${c.slug}`), c.resumen, lista('Contexto:', c.contexto), `Restricción: ${c.restriccion}`, lista('Arquitectura:', c.arquitectura), lista('Resultado:', c.resultado), `Tecnologías: ${c.stack.join(', ')}`, c.enVivo ? `Se puede visitar: ${c.enVivo.url}` : ''].filter(Boolean).join('\n\n')).join('\n\n')}

## Notas

${NOTAS.map((n) => [`### ${n.titulo}`, `${u(`/notas/${n.slug}`)} · ${n.fecha}`, ...n.parrafos.map((p) => (p.h ? `${p.h}. ${p.t}` : p.t))].join('\n\n')).join('\n\n')}

${PIE}
`;
}
