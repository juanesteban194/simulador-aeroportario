package simulador

// =============================================================================
//  MÓDULO 5 · REPORTES (RF07 a RF14)
//  Construye el texto de los tres archivos de salida. Los decimales se calculan con aritmética entera
//  exacta (centésimas redondeadas HALF_UP), sin números de punto flotante.
// =============================================================================
object Reportes:

  private val SinDatos = "Sin datos"
  private val UmbralRetraso = 15

  /** Totales por aerolínea para RF11: el promedio es suma / cantidad. */
  private final case class Aerolinea(nombre: String, suma: Long, cantidad: Long)

  /** Todo lo que necesitan los reportes. */
  final case class Datos(registrosPistas: Int, pistas: Vector[Pista], erroresPistas: Vector[ErrorRegistro],
                         registrosVuelos: Int, vuelosValidos: Int, erroresVuelos: Vector[ErrorRegistro],
                         operaciones: Vector[OperacionAsignada], noAsignables: Vector[NoAsignable])

  // ---------- Formato

  private def dosDigitos(x: Long): String = if x < 10 then s"0$x" else x.toString

  /** a / b con 2 decimales: c = (200a + b) / 2b son las centésimas redondeadas. */
  private def decimal(a: Long, b: Long): String =
    val c = (200 * a + b) / (2 * b)
    s"${c / 100}.${dosDigitos(c % 100)}"

  private def hora(minuto: Long): String =
    s"D${minuto / 1440 + 1} ${dosDigitos(minuto % 1440 / 60)}:${dosDigitos(minuto % 60)}"

  private def seccion(titulo: String, lineas: Seq[String]): Vector[String] =
    (s"== $titulo ==" +: lineas.toVector) :+ ""

  private def oSinDatos(lineas: Seq[String], vacio: String): Seq[String] =
    if lineas.isEmpty then Seq(vacio) else lineas

  private def texto(lineas: Seq[String]): String = lineas.mkString("", "\n", "\n")

  // ---------- Archivos CSV

  /** RF07: una línea por operación, en el orden en que se asignaron. */
  def operacionesCsv(operaciones: Vector[OperacionAsignada]): String =
    texto("codigo,aerolinea,operacion,categoria,prioridad,pista,programada,inicio,fin,retraso" +:
      operaciones.map(o => Vector(
        o.vuelo.codigo, o.vuelo.aerolinea, o.vuelo.operacion.toString, o.vuelo.avion.categoria.toString,
        o.vuelo.prioridad.toString, o.pista.id, hora(o.vuelo.programado), hora(o.inicio), hora(o.fin),
        o.retraso.toString).mkString(",")))

  /** RF03: primero los errores de pistas y luego los de vuelos. */
  def erroresCsv(errores: Vector[ErrorRegistro]): String =
    texto("archivo,linea,motivo" +: errores.map(e => s"${e.archivo},${e.linea},${e.motivo}"))

  // ---------- Secciones del reporte

  private def rf03(d: Datos): Vector[String] =
    seccion("RF03 · Validación de datos", Vector(
      s"Pistas | registros: ${d.registrosPistas} | válidos: ${d.pistas.size} | inválidos: ${d.erroresPistas.size}",
      s"Vuelos | registros: ${d.registrosVuelos} | válidos: ${d.vuelosValidos} | inválidos: ${d.erroresVuelos.size}",
      "Detalle de los registros inválidos: errores.csv"))

  private def sumaRetrasos(ops: Vector[OperacionAsignada]): Long = ops.map(_.retraso).sum

  private def retrasados(ops: Vector[OperacionAsignada]): Long = ops.count(_.retraso > UmbralRetraso).toLong

  private def promedio(ops: Vector[OperacionAsignada]): String =
    if ops.isEmpty then SinDatos else decimal(sumaRetrasos(ops), ops.size) + " min"

  private def porcentajeRetrasados(ops: Vector[OperacionAsignada]): String =
    if ops.isEmpty then SinDatos else decimal(100 * retrasados(ops), ops.size) + "%"

  private def rf08(ops: Vector[OperacionAsignada]): Vector[String] =
    val maximo = ops.map(_.retraso).maxOption.map(m => s"$m min").getOrElse(SinDatos)
    val conRetraso = if ops.isEmpty then SinDatos else s"${retrasados(ops)} (${porcentajeRetrasados(ops)})"
    seccion("RF08 · Resumen de retrasos", Vector(
      s"Operaciones asignadas: ${ops.size}",
      s"Retraso promedio: ${promedio(ops)}",
      s"Retraso máximo: $maximo",
      s"Vuelos retrasados (más de $UmbralRetraso min): $conRetraso"))

  private def rf09(ops: Vector[OperacionAsignada]): Vector[String] =
    val top = ops.sortBy(o => (-o.retraso, o.vuelo.codigo)).take(5)
    seccion("RF09 · 5 vuelos más retrasados", oSinDatos(top.zipWithIndex.map((o, i) =>
      s"${i + 1}. ${o.vuelo.codigo} | retraso: ${o.retraso} min | ${o.vuelo.operacion} | ${o.pista.id}"), SinDatos))

  private def usoDePistas(ops: Vector[OperacionAsignada], pistas: Vector[Pista]): Vector[String] =
    val inicio = ops.map(_.vuelo.programado).min
    val fin = ops.map(_.fin).max
    val porPista = ops.groupBy(_.pista.id)
    s"Período simulado: ${hora(inicio)} a ${hora(fin)} (${fin - inicio} min)" +:
      pistas.sortBy(_.id).map { p =>
        val suyas = porPista.getOrElse(p.id, Vector.empty)
        val ocupada = suyas.map(o => o.fin - o.inicio).sum
        s"${p.id} | ${p.estado} | operaciones: ${suyas.size} | ocupada: $ocupada min | ocupación: " +
          decimal(100 * ocupada, fin - inicio) + "%"
      }

  private def rf10(ops: Vector[OperacionAsignada], pistas: Vector[Pista]): Vector[String] =
    seccion("RF10 · Uso de pistas", if ops.isEmpty || pistas.isEmpty then Vector(SinDatos) else usoDePistas(ops, pistas))

  /** RF11: de mayor a menor promedio (comparando fracciones exactas); si empatan, por nombre. */
  private def aerolineas(ops: Vector[OperacionAsignada]): Vector[Aerolinea] =
    ops.groupBy(_.vuelo.aerolinea).toVector
      .map((nombre, suyas) => Aerolinea(nombre, sumaRetrasos(suyas), suyas.size))
      .sortWith((x, y) =>
        x.suma * y.cantidad > y.suma * x.cantidad
          || (x.suma * y.cantidad == y.suma * x.cantidad && x.nombre < y.nombre))

  private def rf11(lista: Vector[Aerolinea]): Vector[String] =
    seccion("RF11 · Retraso promedio por aerolínea", oSinDatos(lista.map(a =>
      s"${a.nombre} | retraso promedio: ${decimal(a.suma, a.cantidad)} min | operaciones: ${a.cantidad}"), SinDatos))

  private def rf12(noAsignables: Vector[NoAsignable]): Vector[String] =
    seccion("RF12 · Vuelos no asignables", oSinDatos(noAsignables.map(n =>
      s"${n.vuelo.codigo} | ${n.vuelo.operacion} | ${n.vuelo.avion.categoria} | ${n.motivo}"), "Ninguno"))

  private def rf13(ops: Vector[OperacionAsignada]): Vector[String] =
    seccion("RF13 · Operaciones por tipo y categoría",
      Vector(Operacion.Aterrizaje, Operacion.Despegue).map(t => s"$t: ${ops.count(_.vuelo.operacion == t)}")
        ++ Categoria.values.toVector.map(c => s"$c: ${ops.count(_.vuelo.avion.categoria == c)}"))

  private def pistaMasUsada(ops: Vector[OperacionAsignada], pistas: Vector[Pista]): String =
    val usos = ops.groupMapReduce(_.pista.id)(_ => 1L)(_ + _)
    if ops.isEmpty then SinDatos
    else pistas.sortBy(p => (-usos.getOrElse(p.id, 0L), p.id)).headOption
      .map(p => s"${p.id} (operaciones: ${usos.getOrElse(p.id, 0L)})")
      .getOrElse(SinDatos)

  private def rf14(d: Datos, lista: Vector[Aerolinea]): Vector[String] =
    val ops = d.operaciones
    val peor = lista.headOption.map(a => s"${a.nombre} (${decimal(a.suma, a.cantidad)} min)").getOrElse(SinDatos)
    Vector(
      "== RF14 · Resumen ejecutivo ==",
      s"Vuelos cargados: ${d.registrosVuelos}",
      s"Vuelos válidos: ${d.vuelosValidos}",
      s"Vuelos inválidos: ${d.erroresVuelos.size}",
      s"Vuelos asignados: ${ops.size}",
      s"Vuelos no asignables: ${d.noAsignables.size}",
      s"Retraso promedio: ${promedio(ops)}",
      s"Vuelos retrasados: ${porcentajeRetrasados(ops)}",
      s"Pista más usada: ${pistaMasUsada(ops, d.pistas)}",
      s"Aerolínea con mayor retraso promedio: $peor")

  /** reporte.txt completo (RF03 y RF08 a RF14). */
  def reporte(d: Datos): String =
    val lista = aerolineas(d.operaciones)
    texto(Vector(
      Vector("SIMULADOR DE OPERACIONES AEROPORTUARIAS · REPORTE", ""),
      rf03(d), rf08(d.operaciones), rf09(d.operaciones), rf10(d.operaciones, d.pistas),
      rf11(lista), rf12(d.noAsignables), rf13(d.operaciones), rf14(d, lista)).flatten)
