#!/usr/bin/env python3
"""
=============================================================================
 Gráficos del informe (Bloque 7). Lee resultados/crudos/, resultados/consolidado.csv y los CSV de calidad y
 uso funcional, y guarda PNG en resultados/graficos/.

 Colores fijos por lenguaje en todos los gráficos (Java azul, Scala naranja, Clojure verde agua), un solo
 eje por gráfico y escenarios de distinto tamaño en paneles separados (no se mezclan escalas).

 Uso: python3 experimento/graficos.py          (necesita matplotlib)
=============================================================================
"""
import csv
import statistics
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.ticker import FuncFormatter  # noqa: E402

RAIZ = Path(__file__).resolve().parent.parent
RESULTADOS = RAIZ / "resultados"
SALIDA = RESULTADOS / "graficos"
LENGUAJES = ["java", "scala", "clojure"]
NOMBRE = {"java": "Java", "scala": "Scala", "clojure": "Clojure"}
COLOR = {"java": "#2a78d6", "scala": "#eb6834", "clojure": "#1baf7a"}
ESCENARIOS = ["V1", "V2", "V3", "V4", "C1", "X1"]
DESCRIPCION = {"V1": "1.000 vuelos", "V2": "10.000 vuelos", "V3": "100.000 vuelos", "V4": "1.000.000 vuelos",
               "C1": "100.000 · congestión", "X1": "100.000 · 10 % inválidos"}
CRITERIOS = ["Tiempo", "Memoria", "Rendimiento", "Calidad", "Confiabilidad", "Uso funcional"]
PESOS = {"Tiempo": 25, "Memoria": 20, "Rendimiento": 20, "Calidad": 15, "Confiabilidad": 10, "Uso funcional": 10}
TEXTO, TEXTO_2, REJILLA, FONDO = "#0b0b0b", "#52514e", "#e4e3df", "#ffffff"

plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 10, "axes.edgecolor": REJILLA, "axes.labelcolor": TEXTO_2,
    "xtick.color": TEXTO_2, "ytick.color": TEXTO_2, "axes.titlecolor": TEXTO, "axes.titlesize": 11,
    "axes.titleweight": "bold", "axes.spines.top": False, "axes.spines.right": False,
    "axes.grid": True, "grid.color": REJILLA, "grid.linewidth": 0.6, "axes.axisbelow": True,
    "figure.facecolor": FONDO, "axes.facecolor": FONDO, "legend.frameon": False, "savefig.dpi": 200,
})


