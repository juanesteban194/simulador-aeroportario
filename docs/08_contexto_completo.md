# Contexto completo del proyecto · Simulador de operaciones aeroportuarias en Java, Scala y Clojure

> **Para el asistente que lea este documento.** Contiene toda la información del proyecto final de
> Lenguajes y Paradigmas: el enunciado, la teoría que lo sustenta, el diseño, el código completo de las tres
> versiones, el experimento, las fórmulas, los resultados y las decisiones con sus razones. Úsalo como
> **fuente de verdad** para responder preguntas de teoría y de la sustentación:
> - Responde en español y con base en este documento. Cuando expliques teoría general (por ejemplo, qué es la
>   compilación JIT), relaciónala con lo que se hizo en el proyecto.
> - Distingue entre **lo que el equipo hizo y midió** (datos de este documento) y **explicaciones
>   probables** de los resultados (están marcadas como tales). No inventes cifras: todas están aquí.
> - Si algo no está en el documento, dilo en lugar de suponerlo.
> - El código completo de las tres versiones está en los Anexos A, B y C; los datos del ejemplo y los
>   resultados detallados, en los Anexos D a F.

## Índice

1. Ficha del proyecto
2. El enunciado del profesor
3. Método de trabajo y decisiones
4. El problema: dominio, reglas y requisitos
5. El contrato común (entradas, salidas, formatos)
6. Arquitectura: módulos y flujo
7. El algoritmo de la torre de control (teoría y demostración)
8. Teoría de programación funcional aplicada
9. Los tres lenguajes: teoría y cómo se usó cada uno
10. Teoría de la JVM necesaria para entender los resultados
11. Diseño del experimento (teoría experimental)
12. Criterios, fórmulas y clasificación automática
13. Herramientas y scripts del proyecto
14. Resultados completos e interpretación
15. Conclusión técnica y limitaciones
16. Entorno de medición, desviaciones y problemas resueltos
17. Estructura del repositorio y de la entrega
18. Cómo ejecutar todo
19. Preguntas frecuentes de la sustentación (con respuestas)
20. Glosario
- Anexo A · Código completo de Java
- Anexo B · Código completo de Scala
- Anexo C · Código completo de Clojure
- Anexo D · Ejemplo resuelto a mano: entradas y salidas esperadas
- Anexo E · Resultados detallados (medianas por etapa y puntajes por escenario)
- Anexo F · Archivos de configuración y construcción

---

## 1. Ficha del proyecto

| Campo | Valor |
|---|---|
| Curso | Lenguajes y Paradigmas de Programación · Universidad de Medellín · semestre 2026-2 |
| Profesor | Juan Guillermo ("JuanGui") |
| Trabajo | Final "Comparativo – Lenguajes – PF" |
| Equipo | Sebastián Villa · Miguel Guarnizo · Juan Esteban Echavarría |
| Proyecto de clase elegido | 2. Simulador de operaciones aeroportuarias |
| Lenguajes | Java 21, Scala 3.9.0 y Clojure 1.12.0, los tres sobre la JVM (JDK 21) |
| Repositorio | https://github.com/juanesteban194/simulador-aeroportario (público; antes `simulador-aeroportario-`) |
| Resultado | **1.º Java (93,35)** · 2.º Scala (91,45) · 3.º Clojure (75,65) |
| Correctitud | Las tres versiones producen archivos idénticos byte a byte en los 19 casos de verificación |
| Reparto en la sustentación | Sebastián: Java y experimento · Juan Esteban: introducción, diseño, Scala y conclusión · Miguel: Clojure y resultados |

**Resumen en un párrafo.** Se implementó el mismo simulador de operaciones aeroportuarias en Java, Scala y
Clojure, con programación funcional estricta (sin ciclos, sin reasignación, sin colecciones mutables y sin
excepciones). Un contrato común obliga a las tres versiones a producir salidas idénticas byte a byte. Con esa
base se diseñó un experimento con 6 escenarios (1.000 a 1.000.000 de vuelos, uno saturado y uno con 10 % de
errores) y 12 casos de robustez. Cada escenario se ejecutó en 1 ronda de calentamiento y 10 medidas, con el
orden de los lenguajes rotado. Un clasificador automático calcula seis criterios ponderados (tiempo 25 %,
memoria 20 %, rendimiento 20 %, calidad 15 %, confiabilidad 10 %, uso funcional 10 %). Java gana por su
velocidad y rendimiento; Scala queda a 1,9 puntos con el código más corto y más funcional; Clojure queda tercero
por su arranque y su tipado dinámico.

---

## 2. El enunciado del profesor

**Propósito:** implementar el proyecto definido en clase en Java, Scala y un tercer lenguaje, de forma
funcionalmente equivalente. No se trata solo de tener tres programas, sino de **diseñar y ejecutar un proceso
experimental** que obtenga métricas reales, compare resultados y **determine automáticamente** cuál lenguaje
se comporta mejor para el problema. Base: los principios de programación funcional del semestre. Al final se
debe demostrar con evidencia cuantitativa y análisis técnico cuál alternativa es más conveniente.

**Condiciones (1 a 10):**
1. Implementar el proyecto en Java, Scala y un tercer lenguaje.
2. Garantizar los mismos requisitos funcionales y resultados equivalentes en las tres implementaciones.
3. Incorporar funciones de orden superior, expresiones lambda, transformación, filtrado, agrupación,
   reducción y otras operaciones funcionales pertinentes.
4. Diseñar escenarios de prueba para diferentes volúmenes de información o cargas de trabajo.
5. Implementar mecanismos para medir y registrar el comportamiento de cada solución.
6. Ejecutar pruebas bajo condiciones equivalentes para los tres lenguajes.
7. Consolidar los resultados en una estructura que permita compararlos.
8. Implementar un mecanismo que determine automáticamente el lenguaje con mejores resultados.
9. Presentar una clasificación con las métricas que justifican cada posición.
10. Generar una conclusión técnica sobre ventajas y limitaciones identificadas.

**Criterios y pesos (definidos por el profesor):**

| Criterio | Descripción del enunciado | Peso |
|---|---|---|
| Tiempo de ejecución | Duración de las operaciones | 25 % |
| Consumo de memoria | Memoria utilizada durante la ejecución | 20 % |
| Rendimiento | Operaciones procesadas por unidad de tiempo | 20 % |
| Calidad de código | Evaluación de calidad de código | 15 % |
| Confiabilidad | Correctitud y manejo de errores | 10 % |
| Uso funcional | Adaptación funcional | 10 % |

Exigencia textual: "Las métricas cuantitativas deberán obtenerse mediante instrumentos de medición; los
criterios cualitativos deberán evaluarse mediante reglas explícitas y verificables."

**Entregables (11 a 16):**
11. Tres proyectos funcionales con sus códigos fuente.
12. Escenarios de prueba y datos utilizados.
13. Evidencias de rendimiento y consumo de recursos.
14. Mecanismo de consolidación, comparación y clasificación automática.
15. Informe técnico que justifique el lenguaje seleccionado.
16. Sustentación práctica de las soluciones y los resultados.

**Dónde se cumple cada condición:**

| Condición | Cómo se cumple |
|---|---|
| 1 | Carpetas `java/`, `scala/`, `clojure/` con 7 módulos cada una |
| 2 | Contrato común (`docs/02`) y verificación byte a byte con `experimento/verificar.sh`: 19/19 casos en los tres |
| 3 | map, filter, flatMap, groupBy, reduce, sortBy, iterate, takeWhile, Optional/Either, lambdas, composición; reglas F1–F4 verificadas automáticamente |
| 4 | Escenarios V1–V4 (volumen), C1 (carga), X1 (errores), E0 (ejemplo a mano) y R01–R12 (robustez) |
| 5 | Opción `--medir` en los tres programas (tiempo por etapa con `System.nanoTime`) y orquestador `experimento/ejecutar.py` (tiempo de proceso y memoria) |
| 6 | Misma JVM (JDK 21) y opciones (`-Xmx4g -XX:+UseG1GC`), mismos datos, orden rotado, 10 rondas, proceso nuevo por ejecución, mediana |
| 7 | `resultados/crudos/*.csv` (una fila por ejecución), `consolidado.csv`, `puntajes.csv` |
| 8 | `experimento/clasificar.py` |
| 9 | `resultados/clasificacion.md` (con explicación generada de cada posición) e informe técnico |
| 10 | Conclusión del informe técnico y sección 15 de este documento |

---

## 3. Método de trabajo y decisiones

Se trabajó en **9 bloques**. En cada bloque se propusieron opciones, el equipo eligió y se registró la decisión
con su razón en `docs/decisiones.md`. **Primero se documentó qué se iba a construir y cómo se iba a medir; solo
después se programó** (para no adaptar las reglas a los resultados).

| Bloque | Contenido | Documento |
|---|---|---|
| 0 · Marco | Proyecto, tercer lenguaje, repositorio, herramientas | `docs/00_metodo_de_trabajo.md` |
| 1 · Requerimientos | RN01–RN10, RF01–RF14, validaciones, RNF | `docs/01_requerimientos.md` |
| 2 · Modelo y contrato | Entidades, algoritmo, formatos exactos, ejemplo a mano | `docs/02_modelo_y_contrato.md` |
| 3 · Experimento | Escenarios, generador, referencia, métricas, protocolo | `docs/03_experimento.md` |
| 4 · Criterios | Fórmulas de puntaje, desempate, prueba de solidez | `docs/04_criterios.md` |
| 5 · Implementación | Java → Scala → Clojure, 7 módulos, verificación | código y `experimento/verificar.sh` |
| 6 · Medición | Orquestador y 198 ejecuciones | `experimento/ejecutar.py`, `resultados/` |
| 7 · Clasificación | Calidad, uso funcional, puntajes, gráficos | `experimento/*.py`, `resultados/` |
| 8 · Informe y sustentación | Informe Word, documento de estudio, guion | `entrega/`, `docs/06`, `docs/07` |

**Decisiones clave (resumen; detalle en `docs/decisiones.md`):**

