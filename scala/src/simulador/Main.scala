package simulador

import java.nio.charset.StandardCharsets
import java.nio.file.{Files, Path}

// =============================================================================
//  MÓDULO 7 · PROGRAMA PRINCIPAL
//  Revisa los argumentos y encadena las cinco etapas: lectura -> validación -> simulación ->
//  reportes -> escritura. Toda la lógica está en los otros módulos; aquí solo se conectan.
// =============================================================================
object Main:

  private val ModoDeUso =
    "Uso: java -jar simulador-<lenguaje>.jar <pistas.csv> <vuelos.csv> <carpeta_salida> [--medir <archivo>]"

  // ---------- Resultado de cada etapa

  private final case class Lineas(pistas: Vector[String], vuelos: Vector[String])

  private final case class Validados(registrosPistas: Int, pistas: Vector[Pista], erroresPistas: Vector[ErrorRegistro],
                                     registrosVuelos: Int, vuelos: Vector[Vuelo], erroresVuelos: Vector[ErrorRegistro])

  private final case class Simulados(operaciones: Vector[OperacionAsignada], noAsignables: Vector[NoAsignable])

  private final case class Textos(operaciones: String, errores: String, reporte: String)

  // ---------- Etapas

  private def validar(lineas: Lineas): Validados =
    val registrosPistas = Lectura.registros(lineas.pistas)
    val registrosVuelos = Lectura.registros(lineas.vuelos)
    val pistas = Validacion.validarPistas(registrosPistas)
    val vuelos = Validacion.validarVuelos(registrosVuelos)
    Validados(registrosPistas.size, Validacion.validos(pistas), Validacion.errores(pistas),
      registrosVuelos.size, Validacion.validos(vuelos), Validacion.errores(vuelos))

  private def simular(v: Validados): Simulados =
    Simulados(
      TorreControl.simular(TorreControl.asignables(v.vuelos, v.pistas), v.pistas),
      TorreControl.noAsignables(v.vuelos, v.pistas))

  private def reportar(v: Validados, s: Simulados): Textos =
    Textos(
      Reportes.operacionesCsv(s.operaciones),
      Reportes.erroresCsv(v.erroresPistas ++ v.erroresVuelos),
      Reportes.reporte(Reportes.Datos(v.registrosPistas, v.pistas, v.erroresPistas,
        v.registrosVuelos, v.vuelos.size, v.erroresVuelos, s.operaciones, s.noAsignables)))

  private def escribir(salida: Path, t: Textos): Path =
    Files.createDirectories(salida)
    Files.writeString(salida.resolve("operaciones.csv"), t.operaciones, StandardCharsets.UTF_8)
    Files.writeString(salida.resolve("errores.csv"), t.errores, StandardCharsets.UTF_8)
    Files.writeString(salida.resolve("reporte.txt"), t.reporte, StandardCharsets.UTF_8)
    imprimir(t.reporte)
    salida

  /** Escribe en pantalla siempre en UTF-8, sin depender de la configuración regional del equipo. */
  private def imprimir(texto: String): Unit =
    System.out.writeBytes(texto.getBytes(StandardCharsets.UTF_8))
    System.out.flush()

  // ---------- Argumentos

  /** Motivo del error de uso, si lo hay: cantidad de argumentos o archivo de entrada ilegible. */
  private def problemaDeUso(args: Array[String]): Option[String] =
    if !(args.length == 3 || (args.length == 5 && args(3) == "--medir")) then Some("número de argumentos incorrecto")
    else args.take(2).toList
      .find(ruta => !Lectura.sePuedeLeer(Path.of(ruta)))
      .map(ruta => s"no se puede leer el archivo $ruta")

  private def ejecutar(pistas: Path, vuelos: Path, salida: Path, archivoMedicion: Option[Path]): Unit =
    val lectura = Medicion.medir(Lineas(Lectura.leerLineas(pistas), Lectura.leerLineas(vuelos)))
    val validacion = Medicion.medir(validar(lectura.valor))
    val simulacion = Medicion.medir(simular(validacion.valor))
    val reportes = Medicion.medir(reportar(validacion.valor, simulacion.valor))
    val escritura = Medicion.medir(escribir(salida, reportes.valor))
    archivoMedicion.foreach(archivo => Medicion.escribir(archivo,
      List(lectura.ns, validacion.ns, simulacion.ns, reportes.ns, escritura.ns)))

  def main(args: Array[String]): Unit =
    problemaDeUso(args) match
      case Some(motivo) =>
        imprimir(s"ERROR: $motivo\n$ModoDeUso\n")
        sys.exit(2)
      case None =>
        ejecutar(Path.of(args(0)), Path.of(args(1)), Path.of(args(2)), Option.when(args.length == 5)(Path.of(args(4))))
