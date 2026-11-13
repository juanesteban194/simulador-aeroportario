#!/usr/bin/env bash
# =============================================================================
#  Instala y verifica el entorno del Simulador aeroportuario en macOS.
#  Uso: bash herramientas/instalar_entorno.sh      (se puede ejecutar varias veces)
#
#  1. JDK 21 (JVM común), Scala CLI y Leiningen (Clojure)
#  2. Herramientas de medición candidatas (se confirman en los Bloques 3 y 4)
#  3. Plugin Cursive para editar Clojure en IntelliJ
#  4. Prueba real: compila y ejecuta un "hola" en los tres lenguajes con JDK 21
# =============================================================================
set -uo pipefail
export HOMEBREW_NO_ASK=1 HOMEBREW_NO_ENV_HINTS=1 HOMEBREW_NO_INSTALL_CLEANUP=1

FALLAS=0
paso()  { printf '\n==> %s\n' "$*"; }
ok()    { printf '    OK      %s\n' "$*"; }
falla() { printf '    FALLA   %s\n' "$*"; FALLAS=$((FALLAS + 1)); }

# ---------------------------------------------------------------- Homebrew
for brew_bin in /opt/homebrew/bin/brew /usr/local/bin/brew; do
  [ -x "$brew_bin" ] && eval "$("$brew_bin" shellenv)" && break
done
command -v brew >/dev/null 2>&1 || { echo "ERROR: falta Homebrew (https://brew.sh)"; exit 1; }

instalar_formula() {   # $1 = fórmula, $2 = alternativa (opcional)
  if brew list --formula "$1" >/dev/null 2>&1; then ok "$1 ya estaba instalado"; return; fi
  paso "Instalando $1"
  if brew install "$1"; then ok "$1 instalado"
  elif [ -n "${2:-}" ] && brew install "$2"; then ok "$2 instalado"
  else falla "no se pudo instalar $1"; fi
}

# ---------------------------------------------------------------- 1. Lenguajes
paso "1. Lenguajes y compiladores"
instalar_formula openjdk@21
JAVA_HOME="$(brew --prefix openjdk@21)/libexec/openjdk.jdk/Contents/Home"
export JAVA_HOME PATH="$JAVA_HOME/bin:$PATH"
[ -x "$JAVA_HOME/bin/java" ] && ok "JAVA_HOME = $JAVA_HOME" || falla "no encuentro el JDK 21"

if command -v scala-cli >/dev/null 2>&1; then ok "scala-cli ya estaba instalado"
else instalar_formula Virtuslab/scala-cli/scala-cli; fi
instalar_formula leiningen

# ---------------------------------------------------------------- 2. Medición
paso "2. Herramientas de medición (candidatas)"
[ -x /usr/bin/time ] && ok "/usr/bin/time (tiempo y memoria máxima del proceso)" || falla "falta /usr/bin/time"
instalar_formula clj-kondo borkdude/brew/clj-kondo
PYTHON="$HOME/anaconda3/bin/python3"; [ -x "$PYTHON" ] || PYTHON="$(command -v python3)"
if "$PYTHON" -m lizard --version >/dev/null 2>&1; then ok "lizard ya estaba instalado"
elif "$PYTHON" -m pip install --quiet lizard; then ok "lizard instalado (complejidad de Java y Scala)"
else falla "no se pudo instalar lizard"; fi
"$PYTHON" -c "import matplotlib" 2>/dev/null && ok "matplotlib (gráficos del informe)" || falla "falta matplotlib en $PYTHON"
command -v npx >/dev/null 2>&1 && ok "npx (para jscpd: duplicación de código)" || falla "falta Node.js (npx) para jscpd"

