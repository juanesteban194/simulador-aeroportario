package simulador;

import java.util.Comparator;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;
import java.util.stream.IntStream;
import java.util.stream.Stream;

import simulador.Modelo.Categoria;
import simulador.Modelo.ErrorRegistro;
import simulador.Modelo.NoAsignable;
import simulador.Modelo.Operacion;
import simulador.Modelo.OperacionAsignada;
import simulador.Modelo.Pista;

// =============================================================================
//  MÓDULO 5 · REPORTES (RF07 a RF14)
//  Construye el texto de los tres archivos de salida. Los decimales se calculan con
//  aritmética entera exacta (centésimas redondeadas HALF_UP), sin números de punto flotante.
// =============================================================================
public final class Reportes {

    private Reportes() { }

    private static final String SIN_DATOS = "Sin datos";
    private static final int UMBRAL_RETRASO = 15;

    /** Totales por aerolínea para RF11: el promedio es suma / cantidad. */
    private record Aerolinea(String nombre, long suma, long cantidad) { }

    /** Todo lo que necesitan los reportes. */
    public record Datos(int registrosPistas, List<Pista> pistas, List<ErrorRegistro> erroresPistas,
                        int registrosVuelos, int vuelosValidos, List<ErrorRegistro> erroresVuelos,
                        List<OperacionAsignada> operaciones, List<NoAsignable> noAsignables) { }

    // ---------- Formato

    private static String dosDigitos(long x) {
        return x < 10 ? "0" + x : String.valueOf(x);
    }

    /** a / b con 2 decimales: c = (200a + b) div 2b son las centésimas redondeadas. */
    private static String decimal(long a, long b) {
        long c = (200 * a + b) / (2 * b);
        return c / 100 + "." + dosDigitos(c % 100);
    }

    private static String hora(long minuto) {
        return "D" + (minuto / 1440 + 1) + " " + dosDigitos(minuto % 1440 / 60) + ":" + dosDigitos(minuto % 60);
    }

    private static List<String> seccion(String titulo, List<String> lineas) {
        return Stream.concat(Stream.of("== " + titulo + " =="), Stream.concat(lineas.stream(), Stream.of(""))).toList();
    }

    private static List<String> oSinDatos(List<String> lineas, String vacio) {
        return lineas.isEmpty() ? List.of(vacio) : lineas;
    }

    // ---------- Archivos CSV

    /** RF07: una línea por operación, en el orden en que se asignaron. */
    public static String operacionesCsv(List<OperacionAsignada> operaciones) {
        return Stream.concat(
                        Stream.of("codigo,aerolinea,operacion,categoria,prioridad,pista,programada,inicio,fin,retraso"),
                        operaciones.stream().map(o -> String.join(",",
                                o.vuelo().codigo(), o.vuelo().aerolinea(), o.vuelo().operacion().name(),
                                o.vuelo().avion().categoria().name(), o.vuelo().prioridad().name(), o.pista().id(),
                                hora(o.vuelo().programado()), hora(o.inicio()), hora(o.fin()),
                                String.valueOf(o.retraso()))))
                .collect(Collectors.joining("\n", "", "\n"));
    }

    /** RF03: primero los errores de pistas y luego los de vuelos. */
    public static String erroresCsv(List<ErrorRegistro> errores) {
        return Stream.concat(Stream.of("archivo,linea,motivo"),
                        errores.stream().map(e -> e.archivo() + "," + e.linea() + "," + e.motivo()))
                .collect(Collectors.joining("\n", "", "\n"));
    }

    // ---------- Secciones del reporte

    private static List<String> rf03(Datos d) {
        return seccion("RF03 · Validación de datos", List.of(
                "Pistas | registros: " + d.registrosPistas() + " | válidos: " + d.pistas().size()
                        + " | inválidos: " + d.erroresPistas().size(),
                "Vuelos | registros: " + d.registrosVuelos() + " | válidos: " + d.vuelosValidos()
                        + " | inválidos: " + d.erroresVuelos().size(),
                "Detalle de los registros inválidos: errores.csv"));
    }

