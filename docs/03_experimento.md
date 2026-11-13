# 03 · Diseño del experimento

Este documento define **qué se ejecuta, con qué datos, cómo se mide y bajo qué condiciones**. Responde a las
condiciones 4, 5 y 6 del enunciado:
- 4 · escenarios con distintos volúmenes y cargas;
- 5 · medir y registrar el comportamiento de cada solución;
- 6 · condiciones equivalentes para los tres lenguajes.

## 1. Aeropuerto común

Todos los escenarios usan el mismo aeropuerto: [`datos/aeropuerto/pistas.csv`](../datos/aeropuerto/pistas.csv).
Así, lo único que cambia entre escenarios son los vuelos.

| Pista | Longitud | Uso | Estado |
|---|---|---|---|
| P01 | 3.200 m | Mixta | Operativa |
| P02 | 2.800 m | Aterrizaje | Operativa |
| P03 | 2.900 m | Despegue | Operativa |
| P04 | 2.100 m | Mixta | Operativa |
| P05 | 1.500 m | Aterrizaje | Operativa |
| P06 | 3.000 m | Despegue | **Cerrada** |

Pistas compatibles con cada tipo de vuelo (RN03):

| | Ligero | Mediano | Pesado |
|---|---|---|---|
| **Aterrizaje** | P01 · P02 · P04 · P05 | P01 · P02 · P04 | P01 · P02 |
| **Despegue** | P01 · P03 · P04 | P01 · P03 · P04 | P01 · P03 |

P03 mide 2.900 m para que los despegues de aviones pesados tengan dos pistas. En la primera calibración solo
podían usar P01, que quedó como cuello de botella (ver D3.1).

## 2. Escenarios

| ID | Vuelos | Vuelos por día | Inválidos | Semilla | Qué evalúa |
|---|---|---|---|---|---|
| **E0** | 13 | — | 3 | — | Solo correctitud: el ejemplo resuelto a mano del Bloque 2 |
| **V1** | 1.000 | 1.500 | 0 % | 101 | Volumen pequeño |
| **V2** | 10.000 | 1.500 | 0 % | 102 | Volumen mediano |
| **V3** | 100.000 | 1.500 | 0 % | 103 | Volumen grande |
| **V4** | 1.000.000 | 1.500 | 0 % | 104 | Volumen muy grande |
| **C1** | 100.000 | 2.400 | 0 % | 201 | Carga: aeropuerto saturado, colas largas |
| **X1** | 100.000 | 1.500 | 10 % | 301 | Confiabilidad y costo de validar |

**Cómo se comporta cada escenario** (calculado con la implementación de referencia, sección 4):

| ID | Días | Ocupación media de las pistas | Retraso promedio | Vuelos retrasados |
|---|---|---|---|---|
| V1 | 1 | 40,0 % | 0,20 min | 0,00 % |
| V2 | 8 | 57,6 % | 0,96 min | 0,18 % |
| V3 | 68 | 60,1 % | 1,04 min | 0,16 % |
| V4 | 668 | 60,4 % | 1,04 min | 0,12 % |
| C1 | 52 | 78,1 % (P01, P03 y P04 al 100 %) | 5.414 min | 47,42 % |
| X1 | 68 | 54,1 % | 0,64 min | 0,00 % (90.032 válidos) |

**Cómo leer la tabla:**
- **V1 a V4** tienen la misma carga diaria. Cuando crece el tiempo de ejecución, la causa es el volumen.
- **C1** tiene los mismos 100.000 vuelos que V3, pero 60 % más por día, así que el aeropuerto se satura. El
  retraso se concentra en los despegues, porque los aterrizajes tienen prioridad (RN05). Esto también es un
  hallazgo para el informe.
- **X1** tiene los mismos 100.000 vuelos que V3, pero con un 10 % dañado.

## 3. Generador de datos

[`datos/generador.py`](../datos/generador.py) crea `datos/escenarios/<ID>/vuelos.csv`.

**Distribuciones**

