"""
Implementación de referencia del contrato del Bloque 2 (docs/02_modelo_y_contrato.md).

NO participa en la comparación. Solo produce las salidas esperadas de cada escenario, para verificar que
las versiones en Java, Scala y Clojure son correctas. Está escrita de la forma más directa posible, sin
restricciones funcionales, y coincide con el ejemplo resuelto a mano (datos/ejemplo).

Reproduce exactamente el comportamiento de la JVM en los detalles que importan:
  - trim: quita los caracteres con código <= U+0020 (String.trim de Java);
  - texto: UTF-8, los bytes inválidos se reemplazan por U+FFFD;
  - orden de textos: por unidades UTF-16 (String.compareTo de Java);
  - decimales: redondeo HALF_UP exacto con aritmética entera.

Uso: python3 experimento/referencia.py <pistas.csv> <vuelos.csv> <carpeta_salida> [--medir <archivo>]
"""
import os
import re
import sys
from fractions import Fraction

USOS = ["Despegue", "Aterrizaje", "Mixta"]
ESTADOS = ["Operativa", "Cerrada"]
CATEGORIAS = ["Ligero", "Mediano", "Pesado"]
OPERACIONES = ["Despegue", "Aterrizaje"]
PRIORIDADES = ["Normal", "Emergencia"]
LONGITUD_MIN = {"Ligero": 1200, "Mediano": 2000, "Pesado": 2800}
OCUPACION = {"Ligero": 2, "Mediano": 3, "Pesado": 4}
UMBRAL = 15
ENTERO = re.compile(r"-?[0-9]{1,9}")
HORA = re.compile(r"([0-9]{2}):([0-9]{2})")
SIN = "Sin datos"
ESPACIOS_JVM = "".join(chr(i) for i in range(33))
USO_PROGRAMA = "Uso: java -jar simulador-<lenguaje>.jar <pistas.csv> <vuelos.csv> <carpeta_salida> [--medir <archivo>]"


def trim(s):
    return s.strip(ESPACIOS_JVM)


def orden_jvm(s):
    return s.encode("utf-16-be", "surrogatepass")


def hora_texto(m):
    return f"D{m // 1440 + 1} {(m % 1440) // 60:02d}:{m % 60:02d}"


def decimal2(num, den):
    """num/den con 2 decimales, redondeo HALF_UP exacto (num >= 0, den > 0)."""
    c = (200 * num + den) // (2 * den)
    return f"{c // 100}.{c % 100:02d}"


def registros(ruta):
    with open(ruta, "rb") as f:
        lineas = f.read().decode("utf-8", errors="replace").split("\n")
    return [(i + 1, l) for i, l in enumerate(lineas) if i > 0 and trim(l) != ""]


def opcion(valor, campo, opciones):
    return None if valor in opciones else f"{campo} con valor no válido: {valor} (valores: {'/'.join(opciones)})"


def validar_pista(campos, ids):
    if len(campos) != 4:
        return f"se esperaban 4 campos y hay {len(campos)}"
    i, lon, uso, est = campos
    if i == "": return "id vacío"
    if i in ids: return f"id repetido: {i}"
    if not ENTERO.fullmatch(lon): return f"longitud no es un entero: {lon}"
    if int(lon) <= 0: return f"longitud debe ser mayor que 0: {lon}"
    return opcion(uso, "uso", USOS) or opcion(est, "estado", ESTADOS)


def validar_vuelo(campos, codigos):
    if len(campos) != 8:
        return f"se esperaban 8 campos y hay {len(campos)}"
    cod, aer, mat, cat, op, dia, hora, pri = campos
    if cod == "": return "código vacío"
    if cod in codigos: return f"código repetido: {cod}"
    if aer == "": return "aerolínea vacía"
    if mat == "": return "matrícula vacía"
    e = opcion(cat, "categoría", CATEGORIAS) or opcion(op, "operación", OPERACIONES)
    if e: return e
    if not ENTERO.fullmatch(dia): return f"día no es un entero: {dia}"
    if not (1 <= int(dia) <= 9999): return f"día debe estar entre 1 y 9999: {dia}"
    m = HORA.fullmatch(hora)
    if not m or int(m.group(1)) > 23 or int(m.group(2)) > 59:
        return f"hora no válida: {hora} (formato HH:MM de 00:00 a 23:59)"
    return opcion(pri, "prioridad", PRIORIDADES)


def cargar(ruta, validar, construir, archivo):
    validos, errores, claves = [], [], set()
    regs = registros(ruta)
    for n, linea in regs:
        campos = [trim(c) for c in linea.split(",")]
        e = validar(campos, claves)
        if e:
            errores.append((archivo, n, e))
        else:
            claves.add(campos[0]); validos.append(construir(campos))
    return validos, errores, len(regs)


