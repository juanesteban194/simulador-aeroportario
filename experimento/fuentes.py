"""
=============================================================================
 Lectura del código fuente para calidad.py y funcional.py (docs/04_criterios.md, secciones 3 y 5).

 Antes de contar se eliminan los comentarios y el contenido de las cadenas de texto, para que una palabra como
 "if" dentro de un mensaje no cuente. Las comillas se conservan ("") para que una línea que solo tiene una
 cadena siga contando como línea de código.

 Precisión: en Scala, lo que va dentro de ${...} en una cadena interpolada es código (como la concatenación
 con + en Java o (str ...) en Clojure), así que se conserva.
=============================================================================
"""
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
EXTENSIONES = {"java": ".java", "scala": ".scala", "clojure": ".clj"}


def archivos(lenguaje):
    """Código de producción de una versión (todos sus módulos; sin pruebas ni archivos de construcción)."""
    return sorted((RAIZ / lenguaje / "src").rglob("*" + EXTENSIONES[lenguaje]))


def _cadena_c(texto, i, salida):
    """Copia una cadena "..." o \"\"\"...\"\"\" de Java/Scala sin su contenido. Devuelve la nueva posición."""
    if texto.startswith('"""', i):
        fin = texto.find('"""', i + 3)
        fin = len(texto) if fin < 0 else fin + 3
        salida.append('""' + "\n" * texto.count("\n", i, fin))   # conserva los saltos de línea
        return fin
    j = i + 1
    while j < len(texto) and texto[j] not in '"\n':
        j += 2 if texto[j] == "\\" else 1
    salida.append('""')
    return j + 1


def _interpolada(texto, i, salida):
    """Cadena interpolada de Scala (s"..." o f"..."): se quita el texto y se conservan los ${...}."""
    salida.append('"')
    j = i + 1
    while j < len(texto) and texto[j] not in '"\n':
        if texto[j] == "\\":
            j += 2
        elif texto.startswith("${", j):
            profundidad, k = 1, j + 2
            while k < len(texto) and profundidad:
                if texto[k] == '"':
                    k = _cadena_c(texto, k, [])            # cadena dentro del código interpolado
                    continue
                profundidad += {"{": 1, "}": -1}.get(texto[k], 0)
                k += 1
            salida.append(" " + limpiar_c(texto[j + 2:k - 1], "scala") + " ")
            j = k
        else:
            j += 1
    salida.append('"')
    return j + 1


def limpiar_c(texto, lenguaje):
    """Java y Scala: quita // ..., /* ... */ (anidados en Scala) y el contenido de las cadenas."""
    salida, i = [], 0
    while i < len(texto):
        c = texto[i]
        if texto.startswith("//", i):
            fin = texto.find("\n", i)
            i = len(texto) if fin < 0 else fin
        elif texto.startswith("/*", i):
            profundidad, j = 1, i + 2
            while j < len(texto) and profundidad:
                if texto.startswith("/*", j) and lenguaje == "scala":
                    profundidad, j = profundidad + 1, j + 2
                elif texto.startswith("*/", j):
                    profundidad, j = profundidad - 1, j + 2
                else:
                    j += 1
            salida.append("\n" * texto.count("\n", i, j))
            i = j
        elif c == '"':
            interpolada = lenguaje == "scala" and i > 0 and (texto[i - 1].isalnum() or texto[i - 1] == "_")
            i = _interpolada(texto, i, salida) if interpolada and not texto.startswith('"""', i) else \
                _cadena_c(texto, i, salida)
        elif c == "'" and i + 2 < len(texto) and (texto[i + 2] == "'" or texto[i + 1] == "\\"):
            fin = texto.find("'", i + 2 if texto[i + 1] == "\\" else i + 1)
            salida.append("' '")                                  # literal de carácter
            i = fin + 1
        else:
            salida.append(c)
            i += 1
    return "".join(salida)


def _forma(texto, i):
    """Fin de la forma de Clojure que empieza en i (para #_)."""
    while i < len(texto) and texto[i] in " \t\r\n,":
        i += 1
    if i < len(texto) and texto[i] in "([{":
        profundidad = 0
        while i < len(texto):
            c = texto[i]
            if c == '"':
                i = _fin_cadena_clj(texto, i)
                continue
            if c == ";":
                i = texto.find("\n", i) if texto.find("\n", i) >= 0 else len(texto)
                continue
            profundidad += {"(": 1, "[": 1, "{": 1, ")": -1, "]": -1, "}": -1}.get(c, 0)
            i += 1
            if profundidad == 0:
                return i
        return i
    while i < len(texto) and texto[i] not in " \t\r\n,()[]{}":
        i += 1
    return i


def _fin_cadena_clj(texto, i):
    j = i + 1
    while j < len(texto) and texto[j] != '"':
        j += 2 if texto[j] == "\\" else 1
    return j + 1


def limpiar_clojure(texto):
    """Clojure: quita ; ..., las formas descartadas con #_ y el contenido de las cadenas y expresiones regulares."""
    salida, i = [], 0
    while i < len(texto):
        c = texto[i]
        if c == ";":
            fin = texto.find("\n", i)
            i = len(texto) if fin < 0 else fin
        elif texto.startswith("#_", i):
            fin = _forma(texto, i + 2)
            salida.append("\n" * texto.count("\n", i, fin))
            i = fin
        elif c == '"':
            fin = _fin_cadena_clj(texto, i)
            salida.append('""' + "\n" * texto.count("\n", i, fin))
            i = fin
        elif c == "\\" and i + 1 < len(texto):                    # literal de carácter: \a, \", \newline
            j = i + 2
            while j < len(texto) and texto[j].isalpha() and texto[i + 1].isalpha():
                j += 1
            salida.append("\\c")
            i = j
        else:
            salida.append(c)
            i += 1
    return "".join(salida)


def limpio(ruta, lenguaje):
    texto = Path(ruta).read_text(encoding="utf-8")
    return limpiar_clojure(texto) if lenguaje == "clojure" else limpiar_c(texto, lenguaje)


def lineas_de_codigo(texto_limpio):
    """Q1: líneas que no quedan vacías después de quitar comentarios."""
    return [l for l in texto_limpio.splitlines() if l.strip()]