| Campo | Distribución |
|---|---|
| Aerolínea | Avianca 25 %, LATAM 20 %, Copa 15 %, Wingo 10 %, JetSMART 10 %, American 8 %, Iberia 6 %, Viva 6 % |
| Código | Prefijo de la aerolínea + número consecutivo de 7 dígitos (`AV0000002`). Es único |
| Matrícula | Prefijo del país + 4 dígitos al azar (`HK-9711`) |
| Categoría | Ligero 30 %, Mediano 50 %, Pesado 20 % |
| Operación | Aterrizaje 50 %, Despegue 50 % |
| Prioridad | Emergencia 5 %, Normal 95 % |
| Día | El vuelo i va el día `i / vuelos_por_día + 1` (división entera) |
| Hora | Uniforme entre 00:00 y 23:59 |

**Errores en X1.** Cada registro tiene un 10 % de probabilidad de dañarse con uno de 10 errores, uno por cada
regla de validación del Bloque 2:
1. falta un campo;
2. código vacío;
3. código repetido;
4. aerolínea vacía;
5. matrícula vacía;
6. categoría `Jumbo`;
7. operación `Escala`;
8. día `uno`;
9. hora `24:10`;
10. prioridad `Urgente`.

**Determinismo**
- Cada escenario tiene su semilla fija.
- El generador solo usa `random.random()`, que da la misma secuencia en todas las versiones de Python desde
  la 3.2, y hace él mismo las elecciones con pesos.
- Volver a generar produce **exactamente el mismo archivo**. Se comprueba con las huellas SHA-256 de
  [`datos/escenarios/huellas.sha256`](../datos/escenarios/huellas.sha256):
  ```
  python3 datos/generador.py
  cd datos && shasum -a 256 -c escenarios/huellas.sha256
  ```
- En el repositorio están E0, V1 y V2 con sus salidas esperadas. V3, V4, C1 y X1 no se suben (V4 pesa 59 MB):
  se regeneran y se verifican con las huellas.

## 4. Salidas esperadas e implementación de referencia

[`experimento/referencia.py`](../experimento/referencia.py) implementa el contrato del Bloque 2 de la forma
más directa posible, sin restricciones funcionales.
- **No participa en la comparación.** Su único papel es producir las salidas esperadas de cada escenario.
- Coincide con el ejemplo resuelto a mano (E0).
- Si una versión difiere de la referencia, se revisa contra el contrato para saber cuál está mal.

**Salida correcta** = los tres archivos de la versión son **idénticos byte a byte** a los de la referencia.

## 5. Métricas e instrumentos

| Criterio | Peso | Métrica | Instrumento | Mejor |
|---|---|---|---|---|
| Tiempo de ejecución | 25 % | `t_operaciones` = validación + simulación + reportes, en ms | `System.nanoTime()` dentro del programa: el mismo reloj de la JVM en los tres | menor |
| Rendimiento | 20 % | Vuelos procesados por segundo en el proceso completo = registros del archivo de vuelos / `t_proceso` | Reloj externo del orquestador alrededor del proceso | mayor |
| Consumo de memoria | 20 % | Memoria residente máxima del proceso, en MB | `rusage` del sistema operativo (`os.wait4`), el mismo dato que muestra `/usr/bin/time -l` | menor |

Calidad, Confiabilidad y Uso funcional se definen en el Bloque 4.

**Etapas que mide cada programa**

| Etapa | Empieza | Termina cuando… |
|---|---|---|
| `lectura` | Al inicio de `main` | los dos archivos están en memoria como listas de líneas |
| `validacion` | — | existen las listas de pistas válidas, vuelos válidos y errores |
| `simulacion` | — | existe la lista completa de operaciones asignadas y la de vuelos no asignables |
| `reportes` | — | el texto de `reporte.txt`, `operaciones.csv` y `errores.csv` está armado en memoria |
| `escritura` | — | los 3 archivos están escritos y el reporte se mostró en pantalla |

**Regla de materialización:** cada etapa debe dejar su resultado **completamente calculado** antes de tomar
el tiempo. Las operaciones perezosas no pueden pasar trabajo a la etapa siguiente:
- Java: `.toList()`;
- Scala: `.toList` o `.toVector`;
- Clojure: `vec` o `doall`.

