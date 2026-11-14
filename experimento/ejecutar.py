#!/usr/bin/env python3
"""
=============================================================================
 Orquestador del experimento (Bloque 6): ejecuta el protocolo de docs/03_experimento.md, sección 6.

   1. Construye los tres .jar.
   2. Registra el entorno en resultados/entorno.txt.
   3. Regenera los escenarios grandes y comprueba las huellas SHA-256.
   4. Verifica la equivalencia (experimento/verificar.sh) y guarda resultados/verificacion.csv.
   5. Mide: 1 ronda de calentamiento + 10 rondas, orden de lenguajes rotado, un proceso nuevo por ejecución.
   6. Guarda una fila por ejecución en resultados/crudos/<escenario>.csv.
   7. Escribe resultados/resumen.md con la mediana, el mínimo, el máximo y el rango intercuartílico.

 Uso (desde la raíz del repositorio, en la app Terminal y con IntelliJ cerrado):
   python3 experimento/ejecutar.py            medición completa (unos 20 minutos)
   python3 experimento/ejecutar.py --prueba   1 ronda de V1 y V2 para comprobar que todo funciona;
                                              guarda en resultados/prueba/

 Solo usa la biblioteca estándar de Python.
=============================================================================
"""
import argparse
import csv
import datetime
import hashlib
import os
import platform
import shutil
import statistics
import subprocess
import sys
import tempfile
import time
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
LENGUAJES = ["java", "scala", "clojure"]
INICIAL = {"java": "J", "scala": "S", "clojure": "C"}
ESCENARIOS = ["V1", "V2", "V3", "V4", "C1", "X1"]
GRANDES = ["V3", "V4", "C1", "X1"]           # no están en el repositorio: se regeneran
OPCIONES_JVM = ["-Xmx4g", "-XX:+UseG1GC"]
ARCHIVOS = ["operaciones.csv", "errores.csv", "reporte.txt"]
PISTAS = RAIZ / "datos" / "aeropuerto" / "pistas.csv"
PAUSA_S = 1.0
ENCABEZADO = ["lenguaje", "escenario", "ronda", "orden", "vuelos", "t_lectura_ms", "t_validacion_ms",
              "t_simulacion_ms", "t_reportes_ms", "t_escritura_ms", "t_operaciones_ms", "t_proceso_ms",
              "memoria_max_mb", "codigo_salida", "salida_correcta"]


# ---------------------------------------------------------------- utilidades

def paso(texto):
    print(f"\n==> {texto}", flush=True)


def detener(texto):
    print(f"\nERROR: {texto}", flush=True)
    sys.exit(1)


def entorno_comun():
    """El mismo entorno de los scripts .sh: Homebrew y JDK 21 en el PATH (herramientas/entorno.sh)."""
    salida = subprocess.run(["bash", "-c", 'source "$1" && env -0', "_", str(RAIZ / "herramientas" / "entorno.sh")],
                            capture_output=True, check=True).stdout
    env = dict(par.split("=", 1) for par in salida.decode().split("\0") if "=" in par)
    env.pop("JAVA_TOOL_OPTIONS", None)   # la JVM lo anunciaría en stderr
    return env


def comando(args, env):
    """Salida de un comando informativo, o 'no disponible'."""
    if shutil.which(args[0], path=(env or os.environ).get("PATH")) is None:
        return "no disponible"
    resultado = subprocess.run(args, capture_output=True, text=True, env=env)
    texto = (resultado.stdout + resultado.stderr).strip()
    return texto if resultado.returncode == 0 and texto else "no disponible"


def cambios_sin_guardar(env):
    """¿Hay cambios en el código que no están en un commit? (los resultados no cuentan)"""
    estado = subprocess.run(["git", "-C", str(RAIZ), "status", "--porcelain", "--", ".", ":!resultados"],
                            capture_output=True, text=True, env=env).stdout
    return bool(estado.strip())


def sha256(ruta):
    return hashlib.sha256(Path(ruta).read_bytes()).hexdigest()


