#!/usr/bin/env python3
"""
=============================================================================
 Uso funcional (docs/04_criterios.md, sección 5).

   Mitad A · Restricciones F1 a F4 (absoluto): 12,5 puntos por regla; una sola violación anula la regla.
   Mitad B · Densidad funcional: operaciones funcionales cada 100 líneas de código (se puntúa en clasificar.py,
             proporcional al mejor).

 Comentarios y contenido de las cadenas se excluyen (fuentes.py). Cada operación se reconoce por su nombre
 completo: .take no cuenta dentro de .takeWhile.

 Precisiones de las listas del Bloque 4 (para que la misma operación cuente igual en los tres lenguajes):
 - Una variante que solo cambia el tipo del resultado cuenta como la operación base.
   Clojure: mapv -> map, filterv -> filter. Scala: maxOption, minOption, maxByOption, minByOption -> max, min,
   maxBy, minBy.
 - Un nombre usado para otra cosa no cuenta:
   - (count v) de Clojure sobre una colección es su tamaño, como .size() en Java y Scala, que no cuentan.
     Solo cuenta (count (filter ...)) y similares, equivalentes a .filter(...).count() en Java.
   - mapa.getOrElse(clave, valor) de Scala es una búsqueda en un mapa, como getOrDefault en Java o
     (get m k v) en Clojure, que no cuentan. Solo cuenta opcion.getOrElse(valor), con un argumento.
 - Optional.or(...) de Java es la misma operación que Option.orElse(...) de Scala (Java llama orElse a lo que
   Scala llama getOrElse), así que .or( cuenta en Java como Opcionales.

 Uso: python3 experimento/funcional.py    ->  resultados/funcional.csv y el detalle en pantalla
=============================================================================
"""
import csv
import re

from fuentes import RAIZ, archivos, limpio, lineas_de_codigo

LENGUAJES = ["java", "scala", "clojure"]

# ---------------------------------------------------------------- Mitad A: violaciones (patrones)

SIMBOLO_CLJ = r"(?<![\w\-!?*<>=/.:]){}(?![\w\-!?*<>=/])"


def simbolos(*nombres):
    return [SIMBOLO_CLJ.format(re.escape(n)) for n in nombres]


VIOLACIONES = {
    "java": {
        "F1": [r"\bfor\b", r"\bwhile\b", r"\bdo\b"],
        "F2": [r"\+\+", r"--", r"\+=", r"-=", r"\*=", r"/=", r"%=", r"(?m)^\s*[A-Za-z_]\w*\s*=(?!=)"],
        "F3": [r"new\s+(ArrayList|LinkedList|HashMap|TreeMap|HashSet|ArrayDeque|PriorityQueue)\b",
               r"\bStringBuilder\b", r"\.(add|put|remove|set|clear|append)\(", r"\w+\s*\[[^\]]+\]\s*=(?!=)"],
        "F4": [r"\btry\b", r"\bcatch\b", r"\bthrow\b"],
    },
    "scala": {
        "F1": [r"\bfor\b", r"\bwhile\b", r"\bdo\b"],
        "F2": [r"\bvar\b"],
        "F3": [r"scala\.collection\.mutable", r"\bArrayBuffer\b", r"\bListBuffer\b", r"\bStringBuilder\b",
               r"\bArray\(", r"\.update\("],
        "F4": [r"\btry\b", r"\bcatch\b", r"\bthrow\b", r"\bTry\("],
    },
    "clojure": {
        "F1": [r"\((loop|doseq|dotimes|while|for)(?=[\s)])"],
        "F2": simbolos("atom", "swap!", "reset!", "set!", "ref", "alter", "volatile!", "vswap!"),
        "F3": simbolos("transient", "conj!", "assoc!", "aset") + [r"java\.util\.(ArrayList|HashMap)",
                                                                  r"\bStringBuilder\b"],
        "F4": simbolos("try", "catch", "throw", "ex-info"),
    },
}

# ---------------------------------------------------------------- Mitad B: operaciones funcionales

OPERACIONES_JAVA = {
    "Transformar": [".map(", ".flatMap(", ".mapToInt(", ".mapToLong(", ".mapToDouble(", ".mapToObj("],
    "Filtrar": [".filter("],
    "Reducir": [".reduce(", ".collect(", ".sum(", ".count(", ".max(", ".min("],
    "Agrupar": ["groupingBy(", "partitioningBy("],
    "Ordenar": [".sorted(", "Comparator.comparing"],
    "Buscar": [".findFirst(", ".anyMatch(", ".allMatch(", ".noneMatch("],
    "Secuencias": ["Stream.iterate(", ".takeWhile(", ".limit(", ".skip("],
    "Composición": [".andThen(", ".compose("],
    "Opcionales": [".orElse(", ".orElseGet(", ".or("],
}
OPERACIONES_SCALA = {
    "Transformar": ["map", "flatMap", "collect"],
    "Filtrar": ["filter", "filterNot", "partition"],
    "Reducir": ["foldLeft", "fold", "reduce", "reduceOption", "sum", "count", "max", "min", "maxBy", "minBy",
                "maxOption", "minOption", "maxByOption", "minByOption"],
    "Agrupar": ["groupBy", "groupMapReduce"],
    "Ordenar": ["sortBy", "sortWith", "sorted"],
    "Buscar": ["find", "exists", "forall"],
    "Secuencias": ["Iterator.iterate", "takeWhile", "take", "drop", "zip"],
    "Composición": ["andThen", "compose"],
    "Opcionales": ["getOrElse", "orElse"],
}
OPERACIONES_CLOJURE = {
    "Transformar": ["map", "mapv", "mapcat", "keep", "map-indexed"],
    "Filtrar": ["filter", "filterv", "remove"],
    "Reducir": ["reduce", "frequencies", "count", "max-key", "min-key", "apply"],
    "Agrupar": ["group-by", "partition-by"],
    "Ordenar": ["sort", "sort-by"],
    "Buscar": ["some", "every?", "not-any?"],
    "Secuencias": ["iterate", "take-while", "take", "drop", "interleave"],
    "Composición": ["comp", "partial", "juxt"],
    "Opcionales": ["some->", "fnil"],
}


