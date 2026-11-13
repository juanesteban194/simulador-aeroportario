;; Versión Clojure del simulador. Se construye con: bash clojure/construir.sh  (lein uberjar)
(defproject simulador-clojure "1.0.0"
  :description "Simulador de operaciones aeroportuarias · versión Clojure"
  :dependencies [[org.clojure/clojure "1.12.0"]]
  :main simulador.main
  ;; Compilación por adelantado de todos los espacios de nombres: el .jar no compila nada al arrancar.
  :aot :all
  :target-path "target/%s"
  :uberjar-name "simulador-clojure.jar"
  ;; Avisa al compilar si alguna llamada a Java necesitaría reflexión (lenta); el código no debe tener ninguna.
  :global-vars {*warn-on-reflection* true})