def contar_vuelos(ruta):
    """Registros del archivo de vuelos: líneas no vacías sin el encabezado (mismo criterio que el contrato)."""
    espacios = bytes(range(33))   # trim de la JVM: caracteres <= U+0020
    return sum(1 for linea in Path(ruta).read_bytes().split(b"\n")[1:] if linea.strip(espacios))


def memoria_mb(rusage):
    """ru_maxrss viene en bytes en macOS y en KB en Linux."""
    bytes_ = rusage.ru_maxrss if sys.platform == "darwin" else rusage.ru_maxrss * 1024
    return bytes_ / (1024 * 1024)


# ---------------------------------------------------------------- 1. construir

def construir(lenguajes, env, carpeta):
    paso("1. Construcción de los .jar")
    for lenguaje in lenguajes:
        registro = carpeta / f"construccion_{lenguaje}.log"
        inicio = time.perf_counter()
        resultado = subprocess.run(["bash", str(RAIZ / lenguaje / "construir.sh")], capture_output=True, env=env)
        registro.write_bytes(resultado.stdout + resultado.stderr)
        jar = RAIZ / lenguaje / f"simulador-{lenguaje}.jar"
        if resultado.returncode != 0 or not jar.exists():
            detener(f"no se pudo construir {lenguaje}; detalle en {registro.relative_to(RAIZ)}")
        print(f"    {lenguaje:8} {jar.stat().st_size / 1024:9.0f} KB  ({time.perf_counter() - inicio:.0f} s)")


# ---------------------------------------------------------------- 2. entorno

def condiciones_del_equipo():
    """Fuente de energía y modo de bajo consumo (solo macOS)."""
    if sys.platform != "darwin":
        return "no aplica (no es macOS)", "no aplica (no es macOS)"
    bateria = comando(["pmset", "-g", "batt"], None).splitlines()
    energia = "cargador" if bateria and "AC Power" in bateria[0] else "batería"
    ajustes = comando(["pmset", "-g"], None)
    bajo = next((linea.split()[-1] for linea in ajustes.splitlines() if "lowpowermode" in linea), "0")
    return energia, "activado" if bajo == "1" else "desactivado"


def registrar_entorno(env, carpeta, args):
    paso("2. Registro del entorno")
    energia, bajo_consumo = condiciones_del_equipo()
    if sys.platform == "darwin":
        equipo = [
            ("Modelo", comando(["sysctl", "-n", "hw.model"], None)),
            ("Chip", comando(["sysctl", "-n", "machdep.cpu.brand_string"], None)),
            ("Núcleos (rendimiento / eficiencia)",
             f'{comando(["sysctl", "-n", "hw.perflevel0.physicalcpu"], None)} / '
             f'{comando(["sysctl", "-n", "hw.perflevel1.physicalcpu"], None)}'),
            ("Memoria", f'{int(comando(["sysctl", "-n", "hw.memsize"], None)) / 1024 ** 3:.0f} GB'),
            ("Sistema", " ".join(comando(["sw_vers", "-" + c], None) for c in ["productName", "productVersion",
                                                                              "buildVersion"])),
            ("Carga del sistema al empezar", comando(["sysctl", "-n", "vm.loadavg"], None)),
        ]
    else:
        equipo = [("Sistema", platform.platform()), ("Procesador", platform.processor() or platform.machine()),
                  ("Núcleos", str(os.cpu_count()))]
    scala = next((l.split()[-1] for l in (RAIZ / "scala" / "project.scala").read_text().splitlines()
                  if l.startswith("//> using scala")), "?")
    clojure = next((l.split('"')[1] for l in (RAIZ / "clojure" / "project.clj").read_text().splitlines()
                    if "org.clojure/clojure" in l), "?")
    lineas = [
        "ENTORNO DEL EXPERIMENTO",
        f"Fecha: {datetime.datetime.now().astimezone().isoformat(timespec='seconds')}",
        f"Modo: {'prueba' if args.prueba else 'medición completa'}",
        "",
        "== Equipo ==",
        *[f"{nombre}: {valor}" for nombre, valor in equipo],
        f"Energía: {energia}",
        f"Modo de bajo consumo: {bajo_consumo}",
        "",
        "== Software ==",
        f"Java: {' | '.join(comando(['java', '-version'], env).splitlines())}",
        f"Opciones de la JVM: {' '.join(OPCIONES_JVM)}",
        f"Scala: {scala} (project.scala) | {' | '.join(comando(['scala-cli', 'version'], env).splitlines())}",
        f"Clojure: {clojure} (project.clj) | {comando(['lein', 'version'], env)}",
        f"Python (orquestador e implementación de referencia): {platform.python_version()}",
        f"Commit: {comando(['git', '-C', str(RAIZ), 'rev-parse', '--short', 'HEAD'], env)}"
        f"{' (con cambios sin guardar)' if cambios_sin_guardar(env) else ''}",
        "",
        "== Protocolo ==",
        f"Escenarios: {', '.join(args.escenarios)}",
        f"Rondas: {args.calentamiento} de calentamiento (ronda 0, no cuenta) + {args.rondas} medidas",
        f"Orden de los lenguajes rotado por ronda; {PAUSA_S:.0f} s de pausa entre ejecuciones; un proceso nuevo por ejecución",
    ]
    (carpeta / "entorno.txt").write_text("\n".join(lineas) + "\n", encoding="utf-8")
    print("\n".join("    " + l for l in lineas[4:12]))
    avisos = [a for a, mal in [("el Mac está usando la batería: conéctalo al cargador", energia == "batería"),
                               ("el modo de bajo consumo está activado: desactívalo", bajo_consumo == "activado")]
              if mal]
    if avisos and not args.prueba and not args.forzar:
        detener("; ".join(avisos) + ". (Para medir de todos modos: --forzar; quedará registrado.)")
    for aviso in avisos:
        print(f"    AVISO: {aviso}")


