#!/usr/bin/env python3
"""
=============================================================================
 Calidad de código (docs/04_criterios.md, sección 3): las mismas tres métricas para los tres lenguajes.

   Q1 · Tamaño       líneas de código, sin comentarios ni líneas vacías
   Q2 · Complejidad  puntos de decisión cada 100 líneas de código
   Q3 · Duplicación  líneas duplicadas en bloques de 50 o más tokens (jscpd, modo "weak": ignora comentarios)

 Uso: python3 experimento/calidad.py        ->  resultados/calidad.csv y un detalle por archivo en pantalla
 Q3 necesita jscpd (npm install -g jscpd).
=============================================================================
"""
import csv
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from fuentes import RAIZ, archivos, limpio, lineas_de_codigo

LENGUAJES = ["java", "scala", "clojure"]
CONDICIONALES_CLJ = {"if", "if-not", "if-let", "if-some", "when", "when-not", "when-let", "when-some"}


# ---------------------------------------------------------------- Q2 en Java y Scala

def decisiones_java(texto):
    ternarios = re.findall(r"(?<![<\w])\?(?!\s*(?:extends|super)\b)(?![>,])", texto)
    casos = re.findall(r"\bcase\b", texto)                      # default no cuenta
    return (len(re.findall(r"\bif\b", texto)) + len(casos) + len(re.findall(r"&&|\|\|", texto))
            + len(ternarios))


def decisiones_scala(texto):
    """case cuenta solo dentro de match o de una función parcial: lleva => en la misma línea.
    No cuentan case class, case object, los case de un enum (no llevan =>) ni case _ =>."""
    casos = [m for m in re.finditer(r"\bcase\b(.*)", texto)
             if "=>" in m.group(1)
             and not re.match(r"\s*(class|object)\b", m.group(1))
             and not re.match(r"\s*_\s*=>", m.group(1))]
    return len(re.findall(r"\bif\b", texto)) + len(casos) + len(re.findall(r"&&|\|\|", texto))


# ---------------------------------------------------------------- Q2 en Clojure (sobre las formas)

def leer_formas(texto):
    """Lector mínimo: listas anidadas de símbolos (el texto ya no tiene comentarios ni contenido de cadenas)."""
    fichas = re.findall(r'#\(|#\{|[()\[\]{}]|""|[^\s,()\[\]{}"]+', texto)
    pila = [[]]
    for ficha in fichas:
        if ficha in ("(", "[", "{", "#(", "#{"):
            pila.append([ficha])
        elif ficha in (")", "]", "}"):
            forma = pila.pop()
            pila[-1].append(forma)
        else:
            pila[-1].append(ficha)
    return pila[0]


def decisiones_clojure(formas):
    """if/when y sus variantes, and y or: 1 por aparición (como cada && o || en Java y Scala).
    cond, condp y case: 1 por par prueba/resultado, sin :else ni el valor por defecto."""
    total = 0
    for forma in formas:
        if not isinstance(forma, list):
            continue
        es_lista = forma and forma[0] in ("(", "#(")
        cabeza = forma[1] if es_lista and len(forma) > 1 and isinstance(forma[1], str) else None
        argumentos = forma[2:]
        if cabeza in CONDICIONALES_CLJ or cabeza in ("and", "or"):
            total += 1
        elif cabeza == "cond":
            pares = len(argumentos) // 2
            ultima_prueba = argumentos[-2] if len(argumentos) >= 2 else None
            total += pares - (1 if ultima_prueba in (":else", "true") else 0)
        elif cabeza == "condp":
            total += len(argumentos[2:]) // 2
        elif cabeza == "case":
            total += len(argumentos[1:]) // 2
        total += decisiones_clojure(forma[1:])
    return total


# ---------------------------------------------------------------- Q3 con jscpd

def duplicacion(lenguaje):
    """Líneas duplicadas que reporta jscpd en el código de una versión, o None si jscpd no está instalado."""
    if shutil.which("jscpd") is None:
        return None
    formato = {"java": "java", "scala": "scala", "clojure": "clojure"}[lenguaje]
    with tempfile.TemporaryDirectory() as salida:
        subprocess.run(["jscpd", "--min-tokens", "50", "--mode", "weak", "--format", formato,
                        "--reporters", "json", "--output", salida, "--silent", str(RAIZ / lenguaje / "src")],
                       capture_output=True, check=True)
        informe = json.loads((Path(salida) / "jscpd-report.json").read_text())
    return informe["statistics"]["total"]["duplicatedLines"]


# ---------------------------------------------------------------- principal

def medir(lenguaje):
    lineas, decisiones = 0, 0
    print(f"\n{lenguaje}")
    for ruta in archivos(lenguaje):
        texto = limpio(ruta, lenguaje)
        loc = len(lineas_de_codigo(texto))
        dec = decisiones_clojure(leer_formas(texto)) if lenguaje == "clojure" else \
            decisiones_scala(texto) if lenguaje == "scala" else decisiones_java(texto)
        print(f"    {ruta.name:22} {loc:5} líneas  {dec:4} decisiones")
        lineas, decisiones = lineas + loc, decisiones + dec
    duplicadas = duplicacion(lenguaje)
    print(f"    {'TOTAL':22} {lineas:5} líneas  {decisiones:4} decisiones  "
          f"({100 * decisiones / lineas:.2f} cada 100)  duplicadas: {duplicadas}")
    return {"lenguaje": lenguaje, "archivos": len(archivos(lenguaje)), "q1_lineas": lineas,
            "decisiones": decisiones, "q2_decisiones_100": f"{100 * decisiones / lineas:.2f}",
            "q3_duplicadas": "" if duplicadas is None else duplicadas}


def main():
    filas = [medir(l) for l in LENGUAJES]
    destino = RAIZ / "resultados" / "calidad.csv"
    destino.parent.mkdir(exist_ok=True)
    with open(destino, "w", newline="", encoding="utf-8") as f:
        escritor = csv.DictWriter(f, fieldnames=list(filas[0]))
        escritor.writeheader()
        escritor.writerows(filas)
    print(f"\nGuardado en {destino.relative_to(RAIZ)}")
    if any(f["q3_duplicadas"] == "" for f in filas):
        print("AVISO: falta jscpd (npm install -g jscpd); Q3 quedó vacío.", file=sys.stderr)


if __name__ == "__main__":
    main()
