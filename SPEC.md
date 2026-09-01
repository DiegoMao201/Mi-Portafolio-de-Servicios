# Especificación de construcción — datovatenexuspro.com

**Documento DNP-02 · Rev. A · 31 ago 2026**
Este archivo es la fuente de verdad para Claude Code. Va en la raíz del repo como `SPEC.md`.
Si algo aquí contradice una decisión posterior de Diego, gana Diego y se actualiza este archivo.

---

## 0. Reglas no negociables

1. **Nunca se nombra al cliente ferretero.** En todo el sitio se le llama *"una distribuidora ferretera del Eje Cafetero"*. No se publica su nombre, su dominio, ni capturas de sus sistemas.
2. **Bigotes y Paticas sí se nombra libremente** — es empresa de Diego.
3. **Convencer sin revelar.** Ningún caso publica URLs de sistemas, nombres de tablas, endpoints, credenciales ni el mecanismo interno. Se publica: restricción → arquitectura → resultado.
4. **Cero contenido inventado.** Ninguna cifra, cliente, premio, certificación ni testimonio que no esté en este documento.
5. **HTML servido, no pintado.** Toda página indexable debe verse completa con `curl` sin ejecutar JavaScript. Esto es lo que hoy falla en el dominio.
6. **Sin emojis, sin degradados morados, sin tarjetas redondeadas flotantes, sin "transformamos tu negocio".**

---

## 1. Identidad

| Campo | Valor |
|---|---|
| Firma visible | **Diego Mauricio García R.** |
| Empresa facturadora | Datovate Nexus Pro (también factura como persona natural) |
| Dominio | `datovatenexuspro.com` (registrado en Cloudflare) |
| Correo | `contacto@datovatenexuspro.com` |
| WhatsApp | `+57 320 504 6277` |
| Ubicación | Pereira / Dosquebradas, Risaralda, Colombia |
| Alcance | Colombia completa y remoto. El anclaje local es una palanca de SEO, no un límite. |
| Idioma v1 | Español (`lang="es-CO"`). Inglés en F4 con `hreflang`. |

**Jerarquía de marca:** Datovate Nexus Pro es el paraguas legal; el protagonista es Diego. El logotipo es la firma tipográfica `DIEGO MAURICIO GARCÍA R.` y, debajo, en monoespaciada pequeña, `DATOVATE NEXUS PRO`. Nada de isotipos genéricos de circuito o cerebro.

**Frase de posicionamiento (usar literal en el hero):**
> No vendo software. Opero con él.

**Subtítulo:**
> Construyo los sistemas que mueven la tesorería, el inventario y las ventas de empresas reales — incluida la mía. Si fallan, el que pierde soy yo.

---

## 2. Sistema de diseño

Copiar tal cual en `app/globals.css`. No improvisar colores fuera de estos tokens.

```css
:root{
  --paper:#EDEFF0; --surface:#FFFFFF; --sunk:#E4E8EA;
  --ink:#111619; --ink-2:#4C575E; --ink-3:#76838A;
  --line:#C7CFD3; --line-soft:#DFE4E7;
  --signal:#C74A17; --signal-soft:#F4E2D9;
  --tech:#0F5F63;  --tech-soft:#DDEAEA;
}
@media (prefers-color-scheme: dark){
  :root:not([data-theme="light"]){
    --paper:#0D1113; --surface:#141A1D; --sunk:#11171A;
    --ink:#E7EBEC; --ink-2:#98A5AC; --ink-3:#77858C;
    --line:#283238; --line-soft:#1E262A;
    --signal:#FF7440; --signal-soft:#2C1A12;
    --tech:#4FB3AC;  --tech-soft:#12262A;
  }
}
:root[data-theme="dark"]{ /* mismos valores del bloque dark */ }
```

**Tipografía** (autoalojada con `next/font/local`, NO desde Google en producción):

