"""
Secciones de resultados, discusión y conclusión del informe técnico. Las cifras se calculan con los datos del
experimento; el análisis corresponde a la medición registrada en resultados/entorno.txt.
"""
from contenido import CRITERIOS, ESCENARIOS, LENGUAJES, NOMBRE, PESOS, cod, h1, h2, img, nota, p, tabla, vin

PESOS_FRAC = {c: PESOS[c] / 100 for c in CRITERIOS}


def total(crit, l, pesos):
    return sum(pesos[c] * crit[l][c] for c in pesos)


def variantes():
    yield "Pesos del proyecto", PESOS_FRAC
    yield "Pesos iguales", {c: 1 / 6 for c in CRITERIOS}
    for quitado in CRITERIOS:
        resto = {c: w for c, w in PESOS_FRAC.items() if c != quitado}
        suma = sum(resto.values())
        yield f"Sin {quitado}", {c: w / suma for c, w in resto.items()}


def seccion(d, num, crit, final, orden, med, cal, fun):
    gan, seg, ter = orden
    bloques = []
    B = bloques.append

    def pct(a, b):
        return num(100 * (a / b - 1), 0)

    fuera = {(l, e): med[(l, e)]["t_proc"] - med[(l, e)]["t_op"] for l in LENGUAJES for e in ESCENARIOS}

    # ------------------------------------------------------------------ 7. resultados
    B(h1("7. Resultados"))
    B(h2("7.1 Clasificación automática"))
    B(img("02_puntaje_por_criterio.png", "Figura 3. Puntaje de cada criterio (0 a 100). Entre paréntesis, su peso."))
    B(p(f"**{NOMBRE[gan]} ocupa el primer lugar con {num(final[gan])} puntos**, {num(final[gan] - final[seg])} por "
        f"encima de {NOMBRE[seg]} ({num(final[seg])}). {NOMBRE[ter]} queda tercero con {num(final[ter])}. La ventaja de "
        f"{NOMBRE[gan]} viene de los criterios cuantitativos de mayor peso: es el mejor en Tiempo "
        f"({num(crit[gan]['Tiempo'])}) y en Rendimiento (100). {NOMBRE[seg]} es el mejor en Memoria "
        f"({num(crit[seg]['Memoria'])}) y en Uso funcional (100). Los tres empatan en Confiabilidad con 100."))

    # 7.2 tiempo
    B(h2("7.2 Tiempo de ejecución (25 %)"))
    B(img("03_tiempo_por_escenario.png",
          "Figura 4. Tiempo de las operaciones (validación + simulación + reportes) en cada escenario."))
    B(tabla(["Escenario"] + [NOMBRE[l] for l in LENGUAJES] + ["Más rápido"],
            [[e] + [num(med[(l, e)]["t_op"], 0) for l in LENGUAJES]
             + [NOMBRE[min(LENGUAJES, key=lambda l: med[(l, e)]["t_op"])]] for e in ESCENARIOS],
            anchos=[18, 20, 20, 20, 22], numerica=True,
            pie="Tabla 9. Mediana de `t_operaciones` en milisegundos (10 rondas)."))
    B(p(f"{NOMBRE['java']} es el más rápido en cinco de los seis escenarios. En el volumen más grande (V4, un millón "
        f"de vuelos) tarda {num(med[('java', 'V4')]['t_op'] / 1000, 1)} s; {NOMBRE['scala']} tarda "
        f"{num(med[('scala', 'V4')]['t_op'] / 1000, 1)} s ({pct(med[('scala', 'V4')]['t_op'], med[('java', 'V4')]['t_op'])} % "
        f"más) y {NOMBRE['clojure']} {num(med[('clojure', 'V4')]['t_op'] / 1000, 1)} s "
        f"({pct(med[('clojure', 'V4')]['t_op'], med[('java', 'V4')]['t_op'])} % más). Java y Scala están muy cerca en "
        f"todos los escenarios de 100.000 vuelos (V3, C1, X1), con diferencias de 1 a 6 %."))
    B(p(f"**Excepción en V1 (1.000 vuelos):** {NOMBRE['clojure']} tiene el menor `t_operaciones` "
        f"({num(med[('clojure', 'V1')]['t_op'], 0)} ms). Con tan pocos datos, el tiempo dentro del programa lo domina "
        f"el costo de usar por primera vez cada función. La explicación más probable: Java y Scala crean las clases "
        f"de sus lambdas la primera vez que se ejecutan, mientras que Clojure, compilado por adelantado, ya trae sus "
        f"funciones como clases normales y paga antes de `main` la carga de su núcleo. Ese costo no entra en `t_operaciones`; sí entra en el proceso completo "
        f"(sección 7.5)."))
    B(img("06_etapas_V4.png", "Figura 5. Tiempo de cada etapa dentro del programa en V4 (mediana de 10 rondas)."))
    et = {l: med[(l, "V4")]["etapas"] for l in LENGUAJES}
    B(p(f"El desglose por etapas en V4 muestra dónde está cada diferencia:"))
    B(vin(f"**Simulación:** Scala es el más rápido ({num(et['scala']['simulacion'] / 1000, 1)} s, frente a "
          f"{num(et['java']['simulacion'] / 1000, 1)} s de Java y {num(et['clojure']['simulacion'] / 1000, 1)} s de Clojure). "
          f"Probablemente porque actualizar un `Vector` inmutable de Scala (`updated`) es más barato que crear una "
          f"lista nueva con Streams en cada paso, como hace Java.",
          f"**Validación y reportes:** Java es el más rápido (validación {num(et['java']['validacion'] / 1000, 1)} s y "
          f"reportes {num(et['java']['reportes'] / 1000, 1)} s). Sus Streams y colectores (`groupingBy`, `joining`) "
          f"recorren y agrupan un millón de registros con muy poco costo adicional.",
          f"**Clojure** es el más lento en las tres etapas. Lo más probable es que pese su tipado dinámico: los números "
          f"van en objetos (`Long`), los campos se buscan por palabra clave y los mapas persistentes cuestan más de "
          f"crear que un `record` de Java o una `case class`."))

    # 7.3 memoria
    B(h2("7.3 Consumo de memoria (20 %)"))
    B(img("04_memoria_por_escenario.png", "Figura 6. Memoria residente máxima del proceso en cada escenario."))
    B(tabla(["Escenario"] + [NOMBRE[l] for l in LENGUAJES] + ["Menor"],
            [[e] + [num(med[(l, e)]["mem"], 0) for l in LENGUAJES]
             + [NOMBRE[min(LENGUAJES, key=lambda l: med[(l, e)]["mem"])]] for e in ESCENARIOS],
            anchos=[18, 20, 20, 20, 22], numerica=True, pie="Tabla 10. Mediana de la memoria máxima en MB."))
    B(p(f"Scala usa menos memoria en los escenarios de 10.000 y 100.000 vuelos (alrededor de "
        f"{num(med[('scala', 'V3')]['mem'], 0)} MB en V3, frente a {num(med[('java', 'V3')]['mem'], 0)} MB de Java). "
        f"Java usa menos en el más pequeño (V1, {num(med[('java', 'V1')]['mem'], 0)} MB, porque no carga la "
        f"biblioteca de Scala ni el núcleo de Clojure) y en el más grande (V4, {num(med[('java', 'V4')]['mem'], 0)} MB). "
        f"Clojure usa más memoria en la mayoría de escenarios."))
    B(nota("**Cómo leer la memoria.** Es la memoria física máxima del proceso de la JVM, no solo la de los datos "
           "vivos: incluye cuánto decide crecer el montículo el recolector G1 (con un límite de 4 GB). En V4 los tres "
           "llegan a 3–4 GB porque el recolector aprovecha el espacio disponible antes de limpiar. Los tres usan la "
           "misma JVM y las mismas opciones, así que la comparación es justa, pero las cifras dependen de esas "
           "opciones."))

    # 7.4 rendimiento
    B(h2("7.4 Rendimiento (20 %)"))
    B(img("05_rendimiento_por_escenario.png", "Figura 7. Vuelos procesados por segundo en el proceso completo."))
    B(tabla(["Escenario"] + [NOMBRE[l] for l in LENGUAJES],
            [[e] + [num(med[(l, e)]["rend"], 0) for l in LENGUAJES] for e in ESCENARIOS],
            anchos=[22, 26, 26, 26], numerica=True,
            pie="Tabla 11. Mediana de vuelos procesados por segundo (registros del archivo ÷ tiempo del proceso)."))
    B(p(f"Java tiene el mayor rendimiento en los seis escenarios. El rendimiento mide el **proceso completo**: "
        f"incluye arrancar la JVM, cargar el lenguaje, leer y escribir. El tiempo fuera de las operaciones en V1 "
        f"muestra el costo de arranque de cada lenguaje: Java {num(fuera[('java', 'V1')], 0)} ms, Scala "
        f"{num(fuera[('scala', 'V1')], 0)} ms y Clojure {num(fuera[('clojure', 'V1')], 0)} ms. Por eso Clojure, que "
        f"era el más rápido dentro del programa en V1, tiene allí el menor rendimiento. Con volúmenes grandes ese "
        f"costo fijo pesa menos, y el rendimiento lo decide la velocidad de las operaciones."))

    # 7.5 calidad y uso funcional
    B(h2("7.5 Calidad de código (15 %) y uso funcional (10 %)"))
    B(img("07_calidad_y_funcional.png", "Figura 8. Métricas calculadas sobre el código fuente de cada versión."))
    B(tabla(["Métrica", "Java", "Scala", "Clojure"], [
        ["Q1 · Líneas de código", *[cal[l]["q1_lineas"] for l in LENGUAJES]],
        ["Puntos de decisión", *[cal[l]["decisiones"] for l in LENGUAJES]],
        ["Q2 · Decisiones cada 100 líneas", *[num(float(cal[l]["q2_decisiones_100"])) for l in LENGUAJES]],
        ["Q3 · Líneas duplicadas (jscpd)", *[cal[l]["q3_duplicadas"] for l in LENGUAJES]],
        ["Reglas F1–F4 cumplidas", *[str(sum(int(fun[l][f"F{i}_violaciones"]) == 0 for i in range(1, 5))) + "/4"
                                     for l in LENGUAJES]],
        ["Operaciones funcionales", *[fun[l]["operaciones"] for l in LENGUAJES]],
        ["Operaciones funcionales cada 100 líneas", *[num(float(fun[l]["densidad_100"])) for l in LENGUAJES]],
        ["**Puntaje de Calidad**", *[f"**{num(crit[l]['Calidad'])}**" for l in LENGUAJES]],
        ["**Puntaje de Uso funcional**", *[f"**{num(crit[l]['Uso funcional'])}**" for l in LENGUAJES]],
    ], anchos=[40, 20, 20, 20], numerica=True, pie="Tabla 12. Calidad de código y uso funcional."))
    B(vin("**Scala** expresa el mismo programa en el menor número de líneas (352) y con la mayor densidad de "
          "operaciones funcionales. Por eso gana Uso funcional y queda casi empatado con Java en Calidad.",
          "**Java** necesita más líneas (600) por sus tipos explícitos, llaves y lambdas, pero tiene la menor densidad "
          "de decisiones: gran parte de la lógica son cadenas de operaciones sin ramas. Gana Calidad por poco.",
          "**Clojure** tiene la mayor densidad de decisiones: cada regla de validación usa `when` u `or` de forma "
          "explícita, donde Java y Scala usan una función auxiliar. Tampoco tiene operaciones de \"Opcionales\": "
          "trabaja con `nil` en lugar de tipos `Option`. Es una diferencia de estilo del lenguaje, no un defecto.",
          "Ninguna versión tiene código duplicado y las tres cumplen las cuatro reglas funcionales."))
    B(p("**Advertencias de compiladores y analizadores** (se informan; no puntúan):"))
    B(vin("`javac -Xlint:all`: 0 advertencias.",
          "Clojure con `*warn-on-reflection*`: 0 llamadas por reflexión.",
          "Las advertencias de Scala, `clj-kondo` y SonarQube no se registraron en esta medición. Se obtienen en el "
          "Mac con `scala-cli compile scala`, `clj-kondo --lint clojure/src` y el servidor local de SonarQube."))

    # 7.6 confiabilidad
    B(h2("7.6 Confiabilidad (10 %)"))
    casos = {l: {f["caso"]: f["resultado"] for f in d["verificacion"] if f["lenguaje"] == l} for l in LENGUAJES}
    correctitud = ["E0", "V1", "V2", "V3", "V4", "C1", "X1"]
    robustez = [f"R{n:02d}" for n in range(1, 13)]
    B(tabla(["Parte", "Java", "Scala", "Clojure"], [
        ["Correctitud (7 escenarios)", *[f"{sum(casos[l].get(c) == 'ok' for c in correctitud)}/7" for l in LENGUAJES]],
        ["Robustez (12 casos de error)", *[f"{sum(casos[l].get(c) == 'ok' for c in robustez)}/12" for l in LENGUAJES]],
        ["Estabilidad (60 ejecuciones medidas)", *[f"{sum(med[(l, e)]['n'] for e in ESCENARIOS)}/60" for l in LENGUAJES]],
        ["**Puntaje**", *[f"**{num(crit[l]['Confiabilidad'])}**" for l in LENGUAJES]],
    ], anchos=[40, 20, 20, 20], numerica=True, pie="Tabla 13. Confiabilidad de cada versión."))
    B(p("Las tres versiones son igual de confiables. Superan los 12 casos de error sin mostrar ninguna excepción: sin "
        "argumentos, archivo inexistente, archivos vacíos, líneas con espacios, finales de línea de Windows, campos de "
        "más o de menos, números y horas límite, tildes y bytes UTF-8 inválidos. Es el efecto de tratar los errores "
        "como valores y de revisar el archivo antes de leerlo."))

    # 7.7 solidez
    B(h2("7.7 Prueba de solidez"))
    filas, ganadores = [], []
    for nombre, pesos in variantes():
        o = sorted(LENGUAJES, key=lambda l: -total(crit, l, pesos))
        filas.append([nombre] + [NOMBRE[l] for l in o] + [num(total(crit, o[0], pesos) - total(crit, o[1], pesos))])
        if nombre != "Pesos del proyecto":
            ganadores.append(o[0])
    veces = sum(g == gan for g in ganadores)
    B(tabla(["Variante", "1.º", "2.º", "3.º", "Ventaja del 1.º"], filas, anchos=[30, 16, 16, 16, 22],
            resaltar=0, pie="Tabla 14. La clasificación con otros pesos."))
    cambia = [f[0] for f in filas[1:] if f[1] != NOMBRE[gan]]
    B(p(f"**{NOMBRE[gan]} gana en {veces} de las {len(ganadores)} variantes.**"
        + (f" Solo pierde el primer lugar frente a {NOMBRE[seg]} en la variante \"{', '.join(cambia)}\": sin ese "
           f"criterio, las ventajas de {NOMBRE[seg]} en memoria y uso funcional pesan más que la velocidad de "
           f"{NOMBRE[gan]}. El tercer lugar de {NOMBRE[ter]} no cambia en ninguna variante." if cambia else
           " El resultado no depende de los pesos elegidos.")))
    B(p(f"En consecuencia, el primer lugar de {NOMBRE[gan]} es claro pero estrecho: se apoya en su ventaja de "
        f"rendimiento, que es uno de los criterios de mayor peso del enunciado. El tercer lugar de {NOMBRE[ter]} es "
        f"sólido en todas las variantes."))

    # ------------------------------------------------------------------ 8. discusión
    B(h1("8. Ventajas y limitaciones de cada lenguaje"))
    B(tabla(["Lenguaje", "Ventajas observadas", "Limitaciones observadas"], [
        ["Java", "El más rápido en las operaciones y en el proceso completo; arranque más corto; menor densidad de "
                 "decisiones; records, Streams, `Optional` e interfaces selladas permiten un estilo funcional completo.",
         "El código más largo (600 líneas); la evaluación perezosa exige lambdas explícitas; no optimiza la recursión "
         "de cola; más memoria que Scala con volúmenes medianos."],
        ["Scala", "El código más corto y más funcional; la simulación más rápida; la menor memoria con 10.000 a "
                  "100.000 vuelos; colecciones inmutables por defecto, `Either`, `copy` y `@tailrec`.",
         "Arranque más lento que Java por la biblioteca de Scala (el `.jar` pesa 10 MB); validación y reportes más "
         "lentos que Java con un millón de vuelos."],
        ["Clojure", "Datos inmutables por defecto y código centrado en los datos; `or`, `when-let` y `nil` simplifican "
                    "la validación; transductores; igual de confiable que los otros dos.",
         "El más lento y el que más memoria usa en la mayoría de escenarios; el arranque del núcleo de Clojure cuesta "
         "unos 0,6 s; tipos dinámicos (números en objetos, búsqueda por palabra clave); más puntos de decisión."],
    ], anchos=[14, 43, 43], pie="Tabla 15. Ventajas y limitaciones identificadas con la evidencia del experimento."))
    B(p("**Por qué Clojure queda atrás en rendimiento.** Las optimizaciones habituales de Clojure para código intensivo "
        "son las colecciones transitorias (`transient`) y los números primitivos con sugerencias de tipo. Las "
        "transitorias son colecciones mutables y la regla F3 las prohíbe en los tres lenguajes. Se mantuvo el estilo "
        "funcional idiomático para que la comparación sea de lenguajes y no de micro-optimizaciones."))
    B(p("**Por qué Java y Scala están tan cerca.** Los dos son lenguajes con tipos estáticos que compilan a bytecode "
        "con estructuras de datos de tamaño fijo (`record` y `case class`). La JVM los optimiza de forma muy parecida. "
        "La diferencia está en las bibliotecas: los Streams y colectores de Java son más rápidos para recorrer y "
        "agrupar, y los vectores inmutables de Scala son más eficientes para actualizar el estado de la simulación."))

    # ------------------------------------------------------------------ 9. conclusión
    B(h1("9. Conclusión técnica"))
    B(p(f"**Para este proyecto, el lenguaje seleccionado es {NOMBRE[gan]}.** Con el mecanismo automático y los pesos "
        f"del enunciado obtiene {num(final[gan])} puntos y el primer lugar. Las razones, en orden de importancia:"))
    B({"tipo": "numerada", "items": [
        f"Es el más rápido en las operaciones en cinco de seis escenarios y procesa más vuelos por segundo en los "
        f"seis. Con un millón de vuelos procesa {num(med[('java', 'V4')]['rend'], 0)} vuelos/s, frente a "
        f"{num(med[('scala', 'V4')]['rend'], 0)} de Scala y {num(med[('clojure', 'V4')]['rend'], 0)} de Clojure.",
        "Es igual de confiable que los otros dos: salida idéntica en los 19 casos y en las 60 ejecuciones medidas.",
        "Demuestra que Java moderno permite cumplir los principios funcionales del curso sin ciclos, sin "
        "mutación y sin excepciones, gracias a records, Streams, `Optional` e interfaces selladas.",
    ], "ref": "numeros"})
    B(p(f"**{NOMBRE[seg]} es una alternativa casi equivalente** ({num(final[gan] - final[seg])} puntos de diferencia): "
        f"escribe el mismo programa con 41 % menos líneas, es el más funcional, usa menos memoria con volúmenes "
        f"medianos y tiene la simulación más rápida. Si el criterio de rendimiento pesara menos, o si la "
        f"mantenibilidad del código fuera la prioridad, Scala sería la mejor elección. La prueba de solidez lo "
        f"confirma: sin el criterio de Rendimiento, gana Scala."))
    B(p(f"**{NOMBRE[ter]} es correcto y funcional, pero el menos conveniente para este problema:** procesar grandes "
        f"volúmenes en un programa de consola que arranca en cada ejecución. Su arranque y sus tipos dinámicos le "
        f"cuestan entre 30 y 65 % más de tiempo con volúmenes grandes."))
    B(h2("9.1 Limitaciones del estudio"))
    B(vin("**Un solo entorno de medición:** un contenedor Linux de 2 núcleos con OpenJDK 21. Los valores absolutos "
          "cambian en otro equipo; la comparación es válida porque los tres se midieron en el mismo entorno, con el "
          "mismo protocolo y con los mismos `.jar`. Se puede repetir en el Mac con `python3 experimento/ejecutar.py`.",
          "**Un solo problema:** el resultado vale para un procesamiento por lotes de datos tabulares. En otro tipo "
          "de problema (por ejemplo, concurrencia o un servicio de larga duración con la JVM caliente) el orden "
          "podría cambiar.",
          "**Proceso nuevo por ejecución:** incluye el arranque de la JVM, como en el uso real de un programa de "
          "consola. Con un servicio que se mantiene en ejecución, la desventaja de arranque de Scala y Clojure "
          "desaparecería.",
          "**Memoria:** depende de cómo el recolector G1 dimensiona el montículo; con otras opciones de la JVM las "
          "cifras cambian.",
          "**Escenarios pequeños:** en V1 y V2 los rangos de mínimo a máximo de Java y Scala se cruzan. Las "
          "diferencias claras aparecen desde 100.000 vuelos.",
          "**Calidad:** líneas, decisiones y duplicación son indicadores objetivos pero parciales; no miden la "
          "legibilidad para una persona."))

    # ------------------------------------------------------------------ anexos
    B(h1("Anexo A. Entregables y dónde están"))
    B(tabla(["Entregable del enunciado", "Contenido", "Ubicación"], [
        ["11. Tres proyectos con su código fuente", "Java, Scala y Clojure, 7 módulos cada uno", "`java/`, `scala/`, `clojure/`"],
        ["12. Escenarios y datos", "Generador, huellas SHA-256, ejemplo a mano, escenarios y robustez", "`datos/`"],
        ["13. Evidencias de rendimiento y recursos", "198 ejecuciones (180 medidas), entorno y resumen", "`resultados/crudos/`, `entorno.txt`, `resumen.md`"],
        ["14. Consolidación y clasificación automática", "Verificador, orquestador, calidad, uso funcional, clasificador y gráficos", "`experimento/`, `resultados/`"],
        ["15. Informe técnico", "Este documento", "`Informe_tecnico.docx`"],
        ["16. Sustentación", "Guion y documento de estudio", "`Guion_de_exposicion.md`, `Documento_de_estudio.md`"],
    ], anchos=[32, 38, 30], pie="Tabla 16. Entregables del enunciado."))
    B(h1("Anexo B. Cómo reproducir los resultados"))
    B(cod("Terminal", """
bash experimento/verificar.sh          # equivalencia (19 casos)
python3 experimento/ejecutar.py        # medición (unos 20 min)
python3 experimento/calidad.py         # calidad de código
python3 experimento/funcional.py       # uso funcional
python3 experimento/clasificar.py      # puntajes y clasificación
python3 experimento/graficos.py        # gráficos
python3 informe/generar_informe.py     # este informe"""))
    B(h1("Anexo C. Mediciones completas"))
    filas = []
    for e in ESCENARIOS:
        for l in LENGUAJES:
            m = med[(l, e)]
            filas.append([e, NOMBRE[l], num(m["t_op"], 0), f"{num(m['t_op_min'], 0)} – {num(m['t_op_max'], 0)}",
                          num(m["t_proc"], 0), num(m["mem"], 0), num(m["rend"], 0), f"{m['n']}/10"])
    B(tabla(["Esc.", "Lenguaje", "t_oper. (ms)", "Mín – máx (ms)", "t_proceso (ms)", "Memoria (MB)", "Vuelos/s",
             "Correctas"], filas, anchos=[8, 12, 13, 18, 14, 13, 13, 11], numerica=True,
            pie="Tabla 17. Medianas de las 10 rondas por escenario y lenguaje. Datos crudos en `resultados/crudos/`."))
    return bloques
