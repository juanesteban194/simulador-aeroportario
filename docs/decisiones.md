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

## Bloque 1 · Requerimientos

Se aceptaron las recomendaciones. El documento se revisó y el bloque se cerró el 13 de noviembre de 2026.

### D1.1 · Cómo avanza el tiempo
- **Opciones:** por eventos o minuto a minuto.
- **Elegido:** por eventos. La simulación solo actúa cuando llega un vuelo o se libera una pista.
- **Por qué:**
  - Es determinista.
  - El costo depende del número de vuelos, no de la duración simulada.
  - En los tres lenguajes se expresa como una reducción (`reduce`/`fold`) sobre el estado del aeropuerto.

### D1.2 · Prioridad (RN05)
- **Elegido:** primero Emergencia; luego Aterrizaje antes que Despegue; luego la hora programada más temprana;
  luego el código menor.
- **Por qué:** un avión en el aire consume combustible mientras espera.
- **Precisión:** la prioridad se aplica **entre los vuelos que ya están esperando** cuando hay una pista libre
  (RN04 y RN06). Ordenar toda la lista por prioridad sería un error: una emergencia programada a las 18:00
  operaría antes que un vuelo de las 08:00.

### D1.3 · Compatibilidad y ocupación (RN02 y RN03)
- **Elegido:**
  - Ligero: pista de 1.200 m o más; ocupa la pista 2 min.
  - Mediano: 2.000 m o más; 3 min.
  - Pesado: 2.800 m o más; 4 min.
  - La pista debe estar operativa y permitir la operación.
  - Entre las pistas libres compatibles se asigna la de identificador menor.
  - Un vuelo sin pista compatible libre no bloquea a los de menor prioridad (RN06).

### D1.4 · Entrada de datos
- **Opciones:** teclado o archivos.
- **Elegido:** dos archivos (pistas y vuelos) que se pasan como argumentos.
- **Por qué:** el experimento necesita miles de vuelos, y eso no se puede escribir por teclado.

### D1.5 · Alcance funcional
- **Elegido:** RF01 a RF14, con las reglas RN01 a RN10 y las validaciones de `01_requerimientos.md`.
- Retrasado = más de 15 minutos de retraso.

## Bloque 2 · Modelo y contrato

Se aceptaron las recomendaciones. El detalle está en `02_modelo_y_contrato.md`. Bloque cerrado el 13 de noviembre de 2026.

### D2.1 · Archivos de entrada
- **Elegido:** CSV separado por comas, con encabezado. A cada campo se le hace `trim`, se conservan los campos
  vacíos y los valores deben coincidir exactamente (mayúsculas incluidas).
- **Por qué:** es la regla más simple de verificar y la misma en los tres lenguajes.

### D2.2 · Salidas
- **Elegido:** tres archivos (`operaciones.csv`, `errores.csv`, `reporte.txt`) y el reporte en pantalla.
- **Por qué:**
  - Con un millón de vuelos, imprimir cada operación en pantalla haría que el experimento midiera la consola.
  - La equivalencia se verifica con `diff` byte a byte.

### D2.3 · Representación
- **Elegido:**
  - Java: `record`, `enum` y `sealed interface Resultado`.
  - Scala: `case class`, `enum` y `Either`.
  - Clojure: `defrecord`, palabras clave y mapas `{:ok}`/`{:error}`.
  - Los mismos módulos en los tres: Modelo, Lectura, Validación, TorreControl, Reportes y Main.

### D2.4 · Algoritmo de simulación
- **Elegido:** 12 filas precalculadas (`groupBy` + `sortBy`), un estado inmutable pequeño y una secuencia
  perezosa de estados (`iterate` → `takeWhile` → `flatMap`).
- **Por qué:**
  - Da el mismo resultado que recorrer toda la cola (RN06).
  - Tiene el mismo costo en los tres lenguajes, sin depender de colecciones que Java no trae.
  - No usa recursión profunda (Java no optimiza la recursión de cola).

### D2.5 · Números y horas
- **Elegido:** tiempos y sumas en enteros de 64 bits; decimales solo al final, con 2 cifras, `HALF_UP` y
  `Locale.ROOT`; horas en formato `D<día> HH:MM`.
