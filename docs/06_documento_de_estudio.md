# Documento de estudio · Simulador de operaciones aeroportuarias en Java, Scala y Clojure

**Final de Lenguajes y Paradigmas de Programación (Comparativo – Lenguajes – PF, profesor JuanGui)**
Equipo: Sebastián Villa · Miguel Guarnizo · Juan Esteban Echavarría
Repositorio: <https://github.com/juanesteban194/simulador-aeroportario->

Este documento explica **qué se hizo, por qué y cómo**, para estudiar antes de la sustentación. Se puede leer
de corrido; cada sección termina con las ideas que hay que saber decir con palabras propias. Los detalles
completos están en `docs/01` a `docs/04` y en `docs/decisiones.md`.

---

## 1. Qué pedía el trabajo y dónde se cumple

El enunciado pide implementar el mismo proyecto en Java, Scala y un tercer lenguaje, con programación
funcional, y **demostrar con un experimento** cuál lenguaje se comporta mejor. No basta con tres programas:
hay que medir, comparar y clasificar automáticamente.

| Condición o entregable del enunciado | Dónde se cumple |
|---|---|
| 1. Implementar en Java, Scala y un tercer lenguaje | `java/`, `scala/`, `clojure/` (tercer lenguaje: **Clojure**, funcional y también sobre la JVM) |
| 2. Mismos requisitos y resultados equivalentes | Contrato común (`docs/02`) y verificación byte a byte (`experimento/verificar.sh`): 19 de 19 casos en los tres |
| 3. Funciones de orden superior, lambdas, map, filter, agrupación, reducción | Reglas F1–F4 sin ciclos, sin reasignación, sin colecciones mutables y sin excepciones; todo con operaciones funcionales |
| 4. Escenarios para distintos volúmenes y cargas | 6 escenarios de 1.000 a 1.000.000 de vuelos, uno saturado y uno con errores (`datos/`) |
| 5. Medir y registrar el comportamiento | Opción `--medir` en los tres programas y el orquestador `experimento/ejecutar.py` |
| 6. Condiciones equivalentes | Misma JVM, mismas opciones, mismos datos, orden rotado, 10 rondas, proceso nuevo por ejecución |
| 7. Consolidar resultados | `resultados/crudos/`, `consolidado.csv`, `puntajes.csv` |
| 8. Mecanismo automático que elige el mejor | `experimento/clasificar.py` |
| 9. Clasificación con las métricas que la justifican | `resultados/clasificacion.md` y el informe |
| 10. Conclusión técnica | Informe técnico (sección de conclusiones) y la sección 9 de este documento |
| Entregables 11 a 16 | Ver la carpeta `Entregables/` de la solución |

**Idea clave:** el proyecto es un **experimento controlado**. Los tres programas son los "sujetos"; el
contrato, los datos y el orquestador son el "laboratorio" que garantiza que se comparan los lenguajes y no la
habilidad de quien programó cada versión.

---

## 2. Cómo se trabajó: bloques con decisiones

Se trabajó en 9 bloques. En cada uno se propusieron opciones, el equipo eligió y quedó registrado en
`docs/decisiones.md` (decisiones D0.1 a D7.4) con la razón. **Primero se documentó y después se programó.**

| Bloque | Qué se hizo |
|---|---|
| 0 · Marco | Repositorio, herramientas (JDK 21, Scala CLI, Leiningen), elección de Clojure |
| 1 · Requerimientos | Reglas de negocio RN01–RN10, requisitos RF01–RF14, validaciones, RNF |
| 2 · Modelo y contrato | Entidades inmutables, algoritmo de la torre, formato exacto de entrada y salida, ejemplo resuelto a mano |
| 3 · Experimento | Escenarios, generador determinista, implementación de referencia, métricas, protocolo |
| 4 · Criterios | Fórmulas de puntaje de los 6 criterios, desempate y prueba de solidez |
| 5 · Implementación | Las tres versiones con los mismos 7 módulos; verificación 19/19 |
| 6 · Medición | Orquestador y 198 ejecuciones medidas |
| 7 · Clasificación | Calidad, uso funcional, puntajes, clasificación y gráficos |
| 8 · Informe y sustentación | Informe técnico, este documento y el guion |

**Por qué Clojure como tercer lenguaje:** es un lenguaje funcional de verdad (datos inmutables por defecto,
funciones como valores) y corre en la **misma JVM** que Java y Scala. Así la comparación es justa: los tres
se ejecutan con `java -jar` sobre el mismo JDK 21, y las diferencias se deben al lenguaje y a su forma de
compilar, no a la plataforma.

---

## 3. El problema: simulador de operaciones aeroportuarias

