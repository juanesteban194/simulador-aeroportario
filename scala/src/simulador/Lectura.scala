package simulador

import java.nio.charset.StandardCharsets
import java.nio.file.{Files, Path}

// =============================================================================
//  MÓDULO 2 · LECTURA
//  Archivo -> líneas -> registros (número de línea + campos). Solo transforma texto.
// =============================================================================
object Lectura:

  /** ¿Existe el archivo y se puede leer? (se revisa antes de leer, para no depender de excepciones) */
  def sePuedeLeer(ruta: Path): Boolean =
    Files.isRegularFile(ruta) && Files.isReadable(ruta)

  /** Todas las líneas del archivo. Un byte UTF-8 inválido se convierte en U+FFFD, sin error. */
  def leerLineas(ruta: Path): Vector[String] =
    new String(Files.readAllBytes(ruta), StandardCharsets.UTF_8).split("\n", -1).toVector

  /**
   * Registros de datos: se salta el encabezado (línea 1) y las líneas vacías.
   * split(",", -1) conserva los campos vacíos del final; trim es el de la JVM.
   */
  def registros(lineas: Vector[String]): Vector[Registro] =
    lineas.indices
      .drop(1)
      .filter(i => lineas(i).trim.nonEmpty)
      .map(i => Registro(i + 1, lineas(i).split(",", -1).toVector.map(_.trim)))
      .toVector