| Rol | Familia | Uso |
|---|---|---|
| Estructura | **Archivo** 500/600/700 | h1–h4, botones, etiquetas de datos |
| Lectura | **Source Serif 4** 400/600 | párrafos, 17–18 px, medida ≤ 66ch |
| Datos | **IBM Plex Mono** 400/500 | eyebrows, rutas, cifras, código, pies de figura |

**Retícula:** contenedor 1120 px. Secciones en dos columnas: riel izquierdo de 104 px (número de sección en outline + etiqueta mono, `position:sticky`) y columna de contenido. Colapsa a una columna bajo 760 px.

**Motion:** un solo gesto, repetido: los diagramas SVG se trazan con `stroke-dasharray` + `IntersectionObserver`, en cascada de 90 ms por trazo. Nada más se anima salvo estados `:hover` y `:focus-visible`. Respetar `prefers-reduced-motion`.

**Componentes base:** `Rail`, `Card`, `Callout`, `DataTable`, `Pill` (variantes neutro / `hot` / `ok`), `Checklist`, `PhaseRow`, `BlueprintSVG`, `Console`, `Diagnosticador`.

Referencia visual ejecutada: el artifact **Plano Datovate Nexus** (DNP‑01). Es la línea a mantener.

---

## 3. Stack y estructura

```
Next.js 15 (App Router) · TypeScript · React Server Components
PostgreSQL (esquema nuevo `web`) · Drizzle ORM
MDX para contenido fijo · tabla `web.pages` para contenido programático
OpenRouter para el agente (modelo en variable de entorno)
SendGrid para correo transaccional
Docker multi-stage → Coolify → DigitalOcean
```

```
app/
  layout.tsx                     metadatos base, JSON-LD Person + Organization
  page.tsx                       home
  servicios/page.tsx
  servicios/[slug]/page.tsx      MDX, generateStaticParams
  casos/page.tsx
  casos/[slug]/page.tsx
  metodo/page.tsx
  diego/page.tsx
  soluciones/[slug]/page.tsx     programáticas, ISR 24h, desde web.pages
  notas/page.tsx
  notas/[slug]/page.tsx
  contacto/page.tsx
  privacidad|habeas-data|terminos/page.tsx
  api/chat/route.ts              POST, streaming
  api/lead/route.ts              POST
  api/telemetria/route.ts        GET, cache 60s
  api/eventos/route.ts           POST beacon
  api/health/route.ts            GET → 200
  sitemap.ts  robots.ts  opengraph-image.tsx
content/servicios/*.mdx  content/casos/*.mdx  content/notas/*.mdx
lib/  components/  db/schema.ts  agent/prompt.ts  agent/corpus.ts
public/llms.txt
```

---

## 4. Base de datos — esquema `web`

