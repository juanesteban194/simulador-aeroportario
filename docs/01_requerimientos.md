# 01 · Requerimientos · Simulador de operaciones aeroportuarias

## 1. Contexto

Un aeropuerto tiene varias pistas. La **torre de control** recibe la programación de vuelos del día o de
varios días: despegues y aterrizajes. Con ella debe:

- organizar el orden de las operaciones;
- asignar automáticamente cada vuelo a una pista compatible y libre, según su prioridad;
- calcular cuánto se retrasa cada vuelo;
- generar reportes del funcionamiento del aeropuerto.

El mismo simulador se implementa en **Java, Scala y Clojure**. Las tres versiones deben cumplir estos
requisitos y producir **exactamente la misma salida** con las mismas entradas.

## 2. Entidades

Las entidades del enunciado son **datos inmutables**: una vez creadas no cambian, y cualquier "cambio"
produce un dato nuevo. El comportamiento está en funciones puras (TorreControl).

| Entidad | Qué representa | Datos |
|---|---|---|
| **Avión** | La aeronave que opera el vuelo | Matrícula, categoría (Ligero, Mediano o Pesado) |
| **Vuelo** | Una operación programada | Código, aerolínea, avión, operación (Despegue o Aterrizaje), día y hora programados, prioridad (Normal o Emergencia) |
| **Pista** | Una pista del aeropuerto | Identificador, longitud en metros, uso permitido (Despegue, Aterrizaje o Mixta), estado (Operativa o Cerrada) |
| **Aeropuerto** | El estado del aeropuerto en un momento de la simulación | Pistas, momento en que cada pista queda libre, vuelos en espera, operaciones ya asignadas |
| **TorreControl** | Las reglas de operación | Funciones que ordenan, asignan pistas y calculan retrasos. Reciben un estado del aeropuerto y devuelven uno nuevo |

El resultado de la simulación es una lista de **operaciones asignadas**. Cada una indica el vuelo, la pista,
la hora real de inicio y fin, y el retraso.

## 3. Reglas del negocio (RN)

| RN | Regla |
|---|---|
| **RN01** · Tiempo | El tiempo se mide en minutos enteros. Una hora se expresa como día (1, 2, 3…) y HH:MM. |
| **RN02** · Requisitos de cada categoría | Ligero: pista de 1.200 m o más; ocupa la pista 2 min.<br>Mediano: 2.000 m o más; 3 min.<br>Pesado: 2.800 m o más; 4 min. |
| **RN03** · Compatibilidad | Un vuelo puede usar una pista si se cumplen las tres condiciones:<br>1. la pista está **Operativa**;<br>2. su uso es **Mixta** o coincide con la operación del vuelo;<br>3. su longitud es **mayor o igual** a la que exige la categoría del avión. |
| **RN04** · Espera | Un vuelo entra a la cola de espera en su hora programada. Antes de esa hora no puede operar. |
| **RN05** · Prioridad | Entre los vuelos en espera, el orden es:<br>1. **Emergencia** antes que Normal;<br>2. **Aterrizaje** antes que Despegue;<br>3. **hora programada** más temprana;<br>4. **código** de vuelo menor (orden alfabético). |
| **RN06** · Asignación automática (extra del proyecto) | En cada minuto en que haya pistas libres y vuelos en espera, la torre recorre la cola en el orden de RN05. Cada vuelo que tenga una pista **libre y compatible** recibe la de **identificador menor**.<br>El vuelo de mayor prioridad que no tenga pista compatible libre no bloquea a los demás: sigue esperando y se pasa al siguiente. |
| **RN07** · Ocupación | Una pista asignada queda ocupada desde la hora real de inicio hasta inicio + los minutos de la categoría del avión (RN02). |
| **RN08** · Retraso | Retraso = hora real de inicio − hora programada, en minutos. Nunca es negativo. Un vuelo está **retrasado** si su retraso es mayor a **15 minutos**. |
| **RN09** · Vuelo no asignable | Si ninguna pista del aeropuerto es compatible con el vuelo (RN03), el vuelo no entra a la cola. Se reporta con el motivo:<br>· primero se revisa si hay alguna pista operativa habilitada para la operación; si no, "sin pista habilitada para la operación";<br>· si sí la hay pero ninguna es suficientemente larga: "sin pista con longitud suficiente". |
| **RN10** · Determinismo | La simulación no usa números aleatorios ni la hora del sistema. Las mismas entradas producen siempre la misma salida, en los tres lenguajes. |

## 4. Requisitos funcionales (RF)