def pista(c):
    return {"id": c[0], "lon": int(c[1]), "uso": c[2], "estado": c[3]}


def vuelo(c):
    hh, mm = c[6].split(":")
    return {"cod": c[0], "aer": c[1], "mat": c[2], "cat": c[3], "op": c[4], "pri": c[7],
            "prog": (int(c[5]) - 1) * 1440 + int(hh) * 60 + int(mm)}


def habilitada(v, p):
    return p["estado"] == "Operativa" and p["uso"] in ("Mixta", v["op"])


def compatible(v, p):
    return habilitada(v, p) and p["lon"] >= LONGITUD_MIN[v["cat"]]


def motivo_no_asignable(v, pistas):
    if not any(habilitada(v, p) for p in pistas): return "sin pista habilitada para la operación"
    if not any(compatible(v, p) for p in pistas): return "sin pista con longitud suficiente"
    return None


def clave_prioridad(v):
    return (0 if v["pri"] == "Emergencia" else 1, 0 if v["op"] == "Aterrizaje" else 1, v["prog"], orden_jvm(v["cod"]))


def simular(vuelos, pistas):
    operativas = sorted([p for p in pistas if p["estado"] == "Operativa"], key=lambda p: orden_jvm(p["id"]))
    filas = {}
    for v in vuelos:
        filas.setdefault((v["op"], v["cat"], v["pri"]), []).append(v)
    filas = {k: sorted(fs, key=lambda v: (v["prog"], orden_jvm(v["cod"]))) for k, fs in filas.items()}
    cabeza = {k: 0 for k in filas}
    libre = {p["id"]: 0 for p in operativas}
    if not vuelos: return []
    t = min(v["prog"] for v in vuelos)
    ops = []
    while any(cabeza[k] < len(filas[k]) for k in filas):
        while True:
            cand = []
            for k, fs in filas.items():
                if cabeza[k] < len(fs) and fs[cabeza[k]]["prog"] <= t:
                    v = fs[cabeza[k]]
                    libres = [p for p in operativas if libre[p["id"]] <= t and compatible(v, p)]
                    if libres: cand.append((clave_prioridad(v), k, v, libres[0]))
            if not cand: break
            _, k, v, p = min(cand, key=lambda c: c[0])
            fin = t + OCUPACION[v["cat"]]
            libre[p["id"]] = fin; cabeza[k] += 1
            ops.append({**v, "pista": p["id"], "ini": t, "fin": fin, "ret": t - v["prog"]})
        sig = [x for x in libre.values() if x > t] + [fs[cabeza[k]]["prog"] for k, fs in filas.items()
                                                       if cabeza[k] < len(fs) and fs[cabeza[k]]["prog"] > t]
        if not sig: break
        t = min(sig)
    return ops


