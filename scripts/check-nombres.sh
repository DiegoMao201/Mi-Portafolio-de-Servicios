#!/usr/bin/env bash
# Verifica que ningún nombre propio de cliente aparezca en los archivos VERSIONADOS.
# El repositorio es público: lo que no está versionado no se publica.
# Los términos vigilados viven en .terminos-prohibidos, que no se versiona.
set -u
LISTA=".terminos-prohibidos"
if [ ! -f "$LISTA" ]; then
  echo "AVISO: no existe $LISTA en este clon; no se puede verificar. Pídeselo a Diego."
  exit 0
fi
HITS=$(git ls-files -z \
  | grep -zv '^scripts/check-nombres\.sh$' \
  | xargs -0 grep -Iinf "$LISTA" -- 2>/dev/null)
if [ -n "$HITS" ]; then
  echo "FALLA: nombre de cliente encontrado en archivos versionados:"
  echo "$HITS"
  exit 1
fi
echo "OK: ningún nombre propio de cliente en los archivos versionados."
