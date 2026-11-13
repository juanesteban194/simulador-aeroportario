;; =============================================================================
;;  MÓDULO 7 · PROGRAMA PRINCIPAL
;;  Revisa los argumentos y encadena las cinco etapas: lectura -> validación -> simulación ->
;;  reportes -> escritura. Toda la lógica está en los otros módulos; aquí solo se conectan.
;; =============================================================================
(ns simulador.main
  (:require [clojure.java.io :as io]
            [simulador.lectura :as lectura]
            [simulador.medicion :as medicion]
            [simulador.reportes :as reportes]
            [simulador.torre-control :as torre]
            [simulador.validacion :as validacion])
  (:import (java.io File)
           (java.nio.charset StandardCharsets))
  (:gen-class))

(def ^:private modo-de-uso
  "Uso: java -jar simulador-<lenguaje>.jar <pistas.csv> <vuelos.csv> <carpeta_salida> [--medir <archivo>]")

;; ---------- Etapas

(defn- validar [{:keys [pistas vuelos]}]
  (let [registros-pistas (lectura/registros pistas)
        registros-vuelos (lectura/registros vuelos)
        resultados-pistas (validacion/validar-pistas registros-pistas)
        resultados-vuelos (validacion/validar-vuelos registros-vuelos)]
    {:registros-pistas (count registros-pistas)
     :pistas (validacion/validos resultados-pistas)
     :errores-pistas (validacion/errores resultados-pistas)
     :registros-vuelos (count registros-vuelos)
     :vuelos (validacion/validos resultados-vuelos)
     :errores-vuelos (validacion/errores resultados-vuelos)}))

(defn- simular [{:keys [vuelos pistas]}]
  {:operaciones (torre/simular (torre/asignables vuelos pistas) pistas)
   :no-asignables (torre/no-asignables vuelos pistas)})

(defn- reportar [v s]
  {:operaciones (reportes/operaciones-csv (:operaciones s))
   :errores (reportes/errores-csv (into (:errores-pistas v) (:errores-vuelos v)))
   :reporte (reportes/reporte {:registros-pistas (:registros-pistas v)
                               :pistas (:pistas v)
                               :errores-pistas (:errores-pistas v)
                               :registros-vuelos (:registros-vuelos v)
                               :vuelos-validos (count (:vuelos v))
                               :errores-vuelos (:errores-vuelos v)
                               :operaciones (:operaciones s)
                               :no-asignables (:no-asignables s)})})

(defn- imprimir
  "Escribe en pantalla siempre en UTF-8, sin depender de la configuración regional del equipo."
  [^String texto]
  (.writeBytes System/out (.getBytes texto StandardCharsets/UTF_8))
  (.flush System/out))

(defn- escribir [salida {:keys [operaciones errores reporte]}]
  (.mkdirs ^File (io/file salida))
  (spit (io/file salida "operaciones.csv") operaciones :encoding "UTF-8")
  (spit (io/file salida "errores.csv") errores :encoding "UTF-8")
  (spit (io/file salida "reporte.txt") reporte :encoding "UTF-8")
  (imprimir reporte)
  salida)

;; ---------- Argumentos

(defn- problema-de-uso
  "Motivo del error de uso, si lo hay: cantidad de argumentos o archivo de entrada ilegible."
  [args]
  (if-not (or (= 3 (count args)) (and (= 5 (count args)) (= "--medir" (nth args 3))))
    "número de argumentos incorrecto"
    (some #(when-not (lectura/se-puede-leer? %) (str "no se puede leer el archivo " %))
          (take 2 args))))

(defn- ejecutar [pistas vuelos salida archivo-medicion]
  (let [leido (medicion/medir (fn [] {:pistas (lectura/leer-lineas pistas) :vuelos (lectura/leer-lineas vuelos)}))
        validado (medicion/medir #(validar (:valor leido)))
        simulado (medicion/medir #(simular (:valor validado)))
        textos (medicion/medir #(reportar (:valor validado) (:valor simulado)))
        escrito (medicion/medir #(escribir salida (:valor textos)))]
    (when archivo-medicion
      (medicion/escribir archivo-medicion (map :ns [leido validado simulado textos escrito])))))

(defn -main [& args]
  (let [args (vec args)]
    (if-let [motivo (problema-de-uso args)]
      (do (imprimir (str "ERROR: " motivo "\n" modo-de-uso "\n"))
          (System/exit 2))
      (let [[pistas vuelos salida _ archivo-medicion] args]
        (ejecutar pistas vuelos salida archivo-medicion)))))
