#!/usr/bin/env bash
# Mantiene el Mac despierto (pantalla, disco y sistema) mientras se trabaja o se mide.
# Uso: bash herramientas/mantener_activo.sh [horas]     (por defecto 6 horas; Ctrl+C o ■ para detenerlo)
# Usa caffeinate, que viene con macOS. Durante el experimento evita que el equipo se suspenda a mitad de una medición.
set -uo pipefail
HORAS="${1:-6}"
echo "Mac despierto durante $HORAS horas (desde $(date '+%H:%M')). Detén este proceso para volver a lo normal."
exec caffeinate -dimsu -t $((HORAS * 3600))
