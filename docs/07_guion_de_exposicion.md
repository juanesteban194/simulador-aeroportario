# Guion de exposición · Simulador aeroportuario en Java, Scala y Clojure

**Duración objetivo:** 18 minutos de exposición y 7 de preguntas.
**Reparto:** Juan Esteban Echavarría (introducción, diseño, Scala y conclusión) · Sebastián Villa (Java y
experimento) · Miguel Guarnizo (Clojure y resultados).

**Qué tener abierto antes de empezar**
1. El informe técnico (`Informe_tecnico.docx`) en el resumen ejecutivo (figura 1) y la sección 7.
2. IntelliJ con el repositorio y la configuración **Verificar equivalencia** lista.
3. Una terminal en la raíz del repositorio con los `.jar` ya construidos (para la demostración en vivo).
4. `resultados/clasificacion.md` y la carpeta `resultados/graficos/`.

**Plan B:** si falla la demostración en vivo, mostrar los archivos `resultados/verificacion.csv` (19 casos por
lenguaje, todos "ok") y `resultados/crudos/V4.csv` (una fila por ejecución).

---

## 1. Apertura · Juan Esteban · 1:30

**Mostrar:** portada del informe.

> "Nuestro final compara Java, Scala y Clojure resolviendo el mismo problema: un simulador de operaciones
> aeroportuarias. El objetivo no era solo programar tres veces lo mismo, sino montar un experimento que mida
> los tres lenguajes en igualdad de condiciones y que decida automáticamente cuál es mejor para este problema.
> Elegimos Clojure como tercer lenguaje porque es funcional de verdad y corre en la misma JVM que Java y Scala:
> así las diferencias que medimos son del lenguaje, no de la plataforma."

> "Les vamos a mostrar el problema, el diseño común, las tres implementaciones, el experimento y la
> clasificación final."

## 2. El problema y el diseño común · Juan Esteban · 3:00

**Mostrar:** diagrama `docs/diagramas/modelo_y_flujo.png`.

> "La torre de control recibe despegues y aterrizajes y asigna cada vuelo a una pista libre y compatible. Una
> pista es compatible si está operativa, permite la operación y es suficientemente larga para la categoría del
> avión. La prioridad es: emergencias primero, luego aterrizajes, luego la hora y luego el código. El extra del
> proyecto es que la asignación es automática y que un vuelo sin pista no bloquea a los demás."

> "Para que la comparación sea justa escribimos primero un contrato: el formato exacto de entrada y salida,
> los mensajes de error, cómo se redondean los decimales y cómo se ordenan los textos. Así, 'equivalente'
> significa 'archivos idénticos byte a byte', y eso se puede comprobar con una herramienta."

> "El algoritmo es el mismo en los tres: los vuelos se agrupan en 12 filas por operación, categoría y
> prioridad. Todos los vuelos de una fila sirven en las mismas pistas, así que basta mirar el primero de cada
> fila. El estado del aeropuerto es inmutable: cada paso recibe un aeropuerto y devuelve otro nuevo, y la
> simulación completa es una secuencia perezosa de estados: iterate, takeWhile y flatMap."

**Mostrar:** el bloque de código de `simular` en los tres lenguajes (documento de estudio, sección 4.3).

## 3. Java · Sebastián · 2:00

**Mostrar:** `java/src/simulador/TorreControl.java` (`mejorCandidato` y `simular`) y `Modelo.java` (records).

> "En Java las entidades son records, que son inmutables. Las listas son `List.of` o `toList()`, que no se
> pueden modificar. No hay ningún for ni while: todo es Stream. Los errores no son excepciones: cada registro
> termina en Ok o Falla, una interfaz sellada. La validación encadena `Optional.or`: devuelve el primer error."

> "Lo que más cuesta en Java es la ceremonia: tipos explícitos y lambdas para que una regla no se evalúe antes
> de tiempo. Por eso es la versión con más líneas, 600."

## 4. Scala · Juan Esteban · 2:00

**Mostrar:** `scala/src/simulador/Validacion.scala` y `TorreControl.scala`.

> "En Scala las entidades son case classes y para cambiar un dato se usa copy. Los errores son Either. Las
> colecciones son inmutables por defecto, y `orElse` recibe su argumento por nombre, así que no hacen falta
> lambdas para la evaluación perezosa. La recursión de un minuto usa @tailrec. Es la versión más corta: 352
> líneas, y la de mayor densidad de operaciones funcionales."

## 5. Clojure · Miguel · 2:00

**Mostrar:** `clojure/src/simulador/validacion.clj` y `torre_control.clj`.

