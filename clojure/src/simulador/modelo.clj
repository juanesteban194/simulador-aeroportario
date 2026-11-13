;; =============================================================================
;;  MÓDULO 1 · MODELO
;;  Entidades del aeropuerto como registros inmutables (defrecord) y listas cerradas como palabras clave
;;  (:Ligero, :Despegue...). Para "cambiar" un dato se crea uno nuevo con assoc.
;; =============================================================================
(ns simulador.modelo)

;; ---------- Listas cerradas. El nombre de cada valor es el texto exacto del contrato.

(def categorias
  "Categoría del avión con sus requisitos (RN02)."
  {:Ligero  {:longitud-minima 1200 :minutos-ocupacion 2}
   :Mediano {:longitud-minima 2000 :minutos-ocupacion 3}
   :Pesado  {:longitud-minima 2800 :minutos-ocupacion 4}})

(def nombres-categoria ["Ligero" "Mediano" "Pesado"])
(def nombres-operacion ["Despegue" "Aterrizaje"])
(def nombres-uso ["Despegue" "Aterrizaje" "Mixta"])
(def nombres-estado ["Operativa" "Cerrada"])
(def nombres-prioridad ["Normal" "Emergencia"])

;; ---------- Entidades del proyecto

(defrecord Avion [matricula categoria])

;; programado: minuto absoluto = (día - 1) * 1440 + HH * 60 + MM.
(defrecord Vuelo [codigo aerolinea avion operacion programado prioridad])

(defrecord Pista [id longitud uso estado])

;; Resultado de la torre: qué vuelo usa qué pista y cuándo.
(defrecord OperacionAsignada [vuelo pista inicio fin])

(defrecord NoAsignable [vuelo motivo])

;; Estado de la simulación en un minuto. Es inmutable: cada paso crea uno nuevo.
;; cabezas: posición del primer vuelo pendiente de cada fila; libres: minuto en que se libera cada pista.
(defrecord Aeropuerto [minuto cabezas libres asignadas-en-el-paso])

;; ---------- Lectura y validación

;; Una línea de datos del archivo: su número de línea física y sus campos.
(defrecord Registro [linea campos])

(defrecord ErrorRegistro [archivo linea motivo])

;; ---------- Funciones de las entidades

(defn retraso
  "Minutos entre la hora programada y el inicio real de la operación."
  [operacion]
  (- (:inicio operacion) (:programado (:vuelo operacion))))

(defn categoria
  "Requisitos de la categoría del avión de un vuelo."
  [vuelo]
  (categorias (:categoria (:avion vuelo))))