| RF | Descripción |
|---|---|
| **RF01** | Cargar las pistas del aeropuerto desde un archivo: identificador, longitud, uso permitido y estado. |
| **RF02** | Cargar los vuelos desde un archivo: código, aerolínea, matrícula y categoría del avión, operación, día y hora programados, prioridad. |
| **RF03** | Validar cada registro. Un registro inválido se reporta con su número de línea y el motivo, y se excluye. El programa **nunca se detiene** por un dato inválido (ver sección 5). |
| **RF04** | Construir la cola de espera y ordenarla según las prioridades (RN04 y RN05). |
| **RF05** | Asignar automáticamente una pista libre y compatible a cada vuelo (RN03, RN06 y RN07). |
| **RF06** | Calcular la hora real de inicio, la hora de fin y el retraso de cada operación (RN08). |
| **RF07** | Listar el programa final de operaciones, en orden de inicio real: vuelo, operación, pista, hora programada, hora real, retraso. |
| **RF08** | Resumen de retrasos: retraso promedio, retraso máximo y porcentaje de vuelos retrasados (más de 15 min). |
| **RF09** | Los **5 vuelos más retrasados**. Si empatan, se ordenan por código. |
| **RF10** | Uso de cada pista: número de operaciones, minutos ocupada y porcentaje de ocupación. El período simulado va desde la primera hora programada hasta el fin de la última operación. |
| **RF11** | Retraso promedio por aerolínea, de mayor a menor. Si empatan, se ordenan por nombre. |
| **RF12** | Vuelos no asignables, con su motivo (RN09). |
| **RF13** | Número de operaciones por tipo (Despegue o Aterrizaje) y por categoría de avión. |
| **RF14** | Resumen ejecutivo: total de vuelos cargados, válidos, inválidos, asignados y no asignables; retraso promedio; porcentaje de retrasados; pista más usada; aerolínea con mayor retraso promedio. |

## 5. Validaciones (RF03)

| Archivo | Campo | Regla |
|---|---|---|
| Pistas | Identificador | No vacío y no repetido |
| Pistas | Longitud | Entero mayor que 0 |
| Pistas | Uso | Despegue, Aterrizaje o Mixta |
| Pistas | Estado | Operativa o Cerrada |
| Vuelos | Código | No vacío y no repetido |
| Vuelos | Aerolínea y matrícula | No vacías |
| Vuelos | Categoría | Ligero, Mediano o Pesado |
| Vuelos | Operación | Despegue o Aterrizaje |
| Vuelos | Día | Entero mayor o igual a 1 |
| Vuelos | Hora | Formato HH:MM, de 00:00 a 23:59 |
| Vuelos | Prioridad | Normal o Emergencia |
| Ambos | Registro | Tiene exactamente el número de campos esperado |

**Casos límite:** si no hay pistas válidas, no hay vuelos válidos o un archivo está vacío, el programa lo
informa y los reportes muestran "Sin datos". No se divide entre cero ni se detiene.

## 6. Requisitos no funcionales (RNF)

Corresponden a las condiciones del enunciado del profesor.

| RNF | Requisito | Condición del enunciado |
|---|---|---|
| **RNF01** | Las tres versiones (Java, Scala y Clojure) cumplen los mismos RF y producen la misma salida, verificada carácter por carácter | 1 y 2 |
| **RNF02** | Programación funcional: sin `for`, `while` ni variables mutables. Se usan funciones de orden superior, lambdas, transformación (`map`), filtrado (`filter`), agrupación (`groupBy`) y reducción (`reduce` o `fold`) | 3 |
| **RNF03** | Errores como valores (`Optional`/`Either`, `Option`/`Either`, mapas de resultado). Las validaciones no lanzan excepciones | 3 · Confiabilidad |
| **RNF04** | Solo la biblioteca estándar de cada lenguaje | Equidad |
| **RNF05** | Los tres se ejecutan con `java -jar` sobre el mismo JDK 21; Clojure se compila por adelantado (AOT) | 6 |
| **RNF06** | Cada versión puede medir y registrar su propio comportamiento: tiempo por etapa y volumen procesado. Se define en el Bloque 3 | 5 |
| **RNF07** | Cantidades con 2 decimales, porcentajes con 2 decimales y el mismo formato de números en los tres lenguajes, sin depender de la configuración regional del equipo | 2 |

## 7. Ejecución

```
java -jar simulador-<lenguaje>.jar <archivo_pistas> <archivo_vuelos>
```

Imprime los reportes RF07 a RF14 en la salida estándar. El formato exacto de los archivos y de la salida
se define en el Bloque 2 (`02_modelo_y_contrato.md`).