> "En Clojure los datos son inmutables por defecto: records y vectores. No hay Optional: se usa nil, y el
> macro `or` devuelve el primer valor que no es nil, que aquí es el primer error. La simulación usa iterate y
> transductores. Lo compilamos por adelantado para que no compile al arrancar, y evitamos la reflexión con
> sugerencias de tipo: el compilador avisa si alguna llamada a Java sería lenta, y no hay ninguna."

## 6. El experimento · Sebastián · 3:00

**Mostrar:** tabla de escenarios del informe y, en vivo, la configuración **Verificar equivalencia** o:

```bash
bash experimento/verificar.sh
```

> "Diseñamos 6 escenarios: de mil a un millón de vuelos con la misma carga diaria, uno saturado y uno con un
> 10 % de registros dañados, más 12 casos de robustez. Los datos los produce un generador con semilla fija y
> cada archivo se comprueba con su huella SHA-256. Una implementación de referencia en Python produce las
> salidas esperadas; un lenguaje que no coincida no se mide."

> "Medimos tiempo con el reloj de la JVM dentro del programa, memoria con el sistema operativo y rendimiento
> con un reloj externo. Cada escenario tiene una ronda de calentamiento y 10 medidas, con el orden de los
> lenguajes rotado y un proceso nuevo en cada ejecución. Usamos la mediana."

**Demostración (si hay tiempo):**
```bash
java -jar java/simulador-java.jar datos/ejemplo/pistas.csv datos/ejemplo/vuelos.csv salida_java
java -jar clojure/simulador-clojure.jar datos/ejemplo/pistas.csv datos/ejemplo/vuelos.csv salida_clojure
cmp salida_java/reporte.txt salida_clojure/reporte.txt && echo "idénticos"
```

## 7. Resultados y clasificación · Miguel · 3:00

**Mostrar:** figura 1 (puntaje final) y figura 3 (puntaje por criterio) del informe.

> "Las tres versiones pasaron todo: 19 de 19 casos de verificación y 60 de 60 ejecuciones medidas correctas.
> Así que la diferencia no está en la correctitud sino en el rendimiento y en la forma del código."

**Mostrar:** figura 4 (tiempo por escenario).

> "Java es el más rápido en cinco de los seis escenarios. Con un millón de vuelos tarda 12 segundos en las
> operaciones; Scala 13 y Clojure casi 20. En el escenario más pequeño gana Clojure dentro del programa: con
> mil vuelos pesa más el costo de usar cada función por primera vez, y Clojure ya trae sus funciones
> compiladas. Pero paga 0,6 segundos de arranque antes de empezar, y eso se ve en el rendimiento."

**Mostrar:** figura 5 (etapas en V4).

> "Por etapas: Scala tiene la simulación más rápida y Java la validación y los reportes más rápidos. Clojure es
> el más lento en las tres por su tipado dinámico."

**Mostrar:** figura 6 (memoria) y figura 8 (calidad y uso funcional).

> "En memoria gana Scala con volúmenes medianos: unos 600 MB contra 740 de Java. En calidad, Java tiene la
> menor densidad de decisiones y Scala el código más corto, 352 líneas contra 600. En uso funcional gana Scala:
> los tres cumplen las cuatro reglas, pero Scala tiene la mayor densidad de operaciones funcionales."

**Mostrar:** tabla de clasificación y tabla de solidez.

> "Con los pesos del enunciado, el clasificador automático da: Java 93,35, Scala 91,45 y Clojure 75,65. Para
> comprobar que no dependía de los pesos, lo recalculamos con pesos iguales y quitando un criterio a la vez:
> Java gana en 6 de 7 variantes. Solo sin el criterio de rendimiento gana Scala. Clojure es tercero en todas."

## 8. Conclusión · Juan Esteban · 1:30

> "Para este proyecto elegimos Java. Es el más rápido y el de mayor rendimiento, es igual de confiable que los
> otros, y demuestra que Java moderno, con records, Streams, Optional e interfaces selladas, cumple todos los
> principios funcionales del curso."

> "Scala es una alternativa casi equivalente, a menos de dos puntos: escribe lo mismo con 41 % menos código, es
> el más funcional y usa menos memoria. Si el rendimiento pesara menos, ganaría Scala. Clojure es correcto y
> funcional, pero para procesar grandes volúmenes en un programa de consola le pesan su arranque y su tipado
> dinámico."

> "Las limitaciones: medimos en un solo entorno, un contenedor Linux con OpenJDK 21, con los mismos `.jar`
> construidos en el Mac, y para un solo problema. Todo es reproducible con una orden. Gracias; quedamos atentos
> a sus preguntas."

---

## Preguntas: quién responde

| Tema | Responde |
|---|---|
| Diseño, contrato, algoritmo, Scala | Juan Esteban |
| Java, protocolo de medición, instrumentos | Sebastián |
| Clojure, puntajes, clasificación, prueba de solidez | Miguel |

Las respuestas preparadas están en el documento de estudio, sección 12.
