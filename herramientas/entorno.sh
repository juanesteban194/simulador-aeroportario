# Se carga con "source herramientas/entorno.sh" desde los scripts del experimento.
# En macOS, IntelliJ y otras aplicaciones gráficas no heredan el PATH de la terminal: aquí se agregan
# Homebrew y el JDK 21, para que los tres lenguajes usen siempre la misma JVM. En Linux no cambia nada.
for brew_bin in /opt/homebrew/bin/brew /usr/local/bin/brew; do
  [ -x "$brew_bin" ] && eval "$("$brew_bin" shellenv)" && break
done
if command -v brew >/dev/null 2>&1; then
  _jdk="$(brew --prefix openjdk@21 2>/dev/null)/libexec/openjdk.jdk/Contents/Home"
  if [ -x "$_jdk/bin/java" ]; then
    export JAVA_HOME="$_jdk"
    export PATH="$JAVA_HOME/bin:$PATH"
  fi
  unset _jdk
fi
