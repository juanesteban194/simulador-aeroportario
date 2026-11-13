package simulador;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Arrays;
import java.util.List;
import java.util.stream.IntStream;

import simulador.Modelo.Registro;

// =============================================================================
//  MÓDULO 2 · LECTURA
//  Archivo -> líneas -> registros (número de línea + campos). Solo transforma texto.
// =============================================================================
public final class Lectura {

    private Lectura() { }

    /** ¿Existe el archivo y se puede leer? (se revisa antes de leer, para no depender de excepciones) */
    public static boolean sePuedeLeer(Path ruta) {
        return Files.isRegularFile(ruta) && Files.isReadable(ruta);
    }

    /** Todas las líneas del archivo. Un byte UTF-8 inválido se convierte en U+FFFD, sin error. */
    public static List<String> leerLineas(Path ruta) throws IOException {
        return List.of(new String(Files.readAllBytes(ruta), StandardCharsets.UTF_8).split("\n", -1));
    }

    /**
     * Registros de datos: se salta el encabezado (línea 1) y las líneas vacías.
     * split(",", -1) conserva los campos vacíos del final; trim() es el de la JVM.
     */
    public static List<Registro> registros(List<String> lineas) {
        return IntStream.range(1, lineas.size())
                .filter(i -> !lineas.get(i).trim().isEmpty())
                .mapToObj(i -> new Registro(i + 1, Arrays.stream(lineas.get(i).split(",", -1))
                        .map(String::trim)
                        .toList()))
                .toList();
    }
}
