"""
Generador de escenarios del experimento (Bloque 3).

Crea datos/escenarios/<ID>/vuelos.csv para cada escenario. El aeropuerto es común a todos:
datos/aeropuerto/pistas.csv.

Es determinista: con la misma semilla produce exactamente el mismo archivo, byte a byte. Para no depender
de la versión de Python, solo usa random.random() (estable desde Python 3.2) y hace él mismo las elecciones
con pesos.

Uso:  python3 datos/generador.py            genera todos los escenarios y escribe las huellas SHA-256
      python3 datos/generador.py V1 V2      genera solo los escenarios indicados
"""
import hashlib
import os
import random
import sys

# ----------------------------------------------------------------------------- configuración
#   id: (vuelos, vuelos_por_dia, porcentaje_invalidos, semilla, descripción)
ESCENARIOS = {
    "V1": (1_000, 1_500, 0, 101, "Volumen pequeño"),
    "V2": (10_000, 1_500, 0, 102, "Volumen mediano"),
    "V3": (100_000, 1_500, 0, 103, "Volumen grande"),
    "V4": (1_000_000, 1_500, 0, 104, "Volumen muy grande"),
    "C1": (100_000, 2_400, 0, 201, "Congestión: 60 % más vuelos por día que V3 (aeropuerto saturado)"),
    "X1": (100_000, 1_500, 10, 301, "Errores: 10 % de registros inválidos"),
}

AEROLINEAS = [  # (nombre, prefijo del código, prefijo de matrícula, peso)
    ("Avianca", "AV", "HK", 25), ("LATAM", "LA", "CC", 20), ("Copa", "CM", "HP", 15),
    ("Wingo", "P5", "HK", 10), ("JetSMART", "JA", "CC", 10), ("American", "AA", "N", 8),
    ("Iberia", "IB", "EC", 6), ("Viva", "VH", "HK", 6),
]
CATEGORIAS = [("Ligero", 30), ("Mediano", 50), ("Pesado", 20)]
OPERACIONES = [("Aterrizaje", 50), ("Despegue", 50)]
PORCENTAJE_EMERGENCIAS = 5
ENCABEZADO = "codigo,aerolinea,matricula,categoria,operacion,dia,hora,prioridad"

RAIZ = os.path.dirname(os.path.abspath(__file__))


def elegir(azar, opciones):
    """Elige una opción según su peso (último elemento de cada tupla)."""
    total = sum(o[-1] for o in opciones)
    umbral = azar.random() * total
    acumulado = 0
    for opcion in opciones:
        acumulado += opcion[-1]
        if umbral < acumulado:
            return opcion
    return opciones[-1]


def entero(azar, n):
    """Entero uniforme entre 0 y n-1."""
    return min(int(azar.random() * n), n - 1)


def vuelo_valido(azar, i, por_dia):
    nombre, pref_cod, pref_mat, _ = elegir(azar, AEROLINEAS)
    categoria = elegir(azar, CATEGORIAS)[0]
    operacion = elegir(azar, OPERACIONES)[0]
    prioridad = "Emergencia" if azar.random() * 100 < PORCENTAJE_EMERGENCIAS else "Normal"
    minuto = entero(azar, 1440)
    campos = [f"{pref_cod}{i:07d}", nombre, f"{pref_mat}-{entero(azar, 10_000):04d}", categoria, operacion,
              str(i // por_dia + 1), f"{minuto // 60:02d}:{minuto % 60:02d}", prioridad]
    return campos


def corromper(azar, campos, codigo_anterior):
    """Aplica uno de 10 errores (uno por regla de validación de 02_modelo_y_contrato.md)."""
    c = list(campos)
    tipo = entero(azar, 10)
    if tipo == 0: return c[:7]                                 # falta un campo
    if tipo == 1: c[0] = ""                                    # código vacío
    if tipo == 2: c[0] = codigo_anterior or ""                 # código repetido
    if tipo == 3: c[1] = ""                                    # aerolínea vacía
    if tipo == 4: c[2] = ""                                    # matrícula vacía
    if tipo == 5: c[3] = "Jumbo"                               # categoría no válida
    if tipo == 6: c[4] = "Escala"                              # operación no válida
    if tipo == 7: c[5] = "uno"                                 # día no entero
    if tipo == 8: c[6] = "24:10"                               # hora fuera de rango
    if tipo == 9: c[7] = "Urgente"                             # prioridad no válida
    return c


def generar(id_esc):
    vuelos, por_dia, pct_invalidos, semilla, _ = ESCENARIOS[id_esc]
    azar = random.Random(semilla)
    carpeta = os.path.join(RAIZ, "escenarios", id_esc)
    os.makedirs(carpeta, exist_ok=True)
    ruta = os.path.join(carpeta, "vuelos.csv")
    anterior = None
    with open(ruta, "w", encoding="utf-8", newline="\n") as f:
        f.write(ENCABEZADO + "\n")
        for i in range(1, vuelos + 1):
            campos = vuelo_valido(azar, i, por_dia)
            if pct_invalidos and azar.random() * 100 < pct_invalidos:
                campos = corromper(azar, campos, anterior)
            anterior = campos[0] if campos and campos[0] else anterior
            f.write(",".join(campos) + "\n")
    return ruta


def huella(ruta):
    h = hashlib.sha256()
    with open(ruta, "rb") as f:
        for bloque in iter(lambda: f.read(1 << 20), b""):
            h.update(bloque)
    return h.hexdigest()


def main():
    ids = sys.argv[1:] or list(ESCENARIOS)
    lineas = []
    for id_esc in ids:
        ruta = generar(id_esc)
        lineas.append(f"{huella(ruta)}  escenarios/{id_esc}/vuelos.csv")
        print(f"{id_esc}: {ESCENARIOS[id_esc][0]:>9,} vuelos  ->  {os.path.relpath(ruta, RAIZ)}")
    if not sys.argv[1:]:
        with open(os.path.join(RAIZ, "escenarios", "huellas.sha256"), "w", encoding="utf-8", newline="\n") as f:
            f.write("\n".join(lineas) + "\n")
        print("Huellas en datos/escenarios/huellas.sha256  (verificar: cd datos && shasum -a 256 -c escenarios/huellas.sha256)")


if __name__ == "__main__":
    main()
