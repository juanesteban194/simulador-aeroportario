"""
Interfaz gráfica del simulador · servidor local (solo biblioteca estándar de Python).

Ejecuta DE VERDAD el programa del lenguaje elegido (los mismos .jar del experimento, o la implementación de
referencia en Python) sobre un escenario o sobre datos propios, y entrega a la página todo lo que produjo:
las entradas, operaciones.csv, errores.csv, reporte.txt, lo que salió en pantalla y los tiempos de --medir.
La página (interfaz/index.html) reproduce esa ejecución paso a paso.

Uso:  python3 interfaz/servidor.py [--puerto 8765] [--sin-navegador]
      también: bash simular.sh interfaz   o   «Simular · interfaz gráfica» en IntelliJ
Escucha solo en 127.0.0.1. Las salidas quedan en salida/interfaz/<lenguaje>/<escenario>/.
"""
import json
import os
import signal
import socket
import subprocess
import sys
import threading
import time
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

RAIZ = Path(__file__).resolve().parent.parent
PAGINA = RAIZ / "interfaz" / "index.html"
# Tipografías incluidas en el repositorio (licencia SIL OFL 1.1): la página no depende de internet.
FUENTES = {"/fuentes/inter.woff2": "inter.woff2", "/fuentes/jetbrains-mono.woff2": "jetbrains-mono.woff2"}
SALIDA = RAIZ / "salida" / "interfaz"
ARCHIVOS = ("operaciones.csv", "errores.csv", "reporte.txt")
ETAPAS = ("lectura", "validacion", "simulacion", "reportes", "escritura")
LENGUAJES = {"java": "Java", "scala": "Scala", "clojure": "Clojure", "python": "Python (referencia)"}
HERRAMIENTA = {"java": "javac", "scala": "scala-cli", "clojure": "lein"}
LIMITE_PROPIO = 5_000_000          # bytes por archivo de datos propios
CANDADO = threading.Lock()         # una ejecución a la vez: las salidas comparten carpeta

# Escenarios que se pueden animar. V4 (1.000.000 de vuelos) se deja fuera: es demasiado para el navegador.
ESCENARIOS = {
    "E0": ("Ejemplo resuelto a mano", "datos/ejemplo/pistas.csv", "datos/ejemplo/vuelos.csv", "datos/ejemplo/esperado"),
    "V1": ("Volumen · 1.000 vuelos", "datos/aeropuerto/pistas.csv", "datos/escenarios/V1/vuelos.csv", "datos/escenarios/V1/esperado"),
    "V2": ("Volumen · 10.000 vuelos", "datos/aeropuerto/pistas.csv", "datos/escenarios/V2/vuelos.csv", "datos/escenarios/V2/esperado"),
    "V3": ("Volumen · 100.000 vuelos", "datos/aeropuerto/pistas.csv", "datos/escenarios/V3/vuelos.csv", "datos/escenarios/V3/esperado"),
    "C1": ("Congestión · 100.000 vuelos", "datos/aeropuerto/pistas.csv", "datos/escenarios/C1/vuelos.csv", "datos/escenarios/C1/esperado"),
    "X1": ("Errores · 100.000 vuelos, 10 % inválidos", "datos/aeropuerto/pistas.csv", "datos/escenarios/X1/vuelos.csv", "datos/escenarios/X1/esperado"),
}


def entorno():
    """Variables para los programas: sin JAVA_TOOL_OPTIONS, que agrega texto a la salida de error."""
    variables = dict(os.environ)
    variables.pop("JAVA_TOOL_OPTIONS", None)
    return variables


def en_entorno(argumentos):
    """Ejecuta un comando con el PATH de herramientas/entorno.sh (Homebrew y JDK 21 en macOS)."""
    return subprocess.run(["bash", "-c", 'source "$0/herramientas/entorno.sh"; exec "$@"', str(RAIZ), *argumentos],
                          capture_output=True, env=entorno())


def existe_comando(nombre):
    return en_entorno(["bash", "-c", f"command -v {nombre}"]).returncode == 0


def relativa(ruta):
    ruta = Path(ruta)
    return str(ruta.relative_to(RAIZ)) if ruta.is_relative_to(RAIZ) else str(ruta)


def contar_lineas(ruta):
    with open(ruta, "rb") as f:
        return sum(bloque.count(b"\n") for bloque in iter(lambda: f.read(1 << 20), b""))


def jar(lenguaje):
    return RAIZ / lenguaje / f"simulador-{lenguaje}.jar"


