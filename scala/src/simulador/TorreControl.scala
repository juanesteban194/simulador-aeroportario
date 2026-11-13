package simulador

import scala.annotation.tailrec

import Modelo.si

// =============================================================================
//  MÓDULO 4 · TORRE DE CONTROL (RF04, RF05, RF06)
//  Funciones puras: reciben un Aeropuerto y devuelven uno nuevo. No guardan estado.
// =============================================================================
object TorreControl:

  /** Un vuelo listo para operar y la pista libre que le tocaría. */
  private final case class Candidato(fila: Int, pista: Int, vuelo: Vuelo)

  /** RN05: emergencia, luego aterrizaje, luego hora programada, luego código. */
  private val prioridad: Ordering[Vuelo] = Ordering.by((v: Vuelo) =>
    (if v.prioridad == Prioridad.Emergencia then 0 else 1,
     if v.operacion == Operacion.Aterrizaje then 0 else 1,
     v.programado,
     v.codigo))

  // ---------- Compatibilidad (RN03) y vuelos no asignables (RN09)

  private def habilitada(v: Vuelo, p: Pista): Boolean =
    p.estado == Estado.Operativa && (p.uso == Uso.Mixta || p.uso.toString == v.operacion.toString)

  private def compatible(v: Vuelo, p: Pista): Boolean =
    habilitada(v, p) && p.longitud >= v.avion.categoria.longitudMinima

  private def motivoNoAsignable(v: Vuelo, pistas: Vector[Pista]): Option[String] =
    si(!pistas.exists(p => habilitada(v, p)), "sin pista habilitada para la operación")
      .orElse(si(!pistas.exists(p => compatible(v, p)), "sin pista con longitud suficiente"))

  def noAsignables(vuelos: Vector[Vuelo], pistas: Vector[Pista]): Vector[NoAsignable] =
    vuelos.flatMap(v => motivoNoAsignable(v, pistas).map(m => NoAsignable(v, m)))

  def asignables(vuelos: Vector[Vuelo], pistas: Vector[Pista]): Vector[Vuelo] =
    vuelos.filter(v => motivoNoAsignable(v, pistas).isEmpty)

  // ---------- Preparación: 12 filas por (operación, categoría, prioridad)

  /** Todos los vuelos de una fila son compatibles con las mismas pistas: basta mirar el primero. */
  private def filas(asignables: Vector[Vuelo]): Vector[Vector[Vuelo]] =
    asignables
      .groupBy(v => (v.operacion, v.avion.categoria, v.prioridad))
      .values
      .map(fila => fila.sortBy(v => (v.programado, v.codigo)))
      .toVector

  // ---------- Un paso de la simulación

  private def quedanVuelos(a: Aeropuerto, filas: Vector[Vector[Vuelo]], i: Int): Boolean =
    a.cabezas(i) < filas(i).size

  private def primero(a: Aeropuerto, filas: Vector[Vector[Vuelo]], i: Int): Vuelo =
    filas(i)(a.cabezas(i))

  /** La pista libre y compatible de menor id (las pistas ya vienen ordenadas por id). */
  private def pistaLibre(a: Aeropuerto, v: Vuelo, pistas: Vector[Pista]): Option[Int] =
    pistas.indices.find(j => a.libres(j) <= a.minuto && compatible(v, pistas(j)))

  /** Entre los primeros de cada fila que ya esperan y tienen pista libre, el de mayor prioridad. */
  private def mejorCandidato(a: Aeropuerto, filas: Vector[Vector[Vuelo]], pistas: Vector[Pista]): Option[Candidato] =
    filas.indices
      .filter(i => quedanVuelos(a, filas, i) && primero(a, filas, i).programado <= a.minuto)
      .flatMap(i => pistaLibre(a, primero(a, filas, i), pistas).map(j => Candidato(i, j, primero(a, filas, i))))
      .minByOption(_.vuelo)(using prioridad)

  private def asignar(a: Aeropuerto, c: Candidato, pistas: Vector[Pista]): Aeropuerto =
    val fin = a.minuto + c.vuelo.avion.categoria.minutosOcupacion
    a.copy(
      cabezas = a.cabezas.updated(c.fila, a.cabezas(c.fila) + 1),
      libres = a.libres.updated(c.pista, fin),
      asignadasEnElPaso = a.asignadasEnElPaso :+ OperacionAsignada(c.vuelo, pistas(c.pista), a.minuto, fin))

  /** Asigna en el minuto actual mientras haya candidato. Cada asignación ocupa una pista: como mucho k niveles. */
  @tailrec
  private def asignarEnMinuto(a: Aeropuerto, filas: Vector[Vector[Vuelo]], pistas: Vector[Pista]): Aeropuerto =
    mejorCandidato(a, filas, pistas) match
      case Some(c) => asignarEnMinuto(asignar(a, c, pistas), filas, pistas)
      case None => a

  /** Siguiente evento: el menor minuto futuro en que se libera una pista o llega un vuelo. */
  private def siguienteMinuto(a: Aeropuerto, filas: Vector[Vector[Vuelo]]): Long =
    (a.libres ++ filas.indices.filter(i => quedanVuelos(a, filas, i)).map(i => primero(a, filas, i).programado))
      .filter(t => t > a.minuto)
      .minOption
      .getOrElse(a.minuto)

  private def paso(a: Aeropuerto, filas: Vector[Vector[Vuelo]], pistas: Vector[Pista]): Aeropuerto =
    val tras = asignarEnMinuto(a.copy(asignadasEnElPaso = Vector.empty), filas, pistas)
    tras.copy(minuto = siguienteMinuto(tras, filas))

  private def terminado(a: Aeropuerto, filas: Vector[Vector[Vuelo]]): Boolean =
    a.asignadasEnElPaso.isEmpty && !filas.indices.exists(i => quedanVuelos(a, filas, i))

  // ---------- Simulación completa

  /** Secuencia perezosa de estados: iterate -> takeWhile -> flatMap de las asignaciones de cada paso. */
  def simular(asignables: Vector[Vuelo], pistas: Vector[Pista]): Vector[OperacionAsignada] =
    val operativas = pistas.filter(_.estado == Estado.Operativa).sortBy(_.id)
    val todas = filas(asignables)
    val inicial = Aeropuerto(
      todas.map(_.head.programado).minOption.getOrElse(0L),
      todas.map(_ => 0),
      operativas.map(_ => 0L),
      Vector.empty)
    Iterator.iterate(inicial)(a => paso(a, todas, operativas))
      .takeWhile(a => !terminado(a, todas))
      .flatMap(_.asignadasEnElPaso)
      .toVector
