# 04 · Criterios de evaluación y clasificación automática

Este documento define **cómo se convierte cada medición en un puntaje** y **cómo se decide automáticamente el
lenguaje ganador**. Responde a las condiciones 7, 8 y 9 del enunciado y a esta exigencia: "las métricas
cuantitativas deberán obtenerse mediante instrumentos de medición; los criterios cualitativos deberán evaluarse
mediante reglas explícitas y verificables".

Cada criterio termina en un **puntaje de 0 a 100** por lenguaje.

| Criterio | Peso | Tipo de puntaje | Sección |
|---|---|---|---|
| Tiempo de ejecución | 25 % | Proporcional al mejor | 2 |
| Consumo de memoria | 20 % | Proporcional al mejor | 2 |
| Rendimiento | 20 % | Proporcional al mejor | 2 |
| Calidad de código | 15 % | Proporcional al mejor | 3 |
| Confiabilidad | 10 % | Absoluto (% de pruebas superadas) | 4 |
| Uso funcional | 10 % | Mixto: mitad absoluto, mitad proporcional | 5 |

## 1. Dos tipos de puntaje

**Proporcional al mejor.** Se usa en las métricas sin un máximo natural (milisegundos, MB, líneas).
- Si menor es mejor: `puntaje = 100 · mejor / valor`.
- Si mayor es mejor: `puntaje = 100 · valor / mejor`.
- **Conteos que pueden valer 0** (líneas duplicadas): `puntaje = 100 · (mejor + 1) / (valor + 1)`. Se suma 1
  arriba y abajo para no dividir entre cero.
- **Por qué no se escala entre el peor y el mejor:** esa fórmula le da 0 al último lugar aunque esté a un 1 %
  del primero. Con solo tres lenguajes exageraría las diferencias.

**Absoluto.** Se usa en los criterios que ya son un porcentaje de reglas o pruebas cumplidas: el puntaje es
ese porcentaje.

## 2. Tiempo, memoria y rendimiento

1. Para cada lenguaje y escenario (V1, V2, V3, V4, C1, X1) se toma la **mediana de las 10 rondas** medidas
   (Bloque 3).
2. En cada escenario se calcula el puntaje proporcional al mejor.
3. El puntaje del criterio es el **promedio de los 6 escenarios**, todos con el mismo peso.

| Criterio | Métrica | Mejor |
|---|---|---|
| Tiempo de ejecución | `t_operaciones` (validación + simulación + reportes), en ms | menor |
| Consumo de memoria | Memoria residente máxima del proceso, en MB | menor |
| Rendimiento | Registros del archivo de vuelos ÷ `t_proceso` en segundos (vuelos por segundo) | mayor |

Si un lenguaje no tiene una medición válida en un escenario (no corrió o su salida no fue correcta), recibe
**0** en ese escenario en los tres criterios. El fallo también se refleja en Confiabilidad.

## 3. Calidad de código (15 %)

SonarQube no analiza Clojure. Por eso la calidad se mide con **tres métricas que se calculan igual para los
tres lenguajes**. Cada una vale un tercio y todas se puntúan proporcionalmente al mejor.

| Métrica | Cómo se mide | Herramienta | Mejor |
|---|---|---|---|
| **Q1 · Tamaño** | Líneas de código: sin comentarios ni líneas vacías | `experimento/calidad.py` | menor |
| **Q2 · Complejidad** | Puntos de decisión cada 100 líneas de código | `experimento/calidad.py` | menor |
| **Q3 · Duplicación** | Líneas duplicadas (bloques de 50 o más tokens) | `jscpd` (analiza Java, Scala y Clojure) | menor |

**Qué código se analiza:** todo el código de producción de cada versión, incluido el módulo de Medición. No
se analizan las pruebas.

**Comentarios y textos.** Antes de contar, se eliminan los comentarios y el contenido de las cadenas de texto,
para que una palabra como `if` dentro de un mensaje no cuente:

| | Comentarios | Cadenas |
|---|---|---|
| Java | `// …` y `/* … */` | `"…"` y `"""…"""` |
| Scala | `// …` y `/* … */` | `"…"` y `"""…"""` |
| Clojure | `; …` y `#_` (forma descartada) | `"…"` |

**Puntos de decisión** (Q2). Cuentan las ramas que toman una decisión. La rama por defecto no cuenta, igual
que en la complejidad ciclomática:

| Decisión | Java | Scala | Clojure |
|---|---|---|---|
| Condicional | `if` | `if` | `if`, `if-not`, `if-let`, `if-some`, `when`, `when-not`, `when-let`, `when-some` |
| Una rama por caso | `case` (no cuenta `default`) | `case` dentro de `match` o de una función parcial. No cuentan `case class`, `case object` ni `case _ =>` | `cond`, `condp` y `case`: un punto por cada par prueba/resultado, sin contar `:else` ni el valor por defecto |
| Operador lógico | `&&`, `\|\|` | `&&`, `\|\|` | `and`, `or` |
| Ternario | `? :` | — | — |