Un aeropuerto tiene varias pistas. La torre de control recibe la programación de despegues y aterrizajes y
debe asignar cada vuelo a una pista **compatible y libre**, respetando prioridades, calcular retrasos y
generar reportes. El extra del proyecto es la **asignación automática de pistas por prioridad y
disponibilidad**.

**Entidades** (todas inmutables): Avión (matrícula, categoría), Vuelo (código, aerolínea, avión, operación,
hora programada, prioridad), Pista (id, longitud, uso, estado), Aeropuerto (estado de la simulación en un
minuto) y TorreControl (funciones puras que reciben un Aeropuerto y devuelven otro).

**Reglas que hay que saber explicar:**
- **RN02 · Categorías:** Ligero necesita 1.200 m y ocupa la pista 2 min; Mediano 2.000 m y 3 min; Pesado 2.800
  m y 4 min.
- **RN03 · Compatibilidad:** pista Operativa, con uso Mixta o igual a la operación, y suficientemente larga.
- **RN05 · Prioridad:** Emergencia antes que Normal; Aterrizaje antes que Despegue; hora programada más
  temprana; código menor.
- **RN06 · Asignación automática:** cada vuelo recibe la pista libre compatible de **menor id**. Un vuelo que no
  tiene pista libre **no bloquea** a los demás.
- **RN08 · Retraso:** inicio real − hora programada. Retrasado si supera 15 minutos.
- **RN09 · No asignable:** si ninguna pista del aeropuerto le sirve, se reporta con su motivo.
- **RN10 · Determinismo:** sin azar ni reloj: mismas entradas, misma salida.

**Salidas:** `operaciones.csv` (programa final, RF07), `errores.csv` (registros inválidos, RF03) y
`reporte.txt` (RF08 a RF14: retrasos, top 5, uso de pistas, aerolíneas, no asignables, conteos y resumen
ejecutivo).

---

## 4. El diseño común (lo que hace que la comparación sea justa)

### 4.1 Contrato byte a byte

`docs/02_modelo_y_contrato.md` fija **todo** lo que podría salir distinto entre lenguajes:
- **Lectura:** UTF-8 (un byte inválido se vuelve `�` sin error), encabezado en la línea 1, líneas vacías
  ignoradas, `split(",", -1)` para conservar campos vacíos y `trim` con la definición de la JVM.
- **Mensajes de error exactos** y orden de validación (solo se reporta el primer error).
- **Decimales sin punto flotante:** `c = (200·a + b) div (2·b)` da las centésimas redondeadas, y se escribe
  `c div 100` + "." + `c mod 100` con 2 dígitos. Así ningún lenguaje depende de su formateador ni de la
  configuración regional.
- **Orden de textos** por `compareTo` de la JVM (unidades UTF-16), igual en los tres.
- **Errores de uso:** línea `ERROR: …`, línea de uso y código de salida 2, sin escribir archivos.

**Por qué importa:** si dos versiones difieren en un decimal o en el orden de un empate, no se puede decir
que sean equivalentes. El contrato convierte "equivalentes" en algo **verificable con `cmp`**.

### 4.2 Siete módulos iguales en los tres lenguajes

| # | Módulo | Qué hace |
|---|---|---|
| 1 | Modelo | Entidades y listas cerradas |
| 2 | Lectura | Archivo → líneas → registros (número de línea + campos) |
| 3 | Validación | Cada registro → dato válido o error (RF03) |
| 4 | TorreControl | Compatibilidad, no asignables y simulación (RF04–RF06) |
| 5 | Reportes | Texto de los 3 archivos (RF07–RF14) |
| 6 | Medición | Tiempo de cada etapa y opción `--medir` |
| 7 | Main | Argumentos y encadenamiento de las 5 etapas |

### 4.3 El algoritmo de la torre (lo más importante para la sustentación)

1. Los vuelos asignables se agrupan en **12 filas** por (operación, categoría, prioridad) y cada fila se ordena
   por (hora, código).
2. **Por qué basta mirar el primero de cada fila:** todos los vuelos de una fila son compatibles con las
   mismas pistas. Si el primero no tiene pista libre, ninguno de su fila la tiene. Así se evita recorrer toda
   la cola en cada minuto.
3. El estado es un **Aeropuerto inmutable**: minuto actual, posición del primer pendiente de cada fila,
   minuto en que se libera cada pista y operaciones asignadas en el paso.
4. **Un paso** asigna en el minuto actual mientras haya un candidato con pista libre (el de mayor prioridad
   RN05 recibe la pista libre compatible de menor id) y luego salta al **siguiente evento**: el menor minuto
   futuro en que se libera una pista o llega un vuelo. No se simula minuto a minuto.