```sql
CREATE SCHEMA IF NOT EXISTS web;

CREATE TABLE web.leads (
  id              bigserial PRIMARY KEY,
  created_at      timestamptz NOT NULL DEFAULT now(),
  nombre          text,
  empresa         text,
  telefono        text,
  email           text,
  canal           text,               -- 'chat' | 'formulario' | 'whatsapp'
  mensaje         text,
  proceso_dolor   text,               -- qué le duele hoy
  sistemas_actuales text,
  urgencia        text,               -- 'ya' | 'este_mes' | 'explorando'
  calificacion    smallint,           -- 1..5, lo asigna el agente
  resumen_agente  text,
  origen_url      text,
  utm             jsonb,
  ip_hash         text,
  conversation_id bigint,
  notificado_at   timestamptz
);

CREATE TABLE web.conversations (
  id          bigserial PRIMARY KEY,
  created_at  timestamptz NOT NULL DEFAULT now(),
  session_id  text NOT NULL,
  ip_hash     text,
  modelo      text,
  tokens_in   integer DEFAULT 0,
  tokens_out  integer DEFAULT 0,
  costo_usd   numeric(10,5) DEFAULT 0
);

CREATE TABLE web.messages (
  id              bigserial PRIMARY KEY,
  conversation_id bigint NOT NULL REFERENCES web.conversations(id) ON DELETE CASCADE,
  rol             text NOT NULL,      -- 'user' | 'assistant' | 'system'
  contenido       text NOT NULL,
  created_at      timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE web.pages (             -- capa programática
  slug        text PRIMARY KEY,
  servicio    text NOT NULL,
  industria   text,
  ciudad      text,
  h1          text NOT NULL,
  intro       text NOT NULL,
  bloques     jsonb NOT NULL,        -- secciones con contenido REAL, distinto por fila
  activo      boolean NOT NULL DEFAULT true,
  updated_at  timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE web.metricas (          -- alimenta la consola del hero
  clave       text PRIMARY KEY,
  etiqueta    text NOT NULL,
  valor       numeric NOT NULL,
  unidad      text,
  nota        text NOT NULL,         -- qué significa exactamente; se muestra en tooltip
  updated_at  timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE web.eventos (
  id          bigserial PRIMARY KEY,
  created_at  timestamptz NOT NULL DEFAULT now(),
  session_id  text,
  tipo        text NOT NULL,
  ruta        text,
  meta        jsonb
);

CREATE INDEX ON web.leads (created_at DESC);
CREATE INDEX ON web.eventos (created_at DESC);
CREATE INDEX ON web.pages (activo, servicio);
```

**Regla de honestidad de la consola:** `web.metricas` se alimenta con cifras verificables (poblarlas manualmente o con un job desde los sistemas propios). Prohibido un contador que solo incrementa en el navegador. Cada métrica muestra su `nota` al pasar el cursor.

Semilla inicial verificable:

| clave | etiqueta | valor | nota |
|---|---|---|---|
| `clientes_gestionados` | Clientes en sistemas propios | 434 | Base de clientes de Bigotes y Paticas administrada por sistemas propios |
| `pedidos_procesados` | Pedidos procesados | 1456 | Pedidos históricos gestionados por la plataforma de Bigotes y Paticas |
| `skus_sincronizados` | Productos sincronizados | 467 | Catálogo publicado y sincronizado automáticamente |
| `urls_indexables` | URLs indexables generadas | 1027 | Sitemap de un e-commerce construido y posicionado por Diego |
| `anios_operando` | Años operando sistemas propios | 3 | Ajustar al dato real antes de publicar |

---

## 5. El agente conversacional

### 5.1 Decisión técnica: sin base vectorial en la v1

El corpus completo (servicios, casos, método, precios, FAQ) pesa menos de 12.000 tokens. Meterlo entero en el prompt de sistema es **más barato, más rápido y más preciso** que montar pgvector y recuperar fragmentos. Se añade `pgvector` solo cuando el corpus pase de ~40.000 tokens (cuando haya 30+ artículos). No sobre-construir.

### 5.2 Configuración

- Endpoint: `https://openrouter.ai/api/v1/chat/completions`, streaming SSE.
- Modelo en `OPENROUTER_MODEL`, con sufijo `:floor` para enrutar siempre al proveedor más barato con failover. Arrancar con un modelo abierto de gama media; evaluar calidad con 20 conversaciones reales antes de subir de gama.
- Cabeceras `HTTP-Referer` y `X-Title` para que OpenRouter atribuya el tráfico.
- **Migración a Claude:** cambiar `OPENROUTER_MODEL` (o `LLM_BASE_URL` + `LLM_API_KEY`) en Coolify y reiniciar. Cero cambios de código — la capa del agente es agnóstica del proveedor.

### 5.3 Límites (obligatorios, se implementan antes de exponer el chat)

