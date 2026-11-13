;; =============================================================================
;;  MÓDULO 2 · LECTURA
;;  Archivo -> líneas -> registros (número de línea + campos). Solo transforma texto.
;; =============================================================================
(ns simulador.lectura
  (:require [clojure.string :as str]
            [simulador.modelo :as m])
  (:import (java.io File)
           (java.nio.charset StandardCharsets)
           (java.nio.file Files)))

(defn se-puede-leer?
  "¿Existe el archivo y se puede leer? (se revisa antes de leer, para no depender de excepciones)"
  [^String ruta]
  (let [archivo (File. ruta)]
    (and (.isFile archivo) (.canRead archivo))))

(defn leer-lineas
  "Todas las líneas del archivo. Un byte UTF-8 inválido se convierte en U+FFFD, sin error."
  [^String ruta]
  (str/split (String. (Files/readAllBytes (.toPath (File. ruta))) StandardCharsets/UTF_8) #"\n" -1))

(defn registros
  "Registros de datos: se salta el encabezado (línea 1) y las líneas vacías.
  Se usa .trim de la JVM (quita los caracteres <= U+0020); str/trim de Clojure quitaría otros espacios Unicode."
  [lineas]
  (into []
        (comp (map-indexed vector)
              (drop 1)
              (remove (fn [[_ ^String linea]] (.isEmpty (.trim linea))))
              (map (fn [[i ^String linea]]
                     (m/->Registro (inc i) (mapv (fn [^String campo] (.trim campo)) (str/split linea #"," -1))))))
        lineas))
