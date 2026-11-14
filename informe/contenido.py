"""
Contenido del informe técnico. Las cifras se toman de los resultados (argumento d); los textos de análisis se
escriben a partir de ellas.
"""

LENGUAJES = ["java", "scala", "clojure"]
NOMBRE = {"java": "Java", "scala": "Scala", "clojure": "Clojure"}
ESCENARIOS = ["V1", "V2", "V3", "V4", "C1", "X1"]
CRITERIOS = ["Tiempo", "Memoria", "Rendimiento", "Calidad", "Confiabilidad", "Uso funcional"]
PESOS = {"Tiempo": 25, "Memoria": 20, "Rendimiento": 20, "Calidad": 15, "Confiabilidad": 10, "Uso funcional": 10}
G = "../resultados/graficos/"


def h1(t): return {"tipo": "h1", "texto": t}
def h2(t): return {"tipo": "h2", "texto": t}
def h3(t): return {"tipo": "h3", "texto": t}
def p(t): return {"tipo": "p", "texto": t}
def vin(*items): return {"tipo": "vinetas", "items": list(items)}
def nota(t): return {"tipo": "nota", "texto": t}
def img(archivo, pie, ancho=6.5): return {"tipo": "imagen", "ruta": G + archivo, "pie": pie, "ancho_pulgadas": ancho}
def cod(lenguaje, texto): return {"tipo": "codigo", "lenguaje": lenguaje, "texto": texto.strip("\n")}


def tabla(encabezado, filas, anchos=None, pie=None, numerica=False, resaltar=None):
    b = {"tipo": "tabla", "encabezado": encabezado, "filas": filas, "numerica": numerica}
    if anchos: b["anchos"] = anchos
    if pie: b["pie"] = pie
    if resaltar is not None: b["resaltar"] = resaltar
    return b