- **Por qué:** el resultado no depende del orden de las sumas ni de la configuración regional del equipo.

## Bloque 3 · Diseño del experimento

Se aceptaron las recomendaciones. El detalle está en `03_experimento.md`. Bloque cerrado el 13 de noviembre de 2026.

### D3.1 · Escenarios
- **Elegido:** un aeropuerto común (6 pistas, una cerrada) y los escenarios E0, V1 a V4 (1.000 a 1.000.000
  vuelos con la misma carga diaria), C1 (saturado) y X1 (10 % de registros inválidos).
- **Calibración con la implementación de referencia:**
  - La primera versión del aeropuerto solo tenía una pista para despegues de pesados, y P01 quedaba al 97 %.
    Se alargó P03 a 2.900 m.
  - Se eligieron 1.500 vuelos por día para la carga normal (ocupación media ≈ 60 %, retrasos de
    aproximadamente 1 minuto).
  - Se eligieron 2.400 vuelos por día para la congestión (tres pistas al 100 %).

### D3.2 · Generación de datos
- **Elegido:** generador en Python con semilla fija; solo usa `random.random()`, que es estable entre
  versiones. Se suben al repo E0, V1 y V2; los demás se regeneran y se verifican con huellas SHA-256.

### D3.3 · Métricas e instrumentos
- **Tiempo:** `t_operaciones` (validación + simulación + reportes), medido con `System.nanoTime()`.
- **Rendimiento:** vuelos por segundo del proceso completo, medido con un reloj externo.
- **Memoria:** memoria residente máxima del proceso, tomada de `rusage` del sistema operativo.
- Regla de materialización: cada etapa debe terminar su cálculo antes de tomar el tiempo.

### D3.4 · Protocolo
- **Elegido:** `java -Xmx4g -XX:+UseG1GC -jar` en los tres; cada ejecución es un proceso nuevo.
  Se hace 1 ronda de calentamiento y 10 medidas, con el orden rotado, y se reporta la mediana.
  Antes de medir se verifica que la salida sea correcta.

### D3.5 · Registro
- **Elegido:** una fila por ejecución en `resultados/crudos/<escenario>.csv` y el entorno en
  `resultados/entorno.txt`.

### D3.6 · Implementación de referencia
- **Elegido:** `experimento/referencia.py` produce las salidas esperadas. No participa en la comparación.
- **Por qué:** sin ella, si dos versiones difieren no hay forma de saber cuál está mal. Su resultado coincide con
  el ejemplo resuelto a mano del Bloque 2.

## Bloque 4 · Criterios y clasificación

Se aceptaron las recomendaciones. El detalle está en `04_criterios.md`.

### D4.1 · Tiempo, memoria y rendimiento
- **Elegido:** en cada escenario, puntaje proporcional al mejor (el mejor recibe 100). Luego se promedian los
  6 escenarios, todos con el mismo peso.
- **Por qué:** escalar entre el peor y el mejor le da 0 al último aunque esté muy cerca del primero.

### D4.2 · Calidad de código
- **Elegido:** tamaño (líneas), complejidad (puntos de decisión cada 100 líneas) y duplicación (jscpd), con un
  tercio cada una. Las advertencias del compilador y del analizador, y SonarQube, se reportan pero no
  puntúan.
- **Por qué:** son las únicas métricas que se miden con la misma regla en los tres lenguajes.

### D4.3 · Confiabilidad
- **Elegido:** el promedio de correctitud (7 escenarios), robustez (12 casos de error) y estabilidad
  (60 ejecuciones medidas).

### D4.4 · Uso funcional
- **Elegido:** 50 % restricciones (F1 sin ciclos, F2 sin reasignación, F3 sin colecciones mutables, F4 sin
  excepciones; una violación anula la regla) y 50 % densidad funcional (operaciones funcionales cada 100 líneas).

### D4.5 · Clasificación
- **Elegido:** suma con los pesos del profesor; desempate por Tiempo y luego por Memoria. Además, una prueba
  de solidez: se recalcula con pesos iguales y quitando un criterio a la vez.