# ---------------------------------------------------------------- 3. datos

def preparar_datos(escenarios, env):
    paso("3. Datos: escenarios, huellas y salidas esperadas")
    faltan = [e for e in escenarios if e in GRANDES and not (RAIZ / "datos" / "escenarios" / e / "vuelos.csv").exists()]
    if faltan:
        print(f"    generando {', '.join(faltan)}...", flush=True)
        subprocess.run([sys.executable, str(RAIZ / "datos" / "generador.py"), *faltan], check=True,
                       capture_output=True, env=env)
    lineas = (RAIZ / "datos" / "escenarios" / "huellas.sha256").read_text().splitlines()
    huellas = {ruta: huella for huella, ruta in (l.split("  ", 1) for l in lineas if l.strip())}
    for e in escenarios:
        ruta = RAIZ / "datos" / "escenarios" / e / "vuelos.csv"
        if sha256(ruta) != huellas[f"escenarios/{e}/vuelos.csv"]:
            detener(f"la huella de {e} no coincide: el archivo no es el del experimento")
        esperado = ruta.parent / "esperado"
        if not (esperado / "reporte.txt").exists():
            print(f"    salida esperada de {e} (implementación de referencia)...", flush=True)
            subprocess.run([sys.executable, str(RAIZ / "experimento" / "referencia.py"), str(PISTAS), str(ruta),
                            str(esperado)], check=True, stdout=subprocess.DEVNULL, env=env)
        print(f"    {e}: huella correcta, {contar_vuelos(ruta):>9,} vuelos".replace(",", "."))


# ---------------------------------------------------------------- 4. equivalencia

def verificar(lenguajes, env, carpeta):
    paso("4. Verificación de equivalencia (verificar.sh)")
    archivo = carpeta / "verificacion.csv"
    resultado = subprocess.run(["bash", str(RAIZ / "experimento" / "verificar.sh"), *lenguajes],
                               env={**env, "SIN_CONSTRUIR": "1", "RESULTADOS_CSV": str(archivo)},
                               capture_output=True, text=True)
    tabla = resultado.stdout[resultado.stdout.find("\ncaso"):].strip()
    print("\n".join("    " + l for l in tabla.splitlines()))
    with open(archivo, encoding="utf-8") as f:
        return {(fila["caso"], fila["lenguaje"]): fila["resultado"] == "ok" for fila in csv.DictReader(f)}


