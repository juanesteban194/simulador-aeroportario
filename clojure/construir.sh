#!/usr/bin/env bash
# Construye clojure/simulador-clojure.jar con Leiningen (compilación AOT). Uso: bash clojure/construir.sh
set -euo pipefail
cd "$(dirname "$0")"
rm -f simulador-clojure.jar
lein uberjar
cp target/uberjar/simulador-clojure.jar simulador-clojure.jar
echo "Listo: clojure/simulador-clojure.jar"