5. La simulación completa es una **secuencia perezosa de estados**: `iterate(paso)` → `takeWhile(no
   terminado)` → `flatMap(operaciones del paso)`. Sin ciclos ni variables.

```java
// Java
return Stream.iterate(inicial, a -> !terminado(a, filas), a -> paso(a, filas, operativas))
        .flatMap(a -> a.asignadasEnElPaso().stream())
        .toList();
```
```scala
// Scala
Iterator.iterate(inicial)(a => paso(a, todas, operativas))
  .takeWhile(a => !terminado(a, todas))
  .flatMap(_.asignadasEnElPaso)
  .toVector
```
```clojure
;; Clojure
(into []
      (comp (take-while #(not (terminado? % filas)))
            (mapcat :asignadas-en-el-paso))
      (iterate #(paso % filas operativas) inicial))
```

**Costo:** ordenar una vez (n·log n) y luego, por cada evento, un trabajo constante (12 filas y 5 pistas). Hay
como máximo dos eventos por vuelo. Por eso el tiempo crece casi en línea recta con el número de vuelos.

### 4.4 Validación sin estado

La unicidad de los códigos se comprueba contra los registros **válidos anteriores**. En lugar de recorrer el
archivo llevando un conjunto (estado), se calcula el **dueño** de cada código: el primer registro sin otros
errores (agrupar por código y tomar la línea mínima). Un registro está "repetido" si su código tiene un dueño
anterior. Da exactamente el mismo resultado y no necesita variables.

### 4.5 Ejemplo resuelto a mano (E0)

13 vuelos y 5 pistas (una inválida y una cerrada). A las 08:01 llega una **emergencia** (CM304) que solo puede
usar P01, ocupada: espera, pero **no bloquea** a AV103, que aterriza en P03. Resultado: 9 operaciones, retraso
promedio 14/9 = **1,56 min**, AV108 (Pesado) no asignable porque ninguna pista operativa mide 2.800 m. Este
ejemplo se calculó a mano y es la primera prueba de las tres versiones.

---

## 5. Programación funcional en los tres lenguajes

### 5.1 Las cuatro reglas (verificadas automáticamente)

| Regla | Qué prohíbe | Cómo se reemplaza |
|---|---|---|
| F1 · Sin ciclos | `for`, `while`, `loop`, `doseq` | `map`, `filter`, `iterate`, recursión |
| F2 · Sin reasignación | `x = …` de nuevo, `var`, `atom` | valores nuevos (`copy`, `assoc`, records nuevos) |
| F3 · Sin colecciones mutables | `ArrayList.add`, `ArrayBuffer`, `transient` | listas inmutables (`List.of`, `Vector`, vectores de Clojure) |
| F4 · Sin excepciones | `try`, `catch`, `throw` | errores como valores (`Optional`, `Either`, `{:falla …}`) |

Los tres cumplen las 4 reglas (`experimento/funcional.py` no encontró ninguna violación). En Java se permite
`throws` en las firmas que leen o escriben archivos, porque Java obliga a declararlo; no es manejo de
excepciones.

### 5.2 Equivalencias entre lenguajes

| Concepto | Java | Scala | Clojure |
|---|---|---|---|
| Entidad inmutable | `record` | `case class` | `defrecord` |
| Lista cerrada | `enum` | `enum` | palabra clave `:Ligero` |
| Valor que puede faltar | `Optional<T>` | `Option[T]` | `nil` |
| Resultado o error | `sealed interface Resultado` (`Ok`/`Falla`) | `Either[ErrorRegistro, T]` | `{:ok v}` / `{:falla e}` |
| "Cambiar" un dato | `new Aeropuerto(...)` | `a.copy(...)` | `(assoc a ...)` |
| Secuencia perezosa | `Stream` | `Iterator` | secuencia perezosa / transductores |
| Primer error de varias reglas | `Optional.or(...)` | `Option.orElse(...)` | `(or ...)` |
| Recursión de cola | no la optimiza (profundidad ≤ 5) | `@tailrec` | `recur` |

### 5.3 La misma regla en los tres lenguajes

Validación de una pista: se revisan las reglas en orden y se devuelve el **primer error**, o nada si es válida.