# ---------------------------------------------------------------- 5 y 6. medición

def ejecutar_una_vez(lenguaje, vuelos, salida, archivo_medicion, env):
    """Un proceso nuevo; devuelve (código, t_proceso_ms, memoria_mb, stderr)."""
    shutil.rmtree(salida, ignore_errors=True)
    archivo_medicion.unlink(missing_ok=True)
    java = str(Path(env["JAVA_HOME"]) / "bin" / "java") if "JAVA_HOME" in env else "java"
    args = [java, *OPCIONES_JVM, "-jar", str(RAIZ / lenguaje / f"simulador-{lenguaje}.jar"),
            str(PISTAS), str(vuelos), str(salida), "--medir", str(archivo_medicion)]
    with tempfile.TemporaryFile() as errores:
        inicio = time.perf_counter_ns()
        proceso = subprocess.Popen(args, stdout=subprocess.DEVNULL, stderr=errores, env=env)
        _, estado, rusage = os.wait4(proceso.pid, 0)
        t_proceso = (time.perf_counter_ns() - inicio) / 1e6
        proceso.returncode = os.waitstatus_to_exitcode(estado)
        errores.seek(0)
        return proceso.returncode, t_proceso, memoria_mb(rusage), errores.read().decode(errors="replace")


def medir(escenario, lenguajes, primera, ultima, env, carpeta, tmp, correctos):
    """Rondas de primera a ultima; la ronda 0 es el calentamiento."""
    ruta = RAIZ / "datos" / "escenarios" / escenario / "vuelos.csv"
    vuelos = contar_vuelos(ruta)
    esperados = {a: sha256(ruta.parent / "esperado" / a) for a in ARCHIVOS}
    medibles = [l for l in lenguajes if correctos.get((escenario, l), False)]
    for l in sorted(set(lenguajes) - set(medibles)):
        print(f"    {escenario}: {l} no se mide (no coincide con la salida esperada)")
    with open(carpeta / "crudos" / f"{escenario}.csv", "w", newline="", encoding="utf-8") as f:
        escritor = csv.writer(f)
        escritor.writerow(ENCABEZADO)
        for ronda in range(primera, ultima + 1):
            desplazamiento = ronda % len(LENGUAJES)
            orden = [l for l in LENGUAJES[desplazamiento:] + LENGUAJES[:desplazamiento] if l in medibles]
            for posicion, lenguaje in enumerate(orden, start=1):
                codigo, t_proceso, memoria, stderr = ejecutar_una_vez(
                    lenguaje, ruta, tmp / "salida", tmp / "medicion.csv", env)
                etapas = [0.0] * 5
                if codigo == 0 and (tmp / "medicion.csv").exists():
                    valores = (tmp / "medicion.csv").read_text().splitlines()[1].split(",")
                    etapas = [int(v) / 1e6 for v in valores]
                correcta = (codigo == 0 and not stderr.strip()
                            and all((tmp / "salida" / a).exists() and sha256(tmp / "salida" / a) == esperados[a]
                                    for a in ARCHIVOS))
                escritor.writerow([lenguaje, escenario, ronda, posicion, vuelos, *[f"{t:.3f}" for t in etapas],
                                   f"{sum(etapas[1:4]):.3f}", f"{t_proceso:.3f}", f"{memoria:.1f}", codigo,
                                   "si" if correcta else "no"])
                f.flush()
                print(f"    {escenario} ronda {ronda:>2} {INICIAL[lenguaje]}{posicion}  {lenguaje:8}"
                      f"{t_proceso / 1000:7.2f} s {memoria:7.0f} MB  {'ok' if correcta else 'FALLA'}"
                      f"{'  (calentamiento)' if ronda == 0 else ''}", flush=True)
                time.sleep(PAUSA_S)


# ---------------------------------------------------------------- 7. resumen

