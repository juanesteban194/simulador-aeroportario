# Registro de decisiones

Cada decisión indica las opciones que se consideraron, lo que se eligió y por qué.

## Bloque 0 · Marco

### D0.1 · Proyecto base
- **Opciones:** los proyectos definidos en clase.
- **Elegido:** 2. Simulador de operaciones aeroportuarias. Gestionar vuelos, asignar pistas, organizar
  despegues y aterrizajes y controlar retrasos. Entidades: Avión, Vuelo, Pista, Aeropuerto y TorreControl.
  Extra: asignación automática de pistas según prioridades y disponibilidad.
- **Por qué:** decisión del equipo.

### D0.2 · Tercer lenguaje
- **Opciones:** Python, Racket, Haskell, F#, Clojure.
- **Elegido:** Clojure.
- **Por qué:**
  - Es un lenguaje funcional, como pide la base del proyecto.
  - Corre sobre la **misma JVM** que Java y Scala, así que los tres comparten el JDK, el recolector de basura
    y el instrumento de medición de memoria. Las diferencias medidas se deben al lenguaje y a su compilador,
    no a la plataforma.
  - Sus funciones de colecciones (`map`, `filter`, `reduce`, `group-by`, `sort-by`) equivalen a las de Scala.
- **Diferencias a tener en cuenta:**
  - Sintaxis Lisp, con paréntesis y notación prefija, como Racket.
  - Tipado dinámico: los errores de tipo aparecen al ejecutar, no al compilar.
- **Consecuencia:** SonarQube no analiza Clojure. La calidad de código se mide en los tres lenguajes con
  instrumentos comunes (se define en el Bloque 4).

### D0.3 · Equipo
- Sebastián Villa · Miguel Guarnizo · Juan Esteban Echavarría.

### D0.4 · Repositorio
- **Elegido:** https://github.com/juanesteban194/simulador-aeroportario- (público), con las tres soluciones
  y el experimento en un solo repositorio.
- **Copia local recomendada:** `~/IdeaProjects/simulador-aeroportuario`. Se evita iCloud porque su
  sincronización puede dañar la carpeta `.git`.

### D0.5 · Herramientas
- **Elegido:**
  - JDK 21 común para los tres lenguajes.
  - Java: `javac` y `jar`, sin Maven, para no sumar dependencias.
  - Scala: Scala CLI.
  - Clojure: Leiningen (`lein uberjar` compila por adelantado y empaqueta).
  - Los tres se ejecutan con `java -jar` y las mismas opciones.
  - IntelliJ IDEA con el plugin Cursive para Clojure.
- **Por qué:**
  - Misma plataforma y misma forma de lanzar las tres versiones.
  - Clojure compilado por adelantado evita medir la compilación que haría en cada arranque.
