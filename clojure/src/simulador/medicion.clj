;; =============================================================================
;;  MÓDULO 6 · MEDICIÓN (Bloque 3, sección 5)
;;  Toma el tiempo de cada etapa con System/nanoTime y, con --medir, lo escribe en un archivo.
;;  Cada etapa devuelve su resultado ya calculado (regla de materialización: vectores, no secuencias perezosas).
;; =============================================================================
(ns simulador.medicion
  (:require [clojure.string :as str]))

(def encabezado "lectura_ns,validacion_ns,simulacion_ns,reportes_ns,escritura_ns")

(defn medir
  "Ejecuta la etapa (una función sin argumentos) y devuelve su valor y lo que tardó, en nanosegundos."
  [etapa]
  (let [inicio (System/nanoTime)
        valor (etapa)]
    {:valor valor :ns (- (System/nanoTime) inicio)}))

(defn escribir
  "Archivo de --medir: encabezado y una línea con las cinco duraciones."
  [archivo duraciones]
  (spit archivo (str encabezado "\n" (str/join "," duraciones) "\n") :encoding "UTF-8"))