```java
// Java: cadena de Optional.or
return entero(c.get(1), "longitud")
        .or(() -> si(Integer.parseInt(c.get(1)) <= 0, "longitud debe ser mayor que 0: " + c.get(1)))
        .or(() -> opcion(c.get(2), "uso", Modelo.nombres(Uso.values())))
        .or(() -> opcion(c.get(3), "estado", Modelo.nombres(Estado.values())));
```
```scala
// Scala: cadena de Option.orElse (el argumento se evalúa solo si hace falta)
entero(c(1), "longitud")
  .orElse(si(c(1).toInt <= 0, s"longitud debe ser mayor que 0: ${c(1)}"))
  .orElse(opcion(c(2), "uso", Modelo.nombres(Uso.values)))
  .orElse(opcion(c(3), "estado", Modelo.nombres(Estado.values)))
```
```clojure
;; Clojure: or devuelve el primer valor que no es nil
(or (entero longitud "longitud")
    (when (<= (parse-long longitud) 0) (str "longitud debe ser mayor que 0: " longitud))
    (opcion uso "uso" m/nombres-uso)
    (opcion estado "estado" m/nombres-estado))
```

**Qué decir:** las tres expresan lo mismo: "el primer error, si existe". Java necesita lambdas (`() -> …`)
para que la regla no se evalúe antes de tiempo; Scala lo logra con parámetros "por nombre"; Clojure, con el
macro `or`, que ya es perezoso.

### 5.4 Elegir el mejor candidato (RN05)

```java
// Java: Stream + Comparator
return IntStream.range(0, filas.size()).boxed()
        .filter(i -> quedanVuelos(a, filas, i))
        .filter(i -> primero(a, filas, i).programado() <= a.minuto())
        .flatMap(i -> pistaLibre(a, primero(a, filas, i), pistas)
                .map(j -> new Candidato(i, j, primero(a, filas, i))).stream())
        .min(Comparator.comparing(Candidato::vuelo, PRIORIDAD));
```
```scala
// Scala: colecciones + Ordering
filas.indices
  .filter(i => quedanVuelos(a, filas, i) && primero(a, filas, i).programado <= a.minuto)
  .flatMap(i => pistaLibre(a, primero(a, filas, i), pistas).map(j => Candidato(i, j, primero(a, filas, i))))
  .minByOption(_.vuelo)(using prioridad)
```
```clojure
;; Clojure: secuencias + comparador
(->> (range (count filas))
     (filter #(quedan-vuelos? aeropuerto filas %))
     (keep #(candidato aeropuerto filas pistas %))
     (sort-by :vuelo por-prioridad)
     first)
```

---

## 6. El experimento

### 6.1 Datos

| Escenario | Vuelos | Qué evalúa |
|---|---|---|
| E0 | 13 | Correctitud: el ejemplo resuelto a mano |
| V1 · V2 · V3 · V4 | 1.000 · 10.000 · 100.000 · 1.000.000 | Volumen, con la misma carga diaria (1.500 vuelos/día) |
| C1 | 100.000 | Congestión: 2.400 vuelos/día, aeropuerto saturado |
| X1 | 100.000 | Errores: 10 % de registros inválidos |
| R01–R12 | casos pequeños | Robustez: sin argumentos, archivos vacíos, `\r\n`, tildes, bytes inválidos… |

- **Generador determinista** (`datos/generador.py`): misma semilla → mismo archivo byte a byte. Cada archivo se
  comprueba con su huella **SHA-256** antes de medir.
- **Implementación de referencia** (`experimento/referencia.py`, en Python): no compite; produce las salidas
  esperadas. Si un lenguaje no coincide, no se mide en ese escenario.

### 6.2 Qué se mide y con qué instrumento

| Criterio | Métrica | Instrumento |
|---|---|---|
| Tiempo (25 %) | `t_operaciones` = validación + simulación + reportes, en ms | `System.nanoTime()` dentro de cada programa (el mismo reloj de la JVM) |
| Memoria (20 %) | Memoria residente máxima del proceso, en MB | `ru_maxrss` del sistema operativo (`os.wait4`) |
| Rendimiento (20 %) | Vuelos procesados por segundo en el proceso completo | Reloj del orquestador alrededor del proceso |

**Regla de materialización:** cada etapa debe dejar su resultado completamente calculado antes de tomar el
tiempo (`toList`, `toVector`, `vec`). Sin ella, Clojure (perezoso) parecería rápido en una etapa y lento en la
siguiente.

### 6.3 Protocolo

- Cada escenario: **1 ronda de calentamiento** (no cuenta) y **10 rondas medidas**.
- En cada ronda se ejecutan los tres lenguajes con el **orden rotado** (J-S-C, S-C-J, C-J-S…) para que ninguno
  quede siempre primero o último.
- **Un proceso nuevo por ejecución**: `java -Xmx4g -XX:+UseG1GC -jar …`. El arranque de la JVM y la
  compilación JIT son parte del comportamiento real de un programa de consola, y se miden igual en los tres.
- 1 segundo de pausa entre ejecuciones; la salida de cada ejecución se comprueba con SHA-256.
- Resultado por lenguaje y escenario: **mediana** de las 10 rondas, con mínimo, máximo y rango intercuartílico.