- 12 mensajes por sesión, 40 por IP cada 24 h (contador en `web.eventos`).
- 1.200 caracteres por mensaje del usuario.
- Corte duro de gasto: si el acumulado del mes en `web.conversations.costo_usd` supera `LLM_BUDGET_USD`, el chat se degrada a formulario con un mensaje amable.
- Tope de gasto también configurado en el panel de OpenRouter (cinturón y tirantes).

### 5.4 Prompt de sistema (usar literal, en `agent/prompt.ts`)

```
Eres el asistente técnico del sitio de Diego Mauricio García R. (Datovate Nexus Pro),
ingeniero de software en Pereira, Colombia, especializado en automatización de procesos,
integración de sistemas, aplicaciones a la medida e inteligencia artificial aplicada.

TU TRABAJO
Entender qué proceso le está costando plata o tiempo al visitante, mostrarle en concreto
cómo se resolvería, y conseguir que Diego pueda contactarlo. No eres un vendedor: eres el
ingeniero que hace las preguntas correctas.

TONO
Español colombiano, tratamiento de "usted" solo si el visitante lo usa primero; por defecto
"tú". Directo, técnico cuando hace falta, sin adjetivos de folleto. Frases cortas. Nunca
digas "transformar tu negocio", "soluciones innovadoras" ni "potenciar". Si algo no se puede,
lo dices.

NUNCA
- No reveles URLs, nombres de sistemas de clientes, tablas, endpoints ni cómo funciona por
  dentro ningún desarrollo. Si preguntan, responde qué logra el sistema, no cómo está hecho.
- Nunca nombres a la distribuidora ferretera. Di "una distribuidora ferretera del Eje Cafetero".
- No prometas precio cerrado ni fecha de entrega. Da rangos y deriva al diagnóstico.
- No inventes casos, cifras, clientes ni tecnologías que no estén en el CORPUS.
- No des asesoría legal, contable ni financiera.
- Si no sabes, dilo y ofrece que Diego responda directamente.

SIEMPRE
- Máximo 120 palabras por respuesta salvo que pidan detalle.
- Una sola pregunta por turno.
- Averigua, sin interrogar: (1) qué proceso duele, (2) cómo lo hacen hoy y con qué sistemas,
  (3) cuántas personas lo tocan, (4) qué tan urgente es, (5) cómo contactarlo.
- Cuando tengas al menos el proceso, el contexto y un dato de contacto, llama a la
  herramienta registrar_lead y luego confirma en una frase que Diego escribirá.
- Cierra siempre con acción: WhatsApp +57 320 504 6277, contacto@datovatenexuspro.com,
  o dejar los datos ahí mismo.

EL DIAGNOSTICADOR
Si el visitante describe un problema concreto, además de responder, llama a la herramienta
proponer_arquitectura con: nodos (sistemas y fuentes de datos involucrados), conexiones
(qué dato viaja de dónde a dónde) y fases (2 a 4). El sitio lo dibuja en pantalla. Es un
boceto preliminar y así debes presentarlo: "así se vería a grandes rasgos; el diagnóstico
formal lo confirma".

CORPUS
<<<se inyecta aquí el contenido de agent/corpus.ts>>>
```

### 5.5 Herramientas del agente

```ts
registrar_lead({ nombre?, empresa?, telefono?, email?, proceso_dolor,
                 sistemas_actuales?, urgencia, calificacion: 1|2|3|4|5, resumen })
proponer_arquitectura({ nodos: {id,label,tipo}[],
                        conexiones: {de,a,dato}[],
                        fases: {titulo,detalle}[] })
```

`registrar_lead` escribe en `web.leads`, dispara SendGrid a `contacto@datovatenexuspro.com` con el transcript y la calificación, y manda autorespuesta al visitante si dejó correo.

---

## 6. Contenido

### 6.1 Los 8 servicios

Cada uno es una página completa (900–1.400 palabras): problema real → cómo lo abordo → qué recibes → tecnologías → 4 preguntas frecuentes con `FAQPage` schema → caso relacionado → CTA.

