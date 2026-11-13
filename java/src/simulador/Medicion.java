package simulador;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;
import java.util.stream.Collectors;

// =============================================================================
//  MÓDULO 6 · MEDICIÓN (Bloque 3, sección 5)
//  Toma el tiempo de cada etapa con System.nanoTime() y, con --medir, lo escribe en un archivo.
//  Cada etapa devuelve su resultado ya calculado (regla de materialización).
// =============================================================================
public final class Medicion {

    private Medicion() { }

    public static final String ENCABEZADO = "lectura_ns,validacion_ns,simulacion_ns,reportes_ns,escritura_ns";

    /** Una etapa del programa. Puede leer o escribir archivos, por eso declara IOException. */
    @FunctionalInterface
    public interface Etapa<T> {
        T ejecutar() throws IOException;
    }

    /** Resultado de una etapa y lo que tardó, en nanosegundos. */
    public record Medido<T>(T valor, long ns) { }

    public static <T> Medido<T> medir(Etapa<T> etapa) throws IOException {
        long inicio = System.nanoTime();
        T valor = etapa.ejecutar();
        return new Medido<>(valor, System.nanoTime() - inicio);
    }

    /** Archivo de --medir: encabezado y una línea con las cinco duraciones. */
    public static void escribir(Path archivo, List<Long> duraciones) throws IOException {
        Files.writeString(archivo, ENCABEZADO + "\n"
                + duraciones.stream().map(String::valueOf).collect(Collectors.joining(",")) + "\n",
                StandardCharsets.UTF_8);
    }
}