### 6.4 Dónde se midió

Los tres `.jar` se construyeron en el MacBook Pro del equipo con las herramientas oficiales (`javac`,
`scala-cli` con Scala 3.9.0 y `lein uberjar` con Clojure 1.12.0). Con ellos, la verificación dio 19 de 19 casos
en los tres lenguajes. La medición se ejecutó con esos mismos archivos (comprobados con su huella SHA-256) en un
contenedor Linux de 2 núcleos con OpenJDK 21: no se pudo lanzar en el Mac de forma desatendida. Los tres
lenguajes se midieron en el mismo entorno y con el mismo protocolo, así que la comparación es válida. Para
repetirla en el Mac basta `python3 experimento/ejecutar.py` (unos 20 minutos).

**Detalle técnico que vale la pena contar:** en la primera corrida, la memoria de todas las ejecuciones salía
igual (174 MB). La causa: en Linux, la memoria máxima que informa `wait4` para un proceso hijo parte de la
memoria que tenía el proceso padre (el orquestador en Python) cuando lo creó, y el orquestador había cargado
el archivo de un millón de vuelos. Se corrigió leyendo los archivos por partes: el orquestador ocupa 20 MB,
menos que cualquier JVM, y se repitió la medición completa.

---

## 7. Cómo se calcula el puntaje

**Proporcional al mejor** (tiempo, memoria, rendimiento, calidad): el mejor obtiene 100 y los demás
`100 · mejor / valor` (o `valor / mejor` si más es mejor). No se escala entre el peor y el mejor porque eso
le daría 0 al último aunque estuviera a un 1 % del primero.

| Criterio | Peso | Cómo se obtiene |
|---|---|---|
| Tiempo | 25 % | Promedio de los 6 escenarios del puntaje proporcional de `t_operaciones` |
| Memoria | 20 % | Igual, con la memoria máxima |
| Rendimiento | 20 % | Igual, con vuelos por segundo |
| Calidad | 15 % | Tercio cada una: líneas de código (Q1), decisiones cada 100 líneas (Q2), líneas duplicadas (Q3) |
| Confiabilidad | 10 % | Promedio de correctitud (7 escenarios), robustez (12 casos) y estabilidad (60 ejecuciones) |
| Uso funcional | 10 % | Restricciones F1–F4 (0 a 50) + densidad de operaciones funcionales (0 a 50) |

`Final = 0,25·Tiempo + 0,20·Memoria + 0,20·Rendimiento + 0,15·Calidad + 0,10·Confiabilidad + 0,10·Uso funcional`

**Desempate:** mayor Tiempo y luego mayor Memoria. **Prueba de solidez:** se recalcula con pesos iguales y
quitando un criterio a la vez; si el ganador no cambia, el resultado no depende de los pesos elegidos.

**Por qué SonarQube no puntúa:** no analiza Clojure. Usarlo solo para Java y Scala favorecería al lenguaje con
el analizador menos estricto. Por eso la calidad se mide con tres métricas que se calculan igual en los tres.

---

## 8. Resultados

Medición completa: 198 ejecuciones (6 escenarios × 11 rondas × 3 lenguajes), **todas con salida correcta**.

### 8.1 Clasificación

| Posición | Lenguaje | Tiempo | Memoria | Rendimiento | Calidad | Confiabilidad | Uso funcional | **Final** |
|---|---|---|---|---|---|---|---|---|
| 1.º | **Java** | 95,74 | 88,53 | **100,00** | **86,22** | 100,00 | 87,77 | **93,35** |
| 2.º | Scala | 88,87 | **95,70** | 86,66 | 85,06 | 100,00 | **100,00** | **91,45** |
| 3.º | Clojure | 78,64 | 75,97 | 58,71 | 72,78 | 100,00 | 81,35 | **75,65** |

**Java gana con 93,35 puntos, 1,90 por encima de Scala.** Clojure queda tercero con 75,65.

### 8.2 Lo que hay que saber explicar de cada criterio

**Tiempo (mediana de `t_operaciones`, ms)**

| | V1 | V2 | V3 | V4 | C1 | X1 |
|---|---|---|---|---|---|---|
| Java | 285 | **665** | **2.419** | **12.047** | **2.529** | **2.408** |
| Scala | 339 | 755 | 2.554 | 13.001 | 2.585 | 2.475 |
| Clojure | **212** | 759 | 3.311 | 19.806 | 3.288 | 3.280 |

