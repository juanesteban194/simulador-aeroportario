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

Se aceptaron las recomendaciones. El detalle está en `04_criterios.md`. Bloque cerrado el 13 de noviembre de 2026; con él termina la documentación previa al código.

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

## Bloque 5 · Implementación

Se aceptaron las recomendaciones. **Bloque cerrado:** las tres versiones producen exactamente las salidas de la
implementación de referencia.

### D5.1 · Orden de implementación
- **Elegido:** Java → Scala → Clojure (antes: Scala → Java → Clojure).
- **Por qué:** Java solo necesita el JDK, así que se puede compilar y verificar contra todos los casos
  mientras se escribe. Scala y Clojure descargan sus dependencias de Maven Central, y eso solo es posible
  en el Mac. Java queda como versión de referencia para traducir las otras dos.

### D5.2 · Estructura común
- **Elegido:** los mismos 7 módulos, con los mismos nombres de funciones, en los tres lenguajes:
  1. Modelo: entidades (Avión, Vuelo, Pista, Aeropuerto) y tipos de resultado.
  2. Lectura: archivo → líneas → registros.
  3. Validación (RF03).
  4. TorreControl: asignación de pistas y simulación (RF04 a RF06).
  5. Reportes (RF07 a RF14).
  6. Medición: tiempo por etapa y opción `--medir`.
  7. Main: argumentos y encadenamiento de las 5 etapas.
- **Por qué:** permite comparar el código módulo por módulo y que cada integrante explique cualquier versión.

### D5.3 · Algoritmo funcional
- **Elegido:** el mismo algoritmo en los tres:
  - **Estado inmutable.** Cada minuto produce un `Aeropuerto` nuevo:
    `iterate(paso) → takeWhile(no terminado) → flatMap(operaciones asignadas)`.
  - **Asignación en un minuto.** Por recursión, con profundidad máxima igual al número de pistas.
  - **Unicidad sin estado.** El dueño de cada código es el primer registro sin otros errores (agrupar y
    tomar el mínimo). Da el mismo resultado que validar línea por línea.
- **Por qué:** cumple F1 a F4 sin ciclos ni variables, y la complejidad es la misma en los tres lenguajes.

### D5.4 · Estilo
- **Elegido:**
  - Reglas F1 a F4 del Bloque 4.
  - `throws` solo en las funciones que leen o escriben archivos; los errores de datos se manejan como
    valores (`Ok` / `Falla`).
  - Nombres y comentarios en español; cada módulo empieza con un encabezado que dice qué hace.

### D5.5 · Pruebas
- **Elegido:** `experimento/verificar.sh` construye cada versión y compara byte a byte sus 3 archivos y lo
  que muestra en pantalla con lo esperado. Revisa:
  - el ejemplo E0;
  - los escenarios que tengan salida esperada (V1 y V2 en el repo; V3, V4, C1 y X1 al regenerarlos);
  - los 12 casos de robustez de `datos/robustez` (código de salida, archivos y stderr vacío).
- **Resultados:**
  - Java: coincide en los 19 casos, incluido V4 (1.000.000 de vuelos).
  - Clojure: coincide en los 19 casos. Se probó con el Clojure 1.11 de Ubuntu, porque Leiningen no puede
    descargar dependencias en ese entorno; la construcción oficial (`lein uberjar`, Clojure 1.12) se
    verifica en el Mac.
  - En el Mac (14-nov), con la construcción oficial de cada lenguaje (`javac`, `scala-cli` con Scala 3.9.0 y
    `lein uberjar` con Clojure 1.12.0) y el JDK 21: Java, Scala y Clojure coinciden en E0, V1, V2 y R01-R12
    (15/15 cada uno).
  - Pendiente para el inicio del Bloque 6: generar V3, V4, C1 y X1 en el Mac y repetir la verificación, para
    tener también Scala en los 19 casos antes de medir.
  - Tamaño de los `.jar`: Java 49 KB, Clojure 5,2 MB y Scala 10 MB (Clojure y Scala incluyen su biblioteca
    estándar). Es un dato para el informe.
- `SIN_CONSTRUIR=1` usa los `.jar` ya construidos. `herramientas/entorno.sh` pone Homebrew y el JDK 21 en el
  PATH, porque IntelliJ no hereda el de la terminal.

### D5.6 · Precisiones del contrato
Al escribir la primera versión aparecieron detalles que el contrato no fijaba y en los que los lenguajes
podían diferir. Quedan definidos en `02_modelo_y_contrato.md`:
- decimales con aritmética entera exacta y redondeo HALF_UP, sin punto flotante;
- `trim` de la JVM (quita los caracteres con código ≤ U+0020);
- bytes UTF-8 inválidos → U+FFFD, sin error;
- orden de textos por unidades UTF-16 (`compareTo` de Java);
- error de uso: línea `ERROR: <motivo>`, línea de uso y código 2, sin escribir archivos.

La implementación de referencia se actualizó con estas reglas; sus salidas esperadas no cambiaron.

### D5.7 · Reparto para la sustentación (propuesto)
- Sebastián Villa: Java · Juan Esteban Echavarría: Scala · Miguel Guarnizo: Clojure.
- Cada uno explica su versión y debe poder explicar las otras dos con la guía del Bloque 8.

## Bloque 6 · Ejecución del experimento

Se aceptaron las recomendaciones. Bloque en curso.

### D6.1 · Un solo orquestador
- **Elegido:** `experimento/ejecutar.py`, solo con la biblioteca estándar de Python. Hace el protocolo completo
  de `03_experimento.md` (sección 6): construir, registrar el entorno, regenerar y comprobar los escenarios,
  verificar la equivalencia, medir, guardar los datos crudos y resumir.
- **Por qué:** una sola orden, sin pasos manuales en los que equivocarse; el mismo procedimiento para los tres.

### D6.2 · Prueba antes de medir
- **Elegido:** `--prueba` hace 1 ronda de V1 y V2 y guarda en `resultados/prueba/` (no se versiona).
- **Por qué:** detecta errores del orquestador en ~1 minuto, antes de la medición completa.

### D6.3 · Dónde se ejecuta
- **Elegido:** en la app Terminal de macOS, con IntelliJ y las demás aplicaciones cerradas, el Mac conectado al
  cargador y sin modo de bajo consumo. El orquestador se detiene si detecta batería o bajo consumo (salvo
  `--forzar`, que queda registrado en `entorno.txt`).
- **Por qué:** IntelliJ indexa en segundo plano y consume CPU y memoria; eso alteraría la medición.

### D6.4 · Duración y registro de cada ejecución
- 6 escenarios × 11 rondas × 3 lenguajes = 198 ejecuciones, unos 20 minutos.
- La ronda 0 (calentamiento) también queda en `crudos/` para transparencia, pero no entra en ningún cálculo.
- Una ejecución es correcta si termina con código 0, no escribe en stderr y sus 3 archivos tienen la misma
  huella SHA-256 que los esperados.

### D6.5 · Memoria
- **Elegido:** `ru_maxrss` de `os.wait4` sobre el proceso de la JVM. macOS lo entrega en bytes y Linux en KB;
  el orquestador convierte ambos a MB (1 MB = 1.048.576 bytes).

### D6.6 · Qué se versiona
- `resultados/entorno.txt`, `resultados/verificacion.csv`, `resultados/crudos/*.csv` y `resultados/resumen.md`
  (evidencia del entregable 13). No se versionan las salidas generadas ni los registros de construcción.
