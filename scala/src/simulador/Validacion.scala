package simulador

import scala.util.matching.Regex

import Modelo.si

// =============================================================================
//  MÓDULO 3 · VALIDACIÓN (RF03)
//  Cada registro se convierte en Right(dato) o Left(error). Las reglas se revisan en el orden de las
//  columnas y se reporta solo el primer error (cadena de Option.orElse).
// =============================================================================
object Validacion:

  private val Entero: Regex = "-?[0-9]{1,9}".r
  private val Hora: Regex = "([0-9]{2}):([0-9]{2})".r

  /** Revisión de un registro: error previo a la unicidad y error de sus demás campos. */
  private final case class Revision(registro: Registro, previo: Option[String], deCampos: Option[String]):
    def clave: String = registro.campos(0)

  // ---------- Reglas reutilizables

  private def entero(valor: String, campo: String): Option[String] =
    si(!Entero.matches(valor), s"$campo no es un entero: $valor")

  private def opcion(valor: String, campo: String, opciones: List[String]): Option[String] =
    si(!opciones.contains(valor), s"$campo con valor no válido: $valor (valores: ${opciones.mkString("/")})")

  private def hora(valor: String): Option[String] = valor match
    case Hora(hh, mm) if hh.toInt <= 23 && mm.toInt <= 59 => None
    case _ => Some(s"hora no válida: $valor (formato HH:MM de 00:00 a 23:59)")

  // ---------- Reglas de cada archivo (después del número de campos y la clave)

  private def reglasPista(c: Vector[String]): Option[String] =
    entero(c(1), "longitud")
      .orElse(si(c(1).toInt <= 0, s"longitud debe ser mayor que 0: ${c(1)}"))
      .orElse(opcion(c(2), "uso", Modelo.nombres(Uso.values)))
      .orElse(opcion(c(3), "estado", Modelo.nombres(Estado.values)))

  private def reglasVuelo(c: Vector[String]): Option[String] =
    si(c(1).isEmpty, "aerolínea vacía")
      .orElse(si(c(2).isEmpty, "matrícula vacía"))
      .orElse(opcion(c(3), "categoría", Modelo.nombres(Categoria.values)))
      .orElse(opcion(c(4), "operación", Modelo.nombres(Operacion.values)))
      .orElse(entero(c(5), "día"))
      .orElse(si(c(5).toInt < 1 || c(5).toInt > 9999, s"día debe estar entre 1 y 9999: ${c(5)}"))
      .orElse(hora(c(6)))
      .orElse(opcion(c(7), "prioridad", Modelo.nombres(Prioridad.values)))

  // ---------- Construcción de las entidades (solo con campos ya validados)

  private def construirPista(c: Vector[String]): Pista =
    Pista(c(0), c(1).toInt, Uso.valueOf(c(2)), Estado.valueOf(c(3)))

  private def construirVuelo(c: Vector[String]): Vuelo =
    val minuto = (c(5).toInt - 1) * 1440L + c(6).substring(0, 2).toInt * 60L + c(6).substring(3, 5).toInt
    Vuelo(c(0), c(1), Avion(c(2), Categoria.valueOf(c(3))), Operacion.valueOf(c(4)), minuto,
      Prioridad.valueOf(c(7)))

  // ---------- Validación genérica

  /**
   * Valida todos los registros de un archivo.
   * Unicidad: un registro está "repetido" si un registro VÁLIDO anterior tiene su misma clave.
   * El dueño de cada clave es el primer registro sin errores propios (groupMapReduce con mínimo), así no
   * hace falta recorrer el archivo con estado: el resultado es el mismo que validar línea por línea.
   */
  private def validar[T](registros: Vector[Registro], archivo: String, numCampos: Int, nombreClave: String,
                         reglas: Vector[String] => Option[String],
                         construir: Vector[String] => T): Vector[Resultado[T]] =
    val revisiones = registros.map(revisar(_, numCampos, nombreClave, reglas))
    val duenos: Map[String, Int] = revisiones
      .filter(v => v.previo.isEmpty && v.deCampos.isEmpty)
      .groupMapReduce(_.clave)(_.registro.linea)(_ min _)
    revisiones.map(resultado(_, duenos, archivo, nombreClave, construir))

  private def revisar(r: Registro, numCampos: Int, nombreClave: String,
                      reglas: Vector[String] => Option[String]): Revision =
    val previo = si(r.campos.size != numCampos, s"se esperaban $numCampos campos y hay ${r.campos.size}")
      .orElse(si(r.campos(0).isEmpty, s"$nombreClave vacío"))
    Revision(r, previo, if previo.isDefined then None else reglas(r.campos))

  private def resultado[T](v: Revision, duenos: Map[String, Int], archivo: String, nombreClave: String,
                           construir: Vector[String] => T): Resultado[T] =
    v.previo
      .orElse(si(duenos.getOrElse(v.clave, Int.MaxValue) < v.registro.linea, s"$nombreClave repetido: ${v.clave}"))
      .orElse(v.deCampos)
      .map(m => ErrorRegistro(archivo, v.registro.linea, m))
      .toLeft(construir(v.registro.campos))

  def validarPistas(registros: Vector[Registro]): Vector[Resultado[Pista]] =
    validar(registros, "pistas", 4, "id", reglasPista, construirPista)

  def validarVuelos(registros: Vector[Registro]): Vector[Resultado[Vuelo]] =
    validar(registros, "vuelos", 8, "código", reglasVuelo, construirVuelo)

  // ---------- Separar válidos y errores

  def validos[T](resultados: Vector[Resultado[T]]): Vector[T] =
    resultados.collect { case Right(valor) => valor }

  def errores[T](resultados: Vector[Resultado[T]]): Vector[ErrorRegistro] =
    resultados.collect { case Left(error) => error }