def desactualizado(lenguaje):
    """El .jar falta o algún fuente es más nuevo (la misma regla que simular.sh)."""
    if not jar(lenguaje).exists():
        return True
    limite = jar(lenguaje).stat().st_mtime
    fuentes = list((RAIZ / lenguaje / "src").rglob("*")) + list((RAIZ / lenguaje).glob("project.*"))
    return any(f.is_file() and f.stat().st_mtime > limite for f in fuentes)


def info():
    java = existe_comando("java")
    lenguajes = []
    for clave, nombre in LENGUAJES.items():
        if clave == "python":
            lenguajes.append({"id": clave, "nombre": nombre, "disponible": True, "nota": sys.version.split()[0]})
            continue
        construible = existe_comando(HERRAMIENTA[clave])
        listo = java and (jar(clave).exists() or construible)
        nota = "" if listo else ("falta java (JDK 21)" if not java else f"falta {HERRAMIENTA[clave]} para construirlo")
        lenguajes.append({"id": clave, "nombre": nombre, "disponible": listo, "nota": nota})
    escenarios = []
    for clave, (titulo, _, vuelos, _) in ESCENARIOS.items():
        ruta = RAIZ / vuelos
        escenarios.append({"id": clave, "titulo": titulo, "disponible": ruta.exists(),
                           "vuelos": contar_lineas(ruta) - 1 if ruta.exists() else 0})
    return {"lenguajes": lenguajes, "escenarios": escenarios, "raiz": str(RAIZ)}


def preparar(lenguaje):
    """Construye el .jar si hace falta. Devuelve (error, registro de la construcción)."""
    if lenguaje == "python" or not desactualizado(lenguaje):
        return None, ""
    if not existe_comando(HERRAMIENTA[lenguaje]):
        return f"hay que construir {lenguaje} y no se encontró {HERRAMIENTA[lenguaje]}", ""
    r = en_entorno(["bash", str(RAIZ / lenguaje / "construir.sh")])
    registro = (r.stdout + r.stderr).decode("utf-8", "replace")
    return (None if r.returncode == 0 else f"no se pudo construir la versión {lenguaje}"), registro


def comando(lenguaje, pistas, vuelos, salida, medicion):
    if lenguaje == "python":
        return [sys.executable, str(RAIZ / "experimento" / "referencia.py"), str(pistas), str(vuelos), str(salida)]
    return ["java", "-Xmx4g", "-XX:+UseG1GC", "-jar", str(jar(lenguaje)),
            str(pistas), str(vuelos), str(salida), "--medir", str(medicion)]


def leer(ruta):
    return ruta.read_text(encoding="utf-8", errors="replace") if ruta.exists() else ""


def atender(pedido):
    lenguaje = pedido.get("lenguaje")
    if lenguaje not in LENGUAJES:
        return 400, {"error": f"lenguaje desconocido: {lenguaje}"}
    escenario = pedido.get("escenario")
    if escenario == "propio":
        textos = [pedido.get("pistas"), pedido.get("vuelos")]
        if not all(isinstance(t, str) and len(t.encode("utf-8")) <= LIMITE_PROPIO for t in textos):
            return 400, {"error": "los datos propios deben ser texto de 5 MB o menos por archivo"}
        entrada = SALIDA / "entrada_propia"
        entrada.mkdir(parents=True, exist_ok=True)
        pistas, vuelos, esperado = entrada / "pistas.csv", entrada / "vuelos.csv", None
        pistas.write_bytes(textos[0].encode("utf-8"))
        vuelos.write_bytes(textos[1].encode("utf-8"))
        titulo = "Datos propios"
    elif escenario in ESCENARIOS:
        titulo, p, v, e = ESCENARIOS[escenario]
        pistas, vuelos, esperado = RAIZ / p, RAIZ / v, RAIZ / e
        if not vuelos.exists():
            return 400, {"error": f"el escenario {escenario} no está generado: python3 datos/generador.py {escenario}"}
    else:
        return 400, {"error": f"escenario desconocido: {escenario}"}

    salida = SALIDA / lenguaje / escenario
    medicion = SALIDA / lenguaje / f"{escenario}.medicion.csv"
    with CANDADO:
        error, registro = preparar(lenguaje)
        if error:
            return 500, {"error": error, "construccion": registro}
        salida.mkdir(parents=True, exist_ok=True)
        for f in [*(salida / a for a in ARCHIVOS), medicion]:
            if f.exists():
                f.unlink()
        cmd = comando(lenguaje, pistas, vuelos, salida, medicion)
        inicio = time.perf_counter()
        r = en_entorno(cmd)
        segundos = time.perf_counter() - inicio

    etapas = None
    if medicion.exists():
        valores = medicion.read_text().splitlines()[1].split(",")
        etapas = dict(zip(ETAPAS, (int(x) for x in valores)))
    reporte = salida / "reporte.txt"
    coincide = None
    if r.returncode == 0 and esperado is not None and esperado.is_dir():
        coincide = all((salida / a).read_bytes() == (esperado / a).read_bytes() for a in ARCHIVOS)
    return 200, {
        "lenguaje": lenguaje, "nombreLenguaje": LENGUAJES[lenguaje],
        "escenario": escenario, "titulo": titulo,
        "comando": " ".join(["python3" if c == sys.executable else relativa(c) for c in cmd]),
        "codigo": r.returncode,
        "segundos": segundos,
        "etapasNs": etapas,
        "construccion": registro,
        "rutas": {"pistas": relativa(pistas), "vuelos": relativa(vuelos), "salida": relativa(salida)},
        "entrada": {"pistas": leer(pistas), "vuelos": leer(vuelos)},
        "salida": {a: leer(salida / a) for a in ARCHIVOS},
        "tamanos": {a: (salida / a).stat().st_size for a in ARCHIVOS if (salida / a).exists()},
        "pantalla": r.stdout.decode("utf-8", "replace"),
        "errorEstandar": r.stderr.decode("utf-8", "replace"),
        "pantallaIgualReporte": reporte.exists() and r.stdout == reporte.read_bytes(),
        "coincideEsperado": coincide,
    }