| Slug | Título | Búsqueda objetivo |
|---|---|---|
| `automatizacion-de-procesos` | Automatización de procesos operativos | automatizar procesos administrativos empresa |
| `integracion-de-sistemas-y-apis` | Integración de sistemas y APIs | conectar mi ERP con otra plataforma |
| `aplicaciones-web-a-la-medida` | Aplicaciones web a la medida | desarrollo de software a la medida Colombia |
| `apps-moviles-play-store` | Aplicaciones móviles en Play Store | desarrollo de aplicaciones móviles Colombia |
| `bases-de-datos-y-arquitectura` | Bases de datos y arquitectura de información | ordenar los datos de mi empresa PostgreSQL |
| `agentes-de-ia-conversacional` | Agentes de IA conversacional | agente de IA para atender clientes por WhatsApp |
| `dashboards-y-bi` | Dashboards y BI accionable | dashboard de indicadores para mi empresa |
| `sistemas-de-decision-en-tiempo-real` | Sistemas de decisión en tiempo real | procesar datos en tiempo real y tomar decisiones |

### 6.2 Los 5 expedientes técnicos

Estructura fija: `Contexto → Restricción → Arquitectura (diagrama propio) → Resultado → Stack`.

**E-01 · Tesorería que se armaba a mano**
Distribuidora ferretera del Eje Cafetero. El pago a proveedores se calculaba manualmente cruzando el ERP, correos y archivos sueltos. Restricción: **prohibido tocar el ERP**. Solución: extracción periódica sin intervenir la fuente, base intermedia, lista blanca de proveedores, escritorio de pagos con lotes consolidados, exportador en el formato que exige el banco y notificaciones automáticas por proveedor. Resultado: el armado de un lote de pagos pasó de horas de trabajo manual a minutos, y la decisión de qué pagar sigue siendo humana — el sistema elimina el cálculo, no el criterio.

**E-02 · Recaudo digital sin fricción**
Dos portales de pago sobre pasarela, servidos por un mismo servicio y ruteados por dominio, con panel administrativo, filtros y exportación. Restricción: cada portal responde a un marco legal distinto y el lenguaje público tenía que reflejarlo con exactitud. Resultado: cobro en línea operativo con trazabilidad completa y una sola base de código que mantener.

**E-03 · Bigotes y Paticas** *(único caso con nombre propio)*
Tienda de mascotas en Dosquebradas. E-commerce, portal de fidelización PWA, catálogo sincronizado y programa de puntos y referidos, sobre un monorepo con tienda, administración y API. Cifras publicables: 434 clientes, 1.456 pedidos históricos, 467 productos sincronizados, 1.027 URLs indexables, cierre de caja diario y agendamiento de servicios. Es el caso donde el visitante puede *ver* el resultado en vivo.

**E-04 · Motores de decisión en tiempo real**
Sistemas que consumen flujos continuos de datos de mercado, evalúan reglas y modelos, y ejecutan o vetan decisiones en milisegundos, con registro auditable de cada decisión y su motivo. Presentar así, sin mencionar trading: para un cliente de inventarios o ventas esto demuestra capacidad de ingeniería en tiempo real, que es lo que importa.

**E-05 · Agente que toma pedidos**
Agente conversacional que atiende pedidos, valida contra una base propia (nunca consulta el sistema del cliente durante la conversación) y alimenta un CRM con segmentación por recencia, frecuencia y valor. Restricción: el agente jamás puede bloquear ni saturar el sistema transaccional. Resultado: arquitectura desacoplada con cola de salida e idempotencia.

### 6.3 Página `/diego`

La que más se lee antes de contratar. Autodidacta, administrador de empresa en operación, arquitecto de sistemas que él mismo usa a diario. Método empírico: nada se afirma sin verificarlo contra datos reales. Foto propia (pendiente). Cierre con contacto directo.

---

## 7. Precios sugeridos