Sin esta regla, Clojure (perezoso por defecto) parecería más rápido en una etapa y más lento en la siguiente.

**Opción `--medir <archivo>`.** Escribe en ese archivo una línea de encabezado y una línea con las cinco
duraciones en nanosegundos:
```
lectura_ns,validacion_ns,simulacion_ns,reportes_ns,escritura_ns
12804511,40211876,95530112,30876220,18221034
```
Sin esta opción, el programa no escribe ninguna medición y su salida es la misma.

## 6. Protocolo de ejecución

1. **Construir** los tres `.jar` (Java con `javac` y `jar`, Scala con Scala CLI, Clojure con `lein uberjar`).
2. **Registrar el entorno** en `resultados/entorno.txt`: modelo del Mac, chip, memoria, versión de macOS,
   versión de Java, Scala y Clojure, opciones de la JVM y fecha.
3. **Verificar los datos:** regenerar los escenarios y comprobar las huellas SHA-256.
4. **Verificar la equivalencia:** ejecutar cada versión una vez por escenario y comparar sus 3 archivos con
   los esperados. Una versión que no coincide **no se mide** en ese escenario hasta corregirla, y cuenta como
   fallo en Confiabilidad.
5. **Medir**, para cada escenario (V1, V2, V3, V4, C1, X1):
   - **1 ronda de calentamiento** (se descarta) y **10 rondas medidas**;
   - en cada ronda se ejecutan los tres lenguajes, con el orden rotado: J→S→C, luego S→C→J, luego C→J→S…;
   - cada ejecución es **un proceso nuevo**:
     `java -Xmx4g -XX:+UseG1GC -jar <jar> <pistas> <vuelos> <salida> --medir <archivo>`;
   - la pantalla del programa se descarta (`/dev/null`) en los tres por igual;
   - se espera 1 segundo entre ejecuciones;
   - en cada ejecución se comprueba con SHA-256 que la salida sea correcta.
6. **Condiciones del equipo:**
   - el mismo Mac, conectado al cargador y sin modo de bajo consumo;
   - aplicaciones cerradas;
   - todo en una sola sesión sin interrupciones.
7. **Resultado por lenguaje y escenario:** la **mediana** de las 10 rondas. También se guardan el mínimo, el
   máximo y el rango intercuartílico, para mostrar qué tan estables fueron las mediciones.

**Por qué un proceso nuevo en cada ejecución:** así se usa un programa de consola. El tiempo que la JVM tarda
en optimizar el código (JIT) forma parte del comportamiento real de cada lenguaje, y se mide igual en los tres.

## 7. Registro de resultados

El orquestador `experimento/ejecutar.py` (Bloque 6) guarda una fila por ejecución en
`resultados/crudos/<escenario>.csv`:

```
lenguaje,escenario,ronda,orden,vuelos,t_lectura_ms,t_validacion_ms,t_simulacion_ms,t_reportes_ms,t_escritura_ms,t_operaciones_ms,t_proceso_ms,memoria_max_mb,codigo_salida,salida_correcta
```

Estos archivos son la **evidencia de rendimiento y consumo de recursos** (entregable 13). El Bloque 7 los
consolida y calcula la clasificación.

## 8. Limitaciones y cómo se controlan

| Riesgo | Cómo se controla |
|---|---|
| El Mac se calienta y baja su velocidad durante la prueba | Orden rotado, pausas, mediana de 10 rondas |
| Otros procesos del sistema interfieren | Aplicaciones cerradas, mediana y rango intercuartílico |
| La memoria de la JVM depende de su configuración | El mismo `-Xmx4g` y el mismo recolector de basura (G1) en los tres |
| Las operaciones perezosas trasladan trabajo entre etapas | Regla de materialización (sección 5) |
| La referencia podría tener un error | Coincide con el ejemplo resuelto a mano; ante cualquier diferencia, decide el contrato |
| Un solo equipo | Se declara en el informe; el entorno queda registrado en `resultados/entorno.txt` |
