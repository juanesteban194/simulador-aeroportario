#!/usr/bin/env bash
# Construye java/simulador-java.jar con javac y jar (JDK 21). Uso: bash java/construir.sh
set -euo pipefail
cd "$(dirname "$0")"
rm -rf clases simulador-java.jar
javac --release 21 -encoding UTF-8 -d clases src/simulador/*.java
jar --create --file simulador-java.jar --main-class simulador.Main -C clases .
rm -rf clases
echo "Listo: java/simulador-java.jar"