def informe(d, num):
    pun = d["puntajes"]
    orden = d["orden"]
    gan, seg, ter = orden
    final = {l: float(pun[l]["Final"]) for l in LENGUAJES}
    crit = {l: {c: float(pun[l][c]) for c in CRITERIOS} for l in LENGUAJES}
    med = d["medidas"]
    cal, fun = d["calidad"], d["funcional"]
    entorno = d["entorno"]
    linea_entorno = {l.split(":", 1)[0]: l.split(":", 1)[1].strip() for l in entorno.splitlines() if ":" in l}

    def mejor(c):
        return max(LENGUAJES, key=lambda l: crit[l][c])

    def razon(a, b, campo, e):
        return med[(a, e)][campo] / med[(b, e)][campo]

    bloques = []
    B = bloques.append

    # ------------------------------------------------------------------ portada
    B({"tipo": "portada", "institucion": "Universidad de Medellín · Facultad de Ingenierías",
       "curso": "Lenguajes y Paradigmas de Programación · Final: Comparativo de lenguajes",
       "titulo": "Simulador de operaciones aeroportuarias",
       "subtitulo": "Comparación experimental de Java, Scala y Clojure con programación funcional",
       "autores": ["Sebastián Villa", "Miguel Guarnizo", "Juan Esteban Echavarría"],
       "profesor": "Profesor: Juan Guillermo (JuanGui)", "fecha": "Medellín, noviembre de 2026",
       "repositorio": "github.com/juanesteban194/simulador-aeroportario-"})

    # ------------------------------------------------------------------ resumen
    B(h1("Resumen ejecutivo"))
    B(p(f"Se implementó el mismo simulador de operaciones aeroportuarias en **Java, Scala y Clojure**, con "
        f"programación funcional y un contrato común que obliga a las tres versiones a producir archivos "
        f"**idénticos byte a byte**. Sobre esa base se diseñó un experimento con 6 escenarios (de 1.000 a "
        f"1.000.000 de vuelos, uno saturado y uno con 10 % de errores), 10 rondas medidas por escenario y "
        f"lenguaje, y una clasificación automática con los seis criterios y pesos del enunciado."))
    B(p(f"**Resultado: {NOMBRE[gan]} es el lenguaje con mejor comportamiento para este problema**, con "
        f"{num(final[gan])} puntos sobre 100, seguido de {NOMBRE[seg]} ({num(final[seg])}) y {NOMBRE[ter]} "
        f"({num(final[ter])})."))
    B(tabla(["Pos.", "Lenguaje"] + [f"{c} ({PESOS[c]} %)" for c in CRITERIOS] + ["Final"],
            [[f"{i}.º", NOMBRE[l]] + [num(crit[l][c]) for c in CRITERIOS] + [f"**{num(final[l])}**"]
             for i, l in enumerate(orden, start=1)],
            anchos=[7, 10, 10, 10, 13, 9, 14, 11, 9], numerica=True, resaltar=0,
            pie="Tabla 1. Clasificación automática (puntaje de 0 a 100 por criterio; el final es la suma ponderada)."))
    B(p("**Las tres versiones son correctas y cumplen las reglas funcionales:**"))
    casos_ok = {l: sum(1 for f in d["verificacion"] if f["lenguaje"] == l and f["resultado"] == "ok") for l in LENGUAJES}
    total_casos = len({f["caso"] for f in d["verificacion"]})
    correctas = {l: sum(med[(l, e)]["n"] for e in ESCENARIOS) for l in LENGUAJES}
    reglas = {l: sum(int(fun[l][f"F{i}_violaciones"]) == 0 for i in range(1, 5)) for l in LENGUAJES}
    B(vin("Casos de verificación superados (ejemplo resuelto a mano, 6 escenarios y 12 casos de robustez): "
          + ", ".join(f"{NOMBRE[l]} {casos_ok[l]}/{total_casos}" for l in LENGUAJES) + ".",
          "Ejecuciones medidas con salida correcta: "
          + ", ".join(f"{NOMBRE[l]} {correctas[l]}/60" for l in LENGUAJES) + ".",
          "Reglas funcionales cumplidas (sin ciclos, sin reasignación, sin colecciones mutables, sin excepciones): "
          + ", ".join(f"{NOMBRE[l]} {reglas[l]}/4" for l in LENGUAJES) + "."))
    B(p("Las diferencias están en el rendimiento y en la forma del código."))
    B(img("01_puntaje_final.png", "Figura 1. Puntaje final ponderado de cada lenguaje.", 5.4))
    B({"tipo": "salto"})

    # ------------------------------------------------------------------ 1. introducción
    B(h1("1. Introducción y objetivo"))
    B(p("El enunciado pide implementar el proyecto de clase en Java, Scala y un tercer lenguaje, con base en la "
        "programación funcional, y **demostrar con evidencia cuantitativa** cuál alternativa es más conveniente. "
        "El énfasis no está en tener tres programas, sino en un **proceso experimental** que mida, compare y "
        "clasifique automáticamente."))
    B(p("**Tercer lenguaje: Clojure.** Es un lenguaje funcional (datos inmutables por defecto, funciones como "
        "valores) y se ejecuta en la **misma máquina virtual de Java (JVM)** que Java y Scala. Así los tres "
        "programas corren con `java -jar` sobre el mismo JDK 21 y con las mismas opciones, y las diferencias "
        "medidas se deben al lenguaje y a su compilador, no a la plataforma."))
    B(p("**Método de trabajo.** El trabajo se organizó en 9 bloques (marco, requerimientos, modelo y contrato, "
        "experimento, criterios, implementación, medición, clasificación e informe). Primero se documentó qué se "
        "iba a construir y cómo se iba a medir, y solo después se programó. Cada decisión quedó registrada con sus "
        "opciones y su razón en `docs/decisiones.md`."))
    B(tabla(["Condición del enunciado", "Cómo se cumple"], [
        ["1. Java, Scala y un tercer lenguaje", "Tres proyectos: `java/`, `scala/`, `clojure/`"],
        ["2. Mismos requisitos y resultados", "Contrato común y verificación byte a byte: 19 de 19 casos en los tres"],
        ["3. Operaciones funcionales", "map, filter, groupBy, reduce, sortBy, iterate, Optional/Either; reglas F1 a F4 verificadas"],
        ["4. Escenarios de prueba", "6 escenarios de carga y volumen + 12 casos de robustez"],
        ["5. Medir y registrar", "Opción `--medir` en los tres programas y orquestador `ejecutar.py`"],
        ["6. Condiciones equivalentes", "Misma JVM y opciones, mismos datos, orden rotado, 10 rondas, mediana"],
        ["7. Consolidar resultados", "`resultados/crudos/`, `consolidado.csv`, `puntajes.csv`"],
        ["8. Mecanismo automático", "`experimento/clasificar.py`"],
        ["9. Clasificación justificada", "`resultados/clasificacion.md` y sección 7 de este informe"],
        ["10. Conclusión técnica", "Secciones 8 y 9"],
    ], anchos=[38, 62], pie="Tabla 2. Condiciones del enunciado y dónde se cumplen."))

    # ------------------------------------------------------------------ 2. problema
    B(h1("2. El problema: simulador de operaciones aeroportuarias"))
    B(p("Un aeropuerto tiene varias pistas. La torre de control recibe la programación de despegues y "
        "aterrizajes de uno o varios días y debe asignar cada vuelo a una pista **compatible y libre**, según su "
        "prioridad, calcular los retrasos y producir reportes. El extra del proyecto es la **asignación automática "
        "de pistas por prioridad y disponibilidad**."))
    B(h2("2.1 Entidades"))
    B(tabla(["Entidad", "Qué representa", "Datos"], [
        ["Avión", "La aeronave", "Matrícula y categoría (Ligero, Mediano o Pesado)"],
        ["Vuelo", "Una operación programada", "Código, aerolínea, avión, operación, día y hora, prioridad"],
        ["Pista", "Una pista del aeropuerto", "Identificador, longitud, uso permitido y estado"],
        ["Aeropuerto", "El estado de la simulación en un minuto", "Minuto, primer vuelo pendiente de cada fila, minuto en que se libera cada pista, operaciones del paso"],
        ["TorreControl", "Las reglas de operación", "Funciones puras: reciben un Aeropuerto y devuelven otro nuevo"],
    ], anchos=[16, 30, 54], pie="Tabla 3. Entidades del proyecto. Todas son datos inmutables."))
    B(h2("2.2 Reglas de negocio principales"))
    B(vin("**Categorías (RN02):** Ligero necesita una pista de 1.200 m y la ocupa 2 minutos; Mediano, 2.000 m y 3 min; Pesado, 2.800 m y 4 min.",
          "**Compatibilidad (RN03):** la pista está Operativa, su uso es Mixta o igual a la operación, y es suficientemente larga.",
          "**Prioridad (RN05):** Emergencia antes que Normal; Aterrizaje antes que Despegue; hora más temprana; código menor.",
          "**Asignación automática (RN06):** cada vuelo recibe la pista libre y compatible de menor identificador. Un vuelo sin pista libre **no bloquea** a los demás.",
          "**Retraso (RN08):** inicio real menos hora programada; un vuelo está retrasado si supera 15 minutos.",
          "**Vuelo no asignable (RN09):** si ninguna pista del aeropuerto le sirve, se reporta con su motivo.",
          "**Determinismo (RN10):** sin azar ni reloj: las mismas entradas producen siempre la misma salida."))
    B(p("**Salidas:** el programa final de operaciones (`operaciones.csv`), los registros inválidos con su motivo "
        "(`errores.csv`) y los reportes RF08 a RF14 (`reporte.txt`): retrasos, los 5 vuelos más retrasados, uso de "
        "cada pista, retraso por aerolínea, vuelos no asignables, operaciones por tipo y categoría y un resumen ejecutivo."))

    # ------------------------------------------------------------------ 3. diseño
    B(h1("3. Diseño de la solución"))
    B(h2("3.1 Un contrato común, verificable byte a byte"))
    B(p("Para afirmar que tres programas son equivalentes hay que fijar todo lo que podría salir distinto. El "
        "contrato (`docs/02_modelo_y_contrato.md`) define:"))
    B(vin("**Lectura:** UTF-8 (un byte inválido se reemplaza por U+FFFD sin error), encabezado en la línea 1, líneas vacías ignoradas, campos vacíos conservados y `trim` con la definición de la JVM.",
          "**Validación:** reglas en el orden de las columnas, un solo error por registro y mensajes exactos.",
          "**Números:** decimales calculados con aritmética entera exacta, `c = (200·a + b) div (2·b)`, en lugar de números de punto flotante. Así ningún lenguaje depende de su formateador ni de la configuración regional.",
          "**Orden de textos** con la comparación de la JVM, igual en los tres.",
          "**Errores de uso:** una línea `ERROR:`, el modo de uso y el código de salida 2, sin escribir archivos."))
    B(img("../../docs/diagramas/modelo_y_flujo.png", "Figura 2. Modelo de datos y flujo de las cinco etapas del programa.", 6.3))
    B(h2("3.2 Siete módulos iguales"))
    B(tabla(["#", "Módulo", "Responsabilidad"], [
        ["1", "Modelo", "Entidades y listas cerradas"], ["2", "Lectura", "Archivo → líneas → registros"],
        ["3", "Validación", "Cada registro → dato válido o error (RF03)"],
        ["4", "TorreControl", "Compatibilidad, no asignables y simulación (RF04 a RF06)"],
        ["5", "Reportes", "Texto de los tres archivos de salida (RF07 a RF14)"],
        ["6", "Medición", "Tiempo de cada etapa y opción `--medir`"], ["7", "Main", "Argumentos y encadenamiento de las etapas"],
    ], anchos=[6, 20, 74], pie="Tabla 4. Módulos, con los mismos nombres de funciones en los tres lenguajes."))
    B(h2("3.3 El algoritmo de la torre de control"))
    B(p("Los vuelos asignables se agrupan en **12 filas** por (operación, categoría, prioridad) y cada fila se "
        "ordena por hora y código. Todos los vuelos de una fila son compatibles con las mismas pistas: si el "
        "primero no tiene pista libre, ninguno de su fila la tiene. Por eso basta mirar el primer vuelo de cada "
        "fila, y el resultado es el mismo que recorrer toda la cola."))
    B(p("El estado (Aeropuerto) es **inmutable**. Un **paso** asigna en el minuto actual mientras haya un candidato "
        "con pista libre (el de mayor prioridad recibe la pista compatible de menor identificador) y luego salta "
        "al **siguiente evento**: el menor minuto futuro en que se libera una pista o llega un vuelo. La simulación "
        "completa es una secuencia perezosa de estados, igual en los tres lenguajes:"))
    B(cod("Java", """
return Stream.iterate(inicial, a -> !terminado(a, filas), a -> paso(a, filas, operativas))
        .flatMap(a -> a.asignadasEnElPaso().stream())
        .toList();"""))
    B(cod("Scala", """
Iterator.iterate(inicial)(a => paso(a, todas, operativas))
  .takeWhile(a => !terminado(a, todas))
  .flatMap(_.asignadasEnElPaso)
  .toVector"""))
    B(cod("Clojure", """
(into [] (comp (take-while #(not (terminado? % filas)))
               (mapcat :asignadas-en-el-paso))
      (iterate #(paso % filas operativas) inicial))"""))
    B(p("**Costo:** se ordena una vez (n·log n) y cada evento cuesta un trabajo constante (12 filas y 5 pistas), con "
        "como máximo dos eventos por vuelo. La validación de códigos repetidos tampoco usa estado: el dueño de cada "
        "código es el primer registro sin otros errores (agrupar y tomar la línea mínima)."))

    # ------------------------------------------------------------------ 4. implementación funcional
    B(h1("4. Implementación funcional en los tres lenguajes"))
    B(p("Las tres versiones cumplen cuatro reglas que se verifican automáticamente sobre el código fuente "
        "(`experimento/funcional.py`): **F1** sin ciclos, **F2** sin reasignación, **F3** sin colecciones "
        "mutables y **F4** sin excepciones. Los errores se manejan como valores."))
    B(tabla(["Concepto", "Java", "Scala", "Clojure"], [
        ["Entidad inmutable", "`record`", "`case class`", "`defrecord`"],
        ["Lista cerrada", "`enum`", "`enum`", "palabra clave `:Ligero`"],
        ["Valor que puede faltar", "`Optional<T>`", "`Option[T]`", "`nil`"],
        ["Resultado o error", "interfaz sellada `Ok`/`Falla`", "`Either`", "`{:ok v}` / `{:falla e}`"],
        ["\"Cambiar\" un dato", "`new Aeropuerto(...)`", "`a.copy(...)`", "`(assoc a ...)`"],
        ["Secuencia perezosa", "`Stream`", "`Iterator`", "secuencias y transductores"],
        ["Primer error de varias reglas", "`Optional.or(...)`", "`Option.orElse(...)`", "`(or ...)`"],
        ["Recursión de cola", "no la optimiza (profundidad ≤ 5)", "`@tailrec`", "`recur`"],
    ], anchos=[24, 26, 24, 26], pie="Tabla 5. Cómo se expresa cada idea funcional en cada lenguaje."))
    B(p("**Ejemplo: validar una pista.** Las tres versiones devuelven el primer error de una lista de reglas. "
        "Java necesita lambdas para que una regla no se evalúe antes de tiempo; Scala lo consigue con parámetros "
        "por nombre y Clojure con el macro `or`, que ya es perezoso."))
    B(cod("Java", """
return entero(c.get(1), "longitud")
        .or(() -> si(Integer.parseInt(c.get(1)) <= 0, "longitud debe ser mayor que 0: " + c.get(1)))
        .or(() -> opcion(c.get(2), "uso", Modelo.nombres(Uso.values())))
        .or(() -> opcion(c.get(3), "estado", Modelo.nombres(Estado.values())));"""))
    B(cod("Scala", """
entero(c(1), "longitud")
  .orElse(si(c(1).toInt <= 0, s"longitud debe ser mayor que 0: ${c(1)}"))
  .orElse(opcion(c(2), "uso", Modelo.nombres(Uso.values)))
  .orElse(opcion(c(3), "estado", Modelo.nombres(Estado.values)))"""))
    B(cod("Clojure", """
(or (entero longitud "longitud")
    (when (<= (parse-long longitud) 0) (str "longitud debe ser mayor que 0: " longitud))
    (opcion uso "uso" m/nombres-uso)
    (opcion estado "estado" m/nombres-estado))"""))
    B(p("**Construcción y ejecución.** Java se compila con `javac` y `jar`; Scala con Scala CLI (Scala 3.9.0, el "
        "`.jar` incluye la biblioteca de Scala); Clojure con Leiningen (Clojure 1.12.0) y compilación por "
        "adelantado (AOT), sin llamadas por reflexión. Los tres se ejecutan con "
        "`java -Xmx4g -XX:+UseG1GC -jar simulador-<lenguaje>.jar`."))

    # ------------------------------------------------------------------ 5. experimento
    B(h1("5. Diseño del experimento"))
    B(h2("5.1 Escenarios y datos"))
    B(tabla(["Escenario", "Vuelos", "Qué evalúa"], [
        ["E0", "13", "Correctitud: ejemplo resuelto a mano"],
        ["V1", "1.000", "Volumen pequeño (1.500 vuelos por día)"], ["V2", "10.000", "Volumen mediano"],
        ["V3", "100.000", "Volumen grande"], ["V4", "1.000.000", "Volumen muy grande (668 días simulados)"],
        ["C1", "100.000", "Congestión: 2.400 vuelos por día, aeropuerto saturado"],
        ["X1", "100.000", "Errores: 10 % de registros inválidos"],
        ["R01 a R12", "casos pequeños", "Robustez: sin argumentos, archivos vacíos o inexistentes, `\\r\\n`, tildes, bytes inválidos, límites"],
    ], anchos=[14, 16, 70], pie="Tabla 6. Escenarios del experimento."))
    B(p("Los datos los produce un **generador determinista** con semilla fija; antes de medir se comprueba la huella "
        "SHA-256 de cada archivo. Una **implementación de referencia** en Python (que no compite) produce las salidas "
        "esperadas: un lenguaje cuya salida no coincida no se mide en ese escenario."))
    B(h2("5.2 Métricas e instrumentos"))
    B(tabla(["Criterio", "Métrica", "Instrumento"], [
        ["Tiempo (25 %)", "`t_operaciones`: validación + simulación + reportes, en ms", "`System.nanoTime()` dentro de cada programa"],
        ["Memoria (20 %)", "Memoria residente máxima del proceso, en MB", "`ru_maxrss` del sistema operativo (`wait4`)"],
        ["Rendimiento (20 %)", "Vuelos procesados por segundo en el proceso completo", "Reloj del orquestador alrededor del proceso"],
        ["Calidad (15 %)", "Líneas de código, decisiones cada 100 líneas, líneas duplicadas", "`calidad.py` y `jscpd`"],
        ["Confiabilidad (10 %)", "Correctitud, robustez y estabilidad", "`verificar.sh` y las 60 ejecuciones medidas"],
        ["Uso funcional (10 %)", "Reglas F1 a F4 y densidad de operaciones funcionales", "`funcional.py`"],
    ], anchos=[20, 44, 36], pie="Tabla 7. Métricas e instrumentos (los mismos para los tres lenguajes)."))
    B(p("**Regla de materialización:** cada etapa deja su resultado completamente calculado antes de tomar el "
        "tiempo (`toList`, `toVector`, `vec`). Sin ella, un lenguaje perezoso como Clojure trasladaría trabajo de "
        "una etapa a la siguiente."))
    B(h2("5.3 Protocolo"))
    B(vin("1 ronda de calentamiento (no cuenta) y **10 rondas medidas** por escenario.",
          "En cada ronda se ejecutan los tres lenguajes con el **orden rotado** (J-S-C, S-C-J, C-J-S…).",
          "**Un proceso nuevo por ejecución:** el arranque de la JVM y la compilación JIT forman parte del costo real de un programa de consola y se miden igual en los tres.",
          "1 segundo de pausa entre ejecuciones; la salida de cada ejecución se comprueba con SHA-256.",
          "Resultado por lenguaje y escenario: la **mediana** de las 10 rondas (también se guardan mínimo, máximo y rango intercuartílico)."))
    B(h2("5.4 Entorno de la medición"))
    B(tabla(["Elemento", "Valor"], [
        ["Sistema", linea_entorno.get("Sistema", "")], ["Procesador", linea_entorno.get("Procesador", "")],
        ["Núcleos", linea_entorno.get("Núcleos", "")],
        ["Java", linea_entorno.get("Java", "").split(" | ")[0]],
        ["Opciones de la JVM", linea_entorno.get("Opciones de la JVM", "")],
        ["Fecha", linea_entorno.get("Fecha", "")],
    ], anchos=[25, 75], pie="Tabla 8. Entorno registrado en `resultados/entorno.txt`."))
    B(nota("**Dónde se midió y por qué.** Los tres `.jar` se construyeron en el MacBook Pro del equipo con las "
           "herramientas oficiales de cada lenguaje (los mismos archivos, verificados con su huella SHA-256). La "
           "medición se ejecutó en un contenedor Linux de 2 núcleos con OpenJDK 21, porque no se pudo lanzar en el "
           "Mac de forma desatendida. Los tres lenguajes se midieron en el mismo entorno, con las mismas opciones "
           "y el mismo protocolo, así que la comparación es válida. Los valores absolutos (milisegundos y MB) "
           "serían menores en el Mac, que es más rápido; el orquestador permite repetir la medición allí con una "
           "sola orden (`python3 experimento/ejecutar.py`)."))

    # ------------------------------------------------------------------ 6. criterios
    B(h1("6. Criterios y clasificación automática"))
    B(p("Cada criterio termina en un puntaje de 0 a 100 por lenguaje. En las métricas sin máximo natural el "
        "puntaje es **proporcional al mejor**: el mejor obtiene 100 y los demás `100 · mejor / valor` (o "
        "`valor / mejor` cuando más es mejor). No se escala entre el peor y el mejor porque esa fórmula le daría 0 "
        "al último aunque estuviera a un 1 % del primero."))
    B(vin("**Tiempo, Memoria y Rendimiento:** puntaje proporcional en cada escenario y promedio de los 6.",
          "**Calidad:** un tercio para cada métrica: líneas de código (Q1), decisiones cada 100 líneas (Q2) y líneas duplicadas (Q3). SonarQube no se usa en el puntaje porque no analiza Clojure.",
          "**Confiabilidad:** promedio de correctitud (7 escenarios), robustez (12 casos) y estabilidad (60 ejecuciones).",
          "**Uso funcional:** reglas F1 a F4 (12,5 puntos cada una, hasta 50) más la densidad de operaciones funcionales cada 100 líneas, proporcional al mejor (hasta 50)."))
    B(p("`Final = 0,25·Tiempo + 0,20·Memoria + 0,20·Rendimiento + 0,15·Calidad + 0,10·Confiabilidad + 0,10·Uso funcional`. "
        "Si hay empate decide el Tiempo y luego la Memoria. La **prueba de solidez** recalcula la clasificación con "
        "pesos iguales y quitando un criterio a la vez."))

    # ------------------------------------------------------------------ 7. resultados (lo arma resultados.py)
    import resultados
    bloques += resultados.seccion(d, num, crit, final, orden, med, cal, fun)
    return {"titulo": "Informe técnico · Simulador de operaciones aeroportuarias",
            "autor": "Sebastián Villa, Miguel Guarnizo y Juan Esteban Echavarría",
            "descripcion": "Comparación experimental de Java, Scala y Clojure",
            "encabezado": "Comparativo de lenguajes · Simulador de operaciones aeroportuarias",
            "pie": "Universidad de Medellín · Lenguajes y Paradigmas · 2026-2",
            "bloques": bloques}