def reporte(pistas_tot, pistas_val, err_p, vuelos_tot, vuelos_val, err_v, ops, no_asig, pistas):
    L = ["SIMULADOR DE OPERACIONES AEROPORTUARIAS · REPORTE", ""]
    L += ["== RF03 · Validación de datos ==",
          f"Pistas | registros: {pistas_tot} | válidos: {len(pistas_val)} | inválidos: {len(err_p)}",
          f"Vuelos | registros: {vuelos_tot} | válidos: {len(vuelos_val)} | inválidos: {len(err_v)}",
          "Detalle de los registros inválidos: errores.csv", ""]
    n = len(ops)
    suma = sum(o["ret"] for o in ops)
    prom = decimal2(suma, n) + " min" if n else SIN
    retr = sum(1 for o in ops if o["ret"] > UMBRAL)
    pct_retr = decimal2(100 * retr, n) + "%" if n else SIN
    L += ["== RF08 · Resumen de retrasos ==", f"Operaciones asignadas: {n}", f"Retraso promedio: {prom}",
          f"Retraso máximo: {str(max(o['ret'] for o in ops)) + ' min' if n else SIN}",
          f"Vuelos retrasados (más de {UMBRAL} min): {str(retr) + ' (' + pct_retr + ')' if n else SIN}", ""]
    top = sorted(ops, key=lambda o: (-o["ret"], orden_jvm(o["cod"])))[:5]
    L += ["== RF09 · 5 vuelos más retrasados =="] + (
        [f"{i}. {o['cod']} | retraso: {o['ret']} min | {o['op']} | {o['pista']}" for i, o in enumerate(top, 1)] or [SIN]) + [""]
    L += ["== RF10 · Uso de pistas =="]
    if n and pistas:
        ini, fin = min(o["prog"] for o in ops), max(o["fin"] for o in ops)
        per = fin - ini
        L.append(f"Período simulado: {hora_texto(ini)} a {hora_texto(fin)} ({per} min)")
        for p in sorted(pistas, key=lambda p: orden_jvm(p["id"])):
            mias = [o for o in ops if o["pista"] == p["id"]]
            occ = sum(o["fin"] - o["ini"] for o in mias)
            L.append(f"{p['id']} | {p['estado']} | operaciones: {len(mias)} | ocupada: {occ} min | ocupación: {decimal2(100 * occ, per)}%")
    else:
        L.append(SIN)
    L.append("")
    aer = {}
    for o in ops: aer.setdefault(o["aer"], []).append(o["ret"])
    filas = [(a, sum(r), len(r)) for a, r in aer.items()]
    filas.sort(key=lambda x: orden_jvm(x[0]))
    filas.sort(key=lambda x: Fraction(x[1], x[2]), reverse=True)  # estable: empates quedan por nombre
    L += ["== RF11 · Retraso promedio por aerolínea =="] + (
        [f"{a} | retraso promedio: {decimal2(s, c)} min | operaciones: {c}" for a, s, c in filas] or [SIN]) + [""]
    L += ["== RF12 · Vuelos no asignables =="] + (
        [f"{v['cod']} | {v['op']} | {v['cat']} | {m}" for v, m in no_asig] or ["Ninguno"]) + [""]
    L += ["== RF13 · Operaciones por tipo y categoría =="] + [
        f"{x}: {sum(1 for o in ops if o['op'] == x)}" for x in ["Aterrizaje", "Despegue"]] + [
        f"{x}: {sum(1 for o in ops if o['cat'] == x)}" for x in CATEGORIAS] + [""]
    uso = sorted(((p["id"], sum(1 for o in ops if o["pista"] == p["id"])) for p in pistas),
                 key=lambda x: (-x[1], orden_jvm(x[0])))
    mas = f"{uso[0][0]} (operaciones: {uso[0][1]})" if n and uso else SIN
    L += ["== RF14 · Resumen ejecutivo ==", f"Vuelos cargados: {vuelos_tot}", f"Vuelos válidos: {len(vuelos_val)}",
          f"Vuelos inválidos: {len(err_v)}", f"Vuelos asignados: {n}", f"Vuelos no asignables: {len(no_asig)}",
          f"Retraso promedio: {prom}", f"Vuelos retrasados: {pct_retr}", f"Pista más usada: {mas}",
          f"Aerolínea con mayor retraso promedio: {filas[0][0] + ' (' + decimal2(filas[0][1], filas[0][2]) + ' min)' if filas else SIN}"]
    return "\n".join(L) + "\n"


def error_de_uso(motivo):
    sys.stdout.write(f"ERROR: {motivo}\n{USO_PROGRAMA}\n")
    sys.exit(2)


def main():
    args = sys.argv[1:]
    if not (len(args) == 3 or (len(args) == 5 and args[3] == "--medir")):
        error_de_uso("número de argumentos incorrecto")
    rp, rv, sal = args[:3]
    for r in (rp, rv):
        if not (os.path.isfile(r) and os.access(r, os.R_OK)):
            error_de_uso(f"no se puede leer el archivo {r}")
    pistas, err_p, tot_p = cargar(rp, validar_pista, pista, "pistas")
    vuelos, err_v, tot_v = cargar(rv, validar_vuelo, vuelo, "vuelos")
    motivos = [(v, motivo_no_asignable(v, pistas)) for v in vuelos]
    no_asig = [(v, m) for v, m in motivos if m]
    asignables = [v for v, m in motivos if not m]
    ops = simular(asignables, pistas)
    os.makedirs(sal, exist_ok=True)
    with open(os.path.join(sal, "operaciones.csv"), "w", encoding="utf-8", newline="\n") as f:
        f.write("codigo,aerolinea,operacion,categoria,prioridad,pista,programada,inicio,fin,retraso\n")
        f.writelines(f"{o['cod']},{o['aer']},{o['op']},{o['cat']},{o['pri']},{o['pista']},{hora_texto(o['prog'])},"
                     f"{hora_texto(o['ini'])},{hora_texto(o['fin'])},{o['ret']}\n" for o in ops)
    with open(os.path.join(sal, "errores.csv"), "w", encoding="utf-8", newline="\n") as f:
        f.write("archivo,linea,motivo\n")
        f.writelines(f"{a},{n},{m}\n" for a, n, m in err_p + err_v)
    texto = reporte(tot_p, pistas, err_p, tot_v, vuelos, err_v, ops, no_asig, pistas)
    with open(os.path.join(sal, "reporte.txt"), "w", encoding="utf-8", newline="\n") as f:
        f.write(texto)
    sys.stdout.buffer.write(texto.encode("utf-8"))


main()