# ---------------------------------------------------------------- 3. Cursive
paso "3. Plugin Cursive para IntelliJ"
IDEA_APP="$(ls -d /Applications/IntelliJ\ IDEA*.app 2>/dev/null | head -1)"
if [ -z "$IDEA_APP" ]; then falla "no encontré IntelliJ IDEA en /Applications"
else
  INFO="$IDEA_APP/Contents/Resources/product-info.json"
  CODIGO="$(plutil -extract productCode raw "$INFO")"
  BUILD="$(plutil -extract buildNumber raw "$INFO")"
  DATOS="$(plutil -extract dataDirectoryName raw "$INFO")"
  PLUGINS="$HOME/Library/Application Support/JetBrains/$DATOS/plugins"
  mkdir -p "$PLUGINS"
  if ls "$PLUGINS" | grep -qiE "cursive|clojure-plugin"; then ok "Cursive ya estaba instalado"
  else
    ZIP="$(mktemp -d -t cursive)/cursive.zip"
    if curl -fsSL --retry 3 -o "$ZIP" \
         "https://plugins.jetbrains.com/pluginManager?action=download&id=com.cursiveclojure.cursive&build=$CODIGO-$BUILD" \
       && unzip -tq "$ZIP" >/dev/null 2>&1 && unzip -q -o "$ZIP" -d "$PLUGINS"; then
      ok "Cursive instalado para $CODIGO-$BUILD (se activa al reiniciar IntelliJ)"
    else falla "no hay versión de Cursive para $CODIGO-$BUILD"; fi
    rm -f "$ZIP"
  fi
fi

# ---------------------------------------------------------------- 4. Prueba real
paso "4. Prueba: compilar y ejecutar en los tres lenguajes con JDK 21"
PRUEBA="$(mktemp -d -t prueba_entorno)"

mkdir -p "$PRUEBA/java"
printf 'public class Hola { public static void main(String[] a) { System.out.println("Hola desde Java " + Runtime.version()); } }\n' > "$PRUEBA/java/Hola.java"
( cd "$PRUEBA/java" && javac Hola.java && printf 'Main-Class: Hola\n' > m.txt && jar cfm hola.jar m.txt Hola.class ) \
  && java -jar "$PRUEBA/java/hola.jar" && ok "Java" || falla "Java"

mkdir -p "$PRUEBA/scala"
printf '//> using scala 3.9.0\nobject Hola { def main(a: Array[String]): Unit = println(s"Hola desde Scala ${util.Properties.versionNumberString}") }\n' > "$PRUEBA/scala/Hola.scala"
scala-cli --power package "$PRUEBA/scala" --assembly -f -o "$PRUEBA/scala/hola.jar" --main-class Hola >/dev/null 2>&1 \
  && java -jar "$PRUEBA/scala/hola.jar" && ok "Scala" || falla "Scala"

mkdir -p "$PRUEBA/clojure/src/hola"
cat > "$PRUEBA/clojure/project.clj" <<'CLJ'
(defproject hola "0.1.0"
  :dependencies [[org.clojure/clojure "1.12.0"]]
  :main hola.core
  :aot [hola.core]
  :uberjar-name "hola.jar")
CLJ
cat > "$PRUEBA/clojure/src/hola/core.clj" <<'CLJ'
(ns hola.core (:gen-class))
(defn -main [& _] (println "Hola desde Clojure" (clojure-version)))
CLJ
( cd "$PRUEBA/clojure" && lein uberjar >/dev/null 2>&1 ) \
  && java -jar "$PRUEBA/clojure/target/uberjar/hola.jar" && ok "Clojure (compilado por adelantado)" || falla "Clojure"

# ---------------------------------------------------------------- Resumen
paso "Versiones"
java -version 2>&1 | head -1
scala-cli version 2>/dev/null | head -2
lein version 2>/dev/null
clj-kondo --version 2>/dev/null
"$PYTHON" -m lizard --version 2>/dev/null | sed 's/^/lizard /'

paso "Resultado"
if [ "$FALLAS" -eq 0 ]; then echo "    TODO LISTO"; else echo "    $FALLAS paso(s) con falla: revisar arriba"; fi
exit "$FALLAS"