- Java es el más rápido en 5 de 6 escenarios. Con un millón de vuelos, Scala tarda 8 % más y Clojure 64 % más.
- Java y Scala están a 1–6 % en los escenarios de 100.000 vuelos.
- **En V1 gana Clojure dentro del programa.** Con tan pocos datos domina el costo de usar cada función por
  primera vez. La explicación más probable: Java y Scala crean las clases de sus lambdas en ese momento, y
  Clojure (compilado por adelantado) ya las trae, pero paga antes de `main` la carga de su núcleo. Ese costo no
  entra en `t_operaciones`; sí entra en el rendimiento.
- **Por etapas en V4:**
  - Scala tiene la simulación más rápida (3,0 s, frente a 4,4 s de Java y 6,4 s de Clojure).
  - Java tiene la validación más rápida (5,0 s) y también los reportes más rápidos (2,7 s).
  - Clojure es el más lento en las tres etapas.

**Memoria (mediana, MB)**

| | V1 | V2 | V3 | V4 | C1 | X1 |
|---|---|---|---|---|---|---|
| Java | **62** | 171 | 741 | **3.065** | 738 | 734 |
| Scala | 78 | **151** | **599** | 3.238 | **597** | **596** |
| Clojure | 106 | 185 | 659 | 3.883 | 823 | 813 |

- Scala usa menos memoria con 10.000 a 100.000 vuelos. Java usa menos en el más pequeño (no carga la biblioteca
  de Scala ni el núcleo de Clojure) y en el más grande.
- Es la memoria física máxima del proceso: incluye cuánto decide crecer el recolector G1 (límite de 4 GB). Por
  eso en V4 los tres llegan a 3–4 GB.

**Rendimiento (vuelos por segundo, proceso completo)**

| | V1 | V2 | V3 | V4 | C1 | X1 |
|---|---|---|---|---|---|---|
| Java | **2.741** | **12.909** | **38.553** | **78.012** | **37.145** | **38.483** |
| Scala | 1.855 | 10.408 | 35.222 | 71.833 | 35.062 | 36.116 |
| Clojure | 1.193 | 6.999 | 24.747 | 46.884 | 24.729 | 24.494 |

- Java gana en los seis. El rendimiento incluye arrancar la JVM: el tiempo fuera de las operaciones en V1 es
  de 79 ms en Java, 200 ms en Scala y 626 ms en Clojure. Es el costo de arranque de cada lenguaje.

**Calidad y uso funcional**

| | Líneas | Decisiones cada 100 | Duplicadas | F1–F4 | Operaciones funcionales cada 100 |
|---|---|---|---|---|---|
| Java | 600 | **5,33** | 0 | 4/4 | 20,17 |
| Scala | **352** | 9,66 | 0 | 4/4 | **26,70** |
| Clojure | 466 | 12,45 | 0 | 4/4 | 16,74 |

- Scala escribe lo mismo con 41 % menos líneas que Java y es el más funcional: gana Uso funcional.
- Java tiene la menor densidad de decisiones: gana Calidad por poco (86,22 frente a 85,06).
- Clojure tiene más decisiones porque cada regla de validación usa `when` u `or`. Además, no usa tipos `Option`:
  trabaja con `nil`.
- `javac -Xlint:all`: 0 advertencias. Clojure: 0 llamadas por reflexión.

**Confiabilidad:** 100 en los tres. Superan 7/7 escenarios, 12/12 casos de robustez y 60/60 ejecuciones medidas.

### 8.3 Prueba de solidez

Java gana en **6 de 7** variantes. Solo en **"sin Rendimiento"** gana Scala, por 0,96 puntos. El tercer lugar
de Clojure no cambia nunca. Conclusión: el primer lugar de Java es claro pero estrecho, y se apoya en su ventaja
de rendimiento.

---

## 9. Conclusión técnica

**Lenguaje seleccionado para este proyecto: Java** (93,35 puntos). Las razones, en orden de importancia:

1. Es el más rápido en las operaciones en 5 de 6 escenarios y procesa más vuelos por segundo en los 6. Con un
   millón de vuelos procesa 78.012 vuelos/s, frente a 71.833 de Scala y 46.884 de Clojure.
2. Es igual de confiable que los demás.
3. Java moderno (records, Streams, `Optional`, interfaces selladas) permite cumplir todos los principios
   funcionales del curso.

**Scala es una alternativa casi equivalente** (1,90 puntos de diferencia):
- tiene el código más corto y más funcional;
- usa menos memoria con volúmenes medianos;
- tiene la simulación más rápida.

Si la mantenibilidad pesara más que el rendimiento, sería la mejor elección; sin el criterio de Rendimiento,
gana Scala.

**Clojure es correcto y funcional, pero el menos conveniente para este problema.** El problema es procesar
grandes volúmenes en un programa de consola que arranca en cada ejecución. Ahí pesan dos cosas:
- su arranque, unos 0,6 s;
- su tipado dinámico (números en objetos, búsqueda por palabra clave).

