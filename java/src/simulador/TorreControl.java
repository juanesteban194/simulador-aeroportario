package simulador;

import java.util.Comparator;
import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;
import java.util.stream.IntStream;
import java.util.stream.Stream;

import simulador.Modelo.Aeropuerto;
import simulador.Modelo.Estado;
import simulador.Modelo.NoAsignable;
import simulador.Modelo.Operacion;
import simulador.Modelo.OperacionAsignada;
import simulador.Modelo.Pista;
import simulador.Modelo.Prioridad;
import simulador.Modelo.Uso;
import simulador.Modelo.Vuelo;

import static simulador.Modelo.si;

// =============================================================================
//  MÓDULO 4 · TORRE DE CONTROL (RF04, RF05, RF06)
//  Funciones puras: reciben un Aeropuerto y devuelven uno nuevo. No guardan estado.
// =============================================================================
public final class TorreControl {

    private TorreControl() { }

    /** Un vuelo listo para operar y la pista libre que le tocaría. */
    private record Candidato(int fila, int pista, Vuelo vuelo) { }

    /** RN05: emergencia, luego aterrizaje, luego hora programada, luego código. */
    private static final Comparator<Vuelo> PRIORIDAD = Comparator
            .comparing((Vuelo v) -> v.prioridad() == Prioridad.Emergencia ? 0 : 1)
            .thenComparing(v -> v.operacion() == Operacion.Aterrizaje ? 0 : 1)
            .thenComparingLong(Vuelo::programado)
            .thenComparing(Vuelo::codigo);

    // ---------- Compatibilidad (RN03) y vuelos no asignables (RN09)

    private static boolean habilitada(Vuelo v, Pista p) {
        return p.estado() == Estado.Operativa
                && (p.uso() == Uso.Mixta || p.uso().name().equals(v.operacion().name()));
    }

    private static boolean compatible(Vuelo v, Pista p) {
        return habilitada(v, p) && p.longitud() >= v.avion().categoria().longitudMinima;
    }

    private static Optional<String> motivoNoAsignable(Vuelo v, List<Pista> pistas) {
        return si(pistas.stream().noneMatch(p -> habilitada(v, p)), "sin pista habilitada para la operación")
                .or(() -> si(pistas.stream().noneMatch(p -> compatible(v, p)), "sin pista con longitud suficiente"));
    }

    public static List<NoAsignable> noAsignables(List<Vuelo> vuelos, List<Pista> pistas) {
        return vuelos.stream()
                .flatMap(v -> motivoNoAsignable(v, pistas).map(m -> new NoAsignable(v, m)).stream())
                .toList();
    }

    public static List<Vuelo> asignables(List<Vuelo> vuelos, List<Pista> pistas) {
        return vuelos.stream().filter(v -> motivoNoAsignable(v, pistas).isEmpty()).toList();
    }

    // ---------- Preparación: 12 filas por (operación, categoría, prioridad)

    /** Todos los vuelos de una fila son compatibles con las mismas pistas: basta mirar el primero. */
    private static List<List<Vuelo>> filas(List<Vuelo> asignables) {
        return asignables.stream()
                .collect(Collectors.groupingBy(v -> v.operacion() + "|" + v.avion().categoria() + "|" + v.prioridad()))
                .values().stream()
                .map(fila -> fila.stream()
                        .sorted(Comparator.comparingLong(Vuelo::programado).thenComparing(Vuelo::codigo))
                        .toList())
                .toList();
    }

    // ---------- Un paso de la simulación

    private static boolean quedanVuelos(Aeropuerto a, List<List<Vuelo>> filas, int fila) {
        return a.cabezas().get(fila) < filas.get(fila).size();
    }

    private static Vuelo primero(Aeropuerto a, List<List<Vuelo>> filas, int fila) {
        return filas.get(fila).get(a.cabezas().get(fila));
    }

    /** La pista libre y compatible de menor id (las pistas ya vienen ordenadas por id). */
    private static Optional<Integer> pistaLibre(Aeropuerto a, Vuelo v, List<Pista> pistas) {
        return IntStream.range(0, pistas.size()).boxed()
                .filter(j -> a.libres().get(j) <= a.minuto() && compatible(v, pistas.get(j)))
                .findFirst();
    }