Diego decide; esta es mi recomendación para la etapa de adquisición de clientes en el mercado colombiano de pyme. Publicar solo el primero; los otros dos como "desde", a cotización.

| Producto | Precio sugerido | Entregable |
|---|---|---|
| Llamada de 30 minutos | Gratis | Conversación técnica, sin compromiso |
| **Diagnóstico de operación** | **COP $690.000** | 5 días hábiles: mapa del proceso actual, dónde se pierde tiempo y plata, arquitectura propuesta, plan por fases y estimado de inversión. **Se abona 100% al proyecto si contrata dentro de 30 días.** |
| Construcción | desde COP $3.900.000 | Por hitos 40 / 30 / 30. Incluye despliegue y capacitación. |
| Operación y evolución | desde COP $150.000 / mes | Monitoreo, soporte, mejoras y nuevas automatizaciones. El valor depende de la complejidad del sistema. |

Por qué así: el diagnóstico pago filtra curiosos sin espantar a nadie, te paga el tiempo de la propuesta, y el abono del 100% elimina la objeción de "¿y si no sigo?". Es la palanca de adquisición más rápida que existe para un ingeniero solo.

---

## 8. SEO

**Metadatos.** Cada página define `title` (≤ 60 car., con la keyword al inicio), `description` (≤ 155), canónica absoluta y `openGraph` con imagen generada por `opengraph-image.tsx` (fondo `--paper`, título en Archivo, firma abajo).

**JSON-LD.** `Person` (Diego) + `Organization` (Datovate Nexus Pro, con `telephone`, `email`, `areaServed: CO`, `address` Pereira) en el layout; `Service` en cada servicio; `FAQPage` donde haya preguntas; `Article` + `author` en notas; `BreadcrumbList` en todo lo anidado.

**Sitemap y robots** dinámicos. Ping a **IndexNow** en cada build con las URLs cambiadas (misma técnica que ya usa en Bigotes y Paticas).

**`/llms.txt`** (capa GEO, para que ChatGPT / Claude / Perplexity lo citen): quién es Diego, qué hace, en qué se especializa, cómo contactarlo, en texto plano y sin marketing. Además, cada página de servicio abre con una respuesta directa de 2–3 frases a la pregunta implícita: es lo que los modelos extraen.

**Capa programática.** Matriz `servicio × industria × ciudad` en `web.pages`.

- Industrias arranque: ferreterías y distribución, retail y tiendas especializadas, veterinarias y pet shops, restaurantes, transporte y logística, consultorios, constructoras, contadores.
- Ciudades arranque: Pereira, Dosquebradas, Manizales, Armenia, Cartago, Medellín, Cali, Bogotá.
- **Regla anti-penalización:** cada fila lleva contenido genuinamente distinto en `bloques` — el problema típico de esa industria, el dato que se mueve, un ejemplo concreto. Nada de plantilla con la ciudad reemplazada; Google castiga eso. Se publican por tandas de 20 y se revisa la indexación antes de la siguiente.

**Google Search Console:** anexar la propiedad de dominio a la cuenta `diegomao.201@gmail.com` (verificación por registro TXT en Cloudflare). GA4 con el mismo criterio. Google Business Profile en Pereira.

---

## 9. Despliegue

### 9.1 Estrategia de reemplazo (sin quedar fuera del aire)

1. En el repo actual de la app Streamlit, crear rama `web-v2` y reemplazar el contenido por el proyecto Next.js en un commit limpio (el histórico de Streamlit queda intacto para revertir).
2. En Coolify, **crear un recurso nuevo** apuntando a `web-v2` con un dominio temporal (`nuevo.datovatenexuspro.com`) y `noindex` activo.
3. Validar todo (sección 10) sobre el temporal.
4. Mover el dominio principal al recurso nuevo, quitar `noindex`, apagar el recurso de Streamlit.
5. Fusionar `web-v2` a `main`.