def leer(ruta):
    with open(ruta, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def miles(x):
    return f"{x:,.0f}".replace(",", ".")


def coma(x, decimales):
    """Decimal con coma, como en el informe."""
    return f"{x:.{decimales}f}".replace(".", ",")


EJE_MILES = FuncFormatter(lambda v, _: miles(v))


def medidas():
    """Por (lenguaje, escenario): listas de las rondas medidas válidas."""
    datos = {}
    for escenario in ESCENARIOS:
        filas = [f for f in leer(RESULTADOS / "crudos" / f"{escenario}.csv")
                 if f["ronda"] != "0" and f["salida_correcta"] == "si"]
        for lenguaje in LENGUAJES:
            suyas = [f for f in filas if f["lenguaje"] == lenguaje]
            datos[(lenguaje, escenario)] = {
                "t_operaciones": [float(f["t_operaciones_ms"]) for f in suyas],
                "t_proceso": [float(f["t_proceso_ms"]) for f in suyas],
                "memoria": [float(f["memoria_max_mb"]) for f in suyas],
                "rendimiento": [int(f["vuelos"]) / (float(f["t_proceso_ms"]) / 1000) for f in suyas],
                "etapas": {e: statistics.median(float(f[f"t_{e}_ms"]) for f in suyas)
                           for e in ["lectura", "validacion", "simulacion", "reportes", "escritura"]} if suyas else {},
            }
    return datos


def leyenda(figura):
    figura.legend(handles=[plt.Rectangle((0, 0), 1, 1, color=COLOR[l]) for l in LENGUAJES],
                  labels=[NOMBRE[l] for l in LENGUAJES], loc="upper center", ncol=3, bbox_to_anchor=(0.5, 0.995))


def guardar(figura, nombre):
    SALIDA.mkdir(parents=True, exist_ok=True)
    figura.savefig(SALIDA / nombre, bbox_inches="tight")
    plt.close(figura)


# ---------------------------------------------------------------- 1. puntaje final

def puntaje_final():
    filas = {f["lenguaje"]: f for f in leer(RESULTADOS / "puntajes.csv")}
    orden = sorted(LENGUAJES, key=lambda l: float(filas[l]["Final"]))
    figura, eje = plt.subplots(figsize=(7, 2.6))
    barras = eje.barh([NOMBRE[l] for l in orden], [float(filas[l]["Final"]) for l in orden],
                      color=[COLOR[l] for l in orden], height=0.55)
    for barra, l in zip(barras, orden):
        eje.text(barra.get_width() + 1, barra.get_y() + barra.get_height() / 2, coma(float(filas[l]['Final']), 2),
                 va="center", color=TEXTO, fontweight="bold")
    eje.set_xlim(0, 108)
    eje.set_xlabel("Puntaje final (0 a 100)")
    eje.grid(axis="y", visible=False)
    eje.set_title("Puntaje final ponderado", loc="left")
    guardar(figura, "01_puntaje_final.png")


# ---------------------------------------------------------------- 2. puntaje por criterio

def puntajes_por_criterio():
    filas = {f["lenguaje"]: f for f in leer(RESULTADOS / "puntajes.csv")}
    figura, eje = plt.subplots(figsize=(9, 3.6))
    ancho = 0.26
    for i, lenguaje in enumerate(LENGUAJES):
        posiciones = [c + (i - 1) * (ancho + 0.02) for c in range(len(CRITERIOS))]
        eje.bar(posiciones, [float(filas[lenguaje][c]) for c in CRITERIOS], width=ancho, color=COLOR[lenguaje])
    eje.set_xticks(range(len(CRITERIOS)), [f"{c}\n({PESOS[c]} %)" for c in CRITERIOS])
    eje.set_ylim(0, 105)
    eje.set_ylabel("Puntaje (0 a 100)")
    eje.grid(axis="x", visible=False)
    eje.set_title("Puntaje por criterio", loc="left", pad=28)
    leyenda(figura)
    guardar(figura, "02_puntaje_por_criterio.png")


# ---------------------------------------------------------------- 3 a 5. por escenario (paneles)

def por_escenario(datos, campo, titulo, unidad, archivo, formato):
    figura, ejes = plt.subplots(2, 3, figsize=(10, 5.6))
    for eje, escenario in zip(ejes.flat, ESCENARIOS):
        valores = [datos[(l, escenario)][campo] for l in LENGUAJES]
        medianas = [statistics.median(v) if v else 0 for v in valores]
        errores = [[m - min(v) if v else 0 for m, v in zip(medianas, valores)],
                   [max(v) - m if v else 0 for m, v in zip(medianas, valores)]]
        barras = eje.bar(range(3), medianas, color=[COLOR[l] for l in LENGUAJES], width=0.62,
                         yerr=errores, error_kw={"ecolor": TEXTO_2, "elinewidth": 0.8, "capsize": 3})
        for barra, m in zip(barras, medianas):
            eje.text(barra.get_x() + barra.get_width() / 2, barra.get_height() * 0.5, formato(m), ha="center",
                     va="center", color="white", fontsize=8.5, fontweight="bold")
        eje.set_xticks(range(3), [NOMBRE[l] for l in LENGUAJES])
        eje.set_title(f"{escenario} · {DESCRIPCION[escenario]}", fontsize=9.5)
        eje.grid(axis="x", visible=False)
        eje.set_ylim(0, max(max(v) if v else 0 for v in valores) * 1.12 or 1)
        eje.yaxis.set_major_formatter(EJE_MILES)
    figura.supylabel(unidad, color=TEXTO_2, fontsize=10)
    figura.suptitle(titulo, x=0.01, ha="left", fontweight="bold", fontsize=11, color=TEXTO)
    figura.text(0.01, -0.02, "Barra: mediana de 10 rondas. Línea: mínimo a máximo.", color=TEXTO_2, fontsize=8.5)
    figura.tight_layout()
    guardar(figura, archivo)


# ---------------------------------------------------------------- 6. etapas en V4

def etapas_v4(datos):
    nombres = {"lectura": "Lectura", "validacion": "Validación", "simulacion": "Simulación", "reportes": "Reportes",
               "escritura": "Escritura"}
    colores = ["#86b6ef", "#2a78d6", "#184f95", "#eda100", "#c3c2b7"]
    figura, eje = plt.subplots(figsize=(9, 2.8))
    for fila, lenguaje in enumerate(reversed(LENGUAJES)):
        izquierda = 0
        for (etapa, nombre), color in zip(nombres.items(), colores):
            valor = datos[(lenguaje, "V4")]["etapas"].get(etapa, 0) / 1000
            eje.barh(fila, valor, left=izquierda, color=color, height=0.55, edgecolor=FONDO, linewidth=1.5,
                     label=nombre if fila == 0 else None)
            if valor > 0.9:
                eje.text(izquierda + valor / 2, fila, coma(valor, 1), ha="center", va="center", fontsize=8.5,
                         color="white" if etapa in ("validacion", "simulacion") else TEXTO)
            izquierda += valor
        eje.text(izquierda + 0.1, fila, f"{coma(izquierda, 1)} s", va="center", color=TEXTO, fontweight="bold")
    eje.set_yticks(range(3), [NOMBRE[l] for l in reversed(LENGUAJES)])
    eje.set_xlabel("Segundos (mediana de 10 rondas)")
    eje.xaxis.set_major_formatter(FuncFormatter(lambda v, _: coma(v, 1)))
    eje.grid(axis="y", visible=False)
    eje.set_title("V4 (1.000.000 de vuelos): tiempo de cada etapa dentro del programa", loc="left", pad=26)
    eje.legend(loc="upper center", ncol=5, bbox_to_anchor=(0.5, 1.19), fontsize=8.5)
    guardar(figura, "06_etapas_V4.png")


# ---------------------------------------------------------------- 7. calidad y uso funcional

def calidad_y_funcional():
    calidad = {f["lenguaje"]: f for f in leer(RESULTADOS / "calidad.csv")}
    funcional = {f["lenguaje"]: f for f in leer(RESULTADOS / "funcional.csv")}
    paneles = [("Líneas de código (Q1)", lambda l: float(calidad[l]["q1_lineas"]), 0, "menos es mejor"),
               ("Decisiones cada 100 líneas (Q2)", lambda l: float(calidad[l]["q2_decisiones_100"]), 2,
                "menos es mejor"),
               ("Operaciones funcionales cada 100 líneas", lambda l: float(funcional[l]["densidad_100"]), 2,
                "más es mejor")]
    figura, ejes = plt.subplots(1, 3, figsize=(10, 3))
    for eje, (titulo, valor, formato, sentido) in zip(ejes, paneles):
        valores = [valor(l) for l in LENGUAJES]
        barras = eje.bar(range(3), valores, color=[COLOR[l] for l in LENGUAJES], width=0.62)
        for barra, v in zip(barras, valores):
            eje.text(barra.get_x() + barra.get_width() / 2, v * 1.02, coma(v, formato), ha="center", va="bottom",
                     fontsize=8.5, color=TEXTO)
        eje.set_xticks(range(3), [NOMBRE[l] for l in LENGUAJES])
        eje.set_ylim(0, max(valores) * 1.18)
        eje.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:g}".replace(".", ",")))
        eje.set_title(f"{titulo}\n({sentido})", fontsize=9.5)
        eje.grid(axis="x", visible=False)
    figura.suptitle("Calidad de código y uso funcional (análisis del código fuente)", x=0.01, ha="left",
                    fontweight="bold", fontsize=11, color=TEXTO)
    figura.tight_layout()
    guardar(figura, "07_calidad_y_funcional.png")


def main():
    datos = medidas()
    puntaje_final()
    puntajes_por_criterio()
    por_escenario(datos, "t_operaciones", "Tiempo de las operaciones (validación + simulación + reportes)",
                  "Milisegundos (menos es mejor)", "03_tiempo_por_escenario.png", lambda m: miles(m))
    por_escenario(datos, "memoria", "Memoria máxima del proceso", "MB (menos es mejor)",
                  "04_memoria_por_escenario.png", lambda m: miles(m))
    por_escenario(datos, "rendimiento", "Rendimiento: vuelos procesados por segundo (proceso completo)",
                  "Vuelos por segundo (más es mejor)", "05_rendimiento_por_escenario.png", lambda m: miles(m))
    etapas_v4(datos)
    calidad_y_funcional()
    print(f"Gráficos en {SALIDA.relative_to(RAIZ)}/: " + ", ".join(sorted(p.name for p in SALIDA.glob('*.png'))))


if __name__ == "__main__":
    main()
