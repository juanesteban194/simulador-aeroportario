package simulador;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;
import java.util.Optional;
import java.util.stream.Stream;

import simulador.Medicion.Medido;
import simulador.Modelo.ErrorRegistro;
import simulador.Modelo.NoAsignable;
import simulador.Modelo.OperacionAsignada;
import simulador.Modelo.Pista;
import simulador.Modelo.Registro;
import simulador.Modelo.Resultado;
import simulador.Modelo.Vuelo;

// =============================================================================
//  MÓDULO 7 · PROGRAMA PRINCIPAL
//  Revisa los argumentos y encadena las cinco etapas: lectura -> validación -> simulación ->
//  reportes -> escritura. Toda la lógica está en los otros módulos; aquí solo se conectan.
// =============================================================================
public final class Main {

    private Main() { }

    private static final String USO =
            "Uso: java -jar simulador-<lenguaje>.jar <pistas.csv> <vuelos.csv> <carpeta_salida> [--medir <archivo>]";

    // ---------- Resultado de cada etapa

    private record Lineas(List<String> pistas, List<String> vuelos) { }

    private record Validados(int registrosPistas, List<Pista> pistas, List<ErrorRegistro> erroresPistas,
                             int registrosVuelos, List<Vuelo> vuelos, List<ErrorRegistro> erroresVuelos) { }

    private record Simulados(List<OperacionAsignada> operaciones, List<NoAsignable> noAsignables) { }

    private record Textos(String operaciones, String errores, String reporte) { }

    // ---------- Etapas

    private static Validados validar(Lineas lineas) {
        List<Registro> registrosPistas = Lectura.registros(lineas.pistas());
        List<Registro> registrosVuelos = Lectura.registros(lineas.vuelos());
        List<Resultado<Pista>> pistas = Validacion.validarPistas(registrosPistas);
        List<Resultado<Vuelo>> vuelos = Validacion.validarVuelos(registrosVuelos);
        return new Validados(registrosPistas.size(), Validacion.validos(pistas), Validacion.errores(pistas),
                registrosVuelos.size(), Validacion.validos(vuelos), Validacion.errores(vuelos));
    }

    private static Simulados simular(Validados v) {
        return new Simulados(
                TorreControl.simular(TorreControl.asignables(v.vuelos(), v.pistas()), v.pistas()),
                TorreControl.noAsignables(v.vuelos(), v.pistas()));
    }

    private static Textos reportar(Validados v, Simulados s) {
        return new Textos(
                Reportes.operacionesCsv(s.operaciones()),
                Reportes.erroresCsv(Stream.concat(v.erroresPistas().stream(), v.erroresVuelos().stream()).toList()),
                Reportes.reporte(new Reportes.Datos(v.registrosPistas(), v.pistas(), v.erroresPistas(),
                        v.registrosVuelos(), v.vuelos().size(), v.erroresVuelos(),
                        s.operaciones(), s.noAsignables())));
    }

    private static Path escribir(Path salida, Textos t) throws IOException {
        Files.createDirectories(salida);
        Files.writeString(salida.resolve("operaciones.csv"), t.operaciones(), StandardCharsets.UTF_8);
        Files.writeString(salida.resolve("errores.csv"), t.errores(), StandardCharsets.UTF_8);
        Files.writeString(salida.resolve("reporte.txt"), t.reporte(), StandardCharsets.UTF_8);
        imprimir(t.reporte());
        return salida;
    }

    /** Escribe en pantalla siempre en UTF-8, sin depender de la configuración regional del equipo. */
    private static void imprimir(String texto) {
        System.out.writeBytes(texto.getBytes(StandardCharsets.UTF_8));
        System.out.flush();
    }

    // ---------- Argumentos

    /** Motivo del error de uso, si lo hay: cantidad de argumentos o archivo de entrada ilegible. */
    private static Optional<String> problemaDeUso(String[] args) {
        return !(args.length == 3 || (args.length == 5 && args[3].equals("--medir")))
                ? Optional.of("número de argumentos incorrecto")
                : Stream.of(args[0], args[1])
                        .filter(ruta -> !Lectura.sePuedeLeer(Path.of(ruta)))
                        .findFirst()
                        .map(ruta -> "no se puede leer el archivo " + ruta);
    }

    private static void ejecutar(Path pistas, Path vuelos, Path salida, Optional<Path> archivoMedicion)
            throws IOException {
        Medido<Lineas> lectura = Medicion.medir(
                () -> new Lineas(Lectura.leerLineas(pistas), Lectura.leerLineas(vuelos)));
        Medido<Validados> validacion = Medicion.medir(() -> validar(lectura.valor()));
        Medido<Simulados> simulacion = Medicion.medir(() -> simular(validacion.valor()));
        Medido<Textos> reportes = Medicion.medir(() -> reportar(validacion.valor(), simulacion.valor()));
        Medido<Path> escritura = Medicion.medir(() -> escribir(salida, reportes.valor()));
        if (archivoMedicion.isPresent()) {
            Medicion.escribir(archivoMedicion.get(), List.of(lectura.ns(), validacion.ns(), simulacion.ns(),
                    reportes.ns(), escritura.ns()));
        }
    }

    public static void main(String[] args) throws IOException {
        Optional<String> problema = problemaDeUso(args);
        if (problema.isPresent()) {
            imprimir("ERROR: " + problema.get() + "\n" + USO + "\n");
            System.exit(2);
        } else {
            ejecutar(Path.of(args[0]), Path.of(args[1]), Path.of(args[2]),
                    args.length == 5 ? Optional.of(Path.of(args[4])) : Optional.empty());
        }
    }
}