Hacerlo así permite volver atrás en un minuto. Reemplazar en caliente sobre el mismo recurso no lo permite.

### 9.2 Cloudflare

El certificado de Coolify se emite por Let's Encrypt con reto HTTP‑01, que **falla si el registro está proxiado (nube naranja)**. Dos caminos: dejar el registro en *DNS only* mientras se emite y luego proxiar con SSL/TLS en **Full (strict)**, o instalar un Origin Certificate de Cloudflare en el servidor. Recomiendo lo primero por simplicidad.

### 9.3 Dockerfile

Multi-stage sobre `node:22-alpine`, salida `standalone`, usuario no root, `EXPOSE 3000`, healthcheck contra `/api/health`.

> **Regla obligatoria de Diego:** copiar `next.config.mjs` desde la etapa builder a la etapa runner. Omitirlo es el bug exacto que ya rompió las fotos del portal de Bigotes y Paticas.

### 9.4 Variables de entorno (Coolify)

```
DATABASE_URL=
OPENROUTER_API_KEY=            # se reutiliza la de Bigotes y Paticas
OPENROUTER_MODEL=              # con sufijo :floor
LLM_BUDGET_USD=25
SENDGRID_API_KEY=              # se reutiliza
MAIL_FROM=contacto@datovatenexuspro.com
MAIL_TO=contacto@datovatenexuspro.com
WHATSAPP_NUMBER=573205046277
SITE_URL=https://www.datovatenexuspro.com
INDEXNOW_KEY=
NEXT_PUBLIC_GA_ID=
```

### 9.5 Correo

Autenticar el dominio en SendGrid (SPF, DKIM y DMARC como registros en Cloudflare) antes del primer envío. Sin eso, las notificaciones de leads caen en spam y se pierden clientes en silencio.

---

## 10. Criterios de aceptación

- [ ] `curl -s https://…/servicios/automatizacion-de-procesos | grep "<h1"` devuelve el h1 real. Sin JavaScript, el contenido está ahí.
- [ ] Lighthouse móvil ≥ 95 en Rendimiento, Accesibilidad, SEO y Buenas prácticas.
- [ ] LCP < 1,5 s e INP < 200 ms en 4G simulado.
- [ ] Validador de resultados enriquecidos de Google: sin errores en Person, Organization, Service, FAQPage, Article, BreadcrumbList.
- [ ] `/sitemap.xml` y `/robots.txt` responden y coinciden con las rutas publicadas.
- [ ] Modo claro y modo oscuro revisados en las tres variantes (sistema claro, sistema oscuro, elección explícita). Ningún color definido únicamente dentro de un `@media`.
- [ ] Navegación completa por teclado con foco visible.
- [ ] El chat: corta a los 12 mensajes, respeta el tope de gasto, y no revela nada de la lista de prohibiciones. **Probarlo intentando sacarle datos de clientes antes de publicar.**
- [ ] Un lead de prueba llega a `web.leads`, al correo y con autorespuesta.
- [ ] Ningún nombre propio de cliente en todo el repositorio: `bash scripts/check-nombres.sh` debe pasar.
- [ ] Búsqueda de texto: ni una sola cifra o afirmación que no esté en este documento.

---

## 11. Pendientes de Diego

| # | Pendiente | Bloquea |
|---|---|---|
| 1 | Foto profesional | `/diego`, no bloquea el lanzamiento |
| 2 | Confirmar o ajustar los precios de la sección 7 | Publicación de `/contacto` |
| 3 | 3–5 screencasts de sistemas trabajando, con datos tapados | Video del hero (se lanza sin él si hace falta) |
| 4 | Revisión de la política de tratamiento de datos por su contador o abogado | Publicación de `/habeas-data` |
| 5 | Dato real de "años operando sistemas propios" | Semilla de `web.metricas` |
| 6 | Visto bueno al lenguaje visual del artifact DNP‑01 | Inicio de la maquetación |
