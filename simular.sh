#!/usr/bin/env bash
# =============================================================================
#  Ejecuta el simulador en cualquiera de los 4 lenguajes del proyecto.
#  Funciona con el bash 3.2 de macOS, en la terminal o desde IntelliJ (carpeta .run).
#
#  Uso: bash simular.sh <lenguaje> [escenario] [carpeta_salida]
#       bash simular.sh <lenguaje> <pistas.csv> <vuelos.csv> [carpeta_salida]
#       bash simular.sh todos [escenario]      los 4 lenguajes y compara sus salidas
#       bash simular.sh                        menú (solo en una terminal)
#
#  lenguaje:  java | scala | clojure | python   (python = implementación de referencia; no compite)
#  escenario: E0 (ejemplo resuelto a mano, por defecto) | V1 | V2 | V3 | V4 | C1 | X1
#  Salida:    salida/<lenguaje>/<escenario>/ con operaciones.csv, errores.csv y reporte.txt
#
#  Si el .jar no existe o el código fuente es más nuevo, lo construye con <lenguaje>/construir.sh.
#  CONSTRUIR=1 lo reconstruye siempre. PYTHON=<ruta> elige el intérprete de Python.
# =============================================================================
set -uo pipefail

RAIZ="$(cd "$(dirname "$0")" && pwd)"
unset JAVA_TOOL_OPTIONS
# shellcheck source=herramientas/entorno.sh
source "$RAIZ/herramientas/entorno.sh"
LENGUAJES="python java scala clojure"
ESCENARIOS="E0 V1 V2 V3 V4 C1 X1"
ARCHIVOS="operaciones.csv errores.csv reporte.txt"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

uso() {
  cat <<EOF
Uso: bash simular.sh <lenguaje> [escenario] [carpeta_salida]
     bash simular.sh <lenguaje> <pistas.csv> <vuelos.csv> [carpeta_salida]
     bash simular.sh todos [escenario]
  lenguaje:  java | scala | clojure | python
  escenario: $ESCENARIOS (por defecto E0)
EOF
}

fallar() { echo "ERROR: $*" >&2; exit 2; }
relativa() { echo "${1#"$RAIZ"/}"; }
minusculas() { echo "$1" | tr '[:upper:]' '[:lower:]'; }

requiere() {   # $1 comando, $2 fórmula de Homebrew que lo instala
  command -v "$1" >/dev/null 2>&1 \
    || fallar "no se encontró '$1'. Instálalo con: brew install $2  (o bash herramientas/instalar_entorno.sh)"
}

# ---------------------------------------------------------------- Lenguajes

normalizar_lenguaje() {
  case "$(minusculas "$1")" in
    java) echo java ;;
    scala) echo scala ;;
    clojure | clj) echo clojure ;;
    python | py | referencia) echo python ;;
    todos | all) echo todos ;;
    *) fallar "lenguaje desconocido: $1 (opciones: $LENGUAJES todos)" ;;
  esac
}

jar() { echo "$RAIZ/$1/simulador-$1.jar"; }

# Verdadero si hay que construir el .jar: no existe, CONSTRUIR=1 o algún fuente es más nuevo.
desactualizado() {
  [ "${CONSTRUIR:-0}" = 1 ] && return 0
  [ -f "$(jar "$1")" ] || return 0
  [ -n "$(find "$RAIZ/$1/src" "$RAIZ/$1"/project.* -type f -newer "$(jar "$1")" 2>/dev/null | head -n 1)" ]
}

construir() {
  case "$1" in
    java) requiere javac openjdk@21 ;;
    scala) requiere scala-cli Virtuslab/scala-cli/scala-cli ;;
    clojure) requiere lein leiningen ;;
  esac
  echo "Construyendo $1 con $1/construir.sh ..."
  bash "$RAIZ/$1/construir.sh" || fallar "no se pudo construir la versión $1"
}

java_21() {
  requiere java openjdk@21
  local v
  v="$(java -XshowSettings:properties -version 2>&1 | sed -n 's/^ *java.specification.version = //p')"
  [ "${v%%.*}" -ge 21 ] 2>/dev/null || fallar "se necesita el JDK 21 o superior (encontrado: ${v:-desconocido}). brew install openjdk@21"
}

# Deja listo el programa del lenguaje: intérprete de Python o .jar construido.
preparar() {
  case "$1" in
    python)
      PY="${PYTHON:-}"
      [ -n "$PY" ] || { [ -x "$HOME/anaconda3/bin/python3" ] && PY="$HOME/anaconda3/bin/python3"; }
      [ -n "$PY" ] || PY="$(command -v python3 || true)"
      [ -n "$PY" ] || fallar "no se encontró python3. Instálalo con: brew install python"
      ;;
    *)
      java_21
      if desactualizado "$1"; then construir "$1"; fi
      ;;
  esac
}

# Ejecuta el programa del lenguaje con los argumentos dados (la misma JVM y opciones que el experimento).
ejecutar() {
  local l="$1"
  shift
  case "$l" in
    python) "$PY" "$RAIZ/experimento/referencia.py" "$@" ;;
    *) java -Xmx4g -XX:+UseG1GC -jar "$(jar "$l")" "$@" ;;
  esac
}

comando() {
  case "$1" in
    python) echo "python3 experimento/referencia.py" ;;
    *) echo "java -Xmx4g -XX:+UseG1GC -jar $(relativa "$(jar "$1")")" ;;
  esac
}

# ---------------------------------------------------------------- Escenarios