    private static long sumaRetrasos(List<OperacionAsignada> ops) {
        return ops.stream().mapToLong(OperacionAsignada::retraso).sum();
    }

    private static long retrasados(List<OperacionAsignada> ops) {
        return ops.stream().filter(o -> o.retraso() > UMBRAL_RETRASO).count();
    }

    private static String promedio(List<OperacionAsignada> ops) {
        return ops.isEmpty() ? SIN_DATOS : decimal(sumaRetrasos(ops), ops.size()) + " min";
    }

    private static String porcentajeRetrasados(List<OperacionAsignada> ops) {
        return ops.isEmpty() ? SIN_DATOS : decimal(100 * retrasados(ops), ops.size()) + "%";
    }

    private static List<String> rf08(List<OperacionAsignada> ops) {
        return seccion("RF08 · Resumen de retrasos", List.of(
                "Operaciones asignadas: " + ops.size(),
                "Retraso promedio: " + promedio(ops),
                "Retraso máximo: " + ops.stream().mapToLong(OperacionAsignada::retraso).max()
                        .stream().mapToObj(m -> m + " min").findFirst().orElse(SIN_DATOS),
                "Vuelos retrasados (más de " + UMBRAL_RETRASO + " min): "
                        + (ops.isEmpty() ? SIN_DATOS : retrasados(ops) + " (" + porcentajeRetrasados(ops) + ")")));
    }

    private static List<String> rf09(List<OperacionAsignada> ops) {
        List<OperacionAsignada> top = ops.stream()
                .sorted(Comparator.comparingLong(OperacionAsignada::retraso).reversed()
                        .thenComparing(o -> o.vuelo().codigo()))
                .limit(5)
                .toList();
        return seccion("RF09 · 5 vuelos más retrasados", oSinDatos(IntStream.range(0, top.size())
                .mapToObj(i -> (i + 1) + ". " + top.get(i).vuelo().codigo() + " | retraso: " + top.get(i).retraso()
                        + " min | " + top.get(i).vuelo().operacion().name() + " | " + top.get(i).pista().id())
                .toList(), SIN_DATOS));
    }

    private static List<String> rf10(List<OperacionAsignada> ops, List<Pista> pistas) {
        return seccion("RF10 · Uso de pistas", ops.isEmpty() || pistas.isEmpty() ? List.of(SIN_DATOS) : usoDePistas(ops, pistas));
    }

    private static List<String> usoDePistas(List<OperacionAsignada> ops, List<Pista> pistas) {
        long inicio = ops.stream().mapToLong(o -> o.vuelo().programado()).min().orElse(0L);
        long fin = ops.stream().mapToLong(OperacionAsignada::fin).max().orElse(0L);
        Map<String, List<OperacionAsignada>> porPista = ops.stream().collect(Collectors.groupingBy(o -> o.pista().id()));
        return Stream.concat(
                Stream.of("Período simulado: " + hora(inicio) + " a " + hora(fin) + " (" + (fin - inicio) + " min)"),
                pistas.stream().sorted(Comparator.comparing(Pista::id)).map(p -> {
                    List<OperacionAsignada> suyas = porPista.getOrDefault(p.id(), List.of());
                    long ocupada = suyas.stream().mapToLong(o -> o.fin() - o.inicio()).sum();
                    return p.id() + " | " + p.estado().name() + " | operaciones: " + suyas.size() + " | ocupada: "
                            + ocupada + " min | ocupación: " + decimal(100 * ocupada, fin - inicio) + "%";
                })).toList();
    }