Con volúmenes grandes le cuestan entre 30 y 64 % más de tiempo. Sus optimizaciones habituales (colecciones
`transient`) están prohibidas por la regla F3 en los tres lenguajes, para comparar estilo funcional con estilo
funcional.

**Limitaciones que hay que mencionar:**
- un solo entorno de medición;
- un solo problema;
- se mide un proceso nuevo por ejecución, así que el arranque cuenta (con un servicio en ejecución continua, la
  desventaja de arranque de Scala y Clojure desaparecería);
- la memoria depende de las opciones del recolector;
- en V1 y V2 los rangos de Java y Scala se cruzan.

---

## 10. Cómo ejecutar todo

```bash
# Ejecutar el simulador en cualquiera de los 4 lenguajes (construye el .jar si falta o si el código cambió)
bash simular.sh java                 # o scala, clojure, python (referencia); escenario E0 por defecto
bash simular.sh scala V1             # otro escenario: E0, V1, V2, V3, V4, C1, X1
bash simular.sh todos V2             # los 4 lenguajes y compara sus salidas byte a byte
bash simular.sh                      # menú interactivo
bash simular.sh interfaz             # interfaz gráfica en tiempo real (navegador)

# Verificar que las tres versiones producen la misma salida (construye los .jar)
bash experimento/verificar.sh

# Medición: prueba rápida y medición completa (en macOS, desde Terminal)
caffeinate -dims python3 experimento/ejecutar.py --prueba
caffeinate -dims python3 experimento/ejecutar.py

# Calidad, uso funcional, clasificación y gráficos
python3 experimento/calidad.py
python3 experimento/funcional.py
python3 experimento/clasificar.py
python3 experimento/graficos.py

# Ejecutar un programa a mano
java -jar java/simulador-java.jar datos/ejemplo/pistas.csv datos/ejemplo/vuelos.csv salida
```

En IntelliJ hay configuraciones compartidas (`.run/`): **Verificar equivalencia** y la carpeta **Simulador**
(«Simular · Java», «· Scala», «· Clojure», «· Python (referencia)», «· los 4 y comparar» y «· menú»), que
se ejecutan con ▶. Las salidas quedan en `salida/<lenguaje>/<escenario>/`; para otro escenario se cambia
*Script options* (por ejemplo `java V1`).

### 10.1 La interfaz gráfica (para la demostración)

`bash simular.sh interfaz` (o «Simular · interfaz gráfica (tiempo real)» en IntelliJ) abre una página que
**ejecuta de verdad** el programa elegido y luego reproduce lo que hizo. Recorrido guiado:

1. **Lectura:** cuántos registros se leyeron y la tabla de entrada, con las líneas inválidas marcadas.
2. **Validación:** el resumen RF03, `errores.csv` y los no asignables (RN09).
3. **Simulación:**
   - un reloj que salta de evento en evento (los mismos minutos del algoritmo: en E0, 11 eventos);
   - las pistas en una línea de tiempo;
   - las 12 filas con el primer pendiente resaltado;
   - una bitácora que explica cada decisión. Ejemplo: «CM304 (emergencia) espera: P01 ocupada hasta 08:03 · no
     bloquea a AV103».
4. **Reportes:** `reporte.txt`.
5. **Escritura:** los archivos, el comando ejecutado, los tiempos de `--medir` y tres comprobaciones:
   - salida = esperada;
   - pantalla = `reporte.txt`;
   - explicación = salida real.

**Qué decir si preguntan cómo funciona:** el servidor local (`interfaz/servidor.py`, solo biblioteca estándar de
Python) lanza el mismo `java -jar` del experimento con `--medir` y entrega a la página las entradas y las salidas.
Lo que se dibuja son las asignaciones reales de `operaciones.csv`. Las explicaciones se recalculan en la página con
RN03 y RN05, y la página comprueba que lleguen exactamente a las mismas asignaciones; si no, lo marca. Con «Datos
propios» se pueden cambiar las entradas en vivo (por ejemplo, volver emergencia un vuelo) y ver la nueva
asignación en cualquiera de los cuatro lenguajes.

**Escenarios grandes.** Se pueden elegir los siete escenarios, de 1.000 a 1.000.000 de vuelos. Hasta 20.000 vuelos
la página reproduce todo. En V3, V4, C1 y X1 el programa procesa el escenario completo (tiempos, reporte y
comprobaciones son de esa ejecución) y la página reproduce los **primeros días completos**, unos 10.000 vuelos.

