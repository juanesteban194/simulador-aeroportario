#!/usr/bin/env bash
# =============================================================================
#  Verificación de equivalencia (Bloque 3, paso 4 del protocolo)
#  Construye cada versión y la ejecuta en el ejemplo (E0), en los escenarios que tengan salida esperada
#  y en los 12 casos de robustez (R01-R12). Compara byte a byte los 3 archivos y lo que sale en pantalla.
#
#  Uso: bash experimento/verificar.sh [java] [scala] [clojure] [referencia]
#       sin argumentos verifica java, scala y clojure. "referencia" prueba el propio verificador.
#       SIN_CONSTRUIR=1 usa los .jar que ya existen, sin volver a construirlos.
#  Termina con código 0 solo si todo coincide.
# =============================================================================
set -uo pipefail

RAIZ="$(cd "$(dirname "$0")/.." && pwd)"
LENGUAJES="${*:-java scala clojure}"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
unset JAVA_TOOL_OPTIONS
# shellcheck source=../herramientas/entorno.sh
source "$RAIZ/herramientas/entorno.sh"
ARCHIVOS="operaciones.csv errores.csv reporte.txt"

# Ejecuta el programa del lenguaje $L con los argumentos dados (la misma JVM y opciones en los tres).
programa() {
  case "$L" in
    referencia) python3 "$RAIZ/experimento/referencia.py" "$@" ;;
    *) java -Xmx4g -XX:+UseG1GC -jar "$RAIZ/$L/simulador-$L.jar" "$@" ;;
  esac
}

# Compara una ejecución con lo esperado. $1 carpeta obtenida, $2 carpeta esperada, $3 pantalla, $4 errores.
revisar() {
  [ -s "$4" ] && { echo "escribió en stderr"; return; }
  for f in $ARCHIVOS; do
    cmp -s "$1/$f" "$2/$f" || { echo "$f distinto"; return; }
  done
  cmp -s "$3" "$2/reporte.txt" || { echo "pantalla distinta"; return; }
  echo "ok"
}

# Escenario de datos: $1 pistas.csv, $2 vuelos.csv, $3 carpeta esperada.
probar_escenario() {
  rm -rf "$TMP/salida"
  programa "$1" "$2" "$TMP/salida" >"$TMP/pantalla" 2>"$TMP/stderr"
  local codigo=$?
  [ "$codigo" -eq 0 ] || { echo "exit $codigo"; return; }
  revisar "$TMP/salida" "$3" "$TMP/pantalla" "$TMP/stderr"
}

# Caso de robustez: se ejecuta dentro de una copia de su carpeta, con los argumentos de caso.txt.
probar_robustez() {
  local caso="$1" args esperado codigo
  args="$(sed -n 's/^argumentos: *//p' "$caso/caso.txt")"
  esperado="$(sed -n 's/^codigo: *//p' "$caso/caso.txt")"
  rm -rf "$TMP/caso" && cp -R "$caso" "$TMP/caso" && rm -rf "$TMP/caso/esperado"
  # shellcheck disable=SC2086  # los argumentos se separan por espacios a propósito
  ( cd "$TMP/caso" && programa $args >"$TMP/pantalla" 2>"$TMP/stderr" )
  codigo=$?
  [ "$codigo" -eq "$esperado" ] || { echo "exit $codigo (se esperaba $esperado)"; return; }
  if [ "$esperado" -eq 2 ]; then
    [ -s "$TMP/stderr" ] && { echo "escribió en stderr"; return; }
    [ -e "$TMP/caso/salida" ] && { echo "creó la carpeta de salida"; return; }
    head -1 "$TMP/pantalla" | grep -q '^ERROR: ' || { echo "falta la línea ERROR:"; return; }
    echo "ok"
  else
    revisar "$TMP/caso/salida" "$caso/esperado" "$TMP/pantalla" "$TMP/stderr"
  fi
}

# Lista de casos: "nombre|tipo|ruta".
casos() {
  echo "E0|escenario|$RAIZ/datos/ejemplo/pistas.csv|$RAIZ/datos/ejemplo/vuelos.csv|$RAIZ/datos/ejemplo/esperado"
  for e in V1 V2 V3 V4 C1 X1; do
    d="$RAIZ/datos/escenarios/$e"
    [ -f "$d/vuelos.csv" ] && [ -f "$d/esperado/reporte.txt" ] &&
      echo "$e|escenario|$RAIZ/datos/aeropuerto/pistas.csv|$d/vuelos.csv|$d/esperado"
  done
  for d in "$RAIZ"/datos/robustez/R*/; do
    echo "$(basename "$d")|robustez|${d%/}"
  done
}

echo "JVM: $(java -version 2>&1 | head -1)"
FALLAS=0
for L in $LENGUAJES; do
  : >"$TMP/res_$L"
  if [ "$L" != referencia ] && [ "${SIN_CONSTRUIR:-0}" != 1 ]; then
    echo "Construyendo $L..."
    bash "$RAIZ/$L/construir.sh" >"$TMP/construccion_$L" 2>&1 || {
      echo "  no compila (detalle abajo)"; tail -20 "$TMP/construccion_$L"; }
  fi
  casos | while IFS='|' read -r nombre tipo a b c; do
    if [ "$L" != referencia ] && [ ! -f "$RAIZ/$L/simulador-$L.jar" ]; then
      r="sin .jar"
    elif [ "$tipo" = escenario ]; then
      r="$(probar_escenario "$a" "$b" "$c")"
    else
      r="$(probar_robustez "$a")"
    fi
    echo "$nombre|$r" >>"$TMP/res_$L"
  done
  FALLAS=$((FALLAS + $(grep -vc '|ok$' "$TMP/res_$L")))
done

# Tabla: una fila por caso y una columna por lenguaje.
echo
{
  printf "caso"; for L in $LENGUAJES; do printf "|%s" "$L"; done; echo
  casos | while IFS='|' read -r nombre _; do
    printf "%s" "$nombre"
    for L in $LENGUAJES; do printf "|%s" "$(grep "^$nombre|" "$TMP/res_$L" | cut -d'|' -f2)"; done
    echo
  done
} | awk -F'|' '{ for (i = 1; i <= NF; i++) { c[NR, i] = $i; if (length($i) > w[i]) w[i] = length($i) } n = NF }
           END { for (r = 1; r <= NR; r++) { for (i = 1; i <= n; i++) printf ("%-" w[i] "s  "), c[r, i]; print "" } }'
echo
if [ "$FALLAS" -eq 0 ]; then echo "RESULTADO: todo coincide"; else echo "RESULTADO: $FALLAS caso(s) con diferencias"; fi
[ "$FALLAS" -eq 0 ]
