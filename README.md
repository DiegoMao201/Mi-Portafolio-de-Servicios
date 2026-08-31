# datovatenexuspro.com

Sitio profesional de **Diego Mauricio García R. · Datovate Nexus Pro**.
Next.js 15 · TypeScript · PostgreSQL (opcional) · OpenRouter · SendGrid · Docker/Coolify.

## Correr en local

```bash
npm install
cp .env.example .env   # llenar variables
npm run dev            # http://localhost:3000
```

Sin `DATABASE_URL` el sitio funciona completo (los leads llegan solo por correo y el chat no persiste).
Sin `OPENROUTER_API_KEY` todo funciona menos el chat (el Diagnosticador muestra el aviso de contacto directo).

## Estructura

- `app/` — páginas (App Router), APIs (`/api/chat`, `/api/lead`, `/api/telemetria`, `/api/health`), sitemap, robots.
- `content/` — todo el contenido editable: servicios, casos, notas. **Editar aquí es editar el sitio.**
- `agent/prompt.ts` — el cerebro del Diagnosticador: prompt de sistema + corpus (se arma desde `content/`).
- `components/` — `Brain` (red neuronal del hero), `ArchGraph` (diagramas que se trazan), `Diagnosticador`, `Console`, formularios.
- `migrations/001_init.sql` — esquema `web` en PostgreSQL (leads, conversaciones, métricas, páginas programáticas).
- `Dockerfile` — multi-stage, salida standalone, healthcheck en `/api/health`. **Regla: siempre copiar `next.config.mjs` al runner.**
- `SPEC.md` — la especificación completa del proyecto.
- `PROMPT-DESPLIEGUE.md` — instrucciones de despliegue para Claude Code.

## Reglas de contenido (no negociables)

1. **Ningún cliente aparece con su nombre propio** en este repositorio: `bash scripts/check-nombres.sh` debe pasar. El cliente ferretero es siempre "una distribuidora ferretera del Eje Cafetero".
2. Ninguna cifra sin origen verificable. Las métricas del hero llevan su nota de origen.
3. No revelar URLs de clientes ni mecanismos internos de ningún sistema.