def patron_operacion(lenguaje, nombre):
    if lenguaje == "java":
        return re.escape(nombre) + (r"\w*" if nombre == "Comparator.comparing" else "")
    if lenguaje == "scala":
        if nombre in ("Iterator.iterate", "andThen", "compose"):
            return r"\b" + re.escape(nombre) + r"\b"
        return r"\." + re.escape(nombre) + r"\b"
    # Clojure: el símbolo en posición de llamada, (map ...) o #(map ...), o pasado como función (comp, apply...)
    return SIMBOLO_CLJ.format(re.escape(nombre))


def contar(lenguaje, nombre, texto):
    """Apariciones de una operación funcional en un texto ya limpio (con las precisiones del encabezado)."""
    if lenguaje == "clojure" and nombre == "count":
        return len(re.findall(r"\(count\s+\((filter|filterv|remove|keep|map|mapv|mapcat|map-indexed)(?=\s)", texto))
    if lenguaje == "scala" and nombre == "getOrElse":
        return sum(1 for m in re.finditer(r"\.getOrElse\(", texto) if "," not in argumentos(texto, m.end()))
    return len(re.findall(patron_operacion(lenguaje, nombre), texto))


def argumentos(texto, inicio):
    """Lo que hay entre el paréntesis que abre en inicio - 1 y el que lo cierra, sin los paréntesis internos."""
    profundidad, fuera = 1, []
    for c in texto[inicio:]:
        profundidad += {"(": 1, ")": -1}.get(c, 0)
        if profundidad == 0:
            break
        if profundidad == 1 and c not in "()":
            fuera.append(c)
    return "".join(fuera)


def operaciones(lenguaje):
    return {"java": OPERACIONES_JAVA, "scala": OPERACIONES_SCALA, "clojure": OPERACIONES_CLOJURE}[lenguaje]


# ---------------------------------------------------------------- principal

def analizar(lenguaje):
    textos = {ruta.name: limpio(ruta, lenguaje) for ruta in archivos(lenguaje)}
    lineas = sum(len(lineas_de_codigo(t)) for t in textos.values())
    print(f"\n{lenguaje}  ({lineas} líneas de código)")

    violaciones = {}
    for regla, patrones in VIOLACIONES[lenguaje].items():
        encontradas = [(nombre, m.group(0).strip()) for nombre, texto in textos.items()
                       for patron in patrones for m in re.finditer(patron, texto)]
        violaciones[regla] = len(encontradas)
        detalle = ", ".join(f"{n}: {v}" for n, v in encontradas[:5])
        print(f"    {regla}: {'cumple' if not encontradas else f'{len(encontradas)} violaciones ({detalle})'}")

    por_categoria = {}
    for categoria, nombres in operaciones(lenguaje).items():
        por_categoria[categoria] = sum(contar(lenguaje, n, texto) for n in nombres for texto in textos.values())
    total = sum(por_categoria.values())
    print("    operaciones: " + ", ".join(f"{c} {n}" for c, n in por_categoria.items()))
    print(f"    densidad: {total} operaciones / {lineas} líneas = {100 * total / lineas:.2f} cada 100")

    restricciones = 12.5 * sum(1 for n in violaciones.values() if n == 0)
    return {"lenguaje": lenguaje, "lineas": lineas,
            **{f"{r}_violaciones": n for r, n in violaciones.items()},
            "restricciones_puntos": f"{restricciones:.1f}",
            **{f"op_{c.lower()}": n for c, n in por_categoria.items()},
            "operaciones": total, "densidad_100": f"{100 * total / lineas:.2f}"}


def main():
    filas = [analizar(l) for l in LENGUAJES]
    destino = RAIZ / "resultados" / "funcional.csv"
    destino.parent.mkdir(exist_ok=True)
    with open(destino, "w", newline="", encoding="utf-8") as f:
        escritor = csv.DictWriter(f, fieldnames=list(filas[0]))
        escritor.writeheader()
        escritor.writerows(filas)
    print(f"\nGuardado en {destino.relative_to(RAIZ)}")


if __name__ == "__main__":
    main()
