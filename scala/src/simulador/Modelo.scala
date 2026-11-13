package simulador

// =============================================================================
//  MÓDULO 1 · MODELO
//  Entidades del aeropuerto como datos inmutables (case class) y listas cerradas (enum).
//  Una case class no se modifica: para "cambiar" un dato se crea otra con copy.
// =============================================================================

// ---------- Listas cerradas. El nombre de cada valor es el texto exacto del contrato.

/** Categoría del avión con sus requisitos (RN02). */
enum Categoria(val longitudMinima: Int, val minutosOcupacion: Int):
  case Ligero extends Categoria(1200, 2)
  case Mediano extends Categoria(2000, 3)
  case Pesado extends Categoria(2800, 4)

enum Operacion:
  case Despegue, Aterrizaje

enum Uso:
  case Despegue, Aterrizaje, Mixta

enum Estado:
  case Operativa, Cerrada

enum Prioridad:
  case Normal, Emergencia

// ---------- Entidades del proyecto

final case class Avion(matricula: String, categoria: Categoria)

/** programado: minuto absoluto = (día - 1) * 1440 + HH * 60 + MM. */
final case class Vuelo(codigo: String, aerolinea: String, avion: Avion, operacion: Operacion,
                       programado: Long, prioridad: Prioridad)

final case class Pista(id: String, longitud: Int, uso: Uso, estado: Estado)

/** Resultado de la torre: qué vuelo usa qué pista y cuándo. */
final case class OperacionAsignada(vuelo: Vuelo, pista: Pista, inicio: Long, fin: Long):
  def retraso: Long = inicio - vuelo.programado

final case class NoAsignable(vuelo: Vuelo, motivo: String)

/**
 * Estado de la simulación en un minuto. Es inmutable: cada paso crea uno nuevo.
 * cabezas: posición del primer vuelo pendiente de cada fila; libres: minuto en que se libera cada pista.
 */
final case class Aeropuerto(minuto: Long, cabezas: Vector[Int], libres: Vector[Long],
                            asignadasEnElPaso: Vector[OperacionAsignada])

// ---------- Lectura y validación

/** Una línea de datos del archivo: su número de línea física y sus campos. */
final case class Registro(linea: Int, campos: Vector[String])

final case class ErrorRegistro(archivo: String, linea: Int, motivo: String)

/** Resultado de validar un registro: Left con el error o Right con el dato. */
type Resultado[T] = Either[ErrorRegistro, T]

object Modelo:
  /** Los textos válidos de una lista cerrada, en su orden ("Ligero", "Mediano", "Pesado"). */
  def nombres[T](valores: Array[T]): List[String] = valores.toList.map(_.toString)

  /** Some con el mensaje si la condición se cumple; None si no. */
  def si(condicion: Boolean, mensaje: => String): Option[String] = Option.when(condicion)(mensaje)