**No puntúan, pero se reportan en el informe:**
- las advertencias de cada compilador o analizador: `javac -Xlint:all`, Scala con `-deprecation -feature -Wunused:all`
  y `clj-kondo`;
- los resultados de SonarQube para Java y Scala.

Cada herramienta tiene reglas distintas, así que usarlas en el puntaje favorecería al lenguaje con el
analizador menos estricto.

## 4. Confiabilidad (10 %)

Es el **promedio de tres porcentajes**:

| Parte | Qué se cuenta | Total |
|---|---|---|
| **Correctitud** | Escenarios con salida idéntica a la esperada: E0, V1, V2, V3, V4, C1, X1 | 7 |
| **Robustez** | Casos de error superados (tabla siguiente) | 12 |
| **Estabilidad** | Ejecuciones medidas que terminaron con código 0 y salida correcta (6 escenarios × 10 rondas) | 60 |

**Casos de robustez.** Están en `datos/robustez/`, cada uno con sus salidas esperadas. Un caso se supera
cuando se cumplen las tres condiciones:
1. el código de salida es el esperado;
2. los archivos de salida son idénticos a los esperados (cuando el código es 0);
3. no aparece ningún error de Java (como un `Exception`) en pantalla.

| Caso | Situación | Resultado esperado |
|---|---|---|
| R01 | Sin argumentos | `ERROR:` y código 2 |
| R02 | El archivo de pistas no existe | `ERROR:` y código 2 |
| R03 | Archivo de vuelos vacío (0 bytes, sin encabezado) | Código 0; reportes con "Sin datos" |
| R04 | Los dos archivos tienen solo el encabezado | Código 0; reportes con "Sin datos" |
| R05 | Todos los vuelos son inválidos | Código 0; todos en `errores.csv` |
| R06 | Ninguna pista operativa (todas cerradas) | Todos los vuelos en RF12 con "sin pista habilitada para la operación" |
| R07 | Líneas en blanco y espacios alrededor de los campos | Las líneas en blanco se ignoran y los espacios se quitan |
| R08 | Finales de línea de Windows (`\r\n`) | La misma salida que con `\n` |
| R09 | Campos de más, de menos y una coma final | `se esperaban N campos y hay M` |
| R10 | Números límite: 10 dígitos, negativos, `0`, `+5`, `007` | Mensajes del contrato; `007` es válido |
| R11 | Horas límite: `00:00`, `23:59`, `24:00`, `8:5`, `12:60` | Las dos primeras son válidas y el resto no |
| R12 | Tildes y `ñ` en aerolínea y matrícula | Se conservan iguales en las salidas (UTF-8) |

## 5. Uso funcional (10 %)

Se revisa el código fuente con `experimento/funcional.py`. Las comprobaciones son las mismas en los tres
lenguajes; solo cambia cómo se escribe cada cosa.

**Mitad A · Restricciones (50 %, absoluto).** Son 4 reglas de 12,5 puntos cada una. **Una sola violación
anula la regla.** Comentarios y textos se excluyen igual que en la sección 3.

| Regla | Java: cuenta como violación | Scala | Clojure |
|---|---|---|---|
| **F1 · Sin ciclos** | `for`, `while`, `do` | `for`, `while`, `do` | `loop`, `doseq`, `dotimes`, `while`, `for` |
| **F2 · Sin reasignación** | `++`, `--`, `+=`, `-=`, `*=`, `/=`, `%=`; una línea que empieza con `variable = …` sin tipo delante | `var` | `atom`, `swap!`, `reset!`, `set!`, `ref`, `alter`, `volatile!`, `vswap!` |
| **F3 · Sin colecciones mutables** | `new ArrayList`, `new LinkedList`, `new HashMap`, `new TreeMap`, `new HashSet`, `new ArrayDeque`, `new PriorityQueue`, `StringBuilder`, `.add(`, `.put(`, `.remove(`, `.set(`, `.clear(`, `.append(`, asignar a una posición de un arreglo | `scala.collection.mutable`, `ArrayBuffer`, `ListBuffer`, `StringBuilder`, `Array(`, `.update(` | `transient`, `conj!`, `assoc!`, `java.util.ArrayList`, `java.util.HashMap`, `StringBuilder`, `aset` |
| **F4 · Sin excepciones** | `try`, `catch`, `throw` (se permite `throws` en la firma de `main`) | `try`, `catch`, `throw`, `Try(` | `try`, `catch`, `throw`, `ex-info` |

**Mitad B · Densidad funcional (50 %, proporcional al mejor).** Es el número de operaciones funcionales cada
100 líneas de código. Mide cuánto del código es estilo funcional y cuánto es código que el lenguaje obliga a
escribir para lograrlo. Es la "adaptación funcional" del enunciado. Se cuentan solo estas operaciones:

| Categoría | Java | Scala | Clojure |
|---|---|---|---|
| Transformar | `.map(`, `.flatMap(`, `.mapToInt(`, `.mapToLong(`, `.mapToDouble(`, `.mapToObj(` | `.map`, `.flatMap`, `.collect` | `map`, `mapcat`, `keep`, `map-indexed` |
| Filtrar | `.filter(` | `.filter`, `.filterNot`, `.partition` | `filter`, `remove` |
| Reducir | `.reduce(`, `.collect(`, `.sum(`, `.count(`, `.max(`, `.min(` | `.foldLeft`, `.fold`, `.reduce`, `.reduceOption`, `.sum`, `.count`, `.max`, `.min`, `.maxBy`, `.minBy` | `reduce`, `frequencies`, `count`, `max-key`, `min-key`, `apply` |
| Agrupar | `groupingBy(`, `partitioningBy(` | `.groupBy`, `.groupMapReduce` | `group-by`, `partition-by` |
| Ordenar | `.sorted(`, `Comparator.comparing` | `.sortBy`, `.sortWith`, `.sorted` | `sort`, `sort-by` |
| Buscar | `.findFirst(`, `.anyMatch(`, `.allMatch(`, `.noneMatch(` | `.find`, `.exists`, `.forall` | `some`, `every?`, `not-any?` |
| Secuencias | `Stream.iterate(`, `.takeWhile(`, `.limit(`, `.skip(` | `Iterator.iterate`, `.takeWhile`, `.take`, `.drop`, `.zip` | `iterate`, `take-while`, `take`, `drop`, `interleave` |
| Composición | `.andThen(`, `.compose(` | `andThen`, `compose` | `comp`, `partial`, `juxt` |
| Opcionales | `Optional`: `.map(` ya contado, `.orElse(`, `.orElseGet(` | `.getOrElse`, `.orElse` | `some->`, `fnil` |

`densidad = operaciones contadas · 100 / líneas de código (Q1)`

**Uso funcional = restricciones (0 a 50) + densidad (0 a 50).**

## 6. Clasificación automática

```
Puntaje final = 0,25·Tiempo + 0,20·Memoria + 0,20·Rendimiento + 0,15·Calidad + 0,10·Confiabilidad + 0,10·Uso funcional
```

- Los lenguajes se ordenan de mayor a menor puntaje final.
- **Desempate:** primero el mayor puntaje de Tiempo y luego el de Memoria.
- **Salidas** de `experimento/clasificar.py` (Bloque 7):
  - `resultados/consolidado.csv`: cada métrica en bruto y cada puntaje, por lenguaje y criterio;
  - `resultados/clasificacion.md`: la tabla de posiciones y, para cada lenguaje, un texto generado que explica su
    posición (en qué criterios ganó, en cuáles perdió y por cuánto);
  - `resultados/graficos/`: los gráficos del informe.
- **Prueba de solidez:** la clasificación se recalcula con **pesos iguales** (1/6 cada uno) y **quitando un
  criterio a la vez** (6 variantes, repartiendo su peso entre los demás). Se informa en cuántas de las 7
  variantes gana el mismo lenguaje. Si gana en todas, el resultado no depende de los pesos elegidos.

## 7. Ejemplo numérico

**Los números son inventados** y solo ilustran el cálculo. Se usan letras para no anticipar resultados.

**Paso 1 · Puntaje proporcional en un escenario.**

| | Tiempo (ms) | Puntaje | Memoria (MB) | Puntaje | Rendimiento (vuelos/s) | Puntaje |
|---|---|---|---|---|---|---|
| A | 400 | 100·320/400 = **80,0** | 300 | **100** | 150.000 | 100·150/165 = **90,9** |
| B | 320 | **100** | 340 | 100·300/340 = **88,2** | 165.000 | **100** |
| C | 520 | 100·320/520 = **61,5** | 420 | 100·300/420 = **71,4** | 110.000 | 100·110/165 = **66,7** |

**Paso 2 · Puntaje final** (en este ejemplo se supone que todos los escenarios dieron lo mismo):

| | Tiempo | Memoria | Rendimiento | Calidad | Confiabilidad | Uso funcional | **Final** |
|---|---|---|---|---|---|---|---|
| A | 80,0 | 100 | 90,9 | 78,0 | 100 | 81,0 | **87,98** |
| B | 100 | 88,2 | 100 | 91,0 | 100 | 93,0 | **95,60** |
| C | 61,5 | 71,4 | 66,7 | 96,0 | 96,7 | 100 | **77,07** |

Cálculo de B: 0,25·100 + 0,20·88,2 + 0,20·100 + 0,15·91 + 0,10·100 + 0,10·93 = **95,60**.

**Clasificación:** 1.º B · 2.º A · 3.º C.

**Prueba de solidez:** B gana con pesos iguales (95,37) y en las 6 variantes sin un criterio. Gana en **7 de
7**, así que la decisión es sólida.

**Lectura del ejemplo:**
- C tiene la mejor calidad y el mejor uso funcional, pero pierde por rendimiento.
- Los criterios cuantitativos pesan 65 %, así que el lenguaje más rápido y eficiente tiene ventaja aunque no
  sea el más funcional.
- Este tipo de conclusión es la que pide la condición 10.
