package simulador;

import java.util.Arrays;
import java.util.List;
import java.util.Optional;

// =============================================================================
//  MÓDULO 1 · MODELO
//  Entidades del aeropuerto como datos inmutables (record) y listas cerradas (enum).
//  Un record no tiene "setters": para "cambiar" un dato se crea uno nuevo.
// =============================================================================
public final class Modelo {

    private Modelo() { }

    // ---------- Listas cerradas. El nombre de cada valor es el texto exacto del contrato.

    /** Categoría del avión con sus requisitos (RN02). */
    public enum Categoria {
        Ligero(1200, 2), Mediano(2000, 3), Pesado(2800, 4);

        public final int longitudMinima;
        public final int minutosOcupacion;

        Categoria(int longitudMinima, int minutosOcupacion) {
            this.longitudMinima = longitudMinima;
            this.minutosOcupacion = minutosOcupacion;
        }
    }

    public enum Operacion { Despegue, Aterrizaje }

    public enum Uso { Despegue, Aterrizaje, Mixta }

    public enum Estado { Operativa, Cerrada }

    public enum Prioridad { Normal, Emergencia }

    /** Los textos válidos de una lista cerrada, en su orden ("Ligero", "Mediano", "Pesado"). */
    public static List<String> nombres(Enum<?>[] valores) {
        return Arrays.stream(valores).map(Enum::name).toList();
    }

    // ---------- Entidades del proyecto

    public record Avion(String matricula, Categoria categoria) { }

    /** programado: minuto absoluto = (día - 1) * 1440 + HH * 60 + MM. */
    public record Vuelo(String codigo, String aerolinea, Avion avion, Operacion operacion,
                        long programado, Prioridad prioridad) { }

    public record Pista(String id, int longitud, Uso uso, Estado estado) { }

    /** Resultado de la torre: qué vuelo usa qué pista y cuándo. */
    public record OperacionAsignada(Vuelo vuelo, Pista pista, long inicio, long fin) {
        public long retraso() {
            return inicio - vuelo.programado();
        }
    }

    public record NoAsignable(Vuelo vuelo, String motivo) { }

    /**
     * Estado de la simulación en un minuto. Es inmutable: cada paso crea uno nuevo.
     * cabezas: posición del primer vuelo pendiente de cada fila; libres: minuto en que se libera cada pista.
     */
    public record Aeropuerto(long minuto, List<Integer> cabezas, List<Long> libres,
                             List<OperacionAsignada> asignadasEnElPaso) { }

    // ---------- Lectura y validación

    /** Una línea de datos del archivo: su número de línea física y sus campos. */
    public record Registro(int linea, List<String> campos) { }

    public record ErrorRegistro(String archivo, int linea, String motivo) { }

    /** Resultado de validar un registro: Ok con el dato, o Falla con el error (Java no trae Either). */
    public sealed interface Resultado<T> permits Ok, Falla { }

    public record Ok<T>(T valor) implements Resultado<T> { }

    public record Falla<T>(ErrorRegistro error) implements Resultado<T> { }

    /** Optional con el mensaje si la condición se cumple; vacío si no. */
    public static Optional<String> si(boolean condicion, String mensaje) {
        return condicion ? Optional.of(mensaje) : Optional.empty();
    }
}