# Define PISTAS, VUELOS, ESPERADO (vacío si no hay) y NOMBRE a partir del nombre de un escenario.
escenario() {
  local e
  e="$(echo "$1" | tr '[:lower:]' '[:upper:]')"
  case " $ESCENARIOS " in
    *" $e "*) ;;
    *) fallar "escenario desconocido: $1 (opciones: $ESCENARIOS)" ;;
  esac
  NOMBRE="$e"
  if [ "$e" = E0 ]; then
    PISTAS="$RAIZ/datos/ejemplo/pistas.csv"
    VUELOS="$RAIZ/datos/ejemplo/vuelos.csv"
    ESPERADO="$RAIZ/datos/ejemplo/esperado"
  else
    PISTAS="$RAIZ/datos/aeropuerto/pistas.csv"
    VUELOS="$RAIZ/datos/escenarios/$e/vuelos.csv"
    ESPERADO="$RAIZ/datos/escenarios/$e/esperado"
    [ -f "$VUELOS" ] || fallar "el escenario $e no está generado. Créalo con: python3 datos/generador.py $e"
  fi
  [ -d "$ESPERADO" ] || ESPERADO=""
}

# Compara una carpeta de salida y lo que salió en pantalla con una carpeta de referencia.
comparar() {   # $1 carpeta obtenida, $2 pantalla, $3 carpeta de referencia
  local f
  for f in $ARCHIVOS; do
    cmp -s "$1/$f" "$3/$f" || { echo "$f distinto"; return 1; }
  done
  cmp -s "$2" "$3/reporte.txt" || { echo "pantalla distinta"; return 1; }
  echo "ok"
}

# ---------------------------------------------------------------- Modos

un_lenguaje() {   # $1 lenguaje, $2 carpeta de salida
  local l="$1" salida="$2" codigo
  preparar "$l"
  echo "== Simulador en $l · escenario $NOMBRE =="
  echo "\$ $(comando "$l") $(relativa "$PISTAS") $(relativa "$VUELOS") $(relativa "$salida")"
  echo
  ejecutar "$l" "$PISTAS" "$VUELOS" "$salida" | tee "$TMP/pantalla"
  codigo=${PIPESTATUS[0]}
  echo
  [ "$codigo" -eq 0 ] || { echo "El programa terminó con código $codigo."; exit "$codigo"; }
  echo "Archivos en $(relativa "$salida")/: $ARCHIVOS"
  [ -n "$ESPERADO" ] || return 0
  if comparar "$salida" "$TMP/pantalla" "$ESPERADO" >"$TMP/resultado"; then
    echo "Comparación con $(relativa "$ESPERADO"): idéntica"
  else
    echo "Comparación con $(relativa "$ESPERADO"): $(cat "$TMP/resultado")"
    exit 1
  fi
}

todos() {
  local l salida referencia resultado codigo fallas=0
  for l in $LENGUAJES; do preparar "$l"; done
  referencia="${ESPERADO:-$RAIZ/salida/python/$NOMBRE}"
  echo
  echo "== Los 4 lenguajes · escenario $NOMBRE · referencia: $(relativa "$referencia") =="
  printf '%-9s %s\n' "Lenguaje" "Resultado"
  for l in $LENGUAJES; do
    salida="$RAIZ/salida/$l/$NOMBRE"
    ejecutar "$l" "$PISTAS" "$VUELOS" "$salida" >"$TMP/pantalla" 2>"$TMP/errores"
    codigo=$?
    if [ "$codigo" -ne 0 ]; then resultado="exit $codigo"
    elif [ -s "$TMP/errores" ]; then resultado="escribió en stderr"
    elif [ -z "$ESPERADO" ] && [ "$l" = python ]; then resultado="referencia"
    else resultado="$(comparar "$salida" "$TMP/pantalla" "$referencia")"
    fi
    case "$resultado" in ok | referencia) ;; *) fallas=$((fallas + 1)) ;; esac
    printf '%-9s %s\n' "$l" "$resultado"
  done
  echo
  if [ "$fallas" -eq 0 ]; then
    echo "RESULTADO: los 4 lenguajes producen exactamente la misma salida. Archivos en salida/<lenguaje>/$NOMBRE/"
  else
    echo "RESULTADO: $fallas lenguaje(s) con diferencias"
    exit 1
  fi
}

menu() {
  local l e
  echo "Simulador aeroportuario · elige qué ejecutar:"
  PS3="Número: "
  select l in $LENGUAJES todos; do [ -n "$l" ] && break; done
  [ -n "${l:-}" ] || exit 2
  printf 'Escenario (%s) [E0]: ' "$ESCENARIOS"
  read -r e || e=""
  ELEGIDO_LENGUAJE="$l"
  ELEGIDO_ESCENARIO="${e:-E0}"
}

# ---------------------------------------------------------------- Principal

if [ $# -eq 0 ]; then
  [ -t 0 ] || { uso; exit 2; }
  menu
  set -- "$ELEGIDO_LENGUAJE" "$ELEGIDO_ESCENARIO"
fi
case "$1" in -h | --help | ayuda) uso; exit 0 ;; esac
LENGUAJE="$(normalizar_lenguaje "$1")" || exit 2
shift

if [ "$LENGUAJE" = todos ]; then
  [ $# -le 1 ] || fallar "con 'todos' solo se indica el escenario"
  escenario "${1:-E0}"
  todos
elif [ $# -ge 2 ] && [ -f "$1" ]; then
  [ $# -le 3 ] || fallar "demasiados argumentos"
  [ -f "$2" ] || fallar "no existe el archivo de vuelos: $2"
  PISTAS="$1" VUELOS="$2" ESPERADO="" NOMBRE="propio"
  un_lenguaje "$LENGUAJE" "${3:-$RAIZ/salida/$LENGUAJE/propio}"
else
  [ $# -le 2 ] || fallar "demasiados argumentos"
  escenario "${1:-E0}"
  un_lenguaje "$LENGUAJE" "${2:-$RAIZ/salida/$LENGUAJE/$NOMBRE}"
fi
