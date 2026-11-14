#!/usr/bin/env python3
"""
=============================================================================
 Clasificación automática (docs/04_criterios.md, secciones 1 a 6).

 Entradas (en resultados/):
   crudos/<escenario>.csv   una fila por ejecución (ejecutar.py)
   verificacion.csv         correctitud y robustez (verificar.sh)
   calidad.csv              Q1, Q2 y Q3 (calidad.py)
   funcional.csv            restricciones F1-F4 y densidad funcional (funcional.py)

 Salidas (en resultados/):
   consolidado.csv          cada métrica en bruto y cada puntaje, por lenguaje
   puntajes.csv             el puntaje de cada criterio, el final y la posición
   clasificacion.md         posiciones, puntajes por criterio, explicación de cada posición y prueba de solidez

 Uso: python3 experimento/clasificar.py [--resultados <carpeta>]
=============================================================================
"""
import argparse
import csv
import statistics
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
LENGUAJES = ["java", "scala", "clojure"]
NOMBRE = {"java": "Java", "scala": "Scala", "clojure": "Clojure"}
ESCENARIOS = ["V1", "V2", "V3", "V4", "C1", "X1"]
CORRECTITUD = ["E0", "V1", "V2", "V3", "V4", "C1", "X1"]
ROBUSTEZ = [f"R{n:02d}" for n in range(1, 13)]
RONDAS = 10
PESOS = {"Tiempo": 0.25, "Memoria": 0.20, "Rendimiento": 0.20, "Calidad": 0.15, "Confiabilidad": 0.10,
         "Uso funcional": 0.10}


# ---------------------------------------------------------------- puntajes (sección 1)

def proporcional(valores, menor_es_mejor, suavizar=False):
    """100 · mejor / valor (o valor / mejor). Con suavizar: 100 · (mejor + 1) / (valor + 1).
    Un lenguaje sin valor (None) recibe 0."""
    validos = [v for v in valores.values() if v is not None]
    if not validos:
        return {l: 0.0 for l in valores}
    mejor = min(validos) if menor_es_mejor else max(validos)
    puntaje = {}
    for lenguaje, valor in valores.items():
        if valor is None:
            puntaje[lenguaje] = 0.0
        elif suavizar:
            puntaje[lenguaje] = 100 * (mejor + 1) / (valor + 1)
        elif menor_es_mejor:
            puntaje[lenguaje] = 100 * mejor / valor if valor else 100.0
        else:
            puntaje[lenguaje] = 100 * valor / mejor if mejor else 0.0
    return puntaje


# ---------------------------------------------------------------- lectura

