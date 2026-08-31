# Guía para Claude Code en este repositorio

Este es el sitio de Diego Mauricio García R. (datovatenexuspro.com). Lee `SPEC.md` para el contexto completo.

## Reglas duras
- **El nombre propio de ningún cliente puede aparecer en el repositorio** (es público). Antes de cada commit: `bash scripts/check-nombres.sh` debe pasar. Los términos vigilados viven en `.terminos-prohibidos`, que no se versiona. El cliente ferretero se llama siempre "una distribuidora ferretera del Eje Cafetero".
- Ninguna cifra, caso o afirmación que no esté en `SPEC.md` o confirmada por Diego. Cero contenido inventado.
- No revelar URLs de sistemas de clientes ni mecanismos internos en el contenido público ni en el corpus del agente.
- El Dockerfile SIEMPRE copia `next.config.mjs` de builder a runner (bug histórico real si se omite).
- Nunca commitear `.env` ni claves. Las claves viven en Coolify.

## Diseño
- Tokens de color y tipografías están en `app/globals.css` (`:root`). No inventar colores nuevos: usar los tokens.
- Tipos: Archivo (estructura), Source Serif 4 (lectura), IBM Plex Mono (datos) — autoalojadas vía @fontsource.
- El hero ("sala de máquinas") es oscuro siempre, por decisión de diseño; el resto del sitio respeta claro/oscuro del sistema.
- Movimiento: red neuronal en canvas (`Brain.tsx`), diagramas que se trazan (`ArchGraph.tsx`), pulsos en conexiones. Respetar `prefers-reduced-motion` en todo lo nuevo.

## Contenido
- Editar servicios/casos/notas = editar `content/*.ts`. El corpus del agente (`agent/prompt.ts`) se arma solo desde ahí.
- Toda página indexable debe verse completa con `curl` (sin ejecutar JS).
- Cada página nueva: title ≤60 car., description ≤155, canónica, y JSON-LD del tipo que corresponda.

## Verificación mínima antes de dar algo por terminado
```bash
npm run build                       # sin errores
curl -s localhost:3000/ | grep '<h1'
bash scripts/check-nombres.sh     # debe decir OK
```