    /** Entre los primeros de cada fila que ya esperan y tienen pista libre, el de mayor prioridad. */
    private static Optional<Candidato> mejorCandidato(Aeropuerto a, List<List<Vuelo>> filas, List<Pista> pistas) {
        return IntStream.range(0, filas.size()).boxed()
                .filter(i -> quedanVuelos(a, filas, i))
                .filter(i -> primero(a, filas, i).programado() <= a.minuto())
                .flatMap(i -> pistaLibre(a, primero(a, filas, i), pistas)
                        .map(j -> new Candidato(i, j, primero(a, filas, i))).stream())
                .min(Comparator.comparing(Candidato::vuelo, PRIORIDAD));
    }

    /** Copia de la lista con un elemento cambiado (las listas no se modifican). */
    private static <T> List<T> reemplazar(List<T> lista, int indice, T valor) {
        return IntStream.range(0, lista.size()).mapToObj(k -> k == indice ? valor : lista.get(k)).toList();
    }

    private static Aeropuerto asignar(Aeropuerto a, Candidato c, List<Pista> pistas) {
        long fin = a.minuto() + c.vuelo().avion().categoria().minutosOcupacion;
        OperacionAsignada operacion = new OperacionAsignada(c.vuelo(), pistas.get(c.pista()), a.minuto(), fin);
        return new Aeropuerto(a.minuto(),
                reemplazar(a.cabezas(), c.fila(), a.cabezas().get(c.fila()) + 1),
                reemplazar(a.libres(), c.pista(), fin),
                Stream.concat(a.asignadasEnElPaso().stream(), Stream.of(operacion)).toList());
    }

    /** Asigna en el minuto actual mientras haya candidato. Cada asignación ocupa una pista: como mucho k niveles. */
    private static Aeropuerto asignarEnMinuto(Aeropuerto a, List<List<Vuelo>> filas, List<Pista> pistas) {
        return mejorCandidato(a, filas, pistas)
                .map(c -> asignarEnMinuto(asignar(a, c, pistas), filas, pistas))
                .orElse(a);
    }

    /** Siguiente evento: el menor minuto futuro en que se libera una pista o llega un vuelo. */
    private static long siguienteMinuto(Aeropuerto a, List<List<Vuelo>> filas) {
        return Stream.concat(
                        a.libres().stream(),
                        IntStream.range(0, filas.size()).boxed()
                                .filter(i -> quedanVuelos(a, filas, i))
                                .map(i -> primero(a, filas, i).programado()))
                .filter(t -> t > a.minuto())
                .min(Long::compare)
                .orElse(a.minuto());
    }

    private static Aeropuerto paso(Aeropuerto a, List<List<Vuelo>> filas, List<Pista> pistas) {
        Aeropuerto tras = asignarEnMinuto(new Aeropuerto(a.minuto(), a.cabezas(), a.libres(), List.of()), filas, pistas);
        return new Aeropuerto(siguienteMinuto(tras, filas), tras.cabezas(), tras.libres(), tras.asignadasEnElPaso());
    }

    private static boolean terminado(Aeropuerto a, List<List<Vuelo>> filas) {
        return a.asignadasEnElPaso().isEmpty()
                && IntStream.range(0, filas.size()).noneMatch(i -> quedanVuelos(a, filas, i));
    }

    // ---------- Simulación completa

    /** Secuencia perezosa de estados: iterate -> takeWhile -> flatMap de las asignaciones de cada paso. */
    public static List<OperacionAsignada> simular(List<Vuelo> asignables, List<Pista> pistas) {
        List<Pista> operativas = pistas.stream()
                .filter(p -> p.estado() == Estado.Operativa)
                .sorted(Comparator.comparing(Pista::id))
                .toList();
        List<List<Vuelo>> filas = filas(asignables);
        Aeropuerto inicial = new Aeropuerto(
                filas.stream().mapToLong(f -> f.get(0).programado()).min().orElse(0L),
                filas.stream().map(f -> 0).toList(),
                operativas.stream().map(p -> 0L).toList(),
                List.of());
        return Stream.iterate(inicial, a -> !terminado(a, filas), a -> paso(a, filas, operativas))
                .flatMap(a -> a.asignadasEnElPaso().stream())
                .toList();
    }
}