def leer_csv(ruta):
    with open(ruta, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def medianas(carpeta):
    """Mediana de las rondas medidas válidas, por (lenguaje, escenario): tiempo, memoria y rendimiento."""
    resultado, estables = {}, {l: 0 for l in LENGUAJES}
    for escenario in ESCENARIOS:
        ruta = carpeta / "crudos" / f"{escenario}.csv"
        filas = [f for f in leer_csv(ruta) if f["ronda"] != "0"] if ruta.exists() else []
        for lenguaje in LENGUAJES:
            suyas = [f for f in filas if f["lenguaje"] == lenguaje]
            validas = [f for f in suyas if f["codigo_salida"] == "0" and f["salida_correcta"] == "si"]
            estables[lenguaje] += len(validas)
            resultado[(lenguaje, escenario)] = None if not validas else {
                "t_operaciones_ms": statistics.median(float(f["t_operaciones_ms"]) for f in validas),
                "memoria_max_mb": statistics.median(float(f["memoria_max_mb"]) for f in validas),
                "vuelos_por_s": statistics.median(int(f["vuelos"]) / (float(f["t_proceso_ms"]) / 1000)
                                                  for f in validas),
            }
    return resultado, estables


# ---------------------------------------------------------------- criterios

def criterios(carpeta):
    filas_consolidado = []
    puntajes = {l: {} for l in LENGUAJES}

    def anotar(lenguaje, criterio, metrica, detalle, bruto, puntaje):
        filas_consolidado.append({"lenguaje": lenguaje, "criterio": criterio, "metrica": metrica,
                                  "detalle": detalle, "valor": "" if bruto is None else f"{bruto:.4f}",
                                  "puntaje": f"{puntaje:.2f}"})

    # Tiempo, memoria y rendimiento (sección 2): proporcional por escenario y promedio de los 6
    meds, estables = medianas(carpeta)
    for criterio, campo, menor in [("Tiempo", "t_operaciones_ms", True), ("Memoria", "memoria_max_mb", True),
                                   ("Rendimiento", "vuelos_por_s", False)]:
        por_escenario = {l: [] for l in LENGUAJES}
        for escenario in ESCENARIOS:
            valores = {l: None if meds[(l, escenario)] is None else meds[(l, escenario)][campo] for l in LENGUAJES}
            for lenguaje, p in proporcional(valores, menor).items():
                por_escenario[lenguaje].append(p)
                anotar(lenguaje, criterio, campo, escenario, valores[lenguaje], p)
        for lenguaje in LENGUAJES:
            puntajes[lenguaje][criterio] = statistics.mean(por_escenario[lenguaje])

    # Calidad (sección 3): Q1, Q2 y Q3, un tercio cada una
    calidad = {f["lenguaje"]: f for f in leer_csv(carpeta / "calidad.csv")}
    partes = {l: [] for l in LENGUAJES}
    for metrica, campo, suavizar in [("Q1 líneas de código", "q1_lineas", False),
                                     ("Q2 decisiones cada 100 líneas", "q2_decisiones_100", False),
                                     ("Q3 líneas duplicadas", "q3_duplicadas", True)]:
        valores = {l: float(calidad[l][campo]) for l in LENGUAJES}
        for lenguaje, p in proporcional(valores, True, suavizar).items():
            partes[lenguaje].append(p)
            anotar(lenguaje, "Calidad", metrica, "", valores[lenguaje], p)
    for lenguaje in LENGUAJES:
        puntajes[lenguaje]["Calidad"] = statistics.mean(partes[lenguaje])

    # Confiabilidad (sección 4): promedio de correctitud, robustez y estabilidad
    verificacion = {(f["caso"], f["lenguaje"]): f["resultado"] == "ok" for f in leer_csv(carpeta / "verificacion.csv")}
    for lenguaje in LENGUAJES:
        correctos = sum(verificacion.get((c, lenguaje), False) for c in CORRECTITUD)
        robustos = sum(verificacion.get((c, lenguaje), False) for c in ROBUSTEZ)
        total_estabilidad = len(ESCENARIOS) * RONDAS
        partes_conf = [100 * correctos / len(CORRECTITUD), 100 * robustos / len(ROBUSTEZ),
                       100 * estables[lenguaje] / total_estabilidad]
        anotar(lenguaje, "Confiabilidad", "Correctitud", f"{correctos}/{len(CORRECTITUD)}", correctos, partes_conf[0])
        anotar(lenguaje, "Confiabilidad", "Robustez", f"{robustos}/{len(ROBUSTEZ)}", robustos, partes_conf[1])
        anotar(lenguaje, "Confiabilidad", "Estabilidad", f"{estables[lenguaje]}/{total_estabilidad}",
               estables[lenguaje], partes_conf[2])
        puntajes[lenguaje]["Confiabilidad"] = statistics.mean(partes_conf)

    # Uso funcional (sección 5): restricciones (0-50) + densidad proporcional (0-50)
    funcional = {f["lenguaje"]: f for f in leer_csv(carpeta / "funcional.csv")}
    densidad = proporcional({l: float(funcional[l]["densidad_100"]) for l in LENGUAJES}, False)
    for lenguaje in LENGUAJES:
        restricciones = float(funcional[lenguaje]["restricciones_puntos"])
        anotar(lenguaje, "Uso funcional", "Restricciones F1-F4", "", restricciones, restricciones)
        anotar(lenguaje, "Uso funcional", "Densidad funcional cada 100 líneas", "",
               float(funcional[lenguaje]["densidad_100"]), densidad[lenguaje] / 2)
        puntajes[lenguaje]["Uso funcional"] = restricciones + densidad[lenguaje] / 2

    return puntajes, filas_consolidado


# ---------------------------------------------------------------- clasificación (sección 6)

def final(puntaje, pesos):
    return sum(pesos[c] * puntaje[c] for c in pesos)


def ordenar(puntajes, pesos):
    """Mayor puntaje final; desempate por Tiempo y luego por Memoria."""
    return sorted(LENGUAJES, key=lambda l: (-round(final(puntajes[l], pesos), 6), -puntajes[l]["Tiempo"],
                                            -puntajes[l]["Memoria"]))


def variantes():
    yield "Pesos del proyecto", PESOS
    yield "Pesos iguales", {c: 1 / len(PESOS) for c in PESOS}
    for quitado in PESOS:
        resto = {c: p for c, p in PESOS.items() if c != quitado}
        suma = sum(resto.values())
        yield f"Sin {quitado}", {c: p / suma for c, p in resto.items()}


def explicacion(lenguaje, puntajes, posicion):
    suyo = puntajes[lenguaje]
    empate = [c for c in PESOS if max(puntajes[l][c] for l in LENGUAJES) - min(puntajes[l][c] for l in LENGUAJES) < 1e-9]
    gana = [c for c in PESOS if c not in empate and suyo[c] >= max(puntajes[l][c] for l in LENGUAJES) - 1e-9]
    pierde = [(c, max(puntajes[l][c] for l in LENGUAJES) - suyo[c]) for c in PESOS
              if c not in gana and c not in empate]
    pierde.sort(key=lambda par: -par[1] * PESOS[par[0]])
    texto = f"**{posicion}.º {NOMBRE[lenguaje]}** ({final(suyo, PESOS):.2f} puntos). "
    texto += (f"Es el mejor en {', '.join(gana)}. " if gana else "No es el mejor en ningún criterio. ")
    texto += (f"Los tres empatan en {', '.join(empate)}. " if empate else "")
    if pierde:
        texto += "Pierde " + "; ".join(
            f"{d:.1f} puntos en {c} (le restan {d * PESOS[c]:.2f} al final)" for c, d in pierde) + "."
    return texto


def informe(puntajes, carpeta):
    orden = ordenar(puntajes, PESOS)
    lineas = ["# Clasificación automática", "",
              "Generado por `experimento/clasificar.py` con los criterios de `docs/04_criterios.md`.", "",
              "## Posiciones", "",
              "| Posición | Lenguaje | " + " | ".join(f"{c} ({PESOS[c]:.0%})" for c in PESOS) + " | **Final** |",
              "|---|---|" + "---|" * len(PESOS) + "---|"]
    for posicion, lenguaje in enumerate(orden, start=1):
        lineas.append(f"| {posicion} | {NOMBRE[lenguaje]} | "
                      + " | ".join(f"{puntajes[lenguaje][c]:.2f}" for c in PESOS)
                      + f" | **{final(puntajes[lenguaje], PESOS):.2f}** |")
    lineas += ["", "## Por qué cada lenguaje quedó en su posición", ""]
    lineas += [explicacion(l, puntajes, p) + "\n" for p, l in enumerate(orden, start=1)]

    lineas += ["## Prueba de solidez", "",
               "La clasificación se recalcula con pesos iguales y quitando un criterio a la vez (su peso se reparte "
               "entre los demás en proporción a sus pesos).", "",
               "| Variante | 1.º | 2.º | 3.º | Puntaje del 1.º |", "|---|---|---|---|---|"]
    ganadores = []
    for nombre, pesos in variantes():
        o = ordenar(puntajes, pesos)
        ganadores.append(o[0]) if nombre != "Pesos del proyecto" else None
        lineas.append(f"| {nombre} | " + " | ".join(NOMBRE[l] for l in o) + f" | {final(puntajes[o[0]], pesos):.2f} |")
    mismo = sum(g == orden[0] for g in ganadores)
    lineas += ["", f"**{NOMBRE[orden[0]]} gana en {mismo} de las {len(ganadores)} variantes.** "
               + ("La decisión no depende de los pesos elegidos." if mismo == len(ganadores)
                  else "La decisión depende en parte de los pesos: ver las variantes en las que cambia el ganador.")]
    (carpeta / "clasificacion.md").write_text("\n".join(lineas) + "\n", encoding="utf-8")
    return "\n".join(lineas)


def main():
    analizador = argparse.ArgumentParser(description="Clasificación automática (Bloque 7)")
    analizador.add_argument("--resultados", default=str(RAIZ / "resultados"))
    carpeta = Path(analizador.parse_args().resultados)
    puntajes, filas = criterios(carpeta)
    with open(carpeta / "consolidado.csv", "w", newline="", encoding="utf-8") as f:
        escritor = csv.DictWriter(f, fieldnames=list(filas[0]))
        escritor.writeheader()
        escritor.writerows(filas)
    orden = ordenar(puntajes, PESOS)
    with open(carpeta / "puntajes.csv", "w", newline="", encoding="utf-8") as f:
        escritor = csv.writer(f)
        escritor.writerow(["posicion", "lenguaje", *PESOS, "Final"])
        for posicion, lenguaje in enumerate(orden, start=1):
            escritor.writerow([posicion, lenguaje, *[f"{puntajes[lenguaje][c]:.2f}" for c in PESOS],
                               f"{final(puntajes[lenguaje], PESOS):.2f}"])
    print(informe(puntajes, carpeta))


if __name__ == "__main__":
    main()
