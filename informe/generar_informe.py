#!/usr/bin/env python3
"""
=============================================================================
 Genera el informe técnico (Entregable 15) a partir de los resultados del experimento.

   1. Lee resultados/ (puntajes, crudos, calidad, funcional, verificación, entorno).
   2. Escribe informe/informe.json con el contenido (texto, tablas, gráficos y código).
   3. Llama a informe/construir_docx.js para producir Informe_tecnico.docx.

 Uso: python3 informe/generar_informe.py [salida.docx]
 Las cifras salen de los archivos de resultados: si se repite la medición, basta volver a ejecutarlo.
 Los párrafos de análisis (resultados y conclusión) están en contenido.py y se revisan a mano.
=============================================================================
"""
import csv
import json
import statistics
import subprocess
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parent
RES = RAIZ / "resultados"
LENGUAJES = ["java", "scala", "clojure"]
NOMBRE = {"java": "Java", "scala": "Scala", "clojure": "Clojure"}
ESCENARIOS = ["V1", "V2", "V3", "V4", "C1", "X1"]
VUELOS = {"V1": 1_000, "V2": 10_000, "V3": 100_000, "V4": 1_000_000, "C1": 100_000, "X1": 100_000}
CRITERIOS = ["Tiempo", "Memoria", "Rendimiento", "Calidad", "Confiabilidad", "Uso funcional"]


def leer(ruta):
    with open(ruta, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def num(x, decimales=2):
    """Número con formato colombiano: punto de miles y coma decimal."""
    texto = f"{x:,.{decimales}f}"
    return texto.replace(",", "_").replace(".", ",").replace("_", ".")


def datos():
    d = {"puntajes": {f["lenguaje"]: f for f in leer(RES / "puntajes.csv")},
         "calidad": {f["lenguaje"]: f for f in leer(RES / "calidad.csv")},
         "funcional": {f["lenguaje"]: f for f in leer(RES / "funcional.csv")},
         "verificacion": leer(RES / "verificacion.csv"),
         "entorno": (RES / "entorno.txt").read_text(encoding="utf-8"),
         "medidas": {}}
    for e in ESCENARIOS:
        filas = [f for f in leer(RES / "crudos" / f"{e}.csv") if f["ronda"] != "0"]
        for l in LENGUAJES:
            suyas = [f for f in filas if f["lenguaje"] == l and f["salida_correcta"] == "si"]
            d["medidas"][(l, e)] = {
                "n": len(suyas),
                "t_op": statistics.median(float(f["t_operaciones_ms"]) for f in suyas),
                "t_proc": statistics.median(float(f["t_proceso_ms"]) for f in suyas),
                "mem": statistics.median(float(f["memoria_max_mb"]) for f in suyas),
                "rend": statistics.median(int(f["vuelos"]) / (float(f["t_proceso_ms"]) / 1000) for f in suyas),
                "etapas": {k: statistics.median(float(f[f"t_{k}_ms"]) for f in suyas)
                           for k in ["lectura", "validacion", "simulacion", "reportes", "escritura"]},
                "t_op_min": min(float(f["t_operaciones_ms"]) for f in suyas),
                "t_op_max": max(float(f["t_operaciones_ms"]) for f in suyas),
            }
    d["orden"] = sorted(LENGUAJES, key=lambda l: int(d["puntajes"][l]["posicion"]))
    return d


def main():
    import contenido  # textos del informe (en esta misma carpeta)
    d = datos()
    spec = contenido.informe(d, num)
    destino_json = AQUI / "informe.json"
    destino_json.write_text(json.dumps(spec, ensure_ascii=False, indent=1), encoding="utf-8")
    salida = Path(sys.argv[1]) if len(sys.argv) > 1 else RAIZ / "entrega" / "Informe_tecnico.docx"
    salida.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["node", str(AQUI / "construir_docx.js"), str(destino_json), str(salida)], check=True)


if __name__ == "__main__":
    sys.path.insert(0, str(AQUI))
    main()
