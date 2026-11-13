package simulador;

import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.function.Function;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.util.stream.Collectors;
import java.util.stream.Stream;

import simulador.Modelo.Avion;
import simulador.Modelo.Categoria;
import simulador.Modelo.ErrorRegistro;
import simulador.Modelo.Estado;
import simulador.Modelo.Falla;
import simulador.Modelo.Ok;
import simulador.Modelo.Operacion;
import simulador.Modelo.Pista;
import simulador.Modelo.Prioridad;
import simulador.Modelo.Registro;
import simulador.Modelo.Resultado;
import simulador.Modelo.Uso;
import simulador.Modelo.Vuelo;

import static simulador.Modelo.si;

// =============================================================================
//  MÓDULO 3 · VALIDACIÓN (RF03)
//  Cada registro se convierte en Ok(dato) o Falla(error). Las reglas se revisan en el
//  orden de las columnas y se reporta solo el primer error (cadena de Optional.or).
// =============================================================================
public final class Validacion {

    private Validacion() { }

    private static final Pattern ENTERO = Pattern.compile("-?[0-9]{1,9}");
    private static final Pattern HORA = Pattern.compile("([0-9]{2}):([0-9]{2})");

    /** Revisión de un registro: error previo a la unicidad y error de sus demás campos. */
    private record Revision(Registro registro, Optional<String> previo, Optional<String> deCampos) {
        String clave() {
            return registro.campos().get(0);
        }
    }

    // ---------- Reglas reutilizables

    private static Optional<String> entero(String valor, String campo) {
        return si(!ENTERO.matcher(valor).matches(), campo + " no es un entero: " + valor);
    }

    private static Optional<String> opcion(String valor, String campo, List<String> opciones) {
        return si(!opciones.contains(valor),
                campo + " con valor no válido: " + valor + " (valores: " + String.join("/", opciones) + ")");
    }

    private static Optional<String> hora(String valor) {
        Matcher partes = HORA.matcher(valor);
        boolean valida = partes.matches()
                && Integer.parseInt(partes.group(1)) <= 23
                && Integer.parseInt(partes.group(2)) <= 59;
        return si(!valida, "hora no válida: " + valor + " (formato HH:MM de 00:00 a 23:59)");
    }

    // ---------- Reglas de cada archivo (después del número de campos y la clave)

    private static Optional<String> reglasPista(List<String> c) {
        return entero(c.get(1), "longitud")
                .or(() -> si(Integer.parseInt(c.get(1)) <= 0, "longitud debe ser mayor que 0: " + c.get(1)))
                .or(() -> opcion(c.get(2), "uso", Modelo.nombres(Uso.values())))
                .or(() -> opcion(c.get(3), "estado", Modelo.nombres(Estado.values())));
    }

    private static Optional<String> reglasVuelo(List<String> c) {
        return si(c.get(1).isEmpty(), "aerolínea vacía")
                .or(() -> si(c.get(2).isEmpty(), "matrícula vacía"))
                .or(() -> opcion(c.get(3), "categoría", Modelo.nombres(Categoria.values())))
                .or(() -> opcion(c.get(4), "operación", Modelo.nombres(Operacion.values())))
                .or(() -> entero(c.get(5), "día"))
                .or(() -> si(Integer.parseInt(c.get(5)) < 1 || Integer.parseInt(c.get(5)) > 9999,
                        "día debe estar entre 1 y 9999: " + c.get(5)))
                .or(() -> hora(c.get(6)))
                .or(() -> opcion(c.get(7), "prioridad", Modelo.nombres(Prioridad.values())));
    }

    // ---------- Construcción de las entidades (solo con campos ya validados)

    private static Pista construirPista(List<String> c) {
        return new Pista(c.get(0), Integer.parseInt(c.get(1)), Uso.valueOf(c.get(2)), Estado.valueOf(c.get(3)));
    }

    private static Vuelo construirVuelo(List<String> c) {
        long minuto = (Integer.parseInt(c.get(5)) - 1) * 1440L
                + Integer.parseInt(c.get(6).substring(0, 2)) * 60L
                + Integer.parseInt(c.get(6).substring(3, 5));
        return new Vuelo(c.get(0), c.get(1), new Avion(c.get(2), Categoria.valueOf(c.get(3))),
                Operacion.valueOf(c.get(4)), minuto, Prioridad.valueOf(c.get(7)));
    }

    // ---------- Validación genérica

    /**
     * Valida todos los registros de un archivo.
     * Unicidad: un registro está "repetido" si un registro VÁLIDO anterior tiene su misma clave.
     * El dueño de cada clave es el primer registro sin errores propios (groupBy + mínimo), así no hace
     * falta recorrer el archivo con estado: el resultado es el mismo que validar línea por línea.
     */
    private static <T> List<Resultado<T>> validar(List<Registro> registros, String archivo, int numCampos,
                                                  String nombreClave,
                                                  Function<List<String>, Optional<String>> reglas,
                                                  Function<List<String>, T> construir) {
        List<Revision> revisiones = registros.stream()
                .map(r -> revisar(r, numCampos, nombreClave, reglas))
                .toList();
        Map<String, Integer> duenos = revisiones.stream()
                .filter(v -> v.previo().isEmpty() && v.deCampos().isEmpty())
                .collect(Collectors.toMap(Revision::clave, v -> v.registro().linea(), Math::min));
        return revisiones.stream()
                .map(v -> resultado(v, duenos, archivo, nombreClave, construir))
                .toList();
    }

    private static Revision revisar(Registro r, int numCampos, String nombreClave,
                                    Function<List<String>, Optional<String>> reglas) {
        Optional<String> previo = si(r.campos().size() != numCampos,
                "se esperaban " + numCampos + " campos y hay " + r.campos().size())
                .or(() -> si(r.campos().get(0).isEmpty(), nombreClave + " vacío"));
        return new Revision(r, previo, previo.isPresent() ? Optional.empty() : reglas.apply(r.campos()));
    }

    private static <T> Resultado<T> resultado(Revision v, Map<String, Integer> duenos, String archivo,
                                              String nombreClave, Function<List<String>, T> construir) {
        Optional<String> error = v.previo()
                .or(() -> si(duenos.getOrDefault(v.clave(), Integer.MAX_VALUE) < v.registro().linea(),
                        nombreClave + " repetido: " + v.clave()))
                .or(v::deCampos);
        return error.<Resultado<T>>map(m -> new Falla<>(new ErrorRegistro(archivo, v.registro().linea(), m)))
                .orElseGet(() -> new Ok<>(construir.apply(v.registro().campos())));
    }

    public static List<Resultado<Pista>> validarPistas(List<Registro> registros) {
        return validar(registros, "pistas", 4, "id", Validacion::reglasPista, Validacion::construirPista);
    }

    public static List<Resultado<Vuelo>> validarVuelos(List<Registro> registros) {
        return validar(registros, "vuelos", 8, "código", Validacion::reglasVuelo, Validacion::construirVuelo);
    }

    // ---------- Separar válidos y errores

    public static <T> List<T> validos(List<Resultado<T>> resultados) {
        return resultados.stream()
                .flatMap(r -> r instanceof Ok<T> ok ? Stream.of(ok.valor()) : Stream.<T>empty())
                .toList();
    }

    public static <T> List<ErrorRegistro> errores(List<Resultado<T>> resultados) {
        return resultados.stream()
                .flatMap(r -> r instanceof Falla<T> falla ? Stream.of(falla.error()) : Stream.<ErrorRegistro>empty())
                .toList();
    }
}