| Id | Decisión | Razón |
|---|---|---|
| D0.1 | Proyecto: simulador aeroportuario (entidades Avión, Vuelo, Pista, Aeropuerto, TorreControl; extra: asignación automática de pistas por prioridad y disponibilidad) | Decisión del equipo |
| D0.2 | Tercer lenguaje: **Clojure** (opciones: Python, Racket, Haskell, F#, Clojure) | Funcional de verdad y en la **misma JVM**: mismo JDK, recolector e instrumento de memoria; las diferencias son del lenguaje, no de la plataforma. Consecuencia: SonarQube no analiza Clojure, así que la calidad se mide con métricas propias comunes |
| D0.4 | Un solo repositorio público; copia local fuera de iCloud | iCloud puede dañar la carpeta `.git` |
| D0.5 | JDK 21; Java con `javac`+`jar` (sin Maven); Scala con Scala CLI; Clojure con Leiningen (AOT); todos con `java -jar` | Misma plataforma y forma de lanzar; Clojure AOT evita medir su compilación en cada arranque |
| D1.1 | Simulación **por eventos**, no minuto a minuto | Determinista; el costo depende del número de vuelos, no del tiempo simulado |
| D1.2 | Prioridad: Emergencia > Aterrizaje > hora > código, **entre los que ya esperan** | Un avión en el aire consume combustible; ordenar toda la lista haría que una emergencia de las 18:00 operara antes que un vuelo de las 08:00 |
| D1.4 | Entrada por dos archivos CSV | El experimento necesita miles de vuelos |
| D2.2 | Tres archivos de salida y el reporte en pantalla | Con 1.000.000 de vuelos, imprimir cada operación mediría la consola; la equivalencia se verifica con `diff` byte a byte |
| D2.4 | 12 filas precalculadas, estado inmutable y secuencia perezosa de estados | Mismo resultado que recorrer la cola, mismo costo en los tres, sin recursión profunda |
| D2.5 | Tiempos y sumas en enteros de 64 bits; decimales solo al final con aritmética entera | No depende del orden de las sumas ni de la configuración regional |
| D3.1 | Aeropuerto común de 6 pistas; P03 alargada a 2.900 m en la calibración | Con una sola pista para despegues pesados, P01 quedaba al 97 % (cuello de botella) |
| D3.2 | Generador con semilla fija y solo `random.random()` | Misma secuencia en todas las versiones de Python ≥ 3.2; archivos verificables con SHA-256 |
| D3.4 | `java -Xmx4g -XX:+UseG1GC -jar`; proceso nuevo; 1 calentamiento + 10 medidas; orden rotado; mediana | Condiciones equivalentes y medición robusta |
| D3.6 | Implementación de referencia en Python (no compite) | Sin ella no se sabría cuál de dos versiones está mal |
| D4.1 | Puntaje proporcional al mejor, promedio de 6 escenarios | Escalar entre peor y mejor le daría 0 al último aunque esté a 1 % |
| D4.2 | Calidad = líneas, decisiones cada 100 líneas, duplicación; SonarQube solo se reporta | Únicas métricas con la misma regla en los tres lenguajes |
| D5.1 | Orden de implementación: Java → Scala → Clojure | Java solo necesita el JDK y se pudo verificar mientras se escribía |
| D5.3 | Unicidad sin estado ("dueño" de cada código = primer registro sin otros errores) | Cumple F1–F4 sin variables |
| D6.7 | Medición en un contenedor Linux con los `.jar` del Mac | No se pudo lanzar en el Mac de forma desatendida (ver sección 16) |
| D6.8 | Corrección de la medición de memoria | El orquestador inflaba `ru_maxrss` (ver sección 16) |
| D7.2–D7.3 | Precisiones de conteo para que la misma operación cuente igual en los tres lenguajes | Equidad de las reglas |

---

## 4. El problema: dominio, reglas y requisitos

Un aeropuerto tiene varias pistas. La **torre de control** recibe la programación de despegues y aterrizajes de
uno o varios días y debe: ordenar las operaciones, asignar automáticamente cada vuelo a una pista compatible y
libre según su prioridad, calcular el retraso de cada vuelo y generar reportes.

### 4.1 Entidades (todas inmutables)

| Entidad | Qué representa | Datos |
|---|---|---|
| Avión | La aeronave | Matrícula, categoría (Ligero, Mediano, Pesado) |
| Vuelo | Una operación programada | Código, aerolínea, avión, operación (Despegue/Aterrizaje), día y hora programados (como minuto absoluto), prioridad (Normal/Emergencia) |
| Pista | Una pista del aeropuerto | Identificador, longitud en metros, uso (Despegue/Aterrizaje/Mixta), estado (Operativa/Cerrada) |
| Aeropuerto | Estado de la simulación en un minuto | Minuto actual, posición del primer vuelo pendiente de cada fila ("cabezas"), minuto en que se libera cada pista ("libres"), operaciones asignadas en el paso |
| TorreControl | Las reglas de operación | Funciones puras: reciben un Aeropuerto y devuelven uno nuevo |
| OperacionAsignada | Resultado | Vuelo, pista, inicio y fin reales; retraso = inicio − programado |
| NoAsignable | Vuelo sin pista posible | Vuelo y motivo |

### 4.2 Reglas de negocio (RN)

| RN | Regla |
|---|---|
| RN01 · Tiempo | Minutos enteros. Una hora es día (1, 2, 3…) + HH:MM. Minuto absoluto = (día − 1)·1440 + HH·60 + MM |
| RN02 · Categorías | Ligero: pista ≥ 1.200 m, ocupa 2 min. Mediano: ≥ 2.000 m, 3 min. Pesado: ≥ 2.800 m, 4 min |
| RN03 · Compatibilidad | La pista está Operativa **y** su uso es Mixta o igual a la operación **y** su longitud ≥ la exigida por la categoría |
| RN04 · Espera | Un vuelo entra a la cola en su hora programada; antes no puede operar |
| RN05 · Prioridad | Entre los que esperan: Emergencia antes que Normal; Aterrizaje antes que Despegue; hora programada más temprana; código menor (orden alfabético) |
| RN06 · Asignación automática (extra) | En cada minuto con pistas libres y vuelos esperando, se recorre la cola en orden RN05; cada vuelo con pista libre y compatible recibe la de **identificador menor**. El vuelo de mayor prioridad que no tenga pista libre compatible **no bloquea** a los demás |
| RN07 · Ocupación | Una pista queda ocupada desde el inicio real hasta inicio + minutos de la categoría |
| RN08 · Retraso | Retraso = inicio real − hora programada (nunca negativo). Retrasado si > 15 min |
| RN09 · No asignable | Si ninguna pista del aeropuerto es compatible, el vuelo no entra a la cola. Motivo: si no hay pista operativa habilitada para su operación → "sin pista habilitada para la operación"; si la hay pero ninguna es suficientemente larga → "sin pista con longitud suficiente" |
| RN10 · Determinismo | Sin números aleatorios ni hora del sistema: mismas entradas, misma salida en los tres lenguajes |

### 4.3 Requisitos funcionales (RF)

| RF | Descripción |
|---|---|
| RF01 | Cargar pistas desde archivo (id, longitud, uso, estado) |
| RF02 | Cargar vuelos desde archivo (código, aerolínea, matrícula, categoría, operación, día, hora, prioridad) |
| RF03 | Validar cada registro; un inválido se reporta con su línea y motivo y se excluye; el programa nunca se detiene por un dato inválido |
| RF04 | Construir la cola de espera ordenada (RN04, RN05) |
| RF05 | Asignar automáticamente pista libre y compatible (RN03, RN06, RN07) |
| RF06 | Calcular inicio real, fin y retraso (RN08) |
| RF07 | Programa final de operaciones en orden de asignación |
| RF08 | Resumen de retrasos: promedio, máximo, % de retrasados (> 15 min) |
| RF09 | Los 5 vuelos más retrasados (empate: por código) |
| RF10 | Uso de cada pista: operaciones, minutos ocupada, % de ocupación; período = primera hora programada asignada hasta el fin de la última operación |
| RF11 | Retraso promedio por aerolínea, de mayor a menor (empate: por nombre) |
| RF12 | Vuelos no asignables con su motivo |
| RF13 | Operaciones por tipo (Aterrizaje, Despegue) y por categoría (Ligero, Mediano, Pesado) |
| RF14 | Resumen ejecutivo: cargados, válidos, inválidos, asignados, no asignables, retraso promedio, % retrasados, pista más usada, aerolínea con mayor retraso promedio |

### 4.4 Validaciones (RF03)

| Archivo | Campo | Regla |
|---|---|---|
| Pistas | id | No vacío y no repetido |
| Pistas | longitud | Entero > 0 |
| Pistas | uso | Despegue, Aterrizaje o Mixta |
| Pistas | estado | Operativa o Cerrada |
| Vuelos | código | No vacío y no repetido |
| Vuelos | aerolínea, matrícula | No vacías |
| Vuelos | categoría | Ligero, Mediano o Pesado |
| Vuelos | operación | Despegue o Aterrizaje |
| Vuelos | día | Entero entre 1 y 9999 |
| Vuelos | hora | HH:MM de 00:00 a 23:59, con 2 dígitos |
| Vuelos | prioridad | Normal o Emergencia |
| Ambos | registro | Exactamente el número de campos esperado (4 pistas, 8 vuelos) |

Casos límite: sin pistas válidas, sin vuelos válidos o archivo vacío → el programa lo informa y los reportes
dicen "Sin datos"; nunca divide entre cero ni se detiene.

### 4.5 Requisitos no funcionales (RNF)

| RNF | Requisito |
|---|---|
| RNF01 | Las tres versiones cumplen los mismos RF y producen la misma salida, verificada carácter por carácter |
| RNF02 | Programación funcional: sin `for`, `while` ni variables mutables; funciones de orden superior, lambdas, map, filter, groupBy, reduce/fold |
| RNF03 | Errores como valores (Optional/Either, Option/Either, mapas de resultado); las validaciones no lanzan excepciones |
| RNF04 | Solo la biblioteca estándar de cada lenguaje |
| RNF05 | Los tres se ejecutan con `java -jar` sobre el mismo JDK 21; Clojure compilado por adelantado (AOT) |
| RNF06 | Cada versión mide y registra su comportamiento (tiempo por etapa) |
| RNF07 | Números con 2 decimales y el mismo formato en los tres, sin depender de la configuración regional |

---

## 5. El contrato común (entradas, salidas, formatos)

El contrato (`docs/02_modelo_y_contrato.md`) fija todo lo que podría salir distinto entre lenguajes. Con él,
"equivalentes" significa **archivos idénticos byte a byte**, comprobable con `cmp` o `diff`.

### 5.1 Ejecución y códigos de salida

```
java -jar simulador-<lenguaje>.jar <pistas.csv> <vuelos.csv> <carpeta_salida> [--medir <archivo>]
```

| Situación | Comportamiento | Código |
|---|---|---|
| Ejecución normal (aunque haya registros inválidos) | Escribe los 3 archivos y muestra `reporte.txt` en pantalla | 0 |
| Argumentos incorrectos (no son 3, o 5 con `--medir` en la 4.ª posición), o un archivo de entrada no existe o no se puede leer | Muestra `ERROR: <motivo>` y la línea de uso; no escribe archivos | 2 |

Motivos exactos: `número de argumentos incorrecto` o `no se puede leer el archivo <ruta>`. Línea de uso:
`Uso: java -jar simulador-<lenguaje>.jar <pistas.csv> <vuelos.csv> <carpeta_salida> [--medir <archivo>]`.
El error de uso se detecta **antes** de leer (se revisa que el archivo exista y sea legible), así no se
necesita capturar excepciones.

### 5.2 Archivos de entrada

Reglas comunes:
1. UTF-8. Un byte inválido no detiene el programa: se reemplaza por `�` (U+FFFD). Se acepta `\n` y `\r\n`
   (el `\r` desaparece con el `trim`).
2. La línea 1 es el encabezado y no se valida.
3. Las líneas vacías después del `trim` se ignoran y no cuentan como registro.
4. Separación por comas **conservando campos vacíos**, incluidos los del final (`a,b,` tiene 3 campos):
   `split(",", -1)`.
5. `trim` con la definición de la JVM (`String.trim()`): quita los caracteres ≤ U+0020. En Clojure se usa
   `(.trim s)` y no `clojure.string/trim`, porque este usa `Character/isWhitespace` (otra definición).
6. Los valores de listas cerradas coinciden exactamente (mayúsculas incluidas): `Mixta` sí, `mixta` no.
7. El número de línea reportado es la línea física (el encabezado es la 1).

`pistas.csv` (4 campos): `id, longitud, uso, estado`. `vuelos.csv` (8 campos):
`codigo, aerolinea, matricula, categoria, operacion, dia, hora, prioridad`.

Definiciones: **entero** = cumple `-?[0-9]{1,9}` (no `+5`, no `1.5`, no más de 9 dígitos; `007` vale 7).
**Hora** = `[0-9]{2}:[0-9]{2}` con horas 00–23 y minutos 00–59. Todos los tiempos internos son enteros de 64
bits.

### 5.3 Validación y mensajes exactos

- Cada registro se valida en el orden de las columnas y solo se reporta **el primer error**.
- Orden: número de campos → clave vacía → clave repetida → demás campos en orden.
- La unicidad se comprueba contra los registros **válidos anteriores**: un registro inválido no reserva su
  código.
- Primero se valida `pistas.csv` y después `vuelos.csv`.

| Regla | Mensaje |
|---|---|
| Número de campos | `se esperaban 4 campos y hay <n>` / `se esperaban 8 campos y hay <n>` |
| Clave | `id vacío` · `id repetido: <v>` · `código vacío` · `código repetido: <v>` |
| Longitud | `longitud no es un entero: <v>` · `longitud debe ser mayor que 0: <v>` |
| Listas | `<campo> con valor no válido: <v> (valores: A/B/C)` para uso, estado, categoría, operación, prioridad |
| Texto vacío | `aerolínea vacía` · `matrícula vacía` |
| Día | `día no es un entero: <v>` · `día debe estar entre 1 y 9999: <v>` |
| Hora | `hora no válida: <v> (formato HH:MM de 00:00 a 23:59)` |

Los mensajes se redactaron sin género gramatical que dependa del campo ("con valor no válido") y sin comas, para
que `errores.csv` no necesite comillas.

### 5.4 Salidas

**`operaciones.csv`** (RF07), en orden de asignación (por minuto de inicio y, dentro del mismo minuto, en el
orden de prioridad en que se asignaron):
```
codigo,aerolinea,operacion,categoria,prioridad,pista,programada,inicio,fin,retraso
```
**`errores.csv`** (RF03): primero pistas y luego vuelos, cada grupo por línea: `archivo,linea,motivo`.
**`reporte.txt`** (RF03 y RF08–RF14): secciones `== RFxx · Título ==` separadas por una línea vacía (texto
completo del ejemplo en el Anexo D).

**Formato de números (RNF07):** decimales con punto y 2 cifras, calculados con **aritmética entera exacta**:
para mostrar `a / b` se calcula `c = (200·a + b) div (2·b)` (centésimas redondeadas HALF_UP) y se escribe
`c div 100` + "." + `c mod 100` con 2 dígitos.
- Por qué funciona: `100·a/b` son las centésimas exactas; sumar ½ y truncar redondea "mitad hacia arriba":
  `⌊100a/b + 1/2⌋ = ⌊(200a + b) / 2b⌋`.
- Por qué no `double`: los formateadores de cada lenguaje y la configuración regional podrían dar resultados
  distintos (`1,56` frente a `1.56`, o un redondeo distinto en casos como 0,125).

Horas como `D<día> HH:MM` (el minuto 1.935 es `D2 08:15`). Promedio = suma/cantidad; porcentaje =
100·parte/total. **RF11 compara fracciones exactas** por multiplicación cruzada: `a/b > c/d ⇔ a·d > c·b`. El
orden de textos es `compareTo` de la JVM (unidades UTF-16), igual en los tres.

| Sección | Regla | Sin datos |
|---|---|---|
| RF03 | Registros, válidos e inválidos por archivo | — |
| RF08 | Asignadas, promedio, máximo, retrasados y % | `Sin datos` |
| RF09 | Top 5 por retraso descendente; empate por código | `Sin datos` |
| RF10 | Período y todas las pistas válidas por id (también las cerradas) | `Sin datos` |
| RF11 | Promedio por aerolínea descendente; empate por nombre | `Sin datos` |
| RF12 | No asignables en el orden del archivo | `Ninguno` |
| RF13 | Aterrizaje, Despegue, Ligero, Mediano, Pesado (siempre, con ceros) | — |
| RF14 | Totales; pista más usada (más operaciones, empate id menor); aerolínea con mayor promedio (la primera de RF11) | `Sin datos` |

### 5.5 Ejemplo resuelto a mano (E0)

Pistas válidas: P01 2.600 m Mixta Operativa; P02 2.200 m Despegue; P03 1.500 m Aterrizaje; P04 3.500 m
Aterrizaje **Cerrada**; P05 inválida (`abc`). Compatibilidades: aterrizaje Ligero → P01 o P03; aterrizaje
Mediano → solo P01; despegue Ligero/Mediano → P01 o P02; Pesado → ninguna (P01 mide 2.600 < 2.800 y P04 está
cerrada) → AV108 va a RF12 con "sin pista con longitud suficiente" (sí hay pista habilitada para aterrizar).

| Minuto | Esperando (orden RN05) | Pistas libres | Asignación |
|---|---|---|---|
| 08:00 | AV101 (aterrizaje mediano), LA202 (despegue mediano) | P01 P02 P03 | AV101 → P01 (08:00–08:03); LA202 → P02 (08:00–08:03) |
| 08:01 | **CM304 (emergencia)**, AV103 (aterrizaje ligero) | P03 | CM304 solo puede usar P01 (ocupada) y espera; **no bloquea**: AV103 → P03 (08:01–08:03) |
| 08:02 | CM304, AV105, LA206 | ninguna | — |
| 08:03 | CM304, CM307, AV105, LA206 | P01 P02 P03 | CM304 → P01 (retraso 2); CM307 espera P01; AV105 → P02 (retraso 1; empata a las 08:02 con LA206 y gana por código); LA206 espera |
| 08:04 | CM307, LA206, LA209 | P03 | Ninguno puede usar P03 |
| 08:06 | CM307, LA206, LA209 | P01 P02 P03 | CM307 → P01 (retraso 3); LA206 → P02 (retraso 4); LA209 espera |
| 08:08 | LA209 | P02 P03 | LA209 → P02 (retraso 4) |
| 08:20 | LA213 | todas | LA213 → P01 (retraso 0; P01 es el id menor entre P01 y P03) |

Resultado: 9 operaciones; retrasos 0,0,0,2,1,3,4,4,0 → promedio 14/9 = **1,56 min**; máximo 4; 0 retrasados.
Período 08:00–08:22 (22 min): P01 11 min (50,00 %), P02 11 min (50,00 %), P03 2 min (9,09 %), P04 0.
Errores: P05 (`longitud no es un entero: abc`), CM310 (`Jumbo`), el segundo AV101 (`código repetido`) y AV112
(`hora no válida: 8:10`). Este ejemplo se calculó a mano y es la primera prueba de las tres versiones.

---

## 6. Arquitectura: módulos y flujo

Las tres versiones tienen **los mismos 7 módulos y los mismos nombres de funciones**, para comparar módulo por
módulo y que cada integrante pueda explicar cualquier versión.

| # | Módulo | Responsabilidad | Java | Scala | Clojure |
|---|---|---|---|---|---|
| 1 | Modelo | Entidades, listas cerradas, tipos de resultado | `Modelo.java` | `Modelo.scala` | `modelo.clj` |
| 2 | Lectura | Archivo → líneas → registros (línea + campos) | `Lectura.java` | `Lectura.scala` | `lectura.clj` |
| 3 | Validación | Registro → dato válido o error (RF03) | `Validacion.java` | `Validacion.scala` | `validacion.clj` |
| 4 | TorreControl | Compatibilidad, no asignables, simulación (RF04–RF06) | `TorreControl.java` | `TorreControl.scala` | `torre_control.clj` |
| 5 | Reportes | Texto de los 3 archivos (RF07–RF14) | `Reportes.java` | `Reportes.scala` | `reportes.clj` |
| 6 | Medición | Tiempo por etapa y `--medir` | `Medicion.java` | `Medicion.scala` | `medicion.clj` |
| 7 | Main | Argumentos y encadenamiento de etapas | `Main.java` | `Main.scala` | `main.clj` |

**Flujo de 5 etapas (cada una medida por separado):**

```
pistas.csv, vuelos.csv
   │ 1. lectura      → listas de líneas (bytes → UTF-8 → split por "\n")
   │ 2. validación   → registros → Resultado (Ok/Falla) → pistas válidas, vuelos válidos, errores
   │ 3. simulación   → no asignables + asignables → 12 filas → secuencia de estados → operaciones
   │ 4. reportes     → texto de operaciones.csv, errores.csv y reporte.txt (en memoria)
   │ 5. escritura    → crea la carpeta, escribe los 3 archivos y muestra el reporte
   ▼
operaciones.csv, errores.csv, reporte.txt (+ archivo de --medir)
```

**Patrón "núcleo funcional, cáscara imperativa"** (functional core, imperative shell): toda la lógica
(validar, simular, reportar) son funciones puras sobre datos inmutables; los efectos (leer y escribir
archivos, imprimir, salir con código 2, leer el reloj) están concentrados en Lectura, Main y Medición.

---

## 7. El algoritmo de la torre de control (teoría y demostración)

### 7.1 Simulación por eventos discretos

Hay dos formas de simular el tiempo:
- **Paso fijo (minuto a minuto):** se avanza de 1 en 1 aunque no pase nada. V4 cubre 668 días = 961.920
  minutos, la mayoría sin eventos.
- **Eventos discretos (elegida):** el tiempo salta directamente al siguiente instante en que algo cambia: llega
  un vuelo o se libera una pista. El costo depende del número de eventos (como mucho dos por vuelo), no de la
  duración simulada.

### 7.2 Preparación

1. `noAsignables` y `asignables`: se aplica RN09 a cada vuelo válido.
2. Los asignables se agrupan en **12 filas** por (operación × categoría × prioridad) = 2 × 3 × 2.
3. Cada fila se ordena por (minuto programado, código).
4. Las pistas operativas se ordenan por id.

**Por qué 12 filas dan el mismo resultado que recorrer la cola completa (RN06).** Todos los vuelos de una fila
tienen la misma operación y categoría, por lo tanto son compatibles con exactamente las mismas pistas. Dentro de
la fila, el orden (hora, código) coincide con el orden de RN05, porque prioridad y operación son iguales en toda
la fila. Si el primer vuelo de una fila no tiene pista libre compatible, ningún otro de su fila la tiene. Y si
sí la tiene, ningún otro de su fila puede tener más prioridad que él. Por eso el candidato de mayor prioridad
entre todos los vuelos que esperan está siempre entre los primeros de cada fila. Mirando solo 12 candidatos por
asignación se obtiene exactamente la misma elección que recorriendo toda la cola en orden RN05.

### 7.3 Estado inmutable

`Aeropuerto(minuto, cabezas, libres, asignadasEnElPaso)`:
- `minuto`: el instante actual.
- `cabezas`: 12 enteros; la posición del primer vuelo pendiente de cada fila (los vuelos no se borran de la
  fila: se avanza un índice).
- `libres`: por cada pista operativa, el minuto en que queda libre (0 al inicio).
- `asignadasEnElPaso`: operaciones asignadas en este paso.

Estado inicial: minuto = la hora programada más temprana entre los primeros de cada fila; cabezas en 0; pistas
libres desde 0; sin asignaciones.

### 7.4 Un paso (función pura Aeropuerto → Aeropuerto)

1. **Candidatos:** para cada fila con vuelos pendientes, su primer vuelo si su hora programada ≤ minuto.
2. Para cada candidato se busca la **pista libre compatible de menor id** (`libre ≤ minuto` y RN03).
3. Entre los que tienen pista, se elige el de mayor prioridad RN05 (emergencia, aterrizaje, hora, código).
4. Se asigna: inicio = minuto, fin = minuto + ocupación (RN02); la pista queda libre en `fin`; la cabeza de su
   fila avanza 1.
5. Se repite 1–4 **en el mismo minuto** hasta que no haya candidato (recursión; profundidad máxima = número de
   pistas, porque cada asignación ocupa una pista).
6. **Siguiente minuto:** el menor entre (a) los `libres` mayores que el minuto actual y (b) las horas
   programadas de los primeros de cada fila mayores que el minuto actual. Si no hay ninguno, se queda igual (y
   el siguiente estado será terminado).

**Fin:** un estado está terminado si **no quedan vuelos pendientes en ninguna fila y su paso no asignó nada**.
Así el último paso que sí asignó operaciones queda incluido en el resultado.

### 7.5 La simulación como secuencia perezosa

La simulación completa no usa ciclos: es una secuencia (potencialmente infinita y perezosa) de estados:
`iterate(paso)` genera `inicial, paso(inicial), paso(paso(inicial)), …`; `takeWhile(no terminado)` la corta;
`flatMap` concatena las operaciones de cada paso.

| Java | Scala | Clojure |
|---|---|---|
| `Stream.iterate(inicial, a -> !terminado(a, filas), a -> paso(a, filas, operativas)).flatMap(a -> a.asignadasEnElPaso().stream()).toList()` | `Iterator.iterate(inicial)(a => paso(a, todas, operativas)).takeWhile(a => !terminado(a, todas)).flatMap(_.asignadasEnElPaso).toVector` | `(into [] (comp (take-while #(not (terminado? % filas))) (mapcat :asignadas-en-el-paso)) (iterate #(paso % filas operativas) inicial))` |

Java usa la variante de 3 argumentos de `Stream.iterate` (semilla, condición, siguiente), equivalente a
`iterate` + `takeWhile`. Clojure usa **transductores** (`comp` de `take-while` y `mapcat`) aplicados con `into`
sobre `iterate`, que es reducible y se detiene cuando `take-while` señala `reduced`.

### 7.6 Complejidad

- Ordenar las filas: O(n log n).
- Cada evento: trabajo constante, porque hay 12 filas y 5 pistas operativas (k).
- Eventos: como máximo 2 por vuelo (llegada y liberación de pista).
- Total: O(n log n) para ordenar más O(n·k) para simular, en la práctica lineal. V4 tiene 10 veces más vuelos
  que V3 y tarda unas 5 veces más (Java: 12.047 frente a 2.419 ms): el crecimiento no supera lo lineal, y es
  menor que 10× porque el costo fijo de arranque y calentamiento del JIT se reparte entre más datos.
- Recursión: solo dentro de un minuto, con profundidad ≤ k (5). Importa porque **Java no optimiza la recursión de
  cola**; Scala usa `@tailrec` (se compila como salto) y Clojure `recur`.

### 7.7 Validación sin estado: el "dueño" de cada código

Requisito: un registro está repetido si un registro **válido** anterior tiene el mismo código. La forma
imperativa recorre el archivo con un conjunto mutable de códigos vistos. La forma funcional usada:
1. Revisar cada registro de forma independiente: error "previo" (número de campos, clave vacía) y error "de
   campos" (las demás reglas).
2. Los registros sin ningún error compiten por su código: el **dueño** es el de menor número de línea (agrupar
   por clave y tomar el mínimo: `Collectors.toMap(..., Math::min)`, `groupMapReduce(...)(_ min _)`,
   `group-by` + `min`).
3. El resultado de cada registro es: error previo, o "repetido" si el dueño de su código tiene una línea menor,
   o error de campos, o válido.

**Por qué es equivalente:** el primer registro (por línea) con un código dado que no tiene errores propios es
válido en el recorrido secuencial, porque antes de él no hay ningún válido con ese código. Todo registro
posterior con ese código queda repetido, y uno anterior con errores propios es inválido por esos errores. El
orden de los mensajes (previo → repetido → campos) reproduce el orden de las columnas, porque la clave es la
columna 1.

---

## 8. Teoría de programación funcional aplicada

### 8.1 Conceptos y dónde aparecen

| Concepto | Definición | En el proyecto |
|---|---|---|
| Inmutabilidad | Un dato no cambia después de creado; "cambiarlo" es crear otro | `record`, `case class`, `defrecord`; listas inmutables (`List.of`, `toList()`, `Vector`, vectores de Clojure); el estado `Aeropuerto` se recrea en cada paso |
| Función pura | Misma entrada → misma salida y sin efectos secundarios | Toda la validación, la torre y los reportes |
| Transparencia referencial | Una expresión se puede reemplazar por su valor sin cambiar el programa | Consecuencia de las funciones puras; permite verificar por partes |
| Funciones de orden superior | Reciben o devuelven funciones | `map`, `filter`, `sortBy`, `validar(..., reglas, construir)` recibe funciones; comparadores |
| Lambdas y clausuras | Funciones anónimas que capturan variables del entorno | `a -> paso(a, filas, operativas)` captura `filas` y `operativas` |
| Composición | Construir funciones uniendo otras | `comp` y `juxt` en Clojure; cadenas `Optional.or`/`orElse`; `Comparator.comparing(...).thenComparing(...)` |
| Evaluación perezosa | Un valor se calcula cuando se necesita | `Stream`, `Iterator`, `iterate`; parámetros por nombre de Scala; macro `or` de Clojure; `Optional.or(() -> ...)` |
| map / filter / reduce | Transformar, seleccionar, combinar | En todos los módulos |
| Agrupación | Particionar por clave | Las 12 filas; RF10 por pista; RF11 por aerolínea; dueños de códigos |
| Recursión (y de cola) | Una función se llama a sí misma; de cola si es lo último que hace | `asignarEnMinuto`: Java recursión normal (profundidad ≤ 5), Scala `@tailrec`, Clojure `recur` |
| Errores como valores | El error es un dato del tipo de retorno, no una excepción | `Optional`, `Ok`/`Falla`, `Either`, `{:ok}`/`{:falla}`, `nil` |
| Tipos algebraicos | Tipos suma (o uno u otro) y producto (varios campos) | `sealed interface Resultado` (suma) con `record Ok`/`Falla`; `enum`; `Either` |
| Coincidencia de patrones | Desarmar un valor según su forma | `instanceof Ok<T> ok` (Java 21), `case Right(valor)` (Scala), desestructuración `[[_ longitud uso estado]]` (Clojure) |
| Estructuras persistentes | Inmutables que comparten estructura al "modificarse" | `Vector` de Scala y vectores/mapas de Clojure (árboles de 32 ramas: `updated`/`assoc` cuestan O(log₃₂ n)) |
| Núcleo funcional, cáscara imperativa | Efectos solo en los bordes | Lectura, escritura y reloj en Lectura/Main/Medición |

### 8.2 Las cuatro reglas del proyecto (verificadas automáticamente)

| Regla | Prohíbe | Se reemplaza por |
|---|---|---|
| F1 · Sin ciclos | `for`, `while`, `do` (Java/Scala); `loop`, `doseq`, `dotimes`, `while`, `for` (Clojure; el `for` de Clojure es una comprensión, pero se prohibió por igualdad) | `map`, `filter`, `iterate`, recursión |
| F2 · Sin reasignación | `++`, `--`, `+=`, reasignar una variable (Java); `var` (Scala); `atom`, `swap!`, `reset!`, `set!`, `ref`, `alter`, `volatile!`, `vswap!` (Clojure) | Valores nuevos |
| F3 · Sin colecciones mutables | `ArrayList`, `HashMap`, `StringBuilder`, `.add(`, `.put(`… (Java); `mutable`, `ArrayBuffer`, `ListBuffer`, `Array(`, `.update(` (Scala); `transient`, `conj!`, `assoc!`, `aset` (Clojure) | Colecciones inmutables |
| F4 · Sin excepciones | `try`, `catch`, `throw` (+ `Try(` en Scala, `ex-info` en Clojure) | Errores como valores; revisar antes de leer un archivo |

Excepción documentada: en Java se permite `throws IOException` en las firmas que leen o escriben archivos,
porque Java obliga a declarar las excepciones comprobadas; es una declaración, no un manejo.

Resultado: **las tres versiones cumplen las 4 reglas (0 violaciones)**, según `experimento/funcional.py`.

### 8.3 Cómo se resolvió lo que normalmente se hace de forma imperativa

| Problema | Forma imperativa típica | Forma funcional usada |
|---|---|---|
| Recorrer el tiempo | `while (hayVuelos) { ... }` | `iterate` + `takeWhile` + `flatMap` |
| Actualizar el estado | Modificar campos | Crear un `Aeropuerto` nuevo (`new`, `copy`, `assoc`) |
| Cambiar un elemento de una lista | `lista.set(i, x)` | Java: `reemplazar` crea una lista nueva con `IntStream.range(...).mapToObj(...)`; Scala: `updated`; Clojure: `assoc-in`/`update-in` |
| Códigos repetidos | `Set` mutable de vistos | Dueño por agrupación + mínimo |
| Primer error de varias reglas | `if ... return` encadenados | `Optional.or` / `Option.orElse` / `or` |
| Archivo inexistente | `try { leer } catch` | Comprobar `isRegularFile && isReadable` antes y devolver código 2 |
| Contar, sumar, agrupar | Acumuladores | `count`, `sum`, `groupingBy`, `groupBy`, `group-by`, `frequencies` |
| Construir texto grande | `StringBuilder.append` | `Collectors.joining`, `mkString`, `str/join` |

### 8.4 Errores como valores en detalle

- **Java:** `Optional<String>` representa "un mensaje de error o nada". `si(condición, mensaje)` devuelve
  `Optional.of(mensaje)` o `Optional.empty()`. La cadena `regla1.or(() -> regla2).or(() -> regla3)` devuelve el
  primer error; las lambdas `() ->` evitan evaluar reglas posteriores (por ejemplo, no se hace `parseInt` si ya
  falló "no es un entero"). El resultado de validar es la interfaz sellada `Resultado<T>` con dos casos:
  `Ok<T>(valor)` y `Falla<T>(error)` (Java no trae `Either`).
- **Scala:** `Option[String]` y `orElse`, cuyo parámetro es **por nombre** (`=> Option[B]`), así que se evalúa
  solo si hace falta, sin lambdas explícitas. El resultado es `Either[ErrorRegistro, T]` (`Left` = error,
  `Right` = válido); `Option.toLeft(construir(...))` convierte "error o nada" en `Either`.
- **Clojure:** no hay tipo `Option`: se usa `nil` como "nada" (nil-punning). `(or regla1 regla2 ...)` es un
  macro perezoso que devuelve el primer valor que no es `nil`; `(when condición mensaje)` devuelve el mensaje o
  `nil`. El resultado de validar es un mapa `{:ok dato}` o `{:falla error}`, y `(keep :ok resultados)` extrae
  los válidos.

---

## 9. Los tres lenguajes: teoría y cómo se usó cada uno

### 9.1 Comparación general

| Aspecto | Java 21 | Scala 3.9.0 | Clojure 1.12.0 |
|---|---|---|---|
| Paradigma | Orientado a objetos con soporte funcional (desde Java 8: lambdas, Streams; Java 16–21: records, sealed, pattern matching) | Híbrido objeto-funcional | Funcional, dialecto de Lisp |
| Tipado | Estático, nominal | Estático, con inferencia fuerte | Dinámico (los tipos se comprueban al ejecutar) |
| Sintaxis | Llaves, tipos explícitos | Indentación (Scala 3), expresiones | S-expresiones, notación prefija `(f x y)` |
| Compilación | `javac` → bytecode | `scalac` → bytecode + biblioteca de Scala | El compilador de Clojure genera bytecode al cargar cada forma; con **AOT** se genera antes (`lein uberjar`) |
| Inmutabilidad por defecto | No (hay que elegir `List.of`, `toList()`, records) | Sí en colecciones por defecto | Sí en todo (datos persistentes) |
| Ausencia de valor | `Optional<T>` | `Option[T]` | `nil` |
| Lambdas en la JVM | `invokedynamic` + `LambdaMetafactory` (clases creadas al primer uso) | También `invokedynamic` | Cada función es una clase (`AFunction`) generada por el compilador |
| Tamaño del `.jar` | 49 KB | 10 MB (incluye la biblioteca de Scala) | 5,2 MB (incluye el núcleo de Clojure) |
| Líneas de código (Q1) | 600 | 352 | 466 |

### 9.2 Java en el proyecto

- **Entidades:** `record` (inmutables, con `equals`/`hashCode`/`toString` automáticos).
- **Listas cerradas:** `enum` con datos (`Categoria(longitudMinima, minutosOcupacion)`).
- **Colecciones:** `Stream` + `toList()` (lista no modificable) y `List.of`.
- **Comparadores compuestos:** `Comparator.comparing(...).thenComparing(...).thenComparingLong(...)`.
- **Agrupar:** `Collectors.groupingBy`, `Collectors.toMap(..., Math::min)`.
- **Texto:** `Collectors.joining("\n", "", "\n")`.
- **Tipos suma:** `sealed interface Resultado<T> permits Ok, Falla` + `instanceof` con patrón.
- **Evaluación perezosa explícita:** `Optional.or(() -> ...)`.
- **Detalles:**
  - para "modificar" una lista se crea otra (`reemplazar`);
  - la salida a pantalla se escribe en bytes UTF-8 (`System.out.writeBytes`) para no depender de la
    configuración regional;
  - la lectura usa `new String(Files.readAllBytes(p), UTF_8)`, que reemplaza bytes inválidos por U+FFFD.

### 9.3 Scala en el proyecto

- **Entidades:** `case class` (inmutables, `copy`, coincidencia de patrones).
- **Listas cerradas:** `enum` de Scala 3 (con parámetros en `Categoria`).
- **Colecciones inmutables por defecto:** `Vector` (estructura persistente: `updated` y `:+` en tiempo casi
  constante).
- **Inferencia de tipos y desarme de tuplas:** `.map((nombre, suyas) => ...)`.
- **Ordenamientos:** `Ordering.by(v => (tupla))` para la prioridad; `sortBy` y `sortWith`.
- **Reducciones y búsquedas:** `groupMapReduce` (agrupa, transforma y reduce en un paso); `minByOption`,
  `maxOption` (versiones seguras que devuelven `Option`).
- **Errores como valores:** `Option.orElse` con parámetro por nombre; `Either` y `toLeft`; `collect { case
  Right(v) => v }` (función parcial que filtra y transforma a la vez).
- **Recursión:** `@tailrec` en `asignarEnMinuto`, que el compilador convierte en un salto.
- **Simulación:** `Iterator.iterate(...)` para la secuencia perezosa de estados.
- **Medición:** `Medicion.medir[T](etapa: => T)` recibe la etapa por nombre, así que se evalúa entre las dos
  lecturas del reloj.
- **Construcción:** Scala CLI (`scala-cli --power package . --assembly --server=false`).
  - `--assembly` crea un `.jar` único con la biblioteca de Scala.
  - `--server=false` evita dejar un servidor de compilación (Bloop) corriendo, que afectaría las mediciones.

### 9.4 Clojure en el proyecto

- **Entidades:** `defrecord` (mapas con campos fijos, más rápidos que mapas comunes); se accede con palabras
  clave `(:codigo v)`.
- **Listas cerradas:** palabras clave con el texto exacto del contrato (`:Ligero`, `:Aterrizaje`). Como
  `:Despegue` y `:Aterrizaje` son la misma palabra clave en el uso de la pista y en la operación del vuelo, la
  compatibilidad compara `(= (:uso pista) (:operacion vuelo))`.
- **Colecciones persistentes:**
  - vectores y mapas;
  - `assoc-in`/`update-in` para "modificar" el estado;
  - `into []` con **transductores** (`comp`, `map-indexed`, `drop`, `remove`, `keep`, `take-while`, `mapcat`),
    que procesan sin crear secuencias intermedias.
- **Validación:** desestructuración de vectores en los parámetros (`[[_ longitud uso estado]]`); macros `or`,
  `when`, `when-not`, `if-let`, `when-let`, `cond`.
- **Comparadores:** funciones de 2 argumentos que devuelven negativo, cero o positivo (toda función de Clojure
  implementa `java.util.Comparator`).
- **Recursión:** `recur` en `asignar-en-minuto`.
- **Rendimiento:**
  - `:aot :all` compila todo por adelantado;
  - `*warn-on-reflection* true` avisa de cualquier llamada a Java que necesitaría reflexión (lenta). El código
    tiene sugerencias de tipo (`^String`, `^File`) y **0 llamadas por reflexión**;
  - `(.trim s)` en lugar de `clojure.string/trim`, para respetar el contrato.
- **Construcción:** Leiningen, `lein uberjar` (Clojure 1.12.0, `:target-path "target/%s"`).
- **Lo que se evitó por las reglas:** `transient` (colecciones transitorias, la optimización típica de Clojure,
  prohibida por F3), `atom` (F2), `loop` y `doseq` (F1).

### 9.5 La misma regla en los tres lenguajes (validar una pista)

```java
// Java: cadena de Optional.or con lambdas
return entero(c.get(1), "longitud")
        .or(() -> si(Integer.parseInt(c.get(1)) <= 0, "longitud debe ser mayor que 0: " + c.get(1)))
        .or(() -> opcion(c.get(2), "uso", Modelo.nombres(Uso.values())))
        .or(() -> opcion(c.get(3), "estado", Modelo.nombres(Estado.values())));
```
```scala
// Scala: orElse con parámetros por nombre
entero(c(1), "longitud")
  .orElse(si(c(1).toInt <= 0, s"longitud debe ser mayor que 0: ${c(1)}"))
  .orElse(opcion(c(2), "uso", Modelo.nombres(Uso.values)))
  .orElse(opcion(c(3), "estado", Modelo.nombres(Estado.values)))
```
```clojure
;; Clojure: el macro or devuelve el primer valor que no es nil
(or (entero longitud "longitud")
    (when (<= (parse-long longitud) 0) (str "longitud debe ser mayor que 0: " longitud))
    (opcion uso "uso" m/nombres-uso)
    (opcion estado "estado" m/nombres-estado))
```

### 9.6 Elegir el mejor candidato (RN05) en los tres

```java
return IntStream.range(0, filas.size()).boxed()
        .filter(i -> quedanVuelos(a, filas, i))
        .filter(i -> primero(a, filas, i).programado() <= a.minuto())
        .flatMap(i -> pistaLibre(a, primero(a, filas, i), pistas)
                .map(j -> new Candidato(i, j, primero(a, filas, i))).stream())
        .min(Comparator.comparing(Candidato::vuelo, PRIORIDAD));
```
```scala
filas.indices
  .filter(i => quedanVuelos(a, filas, i) && primero(a, filas, i).programado <= a.minuto)
  .flatMap(i => pistaLibre(a, primero(a, filas, i), pistas).map(j => Candidato(i, j, primero(a, filas, i))))
  .minByOption(_.vuelo)(using prioridad)
```
```clojure
(->> (range (count filas))
     (filter #(quedan-vuelos? aeropuerto filas %))
     (keep #(candidato aeropuerto filas pistas %))
     (sort-by :vuelo por-prioridad)
     first)
```

---

## 10. Teoría de la JVM necesaria para entender los resultados

- **Bytecode y JVM:** los tres lenguajes compilan a bytecode que ejecuta la misma máquina virtual (OpenJDK 21).
  Por eso comparten el recolector de basura, el compilador JIT y el instrumento de memoria.
- **Arranque y carga de clases:** al iniciar, la JVM carga las clases que usa el programa.
  - Java carga casi solo las suyas y las del JDK.
  - Scala carga además su biblioteca estándar.
  - Clojure inicializa su núcleo (`clojure.core`: cientos de funciones y variables), que cuesta del orden de
    0,5–0,6 s.
  - Medido en V1 (tiempo del proceso fuera de las operaciones): **Java 79 ms, Scala 200 ms, Clojure 626 ms**.
- **Intérprete y JIT por niveles:** el bytecode empieza interpretado. Los métodos que se usan mucho se compilan a
  código máquina: primero con C1 (rápido de compilar) y luego con C2 (más optimizado). Por eso las primeras
  ejecuciones de un código son más lentas (**calentamiento**). Con 1.000 vuelos casi todo el programa corre
  "frío"; con 1.000.000 domina el código ya optimizado.
- **Lambdas e `invokedynamic`:** Java (y Scala) compilan cada lambda como una llamada `invokedynamic`; la
  primera vez que se ejecuta, `LambdaMetafactory` genera una clase para esa lambda (costo de primer uso).
  Clojure compilado AOT ya trae sus funciones como clases normales. **Explicación más probable** de que Clojure
  tenga el menor `t_operaciones` en V1 (212 ms frente a 285 de Java y 339 de Scala).
- **AOT en Clojure:** sin AOT, Clojure compilaría el código fuente al arrancar; con AOT el `.jar` trae las
  clases. Aun así, el núcleo de Clojure debe inicializarse.
- **Recolector G1 y memoria:**
  - `-Xmx4g` fija el montículo máximo en 4 GB. G1 hace crecer el montículo según la presión de asignación y
    prefiere crecer antes que recolectar a menudo.
  - Por eso la memoria residente máxima (RSS) mide cuánto decidió crecer el montículo, no solo los datos vivos.
    En V4 los tres llegan a 3–4 GB.
  - RSS incluye además código, metaespacio (clases), pilas de hilos y estructuras del JIT.
- **Boxing y tipos dinámicos:** en Clojure, los números de los registros se guardan como objetos `Long` y las
  operaciones aritméticas genéricas comprueban tipos al ejecutar. Además, los campos se buscan por palabra clave
  y los mapas persistentes cuestan más de crear que un `record`. Esto encarece el trabajo por elemento:
  **explicación más probable** del mayor tiempo de Clojure con volúmenes grandes.
- **Reflexión:** si el compilador de Clojure no conoce el tipo de un objeto Java, la llamada se resuelve por
  reflexión en cada ejecución (muy lenta). Se evitó con sugerencias de tipo: 0 llamadas reflexivas.
- **`System.nanoTime()`:** reloj monotónico de alta resolución de la JVM, para medir intervalos (no da la hora
  del día). Es el mismo en los tres lenguajes porque todos corren en la JVM.

---

## 11. Diseño del experimento (teoría experimental)

### 11.1 Variables

- **Independiente:** el lenguaje (Java, Scala, Clojure).
- **Dependientes:** tiempo, memoria, rendimiento (medidos); calidad, confiabilidad, uso funcional
  (calculados).
- **Controladas:**
  - mismos datos (archivos con huella SHA-256);
  - misma JVM y opciones (`-Xmx4g -XX:+UseG1GC`);
  - mismo algoritmo y contrato;
  - mismo equipo y sesión;
  - mismo protocolo;
  - misma salida verificada.
- **Factor de escenario:** volumen (V1–V4), carga (C1) y calidad de los datos (X1).

### 11.2 Aeropuerto común (`datos/aeropuerto/pistas.csv`)

| Pista | Longitud | Uso | Estado |
|---|---|---|---|
| P01 | 3.200 m | Mixta | Operativa |
| P02 | 2.800 m | Aterrizaje | Operativa |
| P03 | 2.900 m | Despegue | Operativa |
| P04 | 2.100 m | Mixta | Operativa |
| P05 | 1.500 m | Aterrizaje | Operativa |
| P06 | 3.000 m | Despegue | Cerrada |

Compatibilidades: aterrizaje Ligero P01·P02·P04·P05; Mediano P01·P02·P04; Pesado P01·P02. Despegue Ligero
P01·P03·P04; Mediano P01·P03·P04; Pesado P01·P03.

### 11.3 Escenarios

| Id | Vuelos | Vuelos/día | Inválidos | Semilla | Evalúa | Comportamiento (referencia) |
|---|---|---|---|---|---|---|
| E0 | 13 | — | 3 | — | Correctitud (ejemplo a mano) | 9 operaciones, promedio 1,56 min |
| V1 | 1.000 | 1.500 | 0 % | 101 | Volumen pequeño | 1 día, ocupación 40,0 %, retraso 0,20 min |
| V2 | 10.000 | 1.500 | 0 % | 102 | Volumen mediano | 8 días, 57,6 %, 0,96 min, 0,18 % retrasados |
| V3 | 100.000 | 1.500 | 0 % | 103 | Volumen grande | 68 días, 60,1 %, 1,04 min, 0,16 % |
| V4 | 1.000.000 | 1.500 | 0 % | 104 | Volumen muy grande | 668 días, 60,4 %, 1,04 min, 0,12 % |
| C1 | 100.000 | 2.400 | 0 % | 201 | Congestión | 52 días, 78,1 % (P01, P03, P04 al 100 %), 5.414 min de retraso promedio, 47,42 % retrasados |
| X1 | 100.000 | 1.500 | 10 % | 301 | Errores | 68 días, 54,1 %, 0,64 min, 90.032 válidos |
| R01–R12 | pequeños | — | — | — | Robustez | ver 12.4 |

V1–V4 tienen la misma carga diaria: si crece el tiempo, la causa es el volumen. C1 tiene los mismos 100.000
vuelos que V3 pero 60 % más por día: el aeropuerto se satura y **los despegues absorben el retraso**, porque los
aterrizajes tienen prioridad (hallazgo del dominio). X1 tiene los mismos 100.000 que V3 con 10 % dañado.

### 11.4 Generador determinista (`datos/generador.py`)

- **Distribuciones:**
  - aerolínea: Avianca 25 %, LATAM 20 %, Copa 15 %, Wingo 10 %, JetSMART 10 %, American 8 %, Iberia 6 %,
    Viva 6 %;
  - código: prefijo + número consecutivo de 7 dígitos;
  - matrícula: prefijo del país + 4 dígitos;
  - categoría: Ligero 30 %, Mediano 50 %, Pesado 20 %;
  - operación: 50/50;
  - prioridad: Emergencia 5 %;
  - día: `i / vuelos_por_día + 1`;
  - hora: uniforme.
- **Errores de X1:** 10 % de los registros con uno de 10 errores, uno por regla: falta un campo, código vacío,
  código repetido, aerolínea vacía, matrícula vacía, categoría `Jumbo`, operación `Escala`, día `uno`, hora
  `24:10`, prioridad `Urgente`.
- **Determinismo:** semilla fija por escenario. Solo se usa `random.random()` (Mersenne Twister, misma secuencia
  desde Python 3.2) y las elecciones con pesos se hacen a mano, no con funciones que cambien entre versiones.
  Regenerar produce el mismo archivo byte a byte; se comprueba con las huellas SHA-256
  (`datos/escenarios/huellas.sha256`).

### 11.5 Implementación de referencia (oráculo)

`experimento/referencia.py` implementa el contrato de la forma más directa, sin restricciones funcionales. **No
compite.** Produce las salidas esperadas (concepto de **oráculo de pruebas**: algo que dice cuál es la salida
correcta). Coincide con el ejemplo resuelto a mano. Si una versión difiere, decide el contrato.

### 11.6 Métricas e instrumentos

| Criterio | Métrica | Instrumento | Por qué |
|---|---|---|---|
| Tiempo | `t_operaciones` = validación + simulación + reportes (ms) | `System.nanoTime()` dentro del programa | Mide "la duración de las operaciones" sin el arranque ni la E/S, con el mismo reloj en los tres |
| Memoria | Memoria residente máxima (MB, 1 MB = 1.048.576 bytes) | `ru_maxrss` de `os.wait4` (macOS: bytes; Linux: KB) | Lo da el sistema operativo, no el programa: igual para los tres |
| Rendimiento | Vuelos / `t_proceso` (vuelos por segundo) | Reloj del orquestador (`perf_counter_ns`) alrededor del proceso | "Operaciones por unidad de tiempo" del programa completo, como lo vería un usuario |

**Regla de materialización:** cada etapa deja su resultado completamente calculado antes de tomar el tiempo
(Java `toList`, Scala `toVector`/`toList`, Clojure `vec`/`into []`). Sin ella, la pereza de Clojure trasladaría
trabajo a la etapa siguiente.

### 11.7 Protocolo y su justificación estadística

| Práctica | Razón |
|---|---|
| 1 ronda de calentamiento descartada | Cachés del disco y del sistema, primera carga de archivos |
| 10 rondas medidas | Suficientes para estimar la mediana y la dispersión |
| Orden rotado (J-S-C, S-C-J, C-J-S) | **Contrabalanceo**: ningún lenguaje queda siempre primero o último (calentamiento térmico, cachés) |
| Proceso nuevo por ejecución | Así se usa un programa de consola; el arranque y el JIT son costo real y se miden igual en los tres |
| 1 s de pausa | Evita que una ejecución afecte a la siguiente |
| Pantalla a `/dev/null` | No medir la consola |
| Salida verificada con SHA-256 en cada ejecución | Solo cuentan mediciones de ejecuciones correctas |
| **Mediana** (no promedio) | Robusta frente a valores atípicos: una ejecución interrumpida mueve mucho el promedio y casi nada la mediana |
| Mínimo, máximo y **rango intercuartílico (RIC = Q3 − Q1)** | Muestran la estabilidad de las mediciones |

### 11.8 Amenazas a la validez y cómo se controlan

| Tipo | Amenaza | Control |
|---|---|---|
| Interna | Otros procesos, calentamiento térmico | Orden rotado, pausas, mediana, RIC |
| Interna | La pereza traslada trabajo entre etapas | Regla de materialización |
| Interna | El orquestador influye en la medición | Corregido (sección 16): el orquestador ocupa 20 MB |
| Interna | Algoritmos distintos entre versiones | Mismo diseño, contrato y complejidad; revisión módulo por módulo |
| Constructo | ¿La memoria mide los datos o el montículo? | Mide el montículo según G1; declarado y con las mismas opciones en los tres |
| Constructo | Métricas de calidad como indicadores parciales | Reglas explícitas y verificables; declarado |
| Externa | Un solo equipo y un solo problema | Declarado; reproducible con una orden |
| Conclusión | Diferencias pequeñas dentro del ruido | Rangos mín–máx: en V1 y V2 los de Java y Scala se cruzan; desde 100.000 vuelos las diferencias son claras |

### 11.9 Casos de robustez (`datos/robustez/R01..R12`)

| Caso | Situación | Esperado |
|---|---|---|
| R01 | Sin argumentos | `ERROR:` y código 2 |
| R02 | El archivo de pistas no existe | `ERROR:` y código 2 |
| R03 | Archivo de vuelos vacío (0 bytes, sin encabezado) | Código 0; "Sin datos" |
| R04 | Ambos archivos solo con encabezado | Código 0; "Sin datos" |
| R05 | Todos los vuelos inválidos | Código 0; todos en `errores.csv` |
| R06 | Todas las pistas cerradas | Todos los vuelos en RF12 con "sin pista habilitada para la operación" |
| R07 | Líneas en blanco y espacios alrededor de campos | Se ignoran y se recortan |
| R08 | Finales de línea de Windows `\r\n` | Misma salida que con `\n` |
| R09 | Campos de más, de menos y coma final | `se esperaban N campos y hay M` |
| R10 | Números límite: 10 dígitos, negativos, `0`, `+5`, `007` | Mensajes del contrato; `007` válido |
| R11 | Horas límite: `00:00`, `23:59`, `24:00`, `8:5`, `12:60` | Las dos primeras válidas |
| R12 | Tildes, `ñ` y un byte UTF-8 inválido | Se conservan; el byte inválido se vuelve `�` |

Un caso se supera si el código de salida es el esperado, los archivos son idénticos a los esperados (cuando el
código es 0) y no hay nada en la salida de error (ninguna excepción de Java).

---

## 12. Criterios, fórmulas y clasificación automática

### 12.1 Tipos de puntaje (0 a 100 por lenguaje)

- **Proporcional al mejor** (métricas sin máximo natural): menor es mejor → `100·mejor/valor`; mayor es mejor →
  `100·valor/mejor`; conteos que pueden valer 0 (duplicación) → `100·(mejor+1)/(valor+1)` (suavizado para no
  dividir entre cero). No se usa escalado mín–máx porque daría 0 al último aunque estuviera a un 1 % del
  primero, exagerando diferencias con solo tres lenguajes.
- **Absoluto** (porcentajes de reglas o pruebas): el puntaje es ese porcentaje.

### 12.2 Cada criterio

| Criterio | Peso | Cálculo |
|---|---|---|
| Tiempo | 25 % | En cada escenario V1–V4, C1, X1: mediana de `t_operaciones` de las rondas válidas → proporcional (menor mejor) → promedio de los 6 |
| Memoria | 20 % | Igual con la memoria máxima |
| Rendimiento | 20 % | Igual con vuelos por segundo (mayor mejor) |
| Calidad | 15 % | ⅓ Q1 líneas de código + ⅓ Q2 decisiones cada 100 líneas + ⅓ Q3 líneas duplicadas (las tres proporcionales, menor mejor; Q3 suavizada) |
| Confiabilidad | 10 % | Promedio de: correctitud (7 escenarios E0, V1–V4, C1, X1), robustez (12 casos) y estabilidad (ejecuciones medidas correctas / 60) |
| Uso funcional | 10 % | Restricciones F1–F4 (12,5 puntos por regla cumplida, total 50) + densidad funcional proporcional al mejor (hasta 50) |

Sin medición válida en un escenario → 0 en ese escenario (y se refleja en confiabilidad).

`Final = 0,25·Tiempo + 0,20·Memoria + 0,20·Rendimiento + 0,15·Calidad + 0,10·Confiabilidad + 0,10·Uso funcional`

**Desempate:** mayor Tiempo y luego mayor Memoria.

**Prueba de solidez (análisis de sensibilidad):** se recalcula con pesos iguales (1/6 cada uno) y quitando un
criterio a la vez (6 variantes; el peso quitado se reparte entre los demás **en proporción a sus pesos**, es
decir, se renormaliza). Si el mismo lenguaje gana en las 7 variantes, el resultado no depende de los pesos.

### 12.3 Calidad: definiciones

- **Q1 · Líneas de código:** líneas que no quedan vacías tras quitar comentarios (se conservan las comillas de
  las cadenas para que una línea con solo una cadena siga contando).
- **Q2 · Puntos de decisión cada 100 líneas** (inspirado en la complejidad ciclomática de McCabe: 1 + número de
  decisiones):

  | Elemento | Java | Scala | Clojure |
  |---|---|---|---|
  | Condicional | `if` | `if` | `if`, `if-not`, `if-let`, `if-some`, `when`, `when-not`, `when-let`, `when-some` |
  | Una rama por caso | `case` (no `default`) | `case` con `=>` (no cuentan `case` de enum, `case class`, `case object` ni `case _ =>`) | `cond`, `condp`, `case`: un punto por par prueba/resultado sin `:else` ni valor por defecto |
  | Operador lógico | `&&`, `\|\|` (cada uno) | `&&`, `\|\|` | `and`, `or` (1 por aparición) |
  | Ternario | `? :` | — | — |

- **Q3 · Duplicación:** `jscpd --min-tokens 50 --mode weak` (detección de clones por tokens, ignorando
  comentarios), cada versión por separado.
- Antes de contar se eliminan comentarios y el contenido de las cadenas (`experimento/fuentes.py`).
  - En Scala, el código dentro de `${...}` de una cadena interpolada se conserva, porque es código (como `+` en
    Java).
- No puntúan pero se reportan:
  - `javac -Xlint:all`: **0 advertencias**;
  - Clojure con `*warn-on-reflection*`: **0 reflexiones**;
  - las advertencias de Scala, `clj-kondo` y SonarQube **no se registraron** en la medición final.
- **Por qué SonarQube no puntúa:** no analiza Clojure; usarlo solo en Java y Scala favorecería al lenguaje con el
  analizador menos estricto.

### 12.4 Uso funcional: definiciones

- **Mitad A (absoluta):** F1–F4 (sección 8.2); una sola violación anula la regla.
- **Mitad B (densidad):** operaciones funcionales contadas cada 100 líneas de código, por categoría:

  | Categoría | Java | Scala | Clojure |
  |---|---|---|---|
  | Transformar | `.map(`, `.flatMap(`, `.mapToInt/Long/Double/Obj(` | `.map`, `.flatMap`, `.collect` | `map`, `mapv`, `mapcat`, `keep`, `map-indexed` |
  | Filtrar | `.filter(` | `.filter`, `.filterNot`, `.partition` | `filter`, `filterv`, `remove` |
  | Reducir | `.reduce(`, `.collect(`, `.sum(`, `.count(`, `.max(`, `.min(` | `.foldLeft`, `.fold`, `.reduce`, `.reduceOption`, `.sum`, `.count`, `.max`, `.min`, `.maxBy`, `.minBy` y variantes `…Option` | `reduce`, `frequencies`, `(count (filter …))`, `max-key`, `min-key`, `apply` |
  | Agrupar | `groupingBy(`, `partitioningBy(` | `.groupBy`, `.groupMapReduce` | `group-by`, `partition-by` |
  | Ordenar | `.sorted(`, `Comparator.comparing…` | `.sortBy`, `.sortWith`, `.sorted` | `sort`, `sort-by` |
  | Buscar | `.findFirst(`, `.anyMatch(`, `.allMatch(`, `.noneMatch(` | `.find`, `.exists`, `.forall` | `some`, `every?`, `not-any?` |
  | Secuencias | `Stream.iterate(`, `.takeWhile(`, `.limit(`, `.skip(` | `Iterator.iterate`, `.takeWhile`, `.take`, `.drop`, `.zip` | `iterate`, `take-while`, `take`, `drop`, `interleave` |
  | Composición | `.andThen(`, `.compose(` | `andThen`, `compose` | `comp`, `partial`, `juxt` |
  | Opcionales | `.orElse(`, `.orElseGet(`, `.or(` | `opcion.getOrElse(v)`, `.orElse` | `some->`, `fnil` |

- **Precisiones de equidad (D7.3):**
  - las variantes que solo cambian el tipo del resultado cuentan como la base (`mapv`, `filterv`, `maxOption`…);
  - `(count v)` sobre una colección es su tamaño (como `.size()`), y solo cuenta `(count (filter …))`;
  - `mapa.getOrElse(clave, v)` de Scala es una búsqueda en un mapa (como `getOrDefault`), y no cuenta;
  - `Optional.or` de Java es la misma operación que `Option.orElse` de Scala (Java llama `orElse` a lo que
    Scala llama `getOrElse`).
- Cada operación se reconoce por su nombre completo (`.take` no cuenta dentro de `.takeWhile`).

### 12.5 Ejemplo numérico del documento de criterios (números inventados)

A: 400 ms, 300 MB, 150.000 vuelos/s; B: 320 ms, 340 MB, 165.000; C: 520 ms, 420 MB, 110.000. Tiempo: A =
100·320/400 = 80; B = 100; C = 61,5. Final de B = 0,25·100 + 0,20·88,2 + 0,20·100 + 0,15·91 + 0,10·100 +
0,10·93 = 95,60. El clasificador real reproduce este ejemplo (95,59 por redondeo de 88,2).

---

## 13. Herramientas y scripts del proyecto

| Archivo | Qué hace |
|---|---|
| `java/construir.sh` | `javac --release 21 -encoding UTF-8` + `jar --main-class simulador.Main` → `java/simulador-java.jar` |
| `scala/construir.sh` | `scala-cli --power package . --assembly --server=false -f -o simulador-scala.jar` |
| `clojure/construir.sh` | `lein uberjar` y copia `target/uberjar/simulador-clojure.jar` |
| `datos/generador.py` | Genera los escenarios con semilla fija (sección 11.4) |
| `experimento/referencia.py` | Implementación de referencia (oráculo) en Python |
| `experimento/verificar.sh` | Construye los `.jar` (o usa los existentes con `SIN_CONSTRUIR=1`). Ejecuta E0, los escenarios con salida esperada y R01–R12. Compara con `cmp` los 3 archivos y la pantalla, revisa el código de salida y que la salida de error esté vacía. Imprime una tabla por lenguaje. Con `RESULTADOS_CSV` guarda `caso,lenguaje,resultado` |
| `herramientas/entorno.sh` | Pone Homebrew y el JDK 21 en el PATH en macOS (IntelliJ no hereda el PATH de la terminal) |
| `experimento/ejecutar.py` | Orquestador: construir → registrar entorno (`entorno.txt`, con huellas SHA-256 de los `.jar`) → regenerar y comprobar escenarios → verificar equivalencia → medir (198 ejecuciones con `subprocess.Popen` + `os.wait4`) → `crudos/*.csv` → `resumen.md`. Opciones: `--prueba`, `--forzar`, `--sin-construir`, `--lenguajes`, `--nota`. En macOS se detiene si el equipo está con batería o en bajo consumo |
| `experimento/fuentes.py` | Lector de fuentes: quita comentarios y contenido de cadenas en Java/Scala/Clojure |
| `experimento/calidad.py` | Q1, Q2 (con un lector mínimo de formas para Clojure) y Q3 (jscpd) → `calidad.csv` |
| `experimento/funcional.py` | Violaciones F1–F4 y densidad funcional por categoría → `funcional.csv` |
| `experimento/clasificar.py` | Puntajes, clasificación, explicación generada y prueba de solidez → `consolidado.csv`, `puntajes.csv`, `clasificacion.md` |
| `experimento/graficos.py` | 7 gráficos PNG (matplotlib) en `resultados/graficos/` |
| `informe/generar_informe.py` + `contenido.py` + `resultados.py` + `construir_docx.js` | Genera `entrega/Informe_tecnico.docx` desde los resultados |
| `.run/Verificar.run.xml` | Configuración compartida de IntelliJ "Verificar equivalencia" |

---

## 14. Resultados completos e interpretación

Medición: 198 ejecuciones (6 escenarios × 11 rondas × 3 lenguajes); **todas con salida correcta**.
Verificación: **19/19 casos en los tres lenguajes** (E0, V1–V4, C1, X1 y R01–R12).

### 14.1 Clasificación

| Pos. | Lenguaje | Tiempo (25 %) | Memoria (20 %) | Rendimiento (20 %) | Calidad (15 %) | Confiabilidad (10 %) | Uso funcional (10 %) | **Final** |
|---|---|---|---|---|---|---|---|---|
| 1.º | **Java** | **95,74** | 88,53 | **100,00** | **86,22** | 100,00 | 87,77 | **93,35** |
| 2.º | Scala | 88,87 | **95,70** | 86,66 | 85,06 | 100,00 | **100,00** | **91,45** |
| 3.º | Clojure | 78,64 | 75,97 | 58,71 | 72,78 | 100,00 | 81,35 | **75,65** |

Explicación generada por el clasificador:
- **Java:** mejor en Tiempo, Rendimiento y Calidad; pierde 7,2 puntos en Memoria (−1,43 al final) y 12,2 en Uso
  funcional (−1,22).
- **Scala:** mejor en Memoria y Uso funcional; pierde 13,3 en Rendimiento (−2,67), 6,9 en Tiempo (−1,72) y 1,2
  en Calidad (−0,17).
- **Clojure:** no es el mejor en ningún criterio. Pierde:
  - 41,3 en Rendimiento (−8,26);
  - 17,1 en Tiempo (−4,27);
  - 19,7 en Memoria (−3,94);
  - 13,4 en Calidad (−2,02);
  - 18,7 en Uso funcional (−1,87).
- Los tres empatan en Confiabilidad.

### 14.2 Tiempo (mediana de `t_operaciones`, ms)

| | V1 | V2 | V3 | V4 | C1 | X1 |
|---|---|---|---|---|---|---|
| Java | 285 | **665** | **2.419** | **12.047** | **2.529** | **2.408** |
| Scala | 339 | 755 | 2.554 | 13.001 | 2.585 | 2.475 |
| Clojure | **212** | 759 | 3.311 | 19.806 | 3.288 | 3.280 |

- Java es el más rápido en 5 de 6 escenarios. En V4, Scala tarda 8 % más y Clojure 64 % más.
- Java y Scala están a 1–6 % en los escenarios de 100.000 vuelos (V3 5,6 %; C1 2,2 %; X1 2,8 %).
- En V1 gana Clojure. **Explicación más probable:** con pocos datos domina el costo de primer uso (lambdas de
  Java/Scala creadas con `invokedynamic`). Clojure AOT ya trae sus funciones como clases, pero paga antes de
  `main` la inicialización de su núcleo, que no entra en `t_operaciones`.
- Clojure/Java en tiempo: V3 1,37; C1 1,30; X1 1,36; V4 1,64 (entre 30 y 64 % más).

### 14.3 Tiempo por etapa en V4 (mediana, s)

| | Lectura | Validación | Simulación | Reportes | Escritura | Suma |
|---|---|---|---|---|---|---|
| Java | 0,39 | **5,01** | 4,37 | **2,66** | 0,17 | 12,6 |
| Scala | 0,42 | 5,56 | **3,00** | 4,38 | 0,13 | 13,5 |
| Clojure | 0,59 | 7,86 | 6,36 | 5,47 | 0,14 | 20,4 |

- Scala tiene la simulación más rápida. **Explicación probable:** actualizar un `Vector` inmutable (`updated`, `:+`)
  cuesta casi lo mismo que en una lista mutable, mientras que Java crea listas nuevas completas con Streams en
  cada asignación (`reemplazar`).
- Java tiene la validación y los reportes más rápidos (Streams y colectores `groupingBy`/`joining` muy
  eficientes).
- Clojure es el más lento en las tres etapas principales (tipado dinámico, `Long` en objetos, búsqueda por
  palabra clave, mapas persistentes).
- Las etapas de los demás escenarios están en el Anexo E.

### 14.4 Memoria (mediana, MB)

| | V1 | V2 | V3 | V4 | C1 | X1 |
|---|---|---|---|---|---|---|
| Java | **62** | 171 | 741 | **3.065** | 738 | 734 |
| Scala | 78 | **151** | **599** | 3.238 | **597** | **596** |
| Clojure | 106 | 185 | 659 | 3.883 | 823 | 813 |

- Scala usa menos memoria con 10.000 a 100.000 vuelos.
- Java usa menos en V1 (no carga la biblioteca de Scala ni el núcleo de Clojure) y en V4.
- Clojure usa más en 5 de 6 escenarios.
- Es memoria física máxima del proceso (incluye el crecimiento del montículo de G1).

### 14.5 Rendimiento (mediana, vuelos por segundo)

| | V1 | V2 | V3 | V4 | C1 | X1 |
|---|---|---|---|---|---|---|
| Java | **2.741** | **12.909** | **38.553** | **78.012** | **37.145** | **38.483** |
| Scala | 1.855 | 10.408 | 35.222 | 71.833 | 35.062 | 36.116 |
| Clojure | 1.193 | 6.999 | 24.747 | 46.884 | 24.729 | 24.494 |

- Java gana los seis.
- El rendimiento incluye el arranque: el tiempo fuera de las operaciones en V1 es Java 79 ms, Scala 200 ms y
  Clojure 626 ms. Por eso Clojure, el más rápido dentro del programa en V1, tiene ahí el menor rendimiento.
- Con volúmenes grandes ese costo fijo pesa menos.

### 14.6 Calidad y uso funcional

| Métrica | Java | Scala | Clojure |
|---|---|---|---|
| Q1 · Líneas de código | 600 | **352** | 466 |
| Puntos de decisión | 32 | 34 | 58 |
| Q2 · Decisiones cada 100 líneas | **5,33** | 9,66 | 12,45 |
| Q3 · Líneas duplicadas | 0 | 0 | 0 |
| Puntaje Q1 / Q2 / Q3 | 58,67 / 100 / 100 | 100 / 55,18 / 100 | 75,54 / 42,81 / 100 |
| **Calidad** | **86,22** | 85,06 | 72,78 |
| Reglas F1–F4 | 4/4 | 4/4 | 4/4 |
| Operaciones funcionales | 121 | 94 | 78 |
| Por categoría: transformar / filtrar / reducir / agrupar / ordenar / buscar / secuencias / composición / opcionales | 39/13/20/4/12/8/2/0/23 | 36/7/11/5/6/5/5/0/19 | 30/9/12/4/7/6/5/5/0 |
| Densidad cada 100 líneas | 20,17 | **26,70** | 16,74 |
| **Uso funcional** (50 + densidad) | 87,77 | **100,00** | 81,35 |

- Scala escribe lo mismo con 41 % menos líneas que Java y es el más funcional.
- Java tiene la menor densidad de decisiones: mucha lógica son cadenas de operaciones sin ramas, y las condiciones
  van dentro de la función auxiliar `si(...)`.
- Clojure tiene más decisiones porque cada regla de validación usa `when` u `or` explícitos. Tiene 0
  "Opcionales" porque usa `nil` en lugar de `Option`: es una diferencia de estilo del lenguaje, no un defecto.
- **Q2 mide densidad, no cantidad:** Scala tiene casi las mismas decisiones que Java (34 frente a 32) en menos
  líneas, por eso su índice es mayor.

### 14.7 Confiabilidad

Los tres: correctitud 7/7, robustez 12/12, estabilidad 60/60 → **100**. Ninguno mostró excepciones: efecto de
tratar los errores como valores y de revisar los archivos antes de leerlos.

### 14.8 Prueba de solidez

| Variante | 1.º | 2.º | 3.º | Puntaje del 1.º | Ventaja del 1.º |
|---|---|---|---|---|---|
| Pesos del proyecto | Java | Scala | Clojure | 93,35 | 1,90 |
| Pesos iguales | Java | Scala | Clojure | 93,04 | 0,33 |
| Sin Tiempo | Java | Scala | Clojure | 92,55 | 0,25 |
| Sin Memoria | Java | Scala | Clojure | 94,56 | 4,17 |
| **Sin Rendimiento** | **Scala** | Java | Clojure | 92,64 | 0,96 |
| Sin Calidad | Java | Scala | Clojure | 94,61 | 2,03 |
| Sin Confiabilidad | Java | Scala | Clojure | 92,61 | 2,11 |
| Sin Uso funcional | Java | Scala | Clojure | 93,97 | 3,47 |

- Java gana en **6 de 7** variantes.
- Sin el criterio de Rendimiento gana Scala, porque sus ventajas en memoria y uso funcional pesan más que la
  velocidad de Java.
- Clojure es tercero en todas.
- Conclusión: el primer lugar de Java es **claro pero estrecho** y se apoya en su ventaja de rendimiento.

---

## 15. Conclusión técnica y limitaciones

**Lenguaje seleccionado: Java (93,35).** Razones:
1. Es el más rápido en las operaciones en 5 de 6 escenarios y procesa más vuelos por segundo en los 6 (V4: 78.012
   frente a 71.833 de Scala y 46.884 de Clojure).
2. Es igual de confiable que los otros.
3. Java moderno (records, Streams, `Optional`, interfaces selladas) cumple todos los principios funcionales del
   curso.

**Scala es una alternativa casi equivalente (1,90 puntos menos):**
- tiene el código más corto (352 líneas) y más funcional;
- usa menos memoria con volúmenes medianos;
- tiene la simulación más rápida.

Si la mantenibilidad o la expresividad pesaran más que el rendimiento, sería la mejor elección (sin Rendimiento,
gana).

**Clojure es correcto y funcional, pero el menos conveniente para este problema** (procesar grandes volúmenes en
un programa de consola que arranca en cada ejecución):
- su arranque cuesta unos 0,6 s;
- su tipado dinámico le cuesta entre 30 y 64 % más de tiempo con volúmenes grandes;
- su optimización típica (`transient`) está prohibida por F3 en los tres lenguajes, para comparar estilo
  funcional con estilo funcional;
- sus ventajas: datos inmutables por defecto, código centrado en datos, `nil`-punning, transductores y la misma
  confiabilidad.

**Ventajas y limitaciones por lenguaje:**

| Lenguaje | Ventajas observadas | Limitaciones observadas |
|---|---|---|
| Java | El más rápido en operaciones y proceso; el arranque más corto; la menor densidad de decisiones; estilo funcional completo con records, Streams, `Optional`, `sealed` | El código más largo (600 líneas); la pereza exige lambdas explícitas; no optimiza la recursión de cola; más memoria que Scala con volúmenes medianos |
| Scala | El código más corto y más funcional; la simulación más rápida; la menor memoria con 10.000–100.000 vuelos; colecciones inmutables por defecto, `Either`, `copy`, `@tailrec` | Arranque más lento que Java (biblioteca de 10 MB); validación y reportes más lentos que Java con 1.000.000 de vuelos |
| Clojure | Inmutabilidad por defecto; código centrado en datos; `or`/`when-let`/`nil` simplifican la validación; transductores; igual de confiable | El más lento y el que más memoria usa en la mayoría de escenarios; arranque de ~0,6 s; tipado dinámico; más puntos de decisión |

**Limitaciones del estudio:**
- Un solo entorno de medición (contenedor Linux de 2 núcleos, OpenJDK 21; ver sección 16).
- Un solo problema (procesamiento por lotes de datos tabulares): en otro tipo de problema (concurrencia, un
  servicio con la JVM caliente) el orden podría cambiar.
- Un proceso nuevo por ejecución: incluye el arranque; con un servicio de larga duración desaparecería la
  desventaja de arranque de Scala y Clojure.
- La memoria depende de cómo G1 dimensiona el montículo.
- En V1 y V2 los rangos mín–máx de Java y Scala se cruzan (diferencia no concluyente en volúmenes pequeños).
- Las métricas de calidad son objetivas pero parciales: no miden la legibilidad para una persona.

---

## 16. Entorno de medición, desviaciones y problemas resueltos

**Dónde se midió:**
- Los tres `.jar` se construyeron en el MacBook Pro del equipo con las herramientas oficiales (`javac`,
  `scala-cli` con Scala 3.9.0, `lein uberjar` con Clojure 1.12.0) y se verificaron allí (15/15 casos).
- La medición se ejecutó con esos mismos `.jar` en un contenedor Linux x86_64 de **2 núcleos**, con OpenJDK
  21.0.12.1 (Ubuntu), Python 3.13 y fecha 14-nov-2026. Allí se verificaron los 19 casos.
- Huellas SHA-256 de los `.jar`:
  - Java `a34b2a53…92c7`;
  - Scala `8bac948c…bd1a`;
  - Clojure `47aad9ed…681e` (completas en `resultados/entorno.txt`).
- **Por qué no en el Mac:** se pidió hacer todo de forma autónoma y la medición no se pudo lanzar en el Mac sin
  intervención (las herramientas de automatización solo podían hacer clics en IntelliJ y Terminal, y el entorno
  aislado disponible tenía Java 11 y 3 GB). El protocolo original (D6.3) preveía el Mac.
- **Efecto:** la comparación es válida (mismo entorno, protocolo, opciones y `.jar` para los tres); los valores
  absolutos serían menores en el Mac. Para repetir en el Mac: `caffeinate -dims python3 experimento/ejecutar.py`
  (unos 20–25 min) y regenerar clasificación, gráficos e informe.

**Problema de medición de memoria resuelto (D6.8):**
- **Síntoma:** en la primera corrida, todas las ejecuciones marcaban 174 MB.
- **Causa:** en Linux, el `ru_maxrss` que entrega `wait4` para un proceso hijo arranca en la memoria que tenía el
  padre cuando lo creó con `fork`. El contador de memoria máxima se conserva al hacer `exec`. El orquestador en
  Python había cargado completo el archivo de un millón de vuelos.
- **Solución:** leer los archivos por partes (huellas SHA-256 por bloques y conteo de líneas en flujo). El
  orquestador quedó en 20 MB, menos que cualquier JVM, y esa cifra se registra en `entorno.txt`.
- Se descartó la corrida y se repitió completa.

**Otros problemas resueltos durante la implementación:**
- Diferencias de redondeo con números de punto flotante: resueltas con la aritmética entera del contrato.
- Distinta definición de `trim` en Clojure (`clojure.string/trim` usa `Character/isWhitespace`): resuelta usando
  `(.trim s)`.
- Formato de salida dependiente del sistema: la pantalla se escribe en bytes UTF-8 en los tres.
- Calibración del aeropuerto: P03 se alargó a 2.900 m para que P01 no fuera el único cuello de botella de los
  despegues pesados.
- Conflictos de nombres en Java: se usó `OperacionAsignada` (no `Operacion`, que es el enum) y `Falla` (no
  `Error`, que choca con `java.lang.Error`).
- En `ejecutar.py` se corrigió una ronda inicial mal numerada en el modo de prueba y se agregaron las huellas de
  los `.jar` a `entorno.txt`.

---

## 17. Estructura del repositorio y de la entrega

```
simulador-aeroportuario/
├── README.md                     resultado, cómo ejecutar, estado por bloques
├── .run/Verificar.run.xml        configuración de IntelliJ
├── java/      src/simulador/*.java (7 módulos) + construir.sh
├── scala/     src/simulador/*.scala (7 módulos) + project.scala + construir.sh
├── clojure/   src/simulador/*.clj (7 módulos) + project.clj + construir.sh
├── datos/
│   ├── aeropuerto/pistas.csv     aeropuerto común (6 pistas)
│   ├── ejemplo/                  E0 + esperado/ (resuelto a mano)
│   ├── escenarios/               V1, V2 (+ esperado/) y huellas.sha256; V3, V4, C1, X1 se regeneran
│   ├── robustez/R01..R12/        caso.txt + entradas + esperado/
│   └── generador.py
├── experimento/  referencia.py, verificar.sh, ejecutar.py, fuentes.py, calidad.py, funcional.py,
│                 clasificar.py, graficos.py
├── resultados/   crudos/*.csv, entorno.txt, verificacion.csv, resumen.md, calidad.csv, funcional.csv,
│                 consolidado.csv, puntajes.csv, clasificacion.md, graficos/*.png
├── informe/      generar_informe.py, contenido.py, resultados.py, construir_docx.js
├── entrega/      Informe_tecnico.docx
├── herramientas/ instalar_entorno.sh, mantener_activo.sh, entorno.sh
└── docs/         00 método, 01 requerimientos, 02 contrato, 03 experimento, 04 criterios, decisiones,
                  06 documento de estudio, 07 guion, 08 este documento, diagramas/
```

Carpeta de entrega (`~/Downloads/Final_Paradigmas_Simulador_Aeroportuario/`):
- `Entregables/`, con las carpetas:
  - `11_Proyectos_fuente` (incluye `ejecutables/`);
  - `12_Escenarios_y_datos`;
  - `13_Evidencias_rendimiento_y_recursos`;
  - `14_Consolidacion_y_clasificacion`;
  - `15_Informe_tecnico` (`.docx` y `.pdf`, 18 páginas, 8 figuras);
  - `16_Sustentacion`;
  - `Documentacion_del_diseno`.
- `simulador-aeroportuario/` (repositorio).
- `Documento_de_estudio.md`.
- `Guion_de_exposicion.md`.
- `LEEME.md`.

---

## 18. Cómo ejecutar todo

```bash
bash experimento/verificar.sh                  # construye y verifica (19 casos con los escenarios grandes)
SIN_CONSTRUIR=1 bash experimento/verificar.sh  # usa los .jar existentes
python3 datos/generador.py V3 V4 C1 X1         # regenera los escenarios grandes
caffeinate -dims python3 experimento/ejecutar.py --prueba   # prueba (1 ronda de V1 y V2)
caffeinate -dims python3 experimento/ejecutar.py            # medición completa
python3 experimento/calidad.py
python3 experimento/funcional.py
python3 experimento/clasificar.py
python3 experimento/graficos.py
python3 informe/generar_informe.py
java -jar java/simulador-java.jar datos/ejemplo/pistas.csv datos/ejemplo/vuelos.csv salida
java -jar java/simulador-java.jar <pistas> <vuelos> <salida> --medir medicion.csv
```

---

## 19. Preguntas frecuentes de la sustentación (con respuestas)

**¿Por qué Clojure y no Python, Haskell o Racket?**
Porque es funcional de verdad y corre en la misma JVM que Java y Scala. Con Python (interpretado) o Haskell
(compilado a código nativo) se compararían plataformas y no lenguajes: cambiarían el recolector de basura, el
compilador y la forma de medir la memoria.

**¿Cómo saben que los tres programas hacen exactamente lo mismo?**
Por el contrato común y la verificación byte a byte: los tres producen archivos idénticos en los 19 casos
(`verificar.sh` con `cmp`). Además, cada una de las 180 ejecuciones medidas se comprobó con SHA-256.

**¿Qué es el oráculo y por qué está en Python?**
Es la implementación de referencia que define la salida correcta. Está en otro lenguaje y sin restricciones
funcionales para que sea lo más directa posible y no comparta errores con las versiones evaluadas. No compite.
Coincide con el ejemplo resuelto a mano.

**¿Por qué 12 filas?**
2 operaciones × 3 categorías × 2 prioridades. Todos los vuelos de una fila sirven en las mismas pistas, así que
basta mirar el primero de cada fila (demostración en 7.2).

**¿Por qué simulación por eventos?**
Porque el costo depende del número de vuelos y no de la duración. V4 cubre 668 días (961.920 minutos), pero
tiene como mucho 2 millones de eventos (llegada y liberación de pista por vuelo), y muchos coinciden en el
mismo minuto.

**¿Cómo se simula sin ciclos?**
Con una secuencia perezosa de estados inmutables: `iterate` + `takeWhile` + `flatMap`. Dentro de un minuto se
usa recursión con profundidad máxima igual al número de pistas.

**¿Cómo detectan códigos repetidos sin un conjunto mutable?**
Con el "dueño" de cada código (7.7): agrupar los registros sin errores por código y tomar la línea mínima.

**¿Cómo se manejan los errores sin excepciones?**
Como valores: `Optional`/`Ok`/`Falla` en Java, `Option`/`Either` en Scala, `nil`/`{:ok}`/`{:falla}` en
Clojure. Un archivo inexistente se detecta antes de abrirlo (código 2).

**¿Por qué Java permite `throws`?**
Porque Java obliga a declarar las excepciones comprobadas de E/S. Declararlas no es manejarlas: no hay `try`,
`catch` ni `throw`.

**¿Por qué un proceso nuevo por ejecución y no medir con la JVM caliente?**
Porque así se usa un programa de consola, y el arranque y el JIT son parte de su costo real. Para separar el
efecto se reportan dos tiempos: `t_operaciones` (dentro) y `t_proceso` (todo).

**¿Por qué la mediana?**
Porque es robusta frente a valores atípicos.

**¿Por qué el orden rotado?**
Es contrabalanceo: ningún lenguaje se beneficia o perjudica por ir siempre primero o último.

**¿Por qué Java fue el más rápido si Scala y Clojure también compilan a bytecode?**
Los tres corren en la misma JVM, pero generan bytecode y estructuras distintas. Java usa `record` con campos
primitivos (`long`, `int`) y sus Streams y colectores son muy eficientes; además arranca más rápido.
- Scala está muy cerca y es mejor en la simulación.
- Clojure paga su tipado dinámico (números en objetos, búsqueda por palabra clave) y la inicialización de su
  núcleo.

**¿Por qué Clojure fue el más rápido en V1 dentro del programa?**
Explicación más probable: costo de primer uso de las lambdas en Java/Scala (`invokedynamic`) frente a funciones
precompiladas en Clojure (AOT). La inicialización del núcleo de Clojure ocurre antes de medir. En el proceso
completo Clojure es el más lento en V1 (838 ms frente a 365 de Java).

**¿Por qué la memoria es de 3–4 GB en V4?**
Se mide la memoria física máxima del proceso. Con `-Xmx4g`, G1 deja crecer el montículo antes de recolectar.
Afecta igual a los tres.

**¿Por qué Scala usa menos memoria que Java en escenarios medianos?**
Explicación probable: sus `Vector` persistentes comparten estructura al actualizar el estado, mientras que Java
crea listas completas nuevas en cada asignación (más basura y más crecimiento del montículo). En V4 la
diferencia se invierte ligeramente.

**¿Por qué Clojure salió último si es el más funcional?**
Porque el 65 % del peso es velocidad y recursos. En confiabilidad empata. En uso funcional su densidad por línea
es menor y no usa tipos `Option` (usa `nil`), así que no suma en la categoría Opcionales. Además, las reglas F1–F4
le prohíben sus optimizaciones típicas (`transient`).

**¿El resultado depende de los pesos?**
En parte: Java gana en 6 de 7 variantes; sin Rendimiento gana Scala por 0,96 puntos. Clojure es tercero en
todas.

**¿Por qué no usaron SonarQube para la calidad?**
Porque no analiza Clojure. Usarlo solo en dos lenguajes favorecería al del analizador menos estricto. Se usaron
tres métricas comunes (líneas, decisiones cada 100 líneas, duplicación).

**¿Por qué el puntaje proporcional y no mín–máx?**
El mín–máx le da 0 al último aunque esté a 1 % del primero; con tres lenguajes exagera las diferencias.

**¿Por qué los decimales con enteros?**
Para que el redondeo y el formato sean idénticos en los tres, sin depender de `double` ni de la configuración
regional. Fórmula: `c = (200a + b) div 2b`.

**¿Dónde se midió y es válido?**
En un contenedor Linux de 2 núcleos con OpenJDK 21, usando los mismos `.jar` construidos en el Mac. Es válido
porque los tres se midieron en las mismas condiciones; los valores absolutos cambian de equipo a equipo. Es
reproducible con una orden.

**¿Qué fue lo más difícil?**
- Garantizar la equivalencia byte a byte (`trim`, UTF-8, decimales, orden de textos).
- Expresar la simulación sin ciclos ni estado mutable.
- Medir la memoria correctamente (problema de `ru_maxrss` heredado; sección 16).

**¿Qué mejorarían?**
- Repetir la medición en el Mac y en más equipos.
- Medir también con la JVM caliente (por ejemplo con JMH) para separar el arranque.
- Agregar las advertencias de Scala, `clj-kondo` y SonarQube.
- Probar opciones de memoria más ajustadas.

**¿Qué es la densidad funcional?**
Operaciones funcionales contadas cada 100 líneas de código. Mide qué parte del código es estilo funcional
frente al código que el lenguaje obliga a escribir.

**¿Qué significa que el primer lugar sea "estrecho"?**
Que la diferencia (1,90 puntos) es pequeña frente a cambios razonables de pesos: sin el criterio de
Rendimiento, el orden de los dos primeros se invierte.

---

## 20. Glosario

- **AOT (ahead-of-time):** compilar antes de ejecutar. En Clojure, el `.jar` trae clases ya compiladas.
- **Bytecode:** instrucciones de la JVM, independientes del procesador.
- **Calentamiento (warm-up):** ejecuciones iniciales más lentas mientras la JVM carga clases y compila con JIT.
- **Clausura (closure):** función que captura variables de su entorno.
- **Complejidad ciclomática:** número de caminos independientes de un programa (1 + decisiones).
- **Contrabalanceo:** rotar el orden de los tratamientos para que el orden no sesgue el resultado.
- **Contrato:** especificación exacta de entradas, salidas y formatos que deben cumplir las tres versiones.
- **Determinismo:** mismas entradas, misma salida.
- **Either:** tipo con dos casos: `Left` (error) o `Right` (valor).
- **Evaluación perezosa:** calcular un valor solo cuando se necesita.
- **Evento discreto:** instante en que cambia el estado del sistema (llega un vuelo, se libera una pista).
- **Función de orden superior:** recibe o devuelve funciones.
- **Función pura:** misma salida para la misma entrada y sin efectos secundarios.
- **G1:** recolector de basura por regiones de la JVM (`-XX:+UseG1GC`).
- **Huella SHA-256:** resumen criptográfico de un archivo; si cambia un byte, cambia la huella.
- **Inmutable:** que no cambia después de creado.
- **`invokedynamic`:** instrucción de la JVM que se usa para crear lambdas en tiempo de ejecución.
- **JIT (just-in-time):** compilación a código máquina durante la ejecución (niveles C1 y C2).
- **Materialización:** forzar que una secuencia perezosa se calcule completa.
- **Mediana:** valor central de las mediciones ordenadas.
- **Montículo (heap):** memoria donde la JVM guarda los objetos.
- **`nil`-punning:** en Clojure, usar `nil` como "falso" o "nada" en lugar de un tipo `Option`.
- **Optional / Option:** contenedor de "un valor o nada".
- **Oráculo de pruebas:** fuente que define la salida correcta (aquí, `referencia.py`).
- **Persistente (estructura):** inmutable que comparte partes con la versión anterior al "modificarse".
- **Puntaje proporcional al mejor:** el mejor obtiene 100 y los demás su proporción.
- **Rango intercuartílico (RIC):** Q3 − Q1; mide la dispersión del 50 % central.
- **Recursión de cola:** llamada recursiva que es lo último que hace la función; se puede convertir en salto
  (`@tailrec`, `recur`). Java no lo hace.
- **Reflexión:** resolver en tiempo de ejecución qué método llamar; lento.
- **RSS (resident set size):** memoria física que ocupa un proceso.
- **`ru_maxrss`:** el máximo de RSS que informa el sistema operativo para un proceso.
- **Tipo sellado (sealed):** jerarquía cerrada de casos conocidos por el compilador.
- **Transductor:** en Clojure, transformación componible (`map`, `filter`, `take-while`…) independiente de la
  colección, que procesa sin crear secuencias intermedias.
- **Transparencia referencial:** poder reemplazar una expresión por su valor sin cambiar el programa.

---

## Anexo A · Código completo de Java

Orden de lectura recomendado: Modelo → Lectura → Validacion → TorreControl → Reportes → Medicion → Main.

### `java/src/simulador/Modelo.java`

```java
package simulador;

import java.util.Arrays;
import java.util.List;
import java.util.Optional;

// =============================================================================
//  MÓDULO 1 · MODELO
//  Entidades del aeropuerto como datos inmutables (record) y listas cerradas (enum).
//  Un record no tiene "setters": para "cambiar" un dato se crea uno nuevo.
// =============================================================================
public final class Modelo {

    private Modelo() { }

    // ---------- Listas cerradas. El nombre de cada valor es el texto exacto del contrato.

    /** Categoría del avión con sus requisitos (RN02). */
    public enum Categoria {
        Ligero(1200, 2), Mediano(2000, 3), Pesado(2800, 4);

        public final int longitudMinima;
        public final int minutosOcupacion;

        Categoria(int longitudMinima, int minutosOcupacion) {
            this.longitudMinima = longitudMinima;
            this.minutosOcupacion = minutosOcupacion;
        }
    }

    public enum Operacion { Despegue, Aterrizaje }

    public enum Uso { Despegue, Aterrizaje, Mixta }

    public enum Estado { Operativa, Cerrada }

    public enum Prioridad { Normal, Emergencia }

    /** Los textos válidos de una lista cerrada, en su orden ("Ligero", "Mediano", "Pesado"). */
    public static List<String> nombres(Enum<?>[] valores) {
        return Arrays.stream(valores).map(Enum::name).toList();
    }

    // ---------- Entidades del proyecto

    public record Avion(String matricula, Categoria categoria) { }

    /** programado: minuto absoluto = (día - 1) * 1440 + HH * 60 + MM. */
    public record Vuelo(String codigo, String aerolinea, Avion avion, Operacion operacion,
                        long programado, Prioridad prioridad) { }

    public record Pista(String id, int longitud, Uso uso, Estado estado) { }

    /** Resultado de la torre: qué vuelo usa qué pista y cuándo. */
    public record OperacionAsignada(Vuelo vuelo, Pista pista, long inicio, long fin) {
        public long retraso() {
            return inicio - vuelo.programado();
        }
    }

    public record NoAsignable(Vuelo vuelo, String motivo) { }

    /**
     * Estado de la simulación en un minuto. Es inmutable: cada paso crea uno nuevo.
     * cabezas: posición del primer vuelo pendiente de cada fila; libres: minuto en que se libera cada pista.
     */
    public record Aeropuerto(long minuto, List<Integer> cabezas, List<Long> libres,
                             List<OperacionAsignada> asignadasEnElPaso) { }

    // ---------- Lectura y validación

    /** Una línea de datos del archivo: su número de línea física y sus campos. */
    public record Registro(int linea, List<String> campos) { }

    public record ErrorRegistro(String archivo, int linea, String motivo) { }

    /** Resultado de validar un registro: Ok con el dato, o Falla con el error (Java no trae Either). */
    public sealed interface Resultado<T> permits Ok, Falla { }

    public record Ok<T>(T valor) implements Resultado<T> { }

    public record Falla<T>(ErrorRegistro error) implements Resultado<T> { }

    /** Optional con el mensaje si la condición se cumple; vacío si no. */
    public static Optional<String> si(boolean condicion, String mensaje) {
        return condicion ? Optional.of(mensaje) : Optional.empty();
    }
}
```

### `java/src/simulador/Lectura.java`

```java
package simulador;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Arrays;
import java.util.List;
import java.util.stream.IntStream;

import simulador.Modelo.Registro;

// =============================================================================
//  MÓDULO 2 · LECTURA
//  Archivo -> líneas -> registros (número de línea + campos). Solo transforma texto.
// =============================================================================
public final class Lectura {

    private Lectura() { }

    /** ¿Existe el archivo y se puede leer? (se revisa antes de leer, para no depender de excepciones) */
    public static boolean sePuedeLeer(Path ruta) {
        return Files.isRegularFile(ruta) && Files.isReadable(ruta);
    }

    /** Todas las líneas del archivo. Un byte UTF-8 inválido se convierte en U+FFFD, sin error. */
    public static List<String> leerLineas(Path ruta) throws IOException {
        return List.of(new String(Files.readAllBytes(ruta), StandardCharsets.UTF_8).split("\n", -1));
    }

    /**
     * Registros de datos: se salta el encabezado (línea 1) y las líneas vacías.
     * split(",", -1) conserva los campos vacíos del final; trim() es el de la JVM.
     */
    public static List<Registro> registros(List<String> lineas) {
        return IntStream.range(1, lineas.size())
                .filter(i -> !lineas.get(i).trim().isEmpty())
                .mapToObj(i -> new Registro(i + 1, Arrays.stream(lineas.get(i).split(",", -1))
                        .map(String::trim)
                        .toList()))
                .toList();
    }
}
```

### `java/src/simulador/Validacion.java`

```java
package simulador;

import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.function.Function;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.util.stream.Collectors;
import java.util.stream.Stream;

import simulador.Modelo.Avion;
import simulador.Modelo.Categoria;
import simulador.Modelo.ErrorRegistro;
import simulador.Modelo.Estado;
import simulador.Modelo.Falla;
import simulador.Modelo.Ok;
import simulador.Modelo.Operacion;
import simulador.Modelo.Pista;
import simulador.Modelo.Prioridad;
import simulador.Modelo.Registro;
import simulador.Modelo.Resultado;
import simulador.Modelo.Uso;
import simulador.Modelo.Vuelo;

import static simulador.Modelo.si;

// =============================================================================
//  MÓDULO 3 · VALIDACIÓN (RF03)
//  Cada registro se convierte en Ok(dato) o Falla(error). Las reglas se revisan en el
//  orden de las columnas y se reporta solo el primer error (cadena de Optional.or).
// =============================================================================
public final class Validacion {

    private Validacion() { }

    private static final Pattern ENTERO = Pattern.compile("-?[0-9]{1,9}");
    private static final Pattern HORA = Pattern.compile("([0-9]{2}):([0-9]{2})");

    /** Revisión de un registro: error previo a la unicidad y error de sus demás campos. */
    private record Revision(Registro registro, Optional<String> previo, Optional<String> deCampos) {
        String clave() {
            return registro.campos().get(0);
        }
    }

    // ---------- Reglas reutilizables

    private static Optional<String> entero(String valor, String campo) {
        return si(!ENTERO.matcher(valor).matches(), campo + " no es un entero: " + valor);
    }

    private static Optional<String> opcion(String valor, String campo, List<String> opciones) {
        return si(!opciones.contains(valor),
                campo + " con valor no válido: " + valor + " (valores: " + String.join("/", opciones) + ")");
    }

    private static Optional<String> hora(String valor) {
        Matcher partes = HORA.matcher(valor);
        boolean valida = partes.matches()
                && Integer.parseInt(partes.group(1)) <= 23
                && Integer.parseInt(partes.group(2)) <= 59;
        return si(!valida, "hora no válida: " + valor + " (formato HH:MM de 00:00 a 23:59)");
    }

    // ---------- Reglas de cada archivo (después del número de campos y la clave)

    private static Optional<String> reglasPista(List<String> c) {
        return entero(c.get(1), "longitud")
                .or(() -> si(Integer.parseInt(c.get(1)) <= 0, "longitud debe ser mayor que 0: " + c.get(1)))
                .or(() -> opcion(c.get(2), "uso", Modelo.nombres(Uso.values())))
                .or(() -> opcion(c.get(3), "estado", Modelo.nombres(Estado.values())));
    }

    private static Optional<String> reglasVuelo(List<String> c) {
        return si(c.get(1).isEmpty(), "aerolínea vacía")
                .or(() -> si(c.get(2).isEmpty(), "matrícula vacía"))
                .or(() -> opcion(c.get(3), "categoría", Modelo.nombres(Categoria.values())))
                .or(() -> opcion(c.get(4), "operación", Modelo.nombres(Operacion.values())))
                .or(() -> entero(c.get(5), "día"))
                .or(() -> si(Integer.parseInt(c.get(5)) < 1 || Integer.parseInt(c.get(5)) > 9999,
                        "día debe estar entre 1 y 9999: " + c.get(5)))
                .or(() -> hora(c.get(6)))
                .or(() -> opcion(c.get(7), "prioridad", Modelo.nombres(Prioridad.values())));
    }

    // ---------- Construcción de las entidades (solo con campos ya validados)

    private static Pista construirPista(List<String> c) {
        return new Pista(c.get(0), Integer.parseInt(c.get(1)), Uso.valueOf(c.get(2)), Estado.valueOf(c.get(3)));
    }

    private static Vuelo construirVuelo(List<String> c) {
        long minuto = (Integer.parseInt(c.get(5)) - 1) * 1440L
                + Integer.parseInt(c.get(6).substring(0, 2)) * 60L
                + Integer.parseInt(c.get(6).substring(3, 5));
        return new Vuelo(c.get(0), c.get(1), new Avion(c.get(2), Categoria.valueOf(c.get(3))),
                Operacion.valueOf(c.get(4)), minuto, Prioridad.valueOf(c.get(7)));
    }

    // ---------- Validación genérica

    /**
     * Valida todos los registros de un archivo.
     * Unicidad: un registro está "repetido" si un registro VÁLIDO anterior tiene su misma clave.
     * El dueño de cada clave es el primer registro sin errores propios (groupBy + mínimo), así no hace
     * falta recorrer el archivo con estado: el resultado es el mismo que validar línea por línea.
     */
    private static <T> List<Resultado<T>> validar(List<Registro> registros, String archivo, int numCampos,
                                                  String nombreClave,
                                                  Function<List<String>, Optional<String>> reglas,
                                                  Function<List<String>, T> construir) {
        List<Revision> revisiones = registros.stream()
                .map(r -> revisar(r, numCampos, nombreClave, reglas))
                .toList();
        Map<String, Integer> duenos = revisiones.stream()
                .filter(v -> v.previo().isEmpty() && v.deCampos().isEmpty())
                .collect(Collectors.toMap(Revision::clave, v -> v.registro().linea(), Math::min));
        return revisiones.stream()
                .map(v -> resultado(v, duenos, archivo, nombreClave, construir))
                .toList();
    }

    private static Revision revisar(Registro r, int numCampos, String nombreClave,
                                    Function<List<String>, Optional<String>> reglas) {
        Optional<String> previo = si(r.campos().size() != numCampos,
                "se esperaban " + numCampos + " campos y hay " + r.campos().size())
                .or(() -> si(r.campos().get(0).isEmpty(), nombreClave + " vacío"));
        return new Revision(r, previo, previo.isPresent() ? Optional.empty() : reglas.apply(r.campos()));
    }

    private static <T> Resultado<T> resultado(Revision v, Map<String, Integer> duenos, String archivo,
                                              String nombreClave, Function<List<String>, T> construir) {
        Optional<String> error = v.previo()
                .or(() -> si(duenos.getOrDefault(v.clave(), Integer.MAX_VALUE) < v.registro().linea(),
                        nombreClave + " repetido: " + v.clave()))
                .or(v::deCampos);
        return error.<Resultado<T>>map(m -> new Falla<>(new ErrorRegistro(archivo, v.registro().linea(), m)))
                .orElseGet(() -> new Ok<>(construir.apply(v.registro().campos())));
    }

    public static List<Resultado<Pista>> validarPistas(List<Registro> registros) {
        return validar(registros, "pistas", 4, "id", Validacion::reglasPista, Validacion::construirPista);
    }

    public static List<Resultado<Vuelo>> validarVuelos(List<Registro> registros) {
        return validar(registros, "vuelos", 8, "código", Validacion::reglasVuelo, Validacion::construirVuelo);
    }

    // ---------- Separar válidos y errores

    public static <T> List<T> validos(List<Resultado<T>> resultados) {
        return resultados.stream()
                .flatMap(r -> r instanceof Ok<T> ok ? Stream.of(ok.valor()) : Stream.<T>empty())
                .toList();
    }

    public static <T> List<ErrorRegistro> errores(List<Resultado<T>> resultados) {
        return resultados.stream()
                .flatMap(r -> r instanceof Falla<T> falla ? Stream.of(falla.error()) : Stream.<ErrorRegistro>empty())
                .toList();
    }
}
```

### `java/src/simulador/TorreControl.java`

```java
package simulador;

import java.util.Comparator;
import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;
import java.util.stream.IntStream;
import java.util.stream.Stream;

import simulador.Modelo.Aeropuerto;
import simulador.Modelo.Estado;
import simulador.Modelo.NoAsignable;
import simulador.Modelo.Operacion;
import simulador.Modelo.OperacionAsignada;
import simulador.Modelo.Pista;
import simulador.Modelo.Prioridad;
import simulador.Modelo.Uso;
import simulador.Modelo.Vuelo;

import static simulador.Modelo.si;

// =============================================================================
//  MÓDULO 4 · TORRE DE CONTROL (RF04, RF05, RF06)
//  Funciones puras: reciben un Aeropuerto y devuelven uno nuevo. No guardan estado.
// =============================================================================
public final class TorreControl {

    private TorreControl() { }

    /** Un vuelo listo para operar y la pista libre que le tocaría. */
    private record Candidato(int fila, int pista, Vuelo vuelo) { }

    /** RN05: emergencia, luego aterrizaje, luego hora programada, luego código. */
    private static final Comparator<Vuelo> PRIORIDAD = Comparator
            .comparing((Vuelo v) -> v.prioridad() == Prioridad.Emergencia ? 0 : 1)
            .thenComparing(v -> v.operacion() == Operacion.Aterrizaje ? 0 : 1)
            .thenComparingLong(Vuelo::programado)
            .thenComparing(Vuelo::codigo);

    // ---------- Compatibilidad (RN03) y vuelos no asignables (RN09)

    private static boolean habilitada(Vuelo v, Pista p) {
        return p.estado() == Estado.Operativa
                && (p.uso() == Uso.Mixta || p.uso().name().equals(v.operacion().name()));
    }

    private static boolean compatible(Vuelo v, Pista p) {
        return habilitada(v, p) && p.longitud() >= v.avion().categoria().longitudMinima;
    }

    private static Optional<String> motivoNoAsignable(Vuelo v, List<Pista> pistas) {
        return si(pistas.stream().noneMatch(p -> habilitada(v, p)), "sin pista habilitada para la operación")
                .or(() -> si(pistas.stream().noneMatch(p -> compatible(v, p)), "sin pista con longitud suficiente"));
    }

    public static List<NoAsignable> noAsignables(List<Vuelo> vuelos, List<Pista> pistas) {
        return vuelos.stream()
                .flatMap(v -> motivoNoAsignable(v, pistas).map(m -> new NoAsignable(v, m)).stream())
                .toList();
    }

    public static List<Vuelo> asignables(List<Vuelo> vuelos, List<Pista> pistas) {
        return vuelos.stream().filter(v -> motivoNoAsignable(v, pistas).isEmpty()).toList();
    }

    // ---------- Preparación: 12 filas por (operación, categoría, prioridad)

    /** Todos los vuelos de una fila son compatibles con las mismas pistas: basta mirar el primero. */
    private static List<List<Vuelo>> filas(List<Vuelo> asignables) {
        return asignables.stream()
                .collect(Collectors.groupingBy(v -> v.operacion() + "|" + v.avion().categoria() + "|" + v.prioridad()))
                .values().stream()
                .map(fila -> fila.stream()
                        .sorted(Comparator.comparingLong(Vuelo::programado).thenComparing(Vuelo::codigo))
                        .toList())
                .toList();
    }

    // ---------- Un paso de la simulación

    private static boolean quedanVuelos(Aeropuerto a, List<List<Vuelo>> filas, int fila) {
        return a.cabezas().get(fila) < filas.get(fila).size();
    }

    private static Vuelo primero(Aeropuerto a, List<List<Vuelo>> filas, int fila) {
        return filas.get(fila).get(a.cabezas().get(fila));
    }

    /** La pista libre y compatible de menor id (las pistas ya vienen ordenadas por id). */
    private static Optional<Integer> pistaLibre(Aeropuerto a, Vuelo v, List<Pista> pistas) {
        return IntStream.range(0, pistas.size()).boxed()
                .filter(j -> a.libres().get(j) <= a.minuto() && compatible(v, pistas.get(j)))
                .findFirst();
    }

    /** Entre los primeros de cada fila que ya esperan y tienen pista libre, el de mayor prioridad. */
    private static Optional<Candidato> mejorCandidato(Aeropuerto a, List<List<Vuelo>> filas, List<Pista> pistas) {
        return IntStream.range(0, filas.size()).boxed()
                .filter(i -> quedanVuelos(a, filas, i))
                .filter(i -> primero(a, filas, i).programado() <= a.minuto())
                .flatMap(i -> pistaLibre(a, primero(a, filas, i), pistas)
                        .map(j -> new Candidato(i, j, primero(a, filas, i))).stream())
                .min(Comparator.comparing(Candidato::vuelo, PRIORIDAD));
    }

    /** Copia de la lista con un elemento cambiado (las listas no se modifican). */
    private static <T> List<T> reemplazar(List<T> lista, int indice, T valor) {
        return IntStream.range(0, lista.size()).mapToObj(k -> k == indice ? valor : lista.get(k)).toList();
    }

    private static Aeropuerto asignar(Aeropuerto a, Candidato c, List<Pista> pistas) {
        long fin = a.minuto() + c.vuelo().avion().categoria().minutosOcupacion;
        OperacionAsignada operacion = new OperacionAsignada(c.vuelo(), pistas.get(c.pista()), a.minuto(), fin);
        return new Aeropuerto(a.minuto(),
                reemplazar(a.cabezas(), c.fila(), a.cabezas().get(c.fila()) + 1),
                reemplazar(a.libres(), c.pista(), fin),
                Stream.concat(a.asignadasEnElPaso().stream(), Stream.of(operacion)).toList());
    }

    /** Asigna en el minuto actual mientras haya candidato. Cada asignación ocupa una pista: como mucho k niveles. */
    private static Aeropuerto asignarEnMinuto(Aeropuerto a, List<List<Vuelo>> filas, List<Pista> pistas) {
        return mejorCandidato(a, filas, pistas)
                .map(c -> asignarEnMinuto(asignar(a, c, pistas), filas, pistas))
                .orElse(a);
    }

    /** Siguiente evento: el menor minuto futuro en que se libera una pista o llega un vuelo. */
    private static long siguienteMinuto(Aeropuerto a, List<List<Vuelo>> filas) {
        return Stream.concat(
                        a.libres().stream(),
                        IntStream.range(0, filas.size()).boxed()
                                .filter(i -> quedanVuelos(a, filas, i))
                                .map(i -> primero(a, filas, i).programado()))
                .filter(t -> t > a.minuto())
                .min(Long::compare)
                .orElse(a.minuto());
    }

    private static Aeropuerto paso(Aeropuerto a, List<List<Vuelo>> filas, List<Pista> pistas) {
        Aeropuerto tras = asignarEnMinuto(new Aeropuerto(a.minuto(), a.cabezas(), a.libres(), List.of()), filas, pistas);
        return new Aeropuerto(siguienteMinuto(tras, filas), tras.cabezas(), tras.libres(), tras.asignadasEnElPaso());
    }

    private static boolean terminado(Aeropuerto a, List<List<Vuelo>> filas) {
        return a.asignadasEnElPaso().isEmpty()
                && IntStream.range(0, filas.size()).noneMatch(i -> quedanVuelos(a, filas, i));
    }

    // ---------- Simulación completa

    /** Secuencia perezosa de estados: iterate -> takeWhile -> flatMap de las asignaciones de cada paso. */
    public static List<OperacionAsignada> simular(List<Vuelo> asignables, List<Pista> pistas) {
        List<Pista> operativas = pistas.stream()
                .filter(p -> p.estado() == Estado.Operativa)
                .sorted(Comparator.comparing(Pista::id))
                .toList();
        List<List<Vuelo>> filas = filas(asignables);
        Aeropuerto inicial = new Aeropuerto(
                filas.stream().mapToLong(f -> f.get(0).programado()).min().orElse(0L),
                filas.stream().map(f -> 0).toList(),
                operativas.stream().map(p -> 0L).toList(),
                List.of());
        return Stream.iterate(inicial, a -> !terminado(a, filas), a -> paso(a, filas, operativas))
                .flatMap(a -> a.asignadasEnElPaso().stream())
                .toList();
    }
}
```

### `java/src/simulador/Reportes.java`

```java
package simulador;

import java.util.Comparator;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;
import java.util.stream.IntStream;
import java.util.stream.Stream;

import simulador.Modelo.Categoria;
import simulador.Modelo.ErrorRegistro;
import simulador.Modelo.NoAsignable;
import simulador.Modelo.Operacion;
import simulador.Modelo.OperacionAsignada;
import simulador.Modelo.Pista;

// =============================================================================
//  MÓDULO 5 · REPORTES (RF07 a RF14)
//  Construye el texto de los tres archivos de salida. Los decimales se calculan con
//  aritmética entera exacta (centésimas redondeadas HALF_UP), sin números de punto flotante.
// =============================================================================
public final class Reportes {

    private Reportes() { }

    private static final String SIN_DATOS = "Sin datos";
    private static final int UMBRAL_RETRASO = 15;

    /** Totales por aerolínea para RF11: el promedio es suma / cantidad. */
    private record Aerolinea(String nombre, long suma, long cantidad) { }

    /** Todo lo que necesitan los reportes. */
    public record Datos(int registrosPistas, List<Pista> pistas, List<ErrorRegistro> erroresPistas,
                        int registrosVuelos, int vuelosValidos, List<ErrorRegistro> erroresVuelos,
                        List<OperacionAsignada> operaciones, List<NoAsignable> noAsignables) { }

    // ---------- Formato

    private static String dosDigitos(long x) {
        return x < 10 ? "0" + x : String.valueOf(x);
    }

    /** a / b con 2 decimales: c = (200a + b) div 2b son las centésimas redondeadas. */
    private static String decimal(long a, long b) {
        long c = (200 * a + b) / (2 * b);
        return c / 100 + "." + dosDigitos(c % 100);
    }

    private static String hora(long minuto) {
        return "D" + (minuto / 1440 + 1) + " " + dosDigitos(minuto % 1440 / 60) + ":" + dosDigitos(minuto % 60);
    }

    private static List<String> seccion(String titulo, List<String> lineas) {
        return Stream.concat(Stream.of("== " + titulo + " =="), Stream.concat(lineas.stream(), Stream.of(""))).toList();
    }

    private static List<String> oSinDatos(List<String> lineas, String vacio) {
        return lineas.isEmpty() ? List.of(vacio) : lineas;
    }

    // ---------- Archivos CSV

    /** RF07: una línea por operación, en el orden en que se asignaron. */
    public static String operacionesCsv(List<OperacionAsignada> operaciones) {
        return Stream.concat(
                        Stream.of("codigo,aerolinea,operacion,categoria,prioridad,pista,programada,inicio,fin,retraso"),
                        operaciones.stream().map(o -> String.join(",",
                                o.vuelo().codigo(), o.vuelo().aerolinea(), o.vuelo().operacion().name(),
                                o.vuelo().avion().categoria().name(), o.vuelo().prioridad().name(), o.pista().id(),
                                hora(o.vuelo().programado()), hora(o.inicio()), hora(o.fin()),
                                String.valueOf(o.retraso()))))
                .collect(Collectors.joining("\n", "", "\n"));
    }

    /** RF03: primero los errores de pistas y luego los de vuelos. */
    public static String erroresCsv(List<ErrorRegistro> errores) {
        return Stream.concat(Stream.of("archivo,linea,motivo"),
                        errores.stream().map(e -> e.archivo() + "," + e.linea() + "," + e.motivo()))
                .collect(Collectors.joining("\n", "", "\n"));
    }

    // ---------- Secciones del reporte

    private static List<String> rf03(Datos d) {
        return seccion("RF03 · Validación de datos", List.of(
                "Pistas | registros: " + d.registrosPistas() + " | válidos: " + d.pistas().size()
                        + " | inválidos: " + d.erroresPistas().size(),
                "Vuelos | registros: " + d.registrosVuelos() + " | válidos: " + d.vuelosValidos()
                        + " | inválidos: " + d.erroresVuelos().size(),
                "Detalle de los registros inválidos: errores.csv"));
    }

    private static long sumaRetrasos(List<OperacionAsignada> ops) {
        return ops.stream().mapToLong(OperacionAsignada::retraso).sum();
    }

    private static long retrasados(List<OperacionAsignada> ops) {
        return ops.stream().filter(o -> o.retraso() > UMBRAL_RETRASO).count();
    }

    private static String promedio(List<OperacionAsignada> ops) {
        return ops.isEmpty() ? SIN_DATOS : decimal(sumaRetrasos(ops), ops.size()) + " min";
    }

    private static String porcentajeRetrasados(List<OperacionAsignada> ops) {
        return ops.isEmpty() ? SIN_DATOS : decimal(100 * retrasados(ops), ops.size()) + "%";
    }

    private static List<String> rf08(List<OperacionAsignada> ops) {
        return seccion("RF08 · Resumen de retrasos", List.of(
                "Operaciones asignadas: " + ops.size(),
                "Retraso promedio: " + promedio(ops),
                "Retraso máximo: " + ops.stream().mapToLong(OperacionAsignada::retraso).max()
                        .stream().mapToObj(m -> m + " min").findFirst().orElse(SIN_DATOS),
                "Vuelos retrasados (más de " + UMBRAL_RETRASO + " min): "
                        + (ops.isEmpty() ? SIN_DATOS : retrasados(ops) + " (" + porcentajeRetrasados(ops) + ")")));
    }

    private static List<String> rf09(List<OperacionAsignada> ops) {
        List<OperacionAsignada> top = ops.stream()
                .sorted(Comparator.comparingLong(OperacionAsignada::retraso).reversed()
                        .thenComparing(o -> o.vuelo().codigo()))
                .limit(5)
                .toList();
        return seccion("RF09 · 5 vuelos más retrasados", oSinDatos(IntStream.range(0, top.size())
                .mapToObj(i -> (i + 1) + ". " + top.get(i).vuelo().codigo() + " | retraso: " + top.get(i).retraso()
                        + " min | " + top.get(i).vuelo().operacion().name() + " | " + top.get(i).pista().id())
                .toList(), SIN_DATOS));
    }

    private static List<String> rf10(List<OperacionAsignada> ops, List<Pista> pistas) {
        return seccion("RF10 · Uso de pistas", ops.isEmpty() || pistas.isEmpty() ? List.of(SIN_DATOS) : usoDePistas(ops, pistas));
    }

    private static List<String> usoDePistas(List<OperacionAsignada> ops, List<Pista> pistas) {
        long inicio = ops.stream().mapToLong(o -> o.vuelo().programado()).min().orElse(0L);
        long fin = ops.stream().mapToLong(OperacionAsignada::fin).max().orElse(0L);
        Map<String, List<OperacionAsignada>> porPista = ops.stream().collect(Collectors.groupingBy(o -> o.pista().id()));
        return Stream.concat(
                Stream.of("Período simulado: " + hora(inicio) + " a " + hora(fin) + " (" + (fin - inicio) + " min)"),
                pistas.stream().sorted(Comparator.comparing(Pista::id)).map(p -> {
                    List<OperacionAsignada> suyas = porPista.getOrDefault(p.id(), List.of());
                    long ocupada = suyas.stream().mapToLong(o -> o.fin() - o.inicio()).sum();
                    return p.id() + " | " + p.estado().name() + " | operaciones: " + suyas.size() + " | ocupada: "
                            + ocupada + " min | ocupación: " + decimal(100 * ocupada, fin - inicio) + "%";
                })).toList();
    }

    /** RF11: de mayor a menor promedio (comparando fracciones exactas); si empatan, por nombre. */
    private static List<Aerolinea> aerolineas(List<OperacionAsignada> ops) {
        return ops.stream()
                .collect(Collectors.groupingBy(o -> o.vuelo().aerolinea()))
                .entrySet().stream()
                .map(e -> new Aerolinea(e.getKey(), sumaRetrasos(e.getValue()), e.getValue().size()))
                .sorted((x, y) -> Long.compare(y.suma() * x.cantidad(), x.suma() * y.cantidad()) != 0
                        ? Long.compare(y.suma() * x.cantidad(), x.suma() * y.cantidad())
                        : x.nombre().compareTo(y.nombre()))
                .toList();
    }

    private static List<String> rf11(List<Aerolinea> lista) {
        return seccion("RF11 · Retraso promedio por aerolínea", oSinDatos(lista.stream()
                .map(a -> a.nombre() + " | retraso promedio: " + decimal(a.suma(), a.cantidad())
                        + " min | operaciones: " + a.cantidad())
                .toList(), SIN_DATOS));
    }

    private static List<String> rf12(List<NoAsignable> noAsignables) {
        return seccion("RF12 · Vuelos no asignables", oSinDatos(noAsignables.stream()
                .map(n -> n.vuelo().codigo() + " | " + n.vuelo().operacion().name() + " | "
                        + n.vuelo().avion().categoria().name() + " | " + n.motivo())
                .toList(), "Ninguno"));
    }

    private static List<String> rf13(List<OperacionAsignada> ops) {
        return seccion("RF13 · Operaciones por tipo y categoría", Stream.concat(
                Stream.of(Operacion.Aterrizaje, Operacion.Despegue)
                        .map(t -> t.name() + ": " + ops.stream().filter(o -> o.vuelo().operacion() == t).count()),
                Stream.of(Categoria.values())
                        .map(c -> c.name() + ": " + ops.stream().filter(o -> o.vuelo().avion().categoria() == c).count()))
                .toList());
    }

    private static String pistaMasUsada(List<OperacionAsignada> ops, List<Pista> pistas) {
        Map<String, Long> usos = ops.stream().collect(Collectors.groupingBy(o -> o.pista().id(), Collectors.counting()));
        return ops.isEmpty() ? SIN_DATOS : pistas.stream()
                .sorted(Comparator.comparing((Pista p) -> usos.getOrDefault(p.id(), 0L)).reversed()
                        .thenComparing(Pista::id))
                .findFirst()
                .map(p -> p.id() + " (operaciones: " + usos.getOrDefault(p.id(), 0L) + ")")
                .orElse(SIN_DATOS);
    }

    private static List<String> rf14(Datos d, List<Aerolinea> lista) {
        List<OperacionAsignada> ops = d.operaciones();
        return List.of(
                "== RF14 · Resumen ejecutivo ==",
                "Vuelos cargados: " + d.registrosVuelos(),
                "Vuelos válidos: " + d.vuelosValidos(),
                "Vuelos inválidos: " + d.erroresVuelos().size(),
                "Vuelos asignados: " + ops.size(),
                "Vuelos no asignables: " + d.noAsignables().size(),
                "Retraso promedio: " + promedio(ops),
                "Vuelos retrasados: " + porcentajeRetrasados(ops),
                "Pista más usada: " + pistaMasUsada(ops, d.pistas()),
                "Aerolínea con mayor retraso promedio: " + lista.stream().findFirst()
                        .map(a -> a.nombre() + " (" + decimal(a.suma(), a.cantidad()) + " min)")
                        .orElse(SIN_DATOS));
    }

    /** reporte.txt completo (RF03 y RF08 a RF14). */
    public static String reporte(Datos d) {
        List<Aerolinea> lista = aerolineas(d.operaciones());
        return Stream.of(
                        List.of("SIMULADOR DE OPERACIONES AEROPORTUARIAS · REPORTE", ""),
                        rf03(d), rf08(d.operaciones()), rf09(d.operaciones()), rf10(d.operaciones(), d.pistas()),
                        rf11(lista), rf12(d.noAsignables()), rf13(d.operaciones()), rf14(d, lista))
                .flatMap(List::stream)
                .collect(Collectors.joining("\n", "", "\n"));
    }
}
```

### `java/src/simulador/Medicion.java`

```java
package simulador;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;
import java.util.stream.Collectors;

// =============================================================================
//  MÓDULO 6 · MEDICIÓN (Bloque 3, sección 5)
//  Toma el tiempo de cada etapa con System.nanoTime() y, con --medir, lo escribe en un archivo.
//  Cada etapa devuelve su resultado ya calculado (regla de materialización).
// =============================================================================
public final class Medicion {

    private Medicion() { }

    public static final String ENCABEZADO = "lectura_ns,validacion_ns,simulacion_ns,reportes_ns,escritura_ns";

    /** Una etapa del programa. Puede leer o escribir archivos, por eso declara IOException. */
    @FunctionalInterface
    public interface Etapa<T> {
        T ejecutar() throws IOException;
    }

    /** Resultado de una etapa y lo que tardó, en nanosegundos. */
    public record Medido<T>(T valor, long ns) { }

    public static <T> Medido<T> medir(Etapa<T> etapa) throws IOException {
        long inicio = System.nanoTime();
        T valor = etapa.ejecutar();
        return new Medido<>(valor, System.nanoTime() - inicio);
    }

    /** Archivo de --medir: encabezado y una línea con las cinco duraciones. */
    public static void escribir(Path archivo, List<Long> duraciones) throws IOException {
        Files.writeString(archivo, ENCABEZADO + "\n"
                + duraciones.stream().map(String::valueOf).collect(Collectors.joining(",")) + "\n",
                StandardCharsets.UTF_8);
    }
}
```

### `java/src/simulador/Main.java`

```java
package simulador;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;
import java.util.Optional;
import java.util.stream.Stream;

import simulador.Medicion.Medido;
import simulador.Modelo.ErrorRegistro;
import simulador.Modelo.NoAsignable;
import simulador.Modelo.OperacionAsignada;
import simulador.Modelo.Pista;
import simulador.Modelo.Registro;
import simulador.Modelo.Resultado;
import simulador.Modelo.Vuelo;

// =============================================================================
//  MÓDULO 7 · PROGRAMA PRINCIPAL
//  Revisa los argumentos y encadena las cinco etapas: lectura -> validación -> simulación ->
//  reportes -> escritura. Toda la lógica está en los otros módulos; aquí solo se conectan.
// =============================================================================
public final class Main {

    private Main() { }

    private static final String USO =
            "Uso: java -jar simulador-<lenguaje>.jar <pistas.csv> <vuelos.csv> <carpeta_salida> [--medir <archivo>]";

    // ---------- Resultado de cada etapa

    private record Lineas(List<String> pistas, List<String> vuelos) { }

    private record Validados(int registrosPistas, List<Pista> pistas, List<ErrorRegistro> erroresPistas,
                             int registrosVuelos, List<Vuelo> vuelos, List<ErrorRegistro> erroresVuelos) { }

    private record Simulados(List<OperacionAsignada> operaciones, List<NoAsignable> noAsignables) { }

    private record Textos(String operaciones, String errores, String reporte) { }

    // ---------- Etapas

    private static Validados validar(Lineas lineas) {
        List<Registro> registrosPistas = Lectura.registros(lineas.pistas());
        List<Registro> registrosVuelos = Lectura.registros(lineas.vuelos());
        List<Resultado<Pista>> pistas = Validacion.validarPistas(registrosPistas);
        List<Resultado<Vuelo>> vuelos = Validacion.validarVuelos(registrosVuelos);
        return new Validados(registrosPistas.size(), Validacion.validos(pistas), Validacion.errores(pistas),
                registrosVuelos.size(), Validacion.validos(vuelos), Validacion.errores(vuelos));
    }

    private static Simulados simular(Validados v) {
        return new Simulados(
                TorreControl.simular(TorreControl.asignables(v.vuelos(), v.pistas()), v.pistas()),
                TorreControl.noAsignables(v.vuelos(), v.pistas()));
    }

    private static Textos reportar(Validados v, Simulados s) {
        return new Textos(
                Reportes.operacionesCsv(s.operaciones()),
                Reportes.erroresCsv(Stream.concat(v.erroresPistas().stream(), v.erroresVuelos().stream()).toList()),
                Reportes.reporte(new Reportes.Datos(v.registrosPistas(), v.pistas(), v.erroresPistas(),
                        v.registrosVuelos(), v.vuelos().size(), v.erroresVuelos(),
                        s.operaciones(), s.noAsignables())));
    }

    private static Path escribir(Path salida, Textos t) throws IOException {
        Files.createDirectories(salida);
        Files.writeString(salida.resolve("operaciones.csv"), t.operaciones(), StandardCharsets.UTF_8);
        Files.writeString(salida.resolve("errores.csv"), t.errores(), StandardCharsets.UTF_8);
        Files.writeString(salida.resolve("reporte.txt"), t.reporte(), StandardCharsets.UTF_8);
        imprimir(t.reporte());
        return salida;
    }

    /** Escribe en pantalla siempre en UTF-8, sin depender de la configuración regional del equipo. */
    private static void imprimir(String texto) {
        System.out.writeBytes(texto.getBytes(StandardCharsets.UTF_8));
        System.out.flush();
    }

    // ---------- Argumentos

    /** Motivo del error de uso, si lo hay: cantidad de argumentos o archivo de entrada ilegible. */
    private static Optional<String> problemaDeUso(String[] args) {
        return !(args.length == 3 || (args.length == 5 && args[3].equals("--medir")))
                ? Optional.of("número de argumentos incorrecto")
                : Stream.of(args[0], args[1])
                        .filter(ruta -> !Lectura.sePuedeLeer(Path.of(ruta)))
                        .findFirst()
                        .map(ruta -> "no se puede leer el archivo " + ruta);
    }

    private static void ejecutar(Path pistas, Path vuelos, Path salida, Optional<Path> archivoMedicion)
            throws IOException {
        Medido<Lineas> lectura = Medicion.medir(
                () -> new Lineas(Lectura.leerLineas(pistas), Lectura.leerLineas(vuelos)));
        Medido<Validados> validacion = Medicion.medir(() -> validar(lectura.valor()));
        Medido<Simulados> simulacion = Medicion.medir(() -> simular(validacion.valor()));
        Medido<Textos> reportes = Medicion.medir(() -> reportar(validacion.valor(), simulacion.valor()));
        Medido<Path> escritura = Medicion.medir(() -> escribir(salida, reportes.valor()));
        if (archivoMedicion.isPresent()) {
            Medicion.escribir(archivoMedicion.get(), List.of(lectura.ns(), validacion.ns(), simulacion.ns(),
                    reportes.ns(), escritura.ns()));
        }
    }

    public static void main(String[] args) throws IOException {
        Optional<String> problema = problemaDeUso(args);
        if (problema.isPresent()) {
            imprimir("ERROR: " + problema.get() + "\n" + USO + "\n");
            System.exit(2);
        } else {
            ejecutar(Path.of(args[0]), Path.of(args[1]), Path.of(args[2]),
                    args.length == 5 ? Optional.of(Path.of(args[4])) : Optional.empty());
        }
    }
}
```

---

## Anexo B · Código completo de Scala

### `scala/project.scala`

```scala
// Versión Scala del simulador. Se construye con: bash scala/construir.sh  (Scala CLI)
//> using scala 3.9.0
//> using options -deprecation -feature -Wunused:all
//> using mainClass simulador.Main
```

### `scala/src/simulador/Modelo.scala`

```scala
package simulador

// =============================================================================
//  MÓDULO 1 · MODELO
//  Entidades del aeropuerto como datos inmutables (case class) y listas cerradas (enum).
//  Una case class no se modifica: para "cambiar" un dato se crea otra con copy.
// =============================================================================

// ---------- Listas cerradas. El nombre de cada valor es el texto exacto del contrato.

/** Categoría del avión con sus requisitos (RN02). */
enum Categoria(val longitudMinima: Int, val minutosOcupacion: Int):
  case Ligero extends Categoria(1200, 2)
  case Mediano extends Categoria(2000, 3)
  case Pesado extends Categoria(2800, 4)

enum Operacion:
  case Despegue, Aterrizaje

enum Uso:
  case Despegue, Aterrizaje, Mixta

enum Estado:
  case Operativa, Cerrada

enum Prioridad:
  case Normal, Emergencia

// ---------- Entidades del proyecto

final case class Avion(matricula: String, categoria: Categoria)

/** programado: minuto absoluto = (día - 1) * 1440 + HH * 60 + MM. */
final case class Vuelo(codigo: String, aerolinea: String, avion: Avion, operacion: Operacion,
                       programado: Long, prioridad: Prioridad)

final case class Pista(id: String, longitud: Int, uso: Uso, estado: Estado)

/** Resultado de la torre: qué vuelo usa qué pista y cuándo. */
final case class OperacionAsignada(vuelo: Vuelo, pista: Pista, inicio: Long, fin: Long):
  def retraso: Long = inicio - vuelo.programado

final case class NoAsignable(vuelo: Vuelo, motivo: String)

/**
 * Estado de la simulación en un minuto. Es inmutable: cada paso crea uno nuevo.
 * cabezas: posición del primer vuelo pendiente de cada fila; libres: minuto en que se libera cada pista.
 */
final case class Aeropuerto(minuto: Long, cabezas: Vector[Int], libres: Vector[Long],
                            asignadasEnElPaso: Vector[OperacionAsignada])

// ---------- Lectura y validación

/** Una línea de datos del archivo: su número de línea física y sus campos. */
final case class Registro(linea: Int, campos: Vector[String])

final case class ErrorRegistro(archivo: String, linea: Int, motivo: String)

/** Resultado de validar un registro: Left con el error o Right con el dato. */
type Resultado[T] = Either[ErrorRegistro, T]

object Modelo:
  /** Los textos válidos de una lista cerrada, en su orden ("Ligero", "Mediano", "Pesado"). */
  def nombres[T](valores: Array[T]): List[String] = valores.toList.map(_.toString)

  /** Some con el mensaje si la condición se cumple; None si no. */
  def si(condicion: Boolean, mensaje: => String): Option[String] = Option.when(condicion)(mensaje)
```

### `scala/src/simulador/Lectura.scala`

```scala
package simulador

import java.nio.charset.StandardCharsets
import java.nio.file.{Files, Path}

// =============================================================================
//  MÓDULO 2 · LECTURA
//  Archivo -> líneas -> registros (número de línea + campos). Solo transforma texto.
// =============================================================================
object Lectura:

  /** ¿Existe el archivo y se puede leer? (se revisa antes de leer, para no depender de excepciones) */
  def sePuedeLeer(ruta: Path): Boolean =
    Files.isRegularFile(ruta) && Files.isReadable(ruta)

  /** Todas las líneas del archivo. Un byte UTF-8 inválido se convierte en U+FFFD, sin error. */
  def leerLineas(ruta: Path): Vector[String] =
    new String(Files.readAllBytes(ruta), StandardCharsets.UTF_8).split("\n", -1).toVector

  /**
   * Registros de datos: se salta el encabezado (línea 1) y las líneas vacías.
   * split(",", -1) conserva los campos vacíos del final; trim es el de la JVM.
   */
  def registros(lineas: Vector[String]): Vector[Registro] =
    lineas.indices
      .drop(1)
      .filter(i => lineas(i).trim.nonEmpty)
      .map(i => Registro(i + 1, lineas(i).split(",", -1).toVector.map(_.trim)))
      .toVector
```

### `scala/src/simulador/Validacion.scala`

```scala
package simulador

import scala.util.matching.Regex

import Modelo.si

// =============================================================================
//  MÓDULO 3 · VALIDACIÓN (RF03)
//  Cada registro se convierte en Right(dato) o Left(error). Las reglas se revisan en el orden de las
//  columnas y se reporta solo el primer error (cadena de Option.orElse).
// =============================================================================
object Validacion:

  private val Entero: Regex = "-?[0-9]{1,9}".r
  private val Hora: Regex = "([0-9]{2}):([0-9]{2})".r

  /** Revisión de un registro: error previo a la unicidad y error de sus demás campos. */
  private final case class Revision(registro: Registro, previo: Option[String], deCampos: Option[String]):
    def clave: String = registro.campos(0)

  // ---------- Reglas reutilizables

  private def entero(valor: String, campo: String): Option[String] =
    si(!Entero.matches(valor), s"$campo no es un entero: $valor")

  private def opcion(valor: String, campo: String, opciones: List[String]): Option[String] =
    si(!opciones.contains(valor), s"$campo con valor no válido: $valor (valores: ${opciones.mkString("/")})")

  private def hora(valor: String): Option[String] = valor match
    case Hora(hh, mm) if hh.toInt <= 23 && mm.toInt <= 59 => None
    case _ => Some(s"hora no válida: $valor (formato HH:MM de 00:00 a 23:59)")

  // ---------- Reglas de cada archivo (después del número de campos y la clave)

  private def reglasPista(c: Vector[String]): Option[String] =
    entero(c(1), "longitud")
      .orElse(si(c(1).toInt <= 0, s"longitud debe ser mayor que 0: ${c(1)}"))
      .orElse(opcion(c(2), "uso", Modelo.nombres(Uso.values)))
      .orElse(opcion(c(3), "estado", Modelo.nombres(Estado.values)))

  private def reglasVuelo(c: Vector[String]): Option[String] =
    si(c(1).isEmpty, "aerolínea vacía")
      .orElse(si(c(2).isEmpty, "matrícula vacía"))
      .orElse(opcion(c(3), "categoría", Modelo.nombres(Categoria.values)))
      .orElse(opcion(c(4), "operación", Modelo.nombres(Operacion.values)))
      .orElse(entero(c(5), "día"))
      .orElse(si(c(5).toInt < 1 || c(5).toInt > 9999, s"día debe estar entre 1 y 9999: ${c(5)}"))
      .orElse(hora(c(6)))
      .orElse(opcion(c(7), "prioridad", Modelo.nombres(Prioridad.values)))

  // ---------- Construcción de las entidades (solo con campos ya validados)

  private def construirPista(c: Vector[String]): Pista =
    Pista(c(0), c(1).toInt, Uso.valueOf(c(2)), Estado.valueOf(c(3)))

  private def construirVuelo(c: Vector[String]): Vuelo =
    val minuto = (c(5).toInt - 1) * 1440L + c(6).substring(0, 2).toInt * 60L + c(6).substring(3, 5).toInt
    Vuelo(c(0), c(1), Avion(c(2), Categoria.valueOf(c(3))), Operacion.valueOf(c(4)), minuto,
      Prioridad.valueOf(c(7)))

  // ---------- Validación genérica

  /**
   * Valida todos los registros de un archivo.
   * Unicidad: un registro está "repetido" si un registro VÁLIDO anterior tiene su misma clave.
   * El dueño de cada clave es el primer registro sin errores propios (groupMapReduce con mínimo), así no
   * hace falta recorrer el archivo con estado: el resultado es el mismo que validar línea por línea.
   */
  private def validar[T](registros: Vector[Registro], archivo: String, numCampos: Int, nombreClave: String,
                         reglas: Vector[String] => Option[String],
                         construir: Vector[String] => T): Vector[Resultado[T]] =
    val revisiones = registros.map(revisar(_, numCampos, nombreClave, reglas))
    val duenos: Map[String, Int] = revisiones
      .filter(v => v.previo.isEmpty && v.deCampos.isEmpty)
      .groupMapReduce(_.clave)(_.registro.linea)(_ min _)
    revisiones.map(resultado(_, duenos, archivo, nombreClave, construir))

  private def revisar(r: Registro, numCampos: Int, nombreClave: String,
                      reglas: Vector[String] => Option[String]): Revision =
    val previo = si(r.campos.size != numCampos, s"se esperaban $numCampos campos y hay ${r.campos.size}")
      .orElse(si(r.campos(0).isEmpty, s"$nombreClave vacío"))
    Revision(r, previo, if previo.isDefined then None else reglas(r.campos))

  private def resultado[T](v: Revision, duenos: Map[String, Int], archivo: String, nombreClave: String,
                           construir: Vector[String] => T): Resultado[T] =
    v.previo
      .orElse(si(duenos.getOrElse(v.clave, Int.MaxValue) < v.registro.linea, s"$nombreClave repetido: ${v.clave}"))
      .orElse(v.deCampos)
      .map(m => ErrorRegistro(archivo, v.registro.linea, m))
      .toLeft(construir(v.registro.campos))

  def validarPistas(registros: Vector[Registro]): Vector[Resultado[Pista]] =
    validar(registros, "pistas", 4, "id", reglasPista, construirPista)

  def validarVuelos(registros: Vector[Registro]): Vector[Resultado[Vuelo]] =
    validar(registros, "vuelos", 8, "código", reglasVuelo, construirVuelo)

  // ---------- Separar válidos y errores

  def validos[T](resultados: Vector[Resultado[T]]): Vector[T] =
    resultados.collect { case Right(valor) => valor }

  def errores[T](resultados: Vector[Resultado[T]]): Vector[ErrorRegistro] =
    resultados.collect { case Left(error) => error }
```

### `scala/src/simulador/TorreControl.scala`

```scala
package simulador

import scala.annotation.tailrec

import Modelo.si

// =============================================================================
//  MÓDULO 4 · TORRE DE CONTROL (RF04, RF05, RF06)
//  Funciones puras: reciben un Aeropuerto y devuelven uno nuevo. No guardan estado.
// =============================================================================
object TorreControl:

  /** Un vuelo listo para operar y la pista libre que le tocaría. */
  private final case class Candidato(fila: Int, pista: Int, vuelo: Vuelo)

  /** RN05: emergencia, luego aterrizaje, luego hora programada, luego código. */
  private val prioridad: Ordering[Vuelo] = Ordering.by((v: Vuelo) =>
    (if v.prioridad == Prioridad.Emergencia then 0 else 1,
     if v.operacion == Operacion.Aterrizaje then 0 else 1,
     v.programado,
     v.codigo))

  // ---------- Compatibilidad (RN03) y vuelos no asignables (RN09)

  private def habilitada(v: Vuelo, p: Pista): Boolean =
    p.estado == Estado.Operativa && (p.uso == Uso.Mixta || p.uso.toString == v.operacion.toString)

  private def compatible(v: Vuelo, p: Pista): Boolean =
    habilitada(v, p) && p.longitud >= v.avion.categoria.longitudMinima

  private def motivoNoAsignable(v: Vuelo, pistas: Vector[Pista]): Option[String] =
    si(!pistas.exists(p => habilitada(v, p)), "sin pista habilitada para la operación")
      .orElse(si(!pistas.exists(p => compatible(v, p)), "sin pista con longitud suficiente"))

  def noAsignables(vuelos: Vector[Vuelo], pistas: Vector[Pista]): Vector[NoAsignable] =
    vuelos.flatMap(v => motivoNoAsignable(v, pistas).map(m => NoAsignable(v, m)))

  def asignables(vuelos: Vector[Vuelo], pistas: Vector[Pista]): Vector[Vuelo] =
    vuelos.filter(v => motivoNoAsignable(v, pistas).isEmpty)

  // ---------- Preparación: 12 filas por (operación, categoría, prioridad)

  /** Todos los vuelos de una fila son compatibles con las mismas pistas: basta mirar el primero. */
  private def filas(asignables: Vector[Vuelo]): Vector[Vector[Vuelo]] =
    asignables
      .groupBy(v => (v.operacion, v.avion.categoria, v.prioridad))
      .values
      .map(fila => fila.sortBy(v => (v.programado, v.codigo)))
      .toVector

  // ---------- Un paso de la simulación

  private def quedanVuelos(a: Aeropuerto, filas: Vector[Vector[Vuelo]], i: Int): Boolean =
    a.cabezas(i) < filas(i).size

  private def primero(a: Aeropuerto, filas: Vector[Vector[Vuelo]], i: Int): Vuelo =
    filas(i)(a.cabezas(i))

  /** La pista libre y compatible de menor id (las pistas ya vienen ordenadas por id). */
  private def pistaLibre(a: Aeropuerto, v: Vuelo, pistas: Vector[Pista]): Option[Int] =
    pistas.indices.find(j => a.libres(j) <= a.minuto && compatible(v, pistas(j)))

  /** Entre los primeros de cada fila que ya esperan y tienen pista libre, el de mayor prioridad. */
  private def mejorCandidato(a: Aeropuerto, filas: Vector[Vector[Vuelo]], pistas: Vector[Pista]): Option[Candidato] =
    filas.indices
      .filter(i => quedanVuelos(a, filas, i) && primero(a, filas, i).programado <= a.minuto)
      .flatMap(i => pistaLibre(a, primero(a, filas, i), pistas).map(j => Candidato(i, j, primero(a, filas, i))))
      .minByOption(_.vuelo)(using prioridad)

  private def asignar(a: Aeropuerto, c: Candidato, pistas: Vector[Pista]): Aeropuerto =
    val fin = a.minuto + c.vuelo.avion.categoria.minutosOcupacion
    a.copy(
      cabezas = a.cabezas.updated(c.fila, a.cabezas(c.fila) + 1),
      libres = a.libres.updated(c.pista, fin),
      asignadasEnElPaso = a.asignadasEnElPaso :+ OperacionAsignada(c.vuelo, pistas(c.pista), a.minuto, fin))

  /** Asigna en el minuto actual mientras haya candidato. Cada asignación ocupa una pista: como mucho k niveles. */
  @tailrec
  private def asignarEnMinuto(a: Aeropuerto, filas: Vector[Vector[Vuelo]], pistas: Vector[Pista]): Aeropuerto =
    mejorCandidato(a, filas, pistas) match
      case Some(c) => asignarEnMinuto(asignar(a, c, pistas), filas, pistas)
      case None => a

  /** Siguiente evento: el menor minuto futuro en que se libera una pista o llega un vuelo. */
  private def siguienteMinuto(a: Aeropuerto, filas: Vector[Vector[Vuelo]]): Long =
    (a.libres ++ filas.indices.filter(i => quedanVuelos(a, filas, i)).map(i => primero(a, filas, i).programado))
      .filter(t => t > a.minuto)
      .minOption
      .getOrElse(a.minuto)

  private def paso(a: Aeropuerto, filas: Vector[Vector[Vuelo]], pistas: Vector[Pista]): Aeropuerto =
    val tras = asignarEnMinuto(a.copy(asignadasEnElPaso = Vector.empty), filas, pistas)
    tras.copy(minuto = siguienteMinuto(tras, filas))

  private def terminado(a: Aeropuerto, filas: Vector[Vector[Vuelo]]): Boolean =
    a.asignadasEnElPaso.isEmpty && !filas.indices.exists(i => quedanVuelos(a, filas, i))

  // ---------- Simulación completa

  /** Secuencia perezosa de estados: iterate -> takeWhile -> flatMap de las asignaciones de cada paso. */
  def simular(asignables: Vector[Vuelo], pistas: Vector[Pista]): Vector[OperacionAsignada] =
    val operativas = pistas.filter(_.estado == Estado.Operativa).sortBy(_.id)
    val todas = filas(asignables)
    val inicial = Aeropuerto(
      todas.map(_.head.programado).minOption.getOrElse(0L),
      todas.map(_ => 0),
      operativas.map(_ => 0L),
      Vector.empty)
    Iterator.iterate(inicial)(a => paso(a, todas, operativas))
      .takeWhile(a => !terminado(a, todas))
      .flatMap(_.asignadasEnElPaso)
      .toVector
```

### `scala/src/simulador/Reportes.scala`

```scala
package simulador

// =============================================================================
//  MÓDULO 5 · REPORTES (RF07 a RF14)
//  Construye el texto de los tres archivos de salida. Los decimales se calculan con aritmética entera
//  exacta (centésimas redondeadas HALF_UP), sin números de punto flotante.
// =============================================================================
object Reportes:

  private val SinDatos = "Sin datos"
  private val UmbralRetraso = 15

  /** Totales por aerolínea para RF11: el promedio es suma / cantidad. */
  private final case class Aerolinea(nombre: String, suma: Long, cantidad: Long)

  /** Todo lo que necesitan los reportes. */
  final case class Datos(registrosPistas: Int, pistas: Vector[Pista], erroresPistas: Vector[ErrorRegistro],
                         registrosVuelos: Int, vuelosValidos: Int, erroresVuelos: Vector[ErrorRegistro],
                         operaciones: Vector[OperacionAsignada], noAsignables: Vector[NoAsignable])

  // ---------- Formato

  private def dosDigitos(x: Long): String = if x < 10 then s"0$x" else x.toString

  /** a / b con 2 decimales: c = (200a + b) / 2b son las centésimas redondeadas. */
  private def decimal(a: Long, b: Long): String =
    val c = (200 * a + b) / (2 * b)
    s"${c / 100}.${dosDigitos(c % 100)}"

  private def hora(minuto: Long): String =
    s"D${minuto / 1440 + 1} ${dosDigitos(minuto % 1440 / 60)}:${dosDigitos(minuto % 60)}"

  private def seccion(titulo: String, lineas: Seq[String]): Vector[String] =
    (s"== $titulo ==" +: lineas.toVector) :+ ""

  private def oSinDatos(lineas: Seq[String], vacio: String): Seq[String] =
    if lineas.isEmpty then Seq(vacio) else lineas

  private def texto(lineas: Seq[String]): String = lineas.mkString("", "\n", "\n")

  // ---------- Archivos CSV

  /** RF07: una línea por operación, en el orden en que se asignaron. */
  def operacionesCsv(operaciones: Vector[OperacionAsignada]): String =
    texto("codigo,aerolinea,operacion,categoria,prioridad,pista,programada,inicio,fin,retraso" +:
      operaciones.map(o => Vector(
        o.vuelo.codigo, o.vuelo.aerolinea, o.vuelo.operacion.toString, o.vuelo.avion.categoria.toString,
        o.vuelo.prioridad.toString, o.pista.id, hora(o.vuelo.programado), hora(o.inicio), hora(o.fin),
        o.retraso.toString).mkString(",")))

  /** RF03: primero los errores de pistas y luego los de vuelos. */
  def erroresCsv(errores: Vector[ErrorRegistro]): String =
    texto("archivo,linea,motivo" +: errores.map(e => s"${e.archivo},${e.linea},${e.motivo}"))

  // ---------- Secciones del reporte

  private def rf03(d: Datos): Vector[String] =
    seccion("RF03 · Validación de datos", Vector(
      s"Pistas | registros: ${d.registrosPistas} | válidos: ${d.pistas.size} | inválidos: ${d.erroresPistas.size}",
      s"Vuelos | registros: ${d.registrosVuelos} | válidos: ${d.vuelosValidos} | inválidos: ${d.erroresVuelos.size}",
      "Detalle de los registros inválidos: errores.csv"))

  private def sumaRetrasos(ops: Vector[OperacionAsignada]): Long = ops.map(_.retraso).sum

  private def retrasados(ops: Vector[OperacionAsignada]): Long = ops.count(_.retraso > UmbralRetraso).toLong

  private def promedio(ops: Vector[OperacionAsignada]): String =
    if ops.isEmpty then SinDatos else decimal(sumaRetrasos(ops), ops.size) + " min"

  private def porcentajeRetrasados(ops: Vector[OperacionAsignada]): String =
    if ops.isEmpty then SinDatos else decimal(100 * retrasados(ops), ops.size) + "%"

  private def rf08(ops: Vector[OperacionAsignada]): Vector[String] =
    val maximo = ops.map(_.retraso).maxOption.map(m => s"$m min").getOrElse(SinDatos)
    val conRetraso = if ops.isEmpty then SinDatos else s"${retrasados(ops)} (${porcentajeRetrasados(ops)})"
    seccion("RF08 · Resumen de retrasos", Vector(
      s"Operaciones asignadas: ${ops.size}",
      s"Retraso promedio: ${promedio(ops)}",
      s"Retraso máximo: $maximo",
      s"Vuelos retrasados (más de $UmbralRetraso min): $conRetraso"))

  private def rf09(ops: Vector[OperacionAsignada]): Vector[String] =
    val top = ops.sortBy(o => (-o.retraso, o.vuelo.codigo)).take(5)
    seccion("RF09 · 5 vuelos más retrasados", oSinDatos(top.zipWithIndex.map((o, i) =>
      s"${i + 1}. ${o.vuelo.codigo} | retraso: ${o.retraso} min | ${o.vuelo.operacion} | ${o.pista.id}"), SinDatos))

  private def usoDePistas(ops: Vector[OperacionAsignada], pistas: Vector[Pista]): Vector[String] =
    val inicio = ops.map(_.vuelo.programado).min
    val fin = ops.map(_.fin).max
    val porPista = ops.groupBy(_.pista.id)
    s"Período simulado: ${hora(inicio)} a ${hora(fin)} (${fin - inicio} min)" +:
      pistas.sortBy(_.id).map { p =>
        val suyas = porPista.getOrElse(p.id, Vector.empty)
        val ocupada = suyas.map(o => o.fin - o.inicio).sum
        s"${p.id} | ${p.estado} | operaciones: ${suyas.size} | ocupada: $ocupada min | ocupación: " +
          decimal(100 * ocupada, fin - inicio) + "%"
      }

  private def rf10(ops: Vector[OperacionAsignada], pistas: Vector[Pista]): Vector[String] =
    seccion("RF10 · Uso de pistas", if ops.isEmpty || pistas.isEmpty then Vector(SinDatos) else usoDePistas(ops, pistas))

  /** RF11: de mayor a menor promedio (comparando fracciones exactas); si empatan, por nombre. */
  private def aerolineas(ops: Vector[OperacionAsignada]): Vector[Aerolinea] =
    ops.groupBy(_.vuelo.aerolinea).toVector
      .map((nombre, suyas) => Aerolinea(nombre, sumaRetrasos(suyas), suyas.size))
      .sortWith((x, y) =>
        x.suma * y.cantidad > y.suma * x.cantidad
          || (x.suma * y.cantidad == y.suma * x.cantidad && x.nombre < y.nombre))

  private def rf11(lista: Vector[Aerolinea]): Vector[String] =
    seccion("RF11 · Retraso promedio por aerolínea", oSinDatos(lista.map(a =>
      s"${a.nombre} | retraso promedio: ${decimal(a.suma, a.cantidad)} min | operaciones: ${a.cantidad}"), SinDatos))

  private def rf12(noAsignables: Vector[NoAsignable]): Vector[String] =
    seccion("RF12 · Vuelos no asignables", oSinDatos(noAsignables.map(n =>
      s"${n.vuelo.codigo} | ${n.vuelo.operacion} | ${n.vuelo.avion.categoria} | ${n.motivo}"), "Ninguno"))

  private def rf13(ops: Vector[OperacionAsignada]): Vector[String] =
    seccion("RF13 · Operaciones por tipo y categoría",
      Vector(Operacion.Aterrizaje, Operacion.Despegue).map(t => s"$t: ${ops.count(_.vuelo.operacion == t)}")
        ++ Categoria.values.toVector.map(c => s"$c: ${ops.count(_.vuelo.avion.categoria == c)}"))

  private def pistaMasUsada(ops: Vector[OperacionAsignada], pistas: Vector[Pista]): String =
    val usos = ops.groupMapReduce(_.pista.id)(_ => 1L)(_ + _)
    if ops.isEmpty then SinDatos
    else pistas.sortBy(p => (-usos.getOrElse(p.id, 0L), p.id)).headOption
      .map(p => s"${p.id} (operaciones: ${usos.getOrElse(p.id, 0L)})")
      .getOrElse(SinDatos)

  private def rf14(d: Datos, lista: Vector[Aerolinea]): Vector[String] =
    val ops = d.operaciones
    val peor = lista.headOption.map(a => s"${a.nombre} (${decimal(a.suma, a.cantidad)} min)").getOrElse(SinDatos)
    Vector(
      "== RF14 · Resumen ejecutivo ==",
      s"Vuelos cargados: ${d.registrosVuelos}",
      s"Vuelos válidos: ${d.vuelosValidos}",
      s"Vuelos inválidos: ${d.erroresVuelos.size}",
      s"Vuelos asignados: ${ops.size}",
      s"Vuelos no asignables: ${d.noAsignables.size}",
      s"Retraso promedio: ${promedio(ops)}",
      s"Vuelos retrasados: ${porcentajeRetrasados(ops)}",
      s"Pista más usada: ${pistaMasUsada(ops, d.pistas)}",
      s"Aerolínea con mayor retraso promedio: $peor")

  /** reporte.txt completo (RF03 y RF08 a RF14). */
  def reporte(d: Datos): String =
    val lista = aerolineas(d.operaciones)
    texto(Vector(
      Vector("SIMULADOR DE OPERACIONES AEROPORTUARIAS · REPORTE", ""),
      rf03(d), rf08(d.operaciones), rf09(d.operaciones), rf10(d.operaciones, d.pistas),
      rf11(lista), rf12(d.noAsignables), rf13(d.operaciones), rf14(d, lista)).flatten)
```

### `scala/src/simulador/Medicion.scala`

```scala
package simulador

import java.nio.charset.StandardCharsets
import java.nio.file.{Files, Path}

// =============================================================================
//  MÓDULO 6 · MEDICIÓN (Bloque 3, sección 5)
//  Toma el tiempo de cada etapa con System.nanoTime() y, con --medir, lo escribe en un archivo.
//  Cada etapa devuelve su resultado ya calculado (regla de materialización: Vector, no Iterator ni LazyList).
// =============================================================================
object Medicion:

  val Encabezado = "lectura_ns,validacion_ns,simulacion_ns,reportes_ns,escritura_ns"

  /** Resultado de una etapa y lo que tardó, en nanosegundos. */
  final case class Medido[T](valor: T, ns: Long)

  /** La etapa se recibe "por nombre" (=> T): se evalúa aquí adentro, entre las dos lecturas del reloj. */
  def medir[T](etapa: => T): Medido[T] =
    val inicio = System.nanoTime()
    val valor = etapa
    Medido(valor, System.nanoTime() - inicio)

  /** Archivo de --medir: encabezado y una línea con las cinco duraciones. */
  def escribir(archivo: Path, duraciones: List[Long]): Unit =
    Files.writeString(archivo, s"$Encabezado\n${duraciones.mkString(",")}\n", StandardCharsets.UTF_8)
    ()
```

### `scala/src/simulador/Main.scala`

```scala
package simulador

import java.nio.charset.StandardCharsets
import java.nio.file.{Files, Path}

// =============================================================================
//  MÓDULO 7 · PROGRAMA PRINCIPAL
//  Revisa los argumentos y encadena las cinco etapas: lectura -> validación -> simulación ->
//  reportes -> escritura. Toda la lógica está en los otros módulos; aquí solo se conectan.
// =============================================================================
object Main:

  private val ModoDeUso =
    "Uso: java -jar simulador-<lenguaje>.jar <pistas.csv> <vuelos.csv> <carpeta_salida> [--medir <archivo>]"

  // ---------- Resultado de cada etapa

  private final case class Lineas(pistas: Vector[String], vuelos: Vector[String])

  private final case class Validados(registrosPistas: Int, pistas: Vector[Pista], erroresPistas: Vector[ErrorRegistro],
                                     registrosVuelos: Int, vuelos: Vector[Vuelo], erroresVuelos: Vector[ErrorRegistro])

  private final case class Simulados(operaciones: Vector[OperacionAsignada], noAsignables: Vector[NoAsignable])

  private final case class Textos(operaciones: String, errores: String, reporte: String)

  // ---------- Etapas

  private def validar(lineas: Lineas): Validados =
    val registrosPistas = Lectura.registros(lineas.pistas)
    val registrosVuelos = Lectura.registros(lineas.vuelos)
    val pistas = Validacion.validarPistas(registrosPistas)
    val vuelos = Validacion.validarVuelos(registrosVuelos)
    Validados(registrosPistas.size, Validacion.validos(pistas), Validacion.errores(pistas),
      registrosVuelos.size, Validacion.validos(vuelos), Validacion.errores(vuelos))

  private def simular(v: Validados): Simulados =
    Simulados(
      TorreControl.simular(TorreControl.asignables(v.vuelos, v.pistas), v.pistas),
      TorreControl.noAsignables(v.vuelos, v.pistas))

  private def reportar(v: Validados, s: Simulados): Textos =
    Textos(
      Reportes.operacionesCsv(s.operaciones),
      Reportes.erroresCsv(v.erroresPistas ++ v.erroresVuelos),
      Reportes.reporte(Reportes.Datos(v.registrosPistas, v.pistas, v.erroresPistas,
        v.registrosVuelos, v.vuelos.size, v.erroresVuelos, s.operaciones, s.noAsignables)))

  private def escribir(salida: Path, t: Textos): Path =
    Files.createDirectories(salida)
    Files.writeString(salida.resolve("operaciones.csv"), t.operaciones, StandardCharsets.UTF_8)
    Files.writeString(salida.resolve("errores.csv"), t.errores, StandardCharsets.UTF_8)
    Files.writeString(salida.resolve("reporte.txt"), t.reporte, StandardCharsets.UTF_8)
    imprimir(t.reporte)
    salida

  /** Escribe en pantalla siempre en UTF-8, sin depender de la configuración regional del equipo. */
  private def imprimir(texto: String): Unit =
    System.out.writeBytes(texto.getBytes(StandardCharsets.UTF_8))
    System.out.flush()

  // ---------- Argumentos

  /** Motivo del error de uso, si lo hay: cantidad de argumentos o archivo de entrada ilegible. */
  private def problemaDeUso(args: Array[String]): Option[String] =
    if !(args.length == 3 || (args.length == 5 && args(3) == "--medir")) then Some("número de argumentos incorrecto")
    else args.take(2).toList
      .find(ruta => !Lectura.sePuedeLeer(Path.of(ruta)))
      .map(ruta => s"no se puede leer el archivo $ruta")

  private def ejecutar(pistas: Path, vuelos: Path, salida: Path, archivoMedicion: Option[Path]): Unit =
    val lectura = Medicion.medir(Lineas(Lectura.leerLineas(pistas), Lectura.leerLineas(vuelos)))
    val validacion = Medicion.medir(validar(lectura.valor))
    val simulacion = Medicion.medir(simular(validacion.valor))
    val reportes = Medicion.medir(reportar(validacion.valor, simulacion.valor))
    val escritura = Medicion.medir(escribir(salida, reportes.valor))
    archivoMedicion.foreach(archivo => Medicion.escribir(archivo,
      List(lectura.ns, validacion.ns, simulacion.ns, reportes.ns, escritura.ns)))

  def main(args: Array[String]): Unit =
    problemaDeUso(args) match
      case Some(motivo) =>
        imprimir(s"ERROR: $motivo\n$ModoDeUso\n")
        sys.exit(2)
      case None =>
        ejecutar(Path.of(args(0)), Path.of(args(1)), Path.of(args(2)), Option.when(args.length == 5)(Path.of(args(4))))
```

---

## Anexo C · Código completo de Clojure

### `clojure/project.clj`

```clojure
;; Versión Clojure del simulador. Se construye con: bash clojure/construir.sh  (lein uberjar)
(defproject simulador-clojure "1.0.0"
  :description "Simulador de operaciones aeroportuarias · versión Clojure"
  :dependencies [[org.clojure/clojure "1.12.0"]]
  :main simulador.main
  ;; Compilación por adelantado de todos los espacios de nombres: el .jar no compila nada al arrancar.
  :aot :all
  :target-path "target/%s"
  :uberjar-name "simulador-clojure.jar"
  ;; Avisa al compilar si alguna llamada a Java necesitaría reflexión (lenta); el código no debe tener ninguna.
  :global-vars {*warn-on-reflection* true})
```

### `clojure/src/simulador/modelo.clj`

```clojure
;; =============================================================================
;;  MÓDULO 1 · MODELO
;;  Entidades del aeropuerto como registros inmutables (defrecord) y listas cerradas como palabras clave
;;  (:Ligero, :Despegue...). Para "cambiar" un dato se crea uno nuevo con assoc.
;; =============================================================================
(ns simulador.modelo)

;; ---------- Listas cerradas. El nombre de cada valor es el texto exacto del contrato.

(def categorias
  "Categoría del avión con sus requisitos (RN02)."
  {:Ligero  {:longitud-minima 1200 :minutos-ocupacion 2}
   :Mediano {:longitud-minima 2000 :minutos-ocupacion 3}
   :Pesado  {:longitud-minima 2800 :minutos-ocupacion 4}})

(def nombres-categoria ["Ligero" "Mediano" "Pesado"])
(def nombres-operacion ["Despegue" "Aterrizaje"])
(def nombres-uso ["Despegue" "Aterrizaje" "Mixta"])
(def nombres-estado ["Operativa" "Cerrada"])
(def nombres-prioridad ["Normal" "Emergencia"])

;; ---------- Entidades del proyecto

(defrecord Avion [matricula categoria])

;; programado: minuto absoluto = (día - 1) * 1440 + HH * 60 + MM.
(defrecord Vuelo [codigo aerolinea avion operacion programado prioridad])

(defrecord Pista [id longitud uso estado])

;; Resultado de la torre: qué vuelo usa qué pista y cuándo.
(defrecord OperacionAsignada [vuelo pista inicio fin])

(defrecord NoAsignable [vuelo motivo])

;; Estado de la simulación en un minuto. Es inmutable: cada paso crea uno nuevo.
;; cabezas: posición del primer vuelo pendiente de cada fila; libres: minuto en que se libera cada pista.
(defrecord Aeropuerto [minuto cabezas libres asignadas-en-el-paso])

;; ---------- Lectura y validación

;; Una línea de datos del archivo: su número de línea física y sus campos.
(defrecord Registro [linea campos])

(defrecord ErrorRegistro [archivo linea motivo])

;; ---------- Funciones de las entidades

(defn retraso
  "Minutos entre la hora programada y el inicio real de la operación."
  [operacion]
  (- (:inicio operacion) (:programado (:vuelo operacion))))

(defn categoria
  "Requisitos de la categoría del avión de un vuelo."
  [vuelo]
  (categorias (:categoria (:avion vuelo))))
```

### `clojure/src/simulador/lectura.clj`

```clojure
;; =============================================================================
;;  MÓDULO 2 · LECTURA
;;  Archivo -> líneas -> registros (número de línea + campos). Solo transforma texto.
;; =============================================================================
(ns simulador.lectura
  (:require [clojure.string :as str]
            [simulador.modelo :as m])
  (:import (java.io File)
           (java.nio.charset StandardCharsets)
           (java.nio.file Files)))

(defn se-puede-leer?
  "¿Existe el archivo y se puede leer? (se revisa antes de leer, para no depender de excepciones)"
  [^String ruta]
  (let [archivo (File. ruta)]
    (and (.isFile archivo) (.canRead archivo))))

(defn leer-lineas
  "Todas las líneas del archivo. Un byte UTF-8 inválido se convierte en U+FFFD, sin error."
  [^String ruta]
  (str/split (String. (Files/readAllBytes (.toPath (File. ruta))) StandardCharsets/UTF_8) #"\n" -1))

(defn registros
  "Registros de datos: se salta el encabezado (línea 1) y las líneas vacías.
  Se usa .trim de la JVM (quita los caracteres <= U+0020); str/trim de Clojure quitaría otros espacios Unicode."
  [lineas]
  (into []
        (comp (map-indexed vector)
              (drop 1)
              (remove (fn [[_ ^String linea]] (.isEmpty (.trim linea))))
              (map (fn [[i ^String linea]]
                     (m/->Registro (inc i) (mapv (fn [^String campo] (.trim campo)) (str/split linea #"," -1))))))
        lineas))
```

### `clojure/src/simulador/validacion.clj`

```clojure
;; =============================================================================
;;  MÓDULO 3 · VALIDACIÓN (RF03)
;;  Cada registro se convierte en {:ok dato} o {:falla error}. Las reglas se revisan en el orden de las
;;  columnas y se reporta solo el primer error: (or regla1 regla2 ...) devuelve el primer mensaje que no es nil.
;; =============================================================================
(ns simulador.validacion
  (:require [clojure.string :as str]
            [simulador.modelo :as m]))

(def ^:private entero-re #"-?[0-9]{1,9}")
(def ^:private hora-re #"([0-9]{2}):([0-9]{2})")

;; ---------- Reglas reutilizables. Cada una devuelve el mensaje de error, o nil si el valor es válido.

(defn- entero [valor campo]
  (when-not (re-matches entero-re valor)
    (str campo " no es un entero: " valor)))

(defn- opcion [valor campo opciones]
  (when-not (some #(= valor %) opciones)
    (str campo " con valor no válido: " valor " (valores: " (str/join "/" opciones) ")")))

(defn- hora [valor]
  (let [[_ hh mm] (re-matches hora-re valor)]
    (when-not (and hh (<= (parse-long hh) 23) (<= (parse-long mm) 59))
      (str "hora no válida: " valor " (formato HH:MM de 00:00 a 23:59)"))))

;; ---------- Reglas de cada archivo (después del número de campos y la clave)

(defn- reglas-pista [[_ longitud uso estado]]
  (or (entero longitud "longitud")
      (when (<= (parse-long longitud) 0) (str "longitud debe ser mayor que 0: " longitud))
      (opcion uso "uso" m/nombres-uso)
      (opcion estado "estado" m/nombres-estado)))

(defn- reglas-vuelo [[_ ^String aerolinea ^String matricula categoria operacion dia hora-texto prioridad]]
  (or (when (.isEmpty aerolinea) "aerolínea vacía")
      (when (.isEmpty matricula) "matrícula vacía")
      (opcion categoria "categoría" m/nombres-categoria)
      (opcion operacion "operación" m/nombres-operacion)
      (entero dia "día")
      (when-not (<= 1 (parse-long dia) 9999) (str "día debe estar entre 1 y 9999: " dia))
      (hora hora-texto)
      (opcion prioridad "prioridad" m/nombres-prioridad)))

;; ---------- Construcción de las entidades (solo con campos ya validados)

(defn- construir-pista [[id longitud uso estado]]
  (m/->Pista id (parse-long longitud) (keyword uso) (keyword estado)))

(defn- construir-vuelo [[codigo aerolinea matricula categoria operacion dia hora-texto prioridad]]
  (m/->Vuelo codigo aerolinea (m/->Avion matricula (keyword categoria)) (keyword operacion)
             (+ (* (dec (parse-long dia)) 1440)
                (* (parse-long (subs hora-texto 0 2)) 60)
                (parse-long (subs hora-texto 3 5)))
             (keyword prioridad)))

;; ---------- Validación genérica

(defn- revisar
  "Error previo a la unicidad (número de campos o clave vacía) y error de los demás campos."
  [{:keys [campos] :as registro} num-campos nombre-clave reglas]
  (let [previo (or (when (not= num-campos (count campos))
                     (str "se esperaban " num-campos " campos y hay " (count campos)))
                   (when (.isEmpty ^String (first campos))
                     (str nombre-clave " vacío")))]
    {:registro registro
     :clave (first campos)
     :previo previo
     :de-campos (when-not previo (reglas campos))}))

(defn- resultado [{:keys [registro clave previo de-campos]} duenos archivo nombre-clave construir]
  (if-let [error (or previo
                     (when (< (get duenos clave Long/MAX_VALUE) (:linea registro))
                       (str nombre-clave " repetido: " clave))
                     de-campos)]
    {:falla (m/->ErrorRegistro archivo (:linea registro) error)}
    {:ok (construir (:campos registro))}))

(defn- validar
  "Valida todos los registros de un archivo.
  Unicidad: un registro está \"repetido\" si un registro VÁLIDO anterior tiene su misma clave. El dueño de
  cada clave es el primer registro sin errores propios (agrupar + mínimo), así no hace falta recorrer el
  archivo con estado: el resultado es el mismo que validar línea por línea."
  [registros archivo num-campos nombre-clave reglas construir]
  (let [revisiones (mapv #(revisar % num-campos nombre-clave reglas) registros)
        sin-errores (remove #(or (:previo %) (:de-campos %)) revisiones)
        duenos (update-vals (group-by :clave sin-errores)
                            #(apply min (map (comp :linea :registro) %)))]
    (mapv #(resultado % duenos archivo nombre-clave construir) revisiones)))

(defn validar-pistas [registros]
  (validar registros "pistas" 4 "id" reglas-pista construir-pista))

(defn validar-vuelos [registros]
  (validar registros "vuelos" 8 "código" reglas-vuelo construir-vuelo))

;; ---------- Separar válidos y errores

(defn validos [resultados]
  (into [] (keep :ok) resultados))

(defn errores [resultados]
  (into [] (keep :falla) resultados))
```

### `clojure/src/simulador/torre_control.clj`

```clojure
;; =============================================================================
;;  MÓDULO 4 · TORRE DE CONTROL (RF04, RF05, RF06)
;;  Funciones puras: reciben un Aeropuerto y devuelven uno nuevo. No guardan estado.
;; =============================================================================
(ns simulador.torre-control
  (:require [simulador.modelo :as m]))

;; ---------- Órdenes (comparadores: negativo si x va antes que y)

(defn- por-hora-y-codigo
  "Orden de una fila: hora programada y, si empatan, código."
  [x y]
  (let [c (compare (:programado x) (:programado y))]
    (if (zero? c) (compare (:codigo x) (:codigo y)) c)))

(defn- rango
  "RN05: 0 emergencia que aterriza, 1 emergencia que despega, 2 normal que aterriza, 3 normal que despega."
  [vuelo]
  (+ (if (= :Emergencia (:prioridad vuelo)) 0 2)
     (if (= :Aterrizaje (:operacion vuelo)) 0 1)))

(defn- por-prioridad
  "RN05: emergencia, luego aterrizaje, luego hora programada, luego código."
  [x y]
  (let [c (compare (rango x) (rango y))]
    (if (zero? c) (por-hora-y-codigo x y) c)))

;; ---------- Compatibilidad (RN03) y vuelos no asignables (RN09)

(defn- habilitada? [vuelo pista]
  (and (= :Operativa (:estado pista))
       ;; :Despegue y :Aterrizaje son la misma palabra clave en el uso de la pista y en la operación.
       (or (= :Mixta (:uso pista)) (= (:uso pista) (:operacion vuelo)))))

(defn- compatible? [vuelo pista]
  (and (habilitada? vuelo pista)
       (>= (:longitud pista) (:longitud-minima (m/categoria vuelo)))))

(defn- motivo-no-asignable [vuelo pistas]
  (cond
    (not-any? #(habilitada? vuelo %) pistas) "sin pista habilitada para la operación"
    (not-any? #(compatible? vuelo %) pistas) "sin pista con longitud suficiente"))

(defn no-asignables [vuelos pistas]
  (into [] (keep (fn [vuelo]
                   (when-let [motivo (motivo-no-asignable vuelo pistas)]
                     (m/->NoAsignable vuelo motivo))))
        vuelos))

(defn asignables [vuelos pistas]
  (into [] (remove #(motivo-no-asignable % pistas)) vuelos))

;; ---------- Preparación: 12 filas por (operación, categoría, prioridad)

(defn- armar-filas
  "Todos los vuelos de una fila son compatibles con las mismas pistas: basta mirar el primero."
  [asignables]
  (->> asignables
       (group-by (juxt :operacion (comp :categoria :avion) :prioridad))
       vals
       (mapv #(vec (sort por-hora-y-codigo %)))))

;; ---------- Un paso de la simulación

(defn- quedan-vuelos? [aeropuerto filas i]
  (< (nth (:cabezas aeropuerto) i) (count (nth filas i))))

(defn- primero [aeropuerto filas i]
  (nth (nth filas i) (nth (:cabezas aeropuerto) i)))

(defn- pista-libre
  "La pista libre y compatible de menor id (las pistas ya vienen ordenadas por id)."
  [aeropuerto vuelo pistas]
  (some (fn [j]
          (when (and (<= (nth (:libres aeropuerto) j) (:minuto aeropuerto))
                     (compatible? vuelo (nth pistas j)))
            j))
        (range (count pistas))))

(defn- candidato
  "El primer vuelo de la fila i, si ya espera y tiene una pista libre."
  [aeropuerto filas pistas i]
  (let [vuelo (primero aeropuerto filas i)
        pista (when (<= (:programado vuelo) (:minuto aeropuerto))
                (pista-libre aeropuerto vuelo pistas))]
    (when pista {:fila i :pista pista :vuelo vuelo})))

(defn- mejor-candidato
  "Entre los primeros de cada fila que ya esperan y tienen pista libre, el de mayor prioridad."
  [aeropuerto filas pistas]
  (->> (range (count filas))
       (filter #(quedan-vuelos? aeropuerto filas %))
       (keep #(candidato aeropuerto filas pistas %))
       (sort-by :vuelo por-prioridad)
       first))

(defn- asignar [aeropuerto {:keys [fila pista vuelo]} pistas]
  (let [inicio (:minuto aeropuerto)
        fin (+ inicio (:minutos-ocupacion (m/categoria vuelo)))]
    (-> aeropuerto
        (update-in [:cabezas fila] inc)
        (assoc-in [:libres pista] fin)
        (update :asignadas-en-el-paso conj (m/->OperacionAsignada vuelo (nth pistas pista) inicio fin)))))

(defn- asignar-en-minuto
  "Asigna en el minuto actual mientras haya candidato. Cada asignación ocupa una pista: como mucho k niveles."
  [aeropuerto filas pistas]
  (if-let [c (mejor-candidato aeropuerto filas pistas)]
    (recur (asignar aeropuerto c pistas) filas pistas)
    aeropuerto))

(defn- siguiente-minuto
  "Siguiente evento: el menor minuto futuro en que se libera una pista o llega un vuelo."
  [aeropuerto filas]
  (let [ahora (:minuto aeropuerto)
        futuros (filter #(> % ahora)
                        (concat (:libres aeropuerto)
                                (keep #(when (quedan-vuelos? aeropuerto filas %)
                                         (:programado (primero aeropuerto filas %)))
                                      (range (count filas)))))]
    (if (seq futuros) (reduce min futuros) ahora)))

(defn- paso [aeropuerto filas pistas]
  (let [tras (asignar-en-minuto (assoc aeropuerto :asignadas-en-el-paso []) filas pistas)]
    (assoc tras :minuto (siguiente-minuto tras filas))))

(defn- terminado? [aeropuerto filas]
  (and (empty? (:asignadas-en-el-paso aeropuerto))
       (not-any? #(quedan-vuelos? aeropuerto filas %) (range (count filas)))))

;; ---------- Simulación completa

(defn simular
  "Secuencia perezosa de estados: iterate -> take-while -> mapcat de las asignaciones de cada paso."
  [asignables pistas]
  (let [operativas (vec (sort-by :id (filter #(= :Operativa (:estado %)) pistas)))
        filas (armar-filas asignables)
        inicial (m/->Aeropuerto (if (seq filas) (reduce min (map #(:programado (first %)) filas)) 0)
                                (vec (repeat (count filas) 0))
                                (vec (repeat (count operativas) 0))
                                [])]
    (into []
          (comp (take-while #(not (terminado? % filas)))
                (mapcat :asignadas-en-el-paso))
          (iterate #(paso % filas operativas) inicial))))
```

### `clojure/src/simulador/reportes.clj`

```clojure
;; =============================================================================
;;  MÓDULO 5 · REPORTES (RF07 a RF14)
;;  Construye el texto de los tres archivos de salida. Los decimales se calculan con aritmética entera
;;  exacta (centésimas redondeadas HALF_UP), sin números de punto flotante.
;; =============================================================================
(ns simulador.reportes
  (:require [clojure.string :as str]
            [simulador.modelo :as m]))

(def ^:private sin-datos "Sin datos")
(def ^:private umbral-retraso 15)

;; ---------- Formato

(defn- dos-digitos [x]
  (if (< x 10) (str "0" x) (str x)))

(defn- decimal
  "a / b con 2 decimales: c = (200a + b) quot 2b son las centésimas redondeadas."
  [a b]
  (let [c (quot (+ (* 200 a) b) (* 2 b))]
    (str (quot c 100) "." (dos-digitos (rem c 100)))))

(defn- hora [minuto]
  (str "D" (inc (quot minuto 1440)) " "
       (dos-digitos (quot (rem minuto 1440) 60)) ":" (dos-digitos (rem minuto 60))))

(defn- seccion [titulo lineas]
  (concat [(str "== " titulo " ==")] lineas [""]))

(defn- o-sin-datos [lineas vacio]
  (if (seq lineas) lineas [vacio]))

(defn- texto
  "Une las líneas con saltos de línea; el archivo termina con un salto de línea."
  [lineas]
  (str (str/join "\n" lineas) "\n"))

(defn- codigo [operacion] (:codigo (:vuelo operacion)))
(defn- id-pista [operacion] (:id (:pista operacion)))

;; ---------- Archivos CSV

(defn operaciones-csv
  "RF07: una línea por operación, en el orden en que se asignaron."
  [operaciones]
  (texto (cons "codigo,aerolinea,operacion,categoria,prioridad,pista,programada,inicio,fin,retraso"
               (map (fn [{:keys [vuelo inicio fin] :as o}]
                      (str/join "," [(:codigo vuelo) (:aerolinea vuelo) (name (:operacion vuelo))
                                     (name (:categoria (:avion vuelo))) (name (:prioridad vuelo)) (id-pista o)
                                     (hora (:programado vuelo)) (hora inicio) (hora fin) (m/retraso o)]))
                    operaciones))))

(defn errores-csv
  "RF03: primero los errores de pistas y luego los de vuelos."
  [errores]
  (texto (cons "archivo,linea,motivo"
               (map (fn [{:keys [archivo linea motivo]}] (str archivo "," linea "," motivo)) errores))))

;; ---------- Secciones del reporte

(defn- rf03 [d]
  (seccion "RF03 · Validación de datos"
           [(str "Pistas | registros: " (:registros-pistas d) " | válidos: " (count (:pistas d))
                 " | inválidos: " (count (:errores-pistas d)))
            (str "Vuelos | registros: " (:registros-vuelos d) " | válidos: " (:vuelos-validos d)
                 " | inválidos: " (count (:errores-vuelos d)))
            "Detalle de los registros inválidos: errores.csv"]))

(defn- suma-retrasos [ops]
  (reduce + 0 (map m/retraso ops)))

(defn- retrasados [ops]
  (count (filter #(> (m/retraso %) umbral-retraso) ops)))

(defn- promedio [ops]
  (if (seq ops) (str (decimal (suma-retrasos ops) (count ops)) " min") sin-datos))

(defn- porcentaje-retrasados [ops]
  (if (seq ops) (str (decimal (* 100 (retrasados ops)) (count ops)) "%") sin-datos))

(defn- rf08 [ops]
  (seccion "RF08 · Resumen de retrasos"
           [(str "Operaciones asignadas: " (count ops))
            (str "Retraso promedio: " (promedio ops))
            (str "Retraso máximo: " (if (seq ops) (str (reduce max (map m/retraso ops)) " min") sin-datos))
            (str "Vuelos retrasados (más de " umbral-retraso " min): "
                 (if (seq ops) (str (retrasados ops) " (" (porcentaje-retrasados ops) ")") sin-datos))]))

(defn- por-retraso
  "De mayor a menor retraso; si empatan, por código."
  [x y]
  (let [c (compare (m/retraso y) (m/retraso x))]
    (if (zero? c) (compare (codigo x) (codigo y)) c)))

(defn- rf09 [ops]
  (seccion "RF09 · 5 vuelos más retrasados"
           (o-sin-datos (map-indexed (fn [i o]
                                       (str (inc i) ". " (codigo o) " | retraso: " (m/retraso o) " min | "
                                            (name (:operacion (:vuelo o))) " | " (id-pista o)))
                                     (take 5 (sort por-retraso ops)))
                        sin-datos)))

(defn- uso-de-pistas [ops pistas]
  (let [inicio (reduce min (map #(:programado (:vuelo %)) ops))
        fin (reduce max (map :fin ops))
        por-pista (group-by id-pista ops)]
    (cons (str "Período simulado: " (hora inicio) " a " (hora fin) " (" (- fin inicio) " min)")
          (map (fn [pista]
                 (let [suyas (get por-pista (:id pista) [])
                       ocupada (reduce + 0 (map #(- (:fin %) (:inicio %)) suyas))]
                   (str (:id pista) " | " (name (:estado pista)) " | operaciones: " (count suyas)
                        " | ocupada: " ocupada " min | ocupación: " (decimal (* 100 ocupada) (- fin inicio)) "%")))
               (sort-by :id pistas)))))

(defn- rf10 [ops pistas]
  (seccion "RF10 · Uso de pistas"
           (if (and (seq ops) (seq pistas)) (uso-de-pistas ops pistas) [sin-datos])))

(defn- por-promedio
  "RF11: de mayor a menor promedio (comparando fracciones exactas); si empatan, por nombre."
  [x y]
  (let [c (compare (* (:suma y) (:cantidad x)) (* (:suma x) (:cantidad y)))]
    (if (zero? c) (compare (:nombre x) (:nombre y)) c)))

(defn- aerolineas [ops]
  (->> (group-by #(:aerolinea (:vuelo %)) ops)
       (map (fn [[nombre suyas]] {:nombre nombre :suma (suma-retrasos suyas) :cantidad (count suyas)}))
       (sort por-promedio)))

(defn- rf11 [lista]
  (seccion "RF11 · Retraso promedio por aerolínea"
           (o-sin-datos (map (fn [{:keys [nombre suma cantidad]}]
                               (str nombre " | retraso promedio: " (decimal suma cantidad) " min | operaciones: " cantidad))
                             lista)
                        sin-datos)))

(defn- rf12 [no-asignables]
  (seccion "RF12 · Vuelos no asignables"
           (o-sin-datos (map (fn [{:keys [vuelo motivo]}]
                               (str (:codigo vuelo) " | " (name (:operacion vuelo)) " | "
                                    (name (:categoria (:avion vuelo))) " | " motivo))
                             no-asignables)
                        "Ninguno")))

(defn- rf13 [ops]
  (seccion "RF13 · Operaciones por tipo y categoría"
           (concat (map (fn [tipo] (str (name tipo) ": " (count (filter #(= tipo (:operacion (:vuelo %))) ops))))
                        [:Aterrizaje :Despegue])
                   (map (fn [categoria] (str categoria ": " (count (filter #(= (keyword categoria) (:categoria (:avion (:vuelo %))))
                                                                           ops))))
                        m/nombres-categoria))))

(defn- pista-mas-usada [ops pistas]
  (let [usos (frequencies (map id-pista ops))
        usos-de #(get usos (:id %) 0)
        mas-usada (first (sort (fn [x y]
                                 (let [c (compare (usos-de y) (usos-de x))]
                                   (if (zero? c) (compare (:id x) (:id y)) c)))
                               pistas))]
    (if (and (seq ops) mas-usada)
      (str (:id mas-usada) " (operaciones: " (usos-de mas-usada) ")")
      sin-datos)))

(defn- rf14 [d lista]
  (let [ops (:operaciones d)]
    ["== RF14 · Resumen ejecutivo =="
     (str "Vuelos cargados: " (:registros-vuelos d))
     (str "Vuelos válidos: " (:vuelos-validos d))
     (str "Vuelos inválidos: " (count (:errores-vuelos d)))
     (str "Vuelos asignados: " (count ops))
     (str "Vuelos no asignables: " (count (:no-asignables d)))
     (str "Retraso promedio: " (promedio ops))
     (str "Vuelos retrasados: " (porcentaje-retrasados ops))
     (str "Pista más usada: " (pista-mas-usada ops (:pistas d)))
     (str "Aerolínea con mayor retraso promedio: "
          (if-let [{:keys [nombre suma cantidad]} (first lista)]
            (str nombre " (" (decimal suma cantidad) " min)")
            sin-datos))]))

(defn reporte
  "reporte.txt completo (RF03 y RF08 a RF14)."
  [d]
  (let [ops (:operaciones d)
        lista (aerolineas ops)]
    (texto (concat ["SIMULADOR DE OPERACIONES AEROPORTUARIAS · REPORTE" ""]
                   (rf03 d) (rf08 ops) (rf09 ops) (rf10 ops (:pistas d))
                   (rf11 lista) (rf12 (:no-asignables d)) (rf13 ops) (rf14 d lista)))))
```

### `clojure/src/simulador/medicion.clj`

```clojure
;; =============================================================================
;;  MÓDULO 6 · MEDICIÓN (Bloque 3, sección 5)
;;  Toma el tiempo de cada etapa con System/nanoTime y, con --medir, lo escribe en un archivo.
;;  Cada etapa devuelve su resultado ya calculado (regla de materialización: vectores, no secuencias perezosas).
;; =============================================================================
(ns simulador.medicion
  (:require [clojure.string :as str]))

(def encabezado "lectura_ns,validacion_ns,simulacion_ns,reportes_ns,escritura_ns")

(defn medir
  "Ejecuta la etapa (una función sin argumentos) y devuelve su valor y lo que tardó, en nanosegundos."
  [etapa]
  (let [inicio (System/nanoTime)
        valor (etapa)]
    {:valor valor :ns (- (System/nanoTime) inicio)}))

(defn escribir
  "Archivo de --medir: encabezado y una línea con las cinco duraciones."
  [archivo duraciones]
  (spit archivo (str encabezado "\n" (str/join "," duraciones) "\n") :encoding "UTF-8"))
```

### `clojure/src/simulador/main.clj`

```clojure
;; =============================================================================
;;  MÓDULO 7 · PROGRAMA PRINCIPAL
;;  Revisa los argumentos y encadena las cinco etapas: lectura -> validación -> simulación ->
;;  reportes -> escritura. Toda la lógica está en los otros módulos; aquí solo se conectan.
;; =============================================================================
(ns simulador.main
  (:require [clojure.java.io :as io]
            [simulador.lectura :as lectura]
            [simulador.medicion :as medicion]
            [simulador.reportes :as reportes]
            [simulador.torre-control :as torre]
            [simulador.validacion :as validacion])
  (:import (java.io File)
           (java.nio.charset StandardCharsets))
  (:gen-class))

(def ^:private modo-de-uso
  "Uso: java -jar simulador-<lenguaje>.jar <pistas.csv> <vuelos.csv> <carpeta_salida> [--medir <archivo>]")

;; ---------- Etapas

(defn- validar [{:keys [pistas vuelos]}]
  (let [registros-pistas (lectura/registros pistas)
        registros-vuelos (lectura/registros vuelos)
        resultados-pistas (validacion/validar-pistas registros-pistas)
        resultados-vuelos (validacion/validar-vuelos registros-vuelos)]
    {:registros-pistas (count registros-pistas)
     :pistas (validacion/validos resultados-pistas)
     :errores-pistas (validacion/errores resultados-pistas)
     :registros-vuelos (count registros-vuelos)
     :vuelos (validacion/validos resultados-vuelos)
     :errores-vuelos (validacion/errores resultados-vuelos)}))

(defn- simular [{:keys [vuelos pistas]}]
  {:operaciones (torre/simular (torre/asignables vuelos pistas) pistas)
   :no-asignables (torre/no-asignables vuelos pistas)})

(defn- reportar [v s]
  {:operaciones (reportes/operaciones-csv (:operaciones s))
   :errores (reportes/errores-csv (into (:errores-pistas v) (:errores-vuelos v)))
   :reporte (reportes/reporte {:registros-pistas (:registros-pistas v)
                               :pistas (:pistas v)
                               :errores-pistas (:errores-pistas v)
                               :registros-vuelos (:registros-vuelos v)
                               :vuelos-validos (count (:vuelos v))
                               :errores-vuelos (:errores-vuelos v)
                               :operaciones (:operaciones s)
                               :no-asignables (:no-asignables s)})})

(defn- imprimir
  "Escribe en pantalla siempre en UTF-8, sin depender de la configuración regional del equipo."
  [^String texto]
  (.writeBytes System/out (.getBytes texto StandardCharsets/UTF_8))
  (.flush System/out))

(defn- escribir [salida {:keys [operaciones errores reporte]}]
  (.mkdirs ^File (io/file salida))
  (spit (io/file salida "operaciones.csv") operaciones :encoding "UTF-8")
  (spit (io/file salida "errores.csv") errores :encoding "UTF-8")
  (spit (io/file salida "reporte.txt") reporte :encoding "UTF-8")
  (imprimir reporte)
  salida)

;; ---------- Argumentos

(defn- problema-de-uso
  "Motivo del error de uso, si lo hay: cantidad de argumentos o archivo de entrada ilegible."
  [args]
  (if-not (or (= 3 (count args)) (and (= 5 (count args)) (= "--medir" (nth args 3))))
    "número de argumentos incorrecto"
    (some #(when-not (lectura/se-puede-leer? %) (str "no se puede leer el archivo " %))
          (take 2 args))))

(defn- ejecutar [pistas vuelos salida archivo-medicion]
  (let [leido (medicion/medir (fn [] {:pistas (lectura/leer-lineas pistas) :vuelos (lectura/leer-lineas vuelos)}))
        validado (medicion/medir #(validar (:valor leido)))
        simulado (medicion/medir #(simular (:valor validado)))
        textos (medicion/medir #(reportar (:valor validado) (:valor simulado)))
        escrito (medicion/medir #(escribir salida (:valor textos)))]
    (when archivo-medicion
      (medicion/escribir archivo-medicion (map :ns [leido validado simulado textos escrito])))))

(defn -main [& args]
  (let [args (vec args)]
    (if-let [motivo (problema-de-uso args)]
      (do (imprimir (str "ERROR: " motivo "\n" modo-de-uso "\n"))
          (System/exit 2))
      (let [[pistas vuelos salida _ archivo-medicion] args]
        (ejecutar pistas vuelos salida archivo-medicion)))))
```

---

## Anexo D · Ejemplo resuelto a mano: entradas y salidas esperadas

Las tres versiones producen exactamente estas salidas con estas entradas.

### `datos/ejemplo/pistas.csv`

```csv
id,longitud,uso,estado
P01,2600,Mixta,Operativa
P02,2200,Despegue,Operativa
P03,1500,Aterrizaje,Operativa
P04,3500,Aterrizaje,Cerrada
P05,abc,Mixta,Operativa
```

### `datos/ejemplo/vuelos.csv`

```csv
codigo,aerolinea,matricula,categoria,operacion,dia,hora,prioridad
AV101,Avianca,HK5021,Mediano,Aterrizaje,1,08:00,Normal
LA202,LATAM,CC-BAW,Mediano,Despegue,1,08:00,Normal
AV103,Avianca,HK5100,Ligero,Aterrizaje,1,08:01,Normal
CM304,Copa,HP1825,Mediano,Aterrizaje,1,08:01,Emergencia
AV105,Avianca,HK5022,Mediano,Despegue,1,08:02,Normal
LA206,LATAM,CC-BAX,Ligero,Despegue,1,08:02,Normal
CM307,Copa,HP1830,Mediano,Aterrizaje,1,08:03,Normal
AV108,Avianca,HK5300,Pesado,Aterrizaje,1,08:05,Normal
LA209,LATAM,CC-BAY,Mediano,Despegue,1,08:04,Normal
CM310,Copa,HP1840,Jumbo,Despegue,1,08:05,Normal
AV101,Avianca,HK5023,Ligero,Despegue,1,08:06,Normal
AV112,Avianca,HK5024,Ligero,Despegue,1,8:10,Normal
LA213,LATAM,CC-BAZ,Ligero,Aterrizaje,1,08:20,Normal
```

### `datos/ejemplo/esperado/operaciones.csv`

```csv
codigo,aerolinea,operacion,categoria,prioridad,pista,programada,inicio,fin,retraso
AV101,Avianca,Aterrizaje,Mediano,Normal,P01,D1 08:00,D1 08:00,D1 08:03,0
LA202,LATAM,Despegue,Mediano,Normal,P02,D1 08:00,D1 08:00,D1 08:03,0
AV103,Avianca,Aterrizaje,Ligero,Normal,P03,D1 08:01,D1 08:01,D1 08:03,0
CM304,Copa,Aterrizaje,Mediano,Emergencia,P01,D1 08:01,D1 08:03,D1 08:06,2
AV105,Avianca,Despegue,Mediano,Normal,P02,D1 08:02,D1 08:03,D1 08:06,1
CM307,Copa,Aterrizaje,Mediano,Normal,P01,D1 08:03,D1 08:06,D1 08:09,3
LA206,LATAM,Despegue,Ligero,Normal,P02,D1 08:02,D1 08:06,D1 08:08,4
LA209,LATAM,Despegue,Mediano,Normal,P02,D1 08:04,D1 08:08,D1 08:11,4
LA213,LATAM,Aterrizaje,Ligero,Normal,P01,D1 08:20,D1 08:20,D1 08:22,0
```

### `datos/ejemplo/esperado/errores.csv`

```csv
archivo,linea,motivo
pistas,6,longitud no es un entero: abc
vuelos,11,categoría con valor no válido: Jumbo (valores: Ligero/Mediano/Pesado)
vuelos,12,código repetido: AV101
vuelos,13,hora no válida: 8:10 (formato HH:MM de 00:00 a 23:59)
```

### `datos/ejemplo/esperado/reporte.txt`

```text
SIMULADOR DE OPERACIONES AEROPORTUARIAS · REPORTE

== RF03 · Validación de datos ==
Pistas | registros: 5 | válidos: 4 | inválidos: 1
Vuelos | registros: 13 | válidos: 10 | inválidos: 3
Detalle de los registros inválidos: errores.csv

== RF08 · Resumen de retrasos ==
Operaciones asignadas: 9
Retraso promedio: 1.56 min
Retraso máximo: 4 min
Vuelos retrasados (más de 15 min): 0 (0.00%)

== RF09 · 5 vuelos más retrasados ==
1. LA206 | retraso: 4 min | Despegue | P02
2. LA209 | retraso: 4 min | Despegue | P02
3. CM307 | retraso: 3 min | Aterrizaje | P01
4. CM304 | retraso: 2 min | Aterrizaje | P01
5. AV105 | retraso: 1 min | Despegue | P02

== RF10 · Uso de pistas ==
Período simulado: D1 08:00 a D1 08:22 (22 min)
P01 | Operativa | operaciones: 4 | ocupada: 11 min | ocupación: 50.00%
P02 | Operativa | operaciones: 4 | ocupada: 11 min | ocupación: 50.00%
P03 | Operativa | operaciones: 1 | ocupada: 2 min | ocupación: 9.09%
P04 | Cerrada | operaciones: 0 | ocupada: 0 min | ocupación: 0.00%

== RF11 · Retraso promedio por aerolínea ==
Copa | retraso promedio: 2.50 min | operaciones: 2
LATAM | retraso promedio: 2.00 min | operaciones: 4
Avianca | retraso promedio: 0.33 min | operaciones: 3

== RF12 · Vuelos no asignables ==
AV108 | Aterrizaje | Pesado | sin pista con longitud suficiente

== RF13 · Operaciones por tipo y categoría ==
Aterrizaje: 5
Despegue: 4
Ligero: 3
Mediano: 6
Pesado: 0

== RF14 · Resumen ejecutivo ==
Vuelos cargados: 13
Vuelos válidos: 10
Vuelos inválidos: 3
Vuelos asignados: 9
Vuelos no asignables: 1
Retraso promedio: 1.56 min
Vuelos retrasados: 0.00%
Pista más usada: P01 (operaciones: 4)
Aerolínea con mayor retraso promedio: Copa (2.50 min)
```

### `datos/aeropuerto/pistas.csv`

```csv
id,longitud,uso,estado
P01,3200,Mixta,Operativa
P02,2800,Aterrizaje,Operativa
P03,2900,Despegue,Operativa
P04,2100,Mixta,Operativa
P05,1500,Aterrizaje,Operativa
P06,3000,Despegue,Cerrada
```

---

## Anexo E · Resultados detallados

### E.1 Mediana por etapa en cada escenario (ms)

| Escenario | Lenguaje | Lectura | Validación | Simulación | Reportes | Escritura | t_operaciones | t_proceso | Fuera de las operaciones |
|---|---|---|---|---|---|---|---|---|---|
| V1 | Java | 6 | 107 | 82 | 93 | 1 | 285 | 365 | 79 |
| V1 | Scala | 14 | 111 | 94 | 131 | 1 | 339 | 539 | 200 |
| V1 | Clojure | 7 | 65 | 98 | 54 | 8 | 212 | 838 | 626 |
| V2 | Java | 14 | 257 | 254 | 164 | 3 | 665 | 775 | 110 |
| V2 | Scala | 16 | 287 | 257 | 216 | 3 | 755 | 961 | 206 |
| V2 | Clojure | 17 | 243 | 343 | 163 | 12 | 759 | 1.429 | 670 |
| V3 | Java | 61 | 878 | 988 | 519 | 15 | 2.419 | 2.594 | 176 |
| V3 | Scala | 48 | 957 | 900 | 715 | 17 | 2.554 | 2.839 | 285 |
| V3 | Clojure | 62 | 1.251 | 1.334 | 718 | 51 | 3.311 | 4.041 | 730 |
| V4 | Java | 394 | 5.010 | 4.367 | 2.660 | 173 | 12.047 | 12.819 | 772 |
| V4 | Scala | 416 | 5.559 | 3.004 | 4.378 | 133 | 13.001 | 13.921 | 921 |
| V4 | Clojure | 590 | 7.856 | 6.363 | 5.473 | 140 | 19.806 | 21.329 | 1.523 |
| C1 | Java | 60 | 898 | 1.079 | 556 | 16 | 2.529 | 2.692 | 164 |
| C1 | Scala | 49 | 992 | 904 | 641 | 19 | 2.585 | 2.852 | 267 |
| C1 | Clojure | 63 | 1.260 | 1.273 | 713 | 49 | 3.288 | 4.044 | 756 |
| X1 | Java | 58 | 910 | 991 | 495 | 24 | 2.408 | 2.599 | 191 |
| X1 | Scala | 50 | 920 | 831 | 727 | 22 | 2.475 | 2.769 | 294 |
| X1 | Clojure | 64 | 1.259 | 1.313 | 650 | 55 | 3.280 | 4.083 | 804 |

"Fuera de las operaciones" = t_proceso − t_operaciones: arranque de la JVM y del lenguaje, lectura, escritura y cierre.

### E.2 Puntaje proporcional por escenario

| Criterio | Lenguaje | V1 | V2 | V3 | V4 | C1 | X1 | Promedio |
|---|---|---|---|---|---|---|---|---|
| Tiempo | Java | 74,45 | 100,00 | 100,00 | 100,00 | 100,00 | 100,00 | **95,74** |
| Tiempo | Scala | 62,61 | 88,13 | 94,69 | 92,66 | 97,83 | 97,27 | **88,86** |
| Tiempo | Clojure | 100,00 | 87,69 | 73,04 | 60,82 | 76,90 | 73,41 | **78,64** |
| Memoria | Java | 100,00 | 88,33 | 80,74 | 100,00 | 80,87 | 81,23 | **88,53** |
| Memoria | Scala | 79,55 | 100,00 | 100,00 | 94,63 | 100,00 | 100,00 | **95,70** |
| Memoria | Clojure | 58,22 | 82,01 | 90,84 | 78,93 | 72,51 | 73,33 | **75,97** |
| Rendimiento | Java | 100,00 | 100,00 | 100,00 | 100,00 | 100,00 | 100,00 | **100,00** |
| Rendimiento | Scala | 67,67 | 80,63 | 91,36 | 92,08 | 94,39 | 93,85 | **86,66** |
| Rendimiento | Clojure | 43,53 | 54,22 | 64,19 | 60,10 | 66,58 | 63,65 | **58,71** |

### E.3 Resumen por escenario (mediana [mínimo – máximo] y RIC)

#### V1 · 1.000 vuelos

| Lenguaje | t_operaciones (ms) | t_proceso (ms) | Vuelos/s | Memoria máx. (MB) | Correctas |
|---|---|---|---|---|---|
| java | 285 [238 – 331] RIC 65 | 365 [326 – 423] RIC 56 | 2741 [2363 – 3068] RIC 413 | 62 [60 – 76] RIC 14 | 10/10 |
| scala | 339 [291 – 379] RIC 17 | 539 [484 – 590] RIC 31 | 1855 [1695 – 2065] RIC 103 | 78 [77 – 92] RIC 2 | 10/10 |
| clojure | 212 [183 – 251] RIC 37 | 838 [760 – 929] RIC 63 | 1193 [1077 – 1316] RIC 90 | 106 [102 – 111] RIC 3 | 10/10 |

#### V2 · 10.000 vuelos

| Lenguaje | t_operaciones (ms) | t_proceso (ms) | Vuelos/s | Memoria máx. (MB) | Correctas |
|---|---|---|---|---|---|
| java | 665 [619 – 888] RIC 89 | 775 [727 – 999] RIC 83 | 12909 [10015 – 13754] RIC 1336 | 171 [146 – 172] RIC 9 | 10/10 |
| scala | 755 [638 – 843] RIC 35 | 961 [883 – 1073] RIC 63 | 10408 [9322 – 11326] RIC 666 | 151 [132 – 169] RIC 30 | 10/10 |
| clojure | 759 [666 – 823] RIC 41 | 1429 [1336 – 1482] RIC 68 | 6999 [6745 – 7487] RIC 333 | 185 [175 – 203] RIC 6 | 10/10 |

#### V3 · 100.000 vuelos

| Lenguaje | t_operaciones (ms) | t_proceso (ms) | Vuelos/s | Memoria máx. (MB) | Correctas |
|---|---|---|---|---|---|
| java | 2419 [2280 – 2627] RIC 136 | 2594 [2460 – 2805] RIC 123 | 38553 [35652 – 40657] RIC 1833 | 741 [660 – 759] RIC 41 | 10/10 |
| scala | 2554 [2342 – 2905] RIC 66 | 2839 [2600 – 3188] RIC 40 | 35222 [31370 – 38468] RIC 498 | 599 [576 – 627] RIC 26 | 10/10 |
| clojure | 3311 [3103 – 3566] RIC 116 | 4041 [3884 – 4462] RIC 128 | 24747 [22414 – 25745] RIC 772 | 659 [604 – 955] RIC 34 | 10/10 |

#### V4 · 1.000.000 vuelos

| Lenguaje | t_operaciones (ms) | t_proceso (ms) | Vuelos/s | Memoria máx. (MB) | Correctas |
|---|---|---|---|---|---|
| java | 12047 [11183 – 12907] RIC 412 | 12819 [11953 – 13751] RIC 390 | 78012 [72722 – 83660] RIC 2390 | 3065 [2865 – 3347] RIC 195 | 10/10 |
| scala | 13001 [12286 – 14062] RIC 992 | 13921 [13194 – 14903] RIC 1042 | 71833 [67101 – 75792] RIC 5429 | 3238 [2630 – 3532] RIC 282 | 10/10 |
| clojure | 19806 [19155 – 20428] RIC 489 | 21329 [20785 – 21952] RIC 558 | 46884 [45553 – 48113] RIC 1237 | 3883 [3765 – 4033] RIC 120 | 10/10 |

#### C1 · 100.000 vuelos

| Lenguaje | t_operaciones (ms) | t_proceso (ms) | Vuelos/s | Memoria máx. (MB) | Correctas |
|---|---|---|---|---|---|
| java | 2529 [2312 – 3093] RIC 137 | 2692 [2482 – 3282] RIC 136 | 37145 [30474 – 40288] RIC 1835 | 738 [696 – 755] RIC 40 | 10/10 |
| scala | 2585 [2357 – 2930] RIC 182 | 2852 [2612 – 3256] RIC 154 | 35062 [30710 – 38285] RIC 1934 | 597 [578 – 620] RIC 19 | 10/10 |
| clojure | 3288 [3080 – 3798] RIC 312 | 4044 [3759 – 4636] RIC 324 | 24729 [21571 – 26600] RIC 1889 | 823 [637 – 921] RIC 209 | 10/10 |

#### X1 · 100.000 vuelos

| Lenguaje | t_operaciones (ms) | t_proceso (ms) | Vuelos/s | Memoria máx. (MB) | Correctas |
|---|---|---|---|---|---|
| java | 2408 [2204 – 2572] RIC 65 | 2599 [2378 – 2779] RIC 53 | 38483 [35985 – 42046] RIC 778 | 734 [682 – 750] RIC 32 | 10/10 |
| scala | 2475 [2418 – 2525] RIC 84 | 2769 [2711 – 2839] RIC 67 | 36116 [35226 – 36893] RIC 874 | 596 [575 – 619] RIC 14 | 10/10 |
| clojure | 3280 [2859 – 3646] RIC 233 | 4083 [3585 – 4370] RIC 298 | 24494 [22886 – 27897] RIC 1820 | 813 [601 – 1006] RIC 276 | 10/10 |


### E.4 Entorno registrado (`resultados/entorno.txt`)

```text
ENTORNO DEL EXPERIMENTO
Fecha: 2026-11-14T15:20:30-05:00
Modo: medición completa

== Equipo ==
Sistema: Linux-6.18.44-fc-v470-x86_64-with-glibc2.39
Procesador: x86_64
Núcleos: 2
Energía: no aplica (no es macOS)
Modo de bajo consumo: no aplica (no es macOS)

== Software ==
Java: openjdk version "21.0.12.1" 2026-08-18 | OpenJDK Runtime Environment (build 21.0.12.1+1-1-24.04.4-Ubuntu) | OpenJDK 64-Bit Server VM (build 21.0.12.1+1-1-24.04.4-Ubuntu, mixed mode, sharing)
Opciones de la JVM: -Xmx4g -XX:+UseG1GC
Scala: 3.9.0 (project.scala) | no disponible
Clojure: 1.12.0 (project.clj) | no disponible
Python (orquestador e implementación de referencia): 3.13.18
SHA-256 de simulador-java.jar: a34b2a538cb84450fa3d5d416c75a0c3aa3ac4adaa617159c28b5c88339f92c7
SHA-256 de simulador-scala.jar: 8bac948c0dfa0149ca143fcf3742abc3e1e732a34509678eccde245c6509bd1a
SHA-256 de simulador-clojure.jar: 47aad9ed1722a22c334d9d0ca61bfc59354454790d694432705da78e3cec681e
Commit: 9c61a84 (con cambios sin guardar)

Nota: Los tres .jar se construyeron en el MacBook Pro del equipo con las herramientas oficiales (javac, scala-cli con Scala 3.9.0, lein uberjar con Clojure 1.12.0) y se midieron en este contenedor Linux de la nube con OpenJDK 21, porque la medición no se pudo lanzar en el Mac de forma desatendida. Los tres lenguajes se midieron en el mismo entorno y con las mismas opciones.

== Protocolo ==
Escenarios: V1, V2, V3, V4, C1, X1
Rondas: 1 de calentamiento (ronda 0, no cuenta) + 10 medidas
Orden de los lenguajes rotado por ronda; 1 s de pausa entre ejecuciones; un proceso nuevo por ejecución
Memoria máxima del orquestador antes de medir: 20 MB
```

### E.5 Casos de verificación (`resultados/verificacion.csv`)

Los 19 casos (E0, V1, V2, V3, V4, C1, X1, R01–R12) dieron "ok" en Java, Scala y Clojure.

---

## Anexo F · Archivos de construcción y configuración

### `java/construir.sh`

```bash
#!/usr/bin/env bash
# Construye java/simulador-java.jar con javac y jar (JDK 21). Uso: bash java/construir.sh
set -euo pipefail
cd "$(dirname "$0")"
rm -rf clases simulador-java.jar
javac --release 21 -encoding UTF-8 -d clases src/simulador/*.java
jar --create --file simulador-java.jar --main-class simulador.Main -C clases .
rm -rf clases
echo "Listo: java/simulador-java.jar"
```

### `scala/construir.sh`

```bash
#!/usr/bin/env bash
# Construye scala/simulador-scala.jar con Scala CLI (incluye la biblioteca de Scala). Uso: bash scala/construir.sh
# --server=false: compila sin dejar un servidor de compilación corriendo, que afectaría las mediciones.
set -euo pipefail
cd "$(dirname "$0")"
rm -f simulador-scala.jar
scala-cli --power package . --assembly --server=false -f -o simulador-scala.jar
echo "Listo: scala/simulador-scala.jar"
```

### `clojure/construir.sh`

```bash
#!/usr/bin/env bash
# Construye clojure/simulador-clojure.jar con Leiningen (compilación AOT). Uso: bash clojure/construir.sh
set -euo pipefail
cd "$(dirname "$0")"
rm -f simulador-clojure.jar
lein uberjar
cp target/uberjar/simulador-clojure.jar simulador-clojure.jar
echo "Listo: clojure/simulador-clojure.jar"
```

### `herramientas/entorno.sh`

```bash
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
```

### `.run/Verificar.run.xml`

```xml
<component name="ProjectRunConfigurationManager">
  <configuration default="false" name="Verificar equivalencia" type="ShConfigurationType">
    <option name="SCRIPT_TEXT" value="" />
    <option name="INDEPENDENT_SCRIPT_PATH" value="true" />
    <option name="SCRIPT_PATH" value="$PROJECT_DIR$/experimento/verificar.sh" />
    <option name="SCRIPT_OPTIONS" value="" />
    <option name="INDEPENDENT_SCRIPT_WORKING_DIRECTORY" value="true" />
    <option name="SCRIPT_WORKING_DIRECTORY" value="$PROJECT_DIR$" />
    <option name="INDEPENDENT_INTERPRETER_PATH" value="true" />
    <option name="INTERPRETER_PATH" value="/bin/bash" />
    <option name="INTERPRETER_OPTIONS" value="" />
    <option name="EXECUTE_IN_TERMINAL" value="false" />
    <option name="EXECUTE_SCRIPT_FILE" value="true" />
    <envs />
    <method v="2" />
  </configuration>
</component>
```

### `experimento/verificar.sh`

```bash
#!/usr/bin/env bash
# =============================================================================
#  Verificación de equivalencia (Bloque 3, paso 4 del protocolo)
#  Construye cada versión y la ejecuta en el ejemplo (E0), en los escenarios que tengan salida esperada
#  y en los 12 casos de robustez (R01-R12). Compara byte a byte los 3 archivos y lo que sale en pantalla.
#
#  Uso: bash experimento/verificar.sh [java] [scala] [clojure] [referencia]
#       sin argumentos verifica java, scala y clojure. "referencia" prueba el propio verificador.
#       SIN_CONSTRUIR=1 usa los .jar que ya existen, sin volver a construirlos.
#       RESULTADOS_CSV=<archivo> guarda además el resultado de cada caso (caso,lenguaje,resultado).
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
if [ -n "${RESULTADOS_CSV:-}" ]; then
  { echo "caso,lenguaje,resultado"
    for L in $LENGUAJES; do sed "s/^\([^|]*\)|\(.*\)$/\1,$L,\2/" "$TMP/res_$L"; done
  } >"$RESULTADOS_CSV"
fi
echo
if [ "$FALLAS" -eq 0 ]; then echo "RESULTADO: todo coincide"; else echo "RESULTADO: $FALLAS caso(s) con diferencias"; fi
[ "$FALLAS" -eq 0 ]
```