    /** RF11: de mayor a menor promedio (comparando fracciones exactas); si empatan, por nombre. */
    private static List<Aerolinea> aerolineas(List<OperacionAsignada> ops) {
        return ops.stream()
                .collect(Collectors.groupingBy(o -> o.vuelo().aerolinea()))
                .entrySet().stream()
                .map(e -> new Aerolinea(e.getKey(), sumaRetrasos(e.getValue()), e.getValue().size()))
                .sorted((x, y) -> Long.compare(y.suma() * x.cantidad(), x.suma() * y.cantidad()) != 0
                        ? Long.compare(y.suma() * x.cantidad(), x.suma() * y.cantidad())
                        : x.nombre().compareTo(y.nombre()))
                .toList();
    }

    private static List<String> rf11(List<Aerolinea> lista) {
        return seccion("RF11 · Retraso promedio por aerolínea", oSinDatos(lista.stream()
                .map(a -> a.nombre() + " | retraso promedio: " + decimal(a.suma(), a.cantidad())
                        + " min | operaciones: " + a.cantidad())
                .toList(), SIN_DATOS));
    }

    private static List<String> rf12(List<NoAsignable> noAsignables) {
        return seccion("RF12 · Vuelos no asignables", oSinDatos(noAsignables.stream()
                .map(n -> n.vuelo().codigo() + " | " + n.vuelo().operacion().name() + " | "
                        + n.vuelo().avion().categoria().name() + " | " + n.motivo())
                .toList(), "Ninguno"));
    }

    private static List<String> rf13(List<OperacionAsignada> ops) {
        return seccion("RF13 · Operaciones por tipo y categoría", Stream.concat(
                Stream.of(Operacion.Aterrizaje, Operacion.Despegue)
                        .map(t -> t.name() + ": " + ops.stream().filter(o -> o.vuelo().operacion() == t).count()),
                Stream.of(Categoria.values())
                        .map(c -> c.name() + ": " + ops.stream().filter(o -> o.vuelo().avion().categoria() == c).count()))
                .toList());
    }

    private static String pistaMasUsada(List<OperacionAsignada> ops, List<Pista> pistas) {
        Map<String, Long> usos = ops.stream().collect(Collectors.groupingBy(o -> o.pista().id(), Collectors.counting()));
        return ops.isEmpty() ? SIN_DATOS : pistas.stream()
                .sorted(Comparator.comparing((Pista p) -> usos.getOrDefault(p.id(), 0L)).reversed()
                        .thenComparing(Pista::id))
                .findFirst()
                .map(p -> p.id() + " (operaciones: " + usos.getOrDefault(p.id(), 0L) + ")")
                .orElse(SIN_DATOS);
    }

    private static List<String> rf14(Datos d, List<Aerolinea> lista) {
        List<OperacionAsignada> ops = d.operaciones();
        return List.of(
                "== RF14 · Resumen ejecutivo ==",
                "Vuelos cargados: " + d.registrosVuelos(),
                "Vuelos válidos: " + d.vuelosValidos(),
                "Vuelos inválidos: " + d.erroresVuelos().size(),
                "Vuelos asignados: " + ops.size(),
                "Vuelos no asignables: " + d.noAsignables().size(),
                "Retraso promedio: " + promedio(ops),
                "Vuelos retrasados: " + porcentajeRetrasados(ops),
                "Pista más usada: " + pistaMasUsada(ops, d.pistas()),
                "Aerolínea con mayor retraso promedio: " + lista.stream().findFirst()
                        .map(a -> a.nombre() + " (" + decimal(a.suma(), a.cantidad()) + " min)")
                        .orElse(SIN_DATOS));
    }

    /** reporte.txt completo (RF03 y RF08 a RF14). */
    public static String reporte(Datos d) {
        List<Aerolinea> lista = aerolineas(d.operaciones());
        return Stream.of(
                        List.of("SIMULADOR DE OPERACIONES AEROPORTUARIAS · REPORTE", ""),
                        rf03(d), rf08(d.operaciones()), rf09(d.operaciones()), rf10(d.operaciones(), d.pistas()),
                        rf11(lista), rf12(d.noAsignables()), rf13(d.operaciones()), rf14(d, lista))
                .flatMap(List::stream)
                .collect(Collectors.joining("\n", "", "\n"));
    }
}
