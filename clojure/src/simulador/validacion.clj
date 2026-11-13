;; =============================================================================
;;  MÓDULO 3 · VALIDACIÓN (RF03)
;;  Cada registro se convierte en {:ok dato} o {:falla error}. Las reglas se revisan en el orden de las
;;  columnas y se reporta solo el primer error: (or regla1 regla2 ...) devuelve el primer mensaje que no es nil.
;; =============================================================================
(ns simulador.validacion
  (:require [clojure.string :as str]
            [simulador.modelo :as m]))

(def ^:private entero-re #"-?[0-9]{1,9}")
(def ^:private hora-re #"([0-9]{2}):([0-9]{2})")

;; ---------- Reglas reutilizables. Cada una devuelve el mensaje de error, o nil si el valor es válido.

(defn- entero [valor campo]
  (when-not (re-matches entero-re valor)
    (str campo " no es un entero: " valor)))

(defn- opcion [valor campo opciones]
  (when-not (some #(= valor %) opciones)
    (str campo " con valor no válido: " valor " (valores: " (str/join "/" opciones) ")")))

(defn- hora [valor]
  (let [[_ hh mm] (re-matches hora-re valor)]
    (when-not (and hh (<= (parse-long hh) 23) (<= (parse-long mm) 59))
      (str "hora no válida: " valor " (formato HH:MM de 00:00 a 23:59)"))))

;; ---------- Reglas de cada archivo (después del número de campos y la clave)

(defn- reglas-pista [[_ longitud uso estado]]
  (or (entero longitud "longitud")
      (when (<= (parse-long longitud) 0) (str "longitud debe ser mayor que 0: " longitud))
      (opcion uso "uso" m/nombres-uso)
      (opcion estado "estado" m/nombres-estado)))

(defn- reglas-vuelo [[_ ^String aerolinea ^String matricula categoria operacion dia hora-texto prioridad]]
  (or (when (.isEmpty aerolinea) "aerolínea vacía")
      (when (.isEmpty matricula) "matrícula vacía")
      (opcion categoria "categoría" m/nombres-categoria)
      (opcion operacion "operación" m/nombres-operacion)
      (entero dia "día")
      (when-not (<= 1 (parse-long dia) 9999) (str "día debe estar entre 1 y 9999: " dia))
      (hora hora-texto)
      (opcion prioridad "prioridad" m/nombres-prioridad)))

;; ---------- Construcción de las entidades (solo con campos ya validados)

(defn- construir-pista [[id longitud uso estado]]
  (m/->Pista id (parse-long longitud) (keyword uso) (keyword estado)))

(defn- construir-vuelo [[codigo aerolinea matricula categoria operacion dia hora-texto prioridad]]
  (m/->Vuelo codigo aerolinea (m/->Avion matricula (keyword categoria)) (keyword operacion)
             (+ (* (dec (parse-long dia)) 1440)
                (* (parse-long (subs hora-texto 0 2)) 60)
                (parse-long (subs hora-texto 3 5)))
             (keyword prioridad)))

;; ---------- Validación genérica

(defn- revisar
  "Error previo a la unicidad (número de campos o clave vacía) y error de los demás campos."
  [{:keys [campos] :as registro} num-campos nombre-clave reglas]
  (let [previo (or (when (not= num-campos (count campos))
                     (str "se esperaban " num-campos " campos y hay " (count campos)))
                   (when (.isEmpty ^String (first campos))
                     (str nombre-clave " vacío")))]
    {:registro registro
     :clave (first campos)
     :previo previo
     :de-campos (when-not previo (reglas campos))}))

(defn- resultado [{:keys [registro clave previo de-campos]} duenos archivo nombre-clave construir]
  (if-let [error (or previo
                     (when (< (get duenos clave Long/MAX_VALUE) (:linea registro))
                       (str nombre-clave " repetido: " clave))
                     de-campos)]
    {:falla (m/->ErrorRegistro archivo (:linea registro) error)}
    {:ok (construir (:campos registro))}))

(defn- validar
  "Valida todos los registros de un archivo.
  Unicidad: un registro está \"repetido\" si un registro VÁLIDO anterior tiene su misma clave. El dueño de
  cada clave es el primer registro sin errores propios (agrupar + mínimo), así no hace falta recorrer el
  archivo con estado: el resultado es el mismo que validar línea por línea."
  [registros archivo num-campos nombre-clave reglas construir]
  (let [revisiones (mapv #(revisar % num-campos nombre-clave reglas) registros)
        sin-errores (remove #(or (:previo %) (:de-campos %)) revisiones)
        duenos (update-vals (group-by :clave sin-errores)
                            #(apply min (map (comp :linea :registro) %)))]
    (mapv #(resultado % duenos archivo nombre-clave construir) revisiones)))

(defn validar-pistas [registros]
  (validar registros "pistas" 4 "id" reglas-pista construir-pista))

(defn validar-vuelos [registros]
  (validar registros "vuelos" 8 "código" reglas-vuelo construir-vuelo))

;; ---------- Separar válidos y errores

(defn validos [resultados]
  (into [] (keep :ok) resultados))

(defn errores [resultados]
  (into [] (keep :falla) resultados))