def resumen(escenarios, carpeta):
    paso("7. Resumen")
    lineas = ["# Resumen de la medición", "",
              "Mediana de las rondas medidas (sin el calentamiento). Entre corchetes: mínimo – máximo; "
              "RIC = rango intercuartílico. Detalle por ejecución en `crudos/`.", ""]
    for escenario in escenarios:
        with open(carpeta / "crudos" / f"{escenario}.csv", encoding="utf-8") as f:
            filas = [fila for fila in csv.DictReader(f) if fila["ronda"] != "0"]
        lineas += [f"## {escenario} · {int(filas[0]['vuelos']):,} vuelos".replace(",", ".") if filas else f"## {escenario}",
                   "",
                   "| Lenguaje | t_operaciones (ms) | t_proceso (ms) | Vuelos/s | Memoria máx. (MB) | Correctas |",
                   "|---|---|---|---|---|---|"]
        for lenguaje in LENGUAJES:
            suyas = [f for f in filas if f["lenguaje"] == lenguaje]
            if not suyas:
                lineas.append(f"| {lenguaje} | no medido | | | | |")
                continue

            def describir(valores, decimales=0):
                cuartiles = statistics.quantiles(valores, n=4, method="inclusive") if len(valores) > 1 else [0, 0, 0]
                return (f"{statistics.median(valores):.{decimales}f} [{min(valores):.{decimales}f} – "
                        f"{max(valores):.{decimales}f}] RIC {cuartiles[2] - cuartiles[0]:.{decimales}f}")

            operaciones = [float(f["t_operaciones_ms"]) for f in suyas]
            proceso = [float(f["t_proceso_ms"]) for f in suyas]
            rendimiento = [int(f["vuelos"]) / (float(f["t_proceso_ms"]) / 1000) for f in suyas]
            memoria = [float(f["memoria_max_mb"]) for f in suyas]
            correctas = sum(f["salida_correcta"] == "si" for f in suyas)
            lineas.append(f"| {lenguaje} | {describir(operaciones)} | {describir(proceso)} | {describir(rendimiento)} "
                          f"| {describir(memoria)} | {correctas}/{len(suyas)} |")
        lineas.append("")
    texto = "\n".join(lineas)
    (carpeta / "resumen.md").write_text(texto, encoding="utf-8")
    print(texto)


# ---------------------------------------------------------------- principal

def main():
    analizador = argparse.ArgumentParser(description="Orquestador del experimento (Bloque 6)")
    analizador.add_argument("--prueba", action="store_true", help="1 ronda de V1 y V2, en resultados/prueba/")
    analizador.add_argument("--forzar", action="store_true", help="medir aunque el Mac use batería o bajo consumo")
    analizador.add_argument("--sin-construir", action="store_true", help="usar los .jar que ya existen")
    analizador.add_argument("--lenguajes", default=",".join(LENGUAJES))
    args = analizador.parse_args()
    args.escenarios = ["V1", "V2"] if args.prueba else ESCENARIOS
    args.calentamiento, args.rondas = (0, 1) if args.prueba else (1, 10)
    lenguajes = [l for l in args.lenguajes.split(",") if l]

    carpeta = RAIZ / "resultados" / ("prueba" if args.prueba else "")
    (carpeta / "crudos").mkdir(parents=True, exist_ok=True)
    env = entorno_comun()
    inicio = time.time()

    if not args.sin_construir:
        construir(lenguajes, env, carpeta)
    registrar_entorno(env, carpeta, args)
    preparar_datos(args.escenarios, env)
    correctos = verificar(lenguajes, env, carpeta)

    paso("5. Medición")
    with tempfile.TemporaryDirectory() as tmp:
        for escenario in args.escenarios:
            medir(escenario, lenguajes, 1 - args.calentamiento, args.rondas, env, carpeta, Path(tmp), correctos)

    resumen(args.escenarios, carpeta)
    print(f"\nListo en {(time.time() - inicio) / 60:.1f} min. Resultados en {carpeta.relative_to(RAIZ)}/")


if __name__ == "__main__":
    main()