- **Por qué es exacto:** en el minuto *t* el algoritmo solo decide con vuelos programados hasta *t*. Lo que pase
  después no cambia el pasado, así que las asignaciones de los primeros días son las mismas que en la ejecución
  completa.
- **Qué se ve:** V4 con Java tarda unos 13 s; con la referencia en Python, unos 23 s.

## 11. Estructura del repositorio

```
java/ scala/ clojure/        las tres versiones (src/ + construir.sh)
datos/                       aeropuerto, ejemplo resuelto a mano, generador, escenarios y robustez
experimento/                 referencia, verificador, orquestador, calidad, uso funcional, clasificación, gráficos
resultados/                  datos crudos, verificación, entorno, puntajes, clasificación y gráficos
docs/                        requerimientos, contrato, experimento, criterios, decisiones y este documento
```

---

## 12. Preguntas probables y cómo responderlas

**¿Cómo saben que los tres programas hacen lo mismo?**
Porque producen archivos idénticos byte a byte en 19 casos: el ejemplo resuelto a mano, los 6 escenarios y los
12 casos de robustez. Lo comprueba `verificar.sh` con `cmp`; además, cada ejecución medida se compara con
SHA-256.

**¿Por qué Clojure y no Python o Haskell?**
Porque es funcional y corre en la misma JVM. Con Python o Haskell la diferencia sería de plataforma
(intérprete o compilador nativo) y no del lenguaje.

**¿Por qué un proceso nuevo en cada ejecución y no medir con la JVM ya caliente?**
Porque el simulador es un programa de consola: se usa así. El arranque y el JIT son parte de su costo real y
afectan igual a los tres. Para separar el arranque, se reportan dos tiempos: `t_operaciones` (dentro del
programa) y `t_proceso` (todo el proceso).

**¿Por qué la mediana y no el promedio?**
Porque una ejecución afectada por otro proceso del sistema mueve mucho el promedio y casi nada la mediana.

**¿Cómo se evita que una versión tenga un algoritmo mejor?**
Las tres usan el mismo diseño (12 filas, estado inmutable, salto al siguiente evento) y la misma complejidad.
Está en el contrato y se revisó módulo por módulo.

**¿Cómo se manejan los errores sin excepciones?**
Como valores: cada registro termina en `Ok`/`Falla` (Java), `Right`/`Left` (Scala) o `{:ok}`/`{:falla}`
(Clojure). Un archivo inexistente se detecta antes de leerlo y se responde con código 2.

**¿Por qué Java tiene más líneas?**
Por la sintaxis: tipos explícitos, `return`, llaves y lambdas para la evaluación perezosa. La lógica es la
misma.

**¿El resultado depende de los pesos del profesor?**
En parte. Java gana en 6 de 7 variantes (pesos iguales y quitando cada criterio). Solo sin el criterio de
Rendimiento gana Scala, por menos de un punto. El último lugar de Clojure no cambia en ninguna.

**¿Por qué Clojure salió último si es el más funcional de los tres?**
Porque el experimento premia sobre todo la velocidad (65 % del peso es tiempo, memoria y rendimiento) y
Clojure paga su tipado dinámico y su arranque. En confiabilidad empata con los demás. En uso funcional le
afecta que no usa tipos `Option` (trabaja con `nil`) y que su densidad de operaciones por línea es menor.

**¿Por qué la memoria es tan alta en V4 (3–4 GB)?**
Porque se mide la memoria física del proceso. Con `-Xmx4g`, el recolector G1 deja crecer el montículo antes de
limpiar. Afecta igual a los tres.

**¿Dónde se midió?**
En un contenedor Linux de 2 núcleos con OpenJDK 21, con los `.jar` construidos en el Mac. Es el mismo entorno
para los tres, así que la comparación vale. Se puede repetir en el Mac con una orden.

## 13. Glosario

- **Inmutable:** un dato que no cambia después de creado; para "cambiarlo" se crea otro.
- **Función pura:** con las mismas entradas da la misma salida y no modifica nada fuera de ella.
- **Función de orden superior:** recibe o devuelve funciones (`map`, `filter`, `sortBy`).
- **Evaluación perezosa:** un valor se calcula solo cuando se necesita (`Stream`, `Iterator`, secuencias de Clojure).
- **JIT:** compilación "justo a tiempo" de la JVM, que optimiza el código mientras se ejecuta.
- **AOT:** compilación por adelantado; Clojure se compila así para no compilar al arrancar.
- **RSS:** memoria residente, la memoria física que ocupa un proceso.
- **Mediana:** el valor del medio cuando se ordenan las mediciones.
- **Rango intercuartílico (RIC):** distancia entre el cuartil 1 y el 3; mide qué tan dispersas son las mediciones.