class Manejador(BaseHTTPRequestHandler):
    def log_message(self, formato, *args):
        sys.stderr.write("  " + (formato % args) + "\n")

    def responder(self, codigo, cuerpo, tipo):
        self.send_response(codigo)
        self.send_header("Content-Type", tipo)
        self.send_header("Content-Length", str(len(cuerpo)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(cuerpo)

    def json(self, codigo, objeto):
        self.responder(codigo, json.dumps(objeto, ensure_ascii=False).encode("utf-8"), "application/json; charset=utf-8")

    def origen_valido(self):
        """Solo se aceptan pedidos de la propia página (evita que otro sitio lance ejecuciones)."""
        origen = self.headers.get("Origin")
        return origen is None or origen == f"http://{self.headers.get('Host')}"

    def do_GET(self):
        ruta = urlparse(self.path)
        if ruta.path in ("/", "/index.html"):
            self.responder(200, PAGINA.read_bytes(), "text/html; charset=utf-8")
        elif ruta.path in FUENTES:
            self.responder(200, (RAIZ / "interfaz" / "fuentes" / FUENTES[ruta.path]).read_bytes(), "font/woff2")
        elif ruta.path == "/api/info":
            self.json(200, info())
        elif ruta.path == "/api/entrada":
            escenario = parse_qs(ruta.query).get("escenario", [""])[0]
            if escenario not in ESCENARIOS or not (RAIZ / ESCENARIOS[escenario][2]).exists():
                self.json(404, {"error": f"escenario no disponible: {escenario}"})
            else:
                _, p, v, _ = ESCENARIOS[escenario]
                self.json(200, {"pistas": leer(RAIZ / p), "vuelos": leer(RAIZ / v)})
        else:
            self.json(404, {"error": "no existe"})

    def do_POST(self):
        largo = int(self.headers.get("Content-Length") or 0)
        if self.path != "/api/ejecutar" or not self.origen_valido():
            self.json(404, {"error": "no existe"})
        elif largo > 2 * LIMITE_PROPIO + 100_000:
            self.json(413, {"error": "datos demasiado grandes"})
        else:
            codigo, respuesta = atender(json.loads(self.rfile.read(largo) or b"{}"))
            self.json(codigo, respuesta)


def puerto_en_uso(puerto):
    with socket.socket() as s:
        return s.connect_ex(("127.0.0.1", puerto)) == 0


def cerrar(*_):
    print("\nInterfaz cerrada.", flush=True)
    os._exit(0)


def main():
    argumentos = sys.argv[1:]
    puerto = int(argumentos[argumentos.index("--puerto") + 1]) if "--puerto" in argumentos else 8765
    puerto = next(p for p in range(puerto, puerto + 50) if not puerto_en_uso(p))
    servidor = ThreadingHTTPServer(("127.0.0.1", puerto), Manejador)
    url = f"http://127.0.0.1:{puerto}/"
    signal.signal(signal.SIGINT, cerrar)
    signal.signal(signal.SIGTERM, cerrar)
    print(f"Interfaz gráfica del simulador: {url}", flush=True)
    print("Ejecuta los .jar reales (o la referencia en Python). Ciérrala con Ctrl+C o con el botón de parar.", flush=True)
    if "--sin-navegador" not in argumentos:
        threading.Timer(0.7, webbrowser.open, [url]).start()
    servidor.serve_forever()


if __name__ == "__main__":
    main()
