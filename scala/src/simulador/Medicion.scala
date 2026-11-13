package simulador

import java.nio.charset.StandardCharsets
import java.nio.file.{Files, Path}

// =============================================================================
//  MÓDULO 6 · MEDICIÓN (Bloque 3, sección 5)
//  Toma el tiempo de cada etapa con System.nanoTime() y, con --medir, lo escribe en un archivo.
//  Cada etapa devuelve su resultado ya calculado (regla de materialización: Vector, no Iterator ni LazyList).
// =============================================================================
object Medicion:

  val Encabezado = "lectura_ns,validacion_ns,simulacion_ns,reportes_ns,escritura_ns"

  /** Resultado de una etapa y lo que tardó, en nanosegundos. */
  final case class Medido[T](valor: T, ns: Long)

  /** La etapa se recibe "por nombre" (=> T): se evalúa aquí adentro, entre las dos lecturas del reloj. */
  def medir[T](etapa: => T): Medido[T] =
    val inicio = System.nanoTime()
    val valor = etapa
    Medido(valor, System.nanoTime() - inicio)

  /** Archivo de --medir: encabezado y una línea con las cinco duraciones. */
  def escribir(archivo: Path, duraciones: List[Long]): Unit =
    Files.writeString(archivo, s"$Encabezado\n${duraciones.mkString(",")}\n", StandardCharsets.UTF_8)
    ()
