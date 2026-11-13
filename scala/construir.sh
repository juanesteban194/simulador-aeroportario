#!/usr/bin/env bash
# Construye scala/simulador-scala.jar con Scala CLI (incluye la biblioteca de Scala). Uso: bash scala/construir.sh
# --server=false: compila sin dejar un servidor de compilación corriendo, que afectaría las mediciones.
set -euo pipefail
cd "$(dirname "$0")"
rm -f simulador-scala.jar
scala-cli --power package . --assembly --server=false -f -o simulador-scala.jar
echo "Listo: scala/simulador-scala.jar"
