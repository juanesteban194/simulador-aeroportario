;; =============================================================================
;;  MÓDULO 4 · TORRE DE CONTROL (RF04, RF05, RF06)
;;  Funciones puras: reciben un Aeropuerto y devuelven uno nuevo. No guardan estado.
;; =============================================================================
(ns simulador.torre-control
  (:require [simulador.modelo :as m]))

;; ---------- Órdenes (comparadores: negativo si x va antes que y)

(defn- por-hora-y-codigo
  "Orden de una fila: hora programada y, si empatan, código."
  [x y]
  (let [c (compare (:programado x) (:programado y))]
    (if (zero? c) (compare (:codigo x) (:codigo y)) c)))

(defn- rango
  "RN05: 0 emergencia que aterriza, 1 emergencia que despega, 2 normal que aterriza, 3 normal que despega."
  [vuelo]
  (+ (if (= :Emergencia (:prioridad vuelo)) 0 2)
     (if (= :Aterrizaje (:operacion vuelo)) 0 1)))

(defn- por-prioridad
  "RN05: emergencia, luego aterrizaje, luego hora programada, luego código."
  [x y]
  (let [c (compare (rango x) (rango y))]
    (if (zero? c) (por-hora-y-codigo x y) c)))

;; ---------- Compatibilidad (RN03) y vuelos no asignables (RN09)

(defn- habilitada? [vuelo pista]
  (and (= :Operativa (:estado pista))
       ;; :Despegue y :Aterrizaje son la misma palabra clave en el uso de la pista y en la operación.
       (or (= :Mixta (:uso pista)) (= (:uso pista) (:operacion vuelo)))))

(defn- compatible? [vuelo pista]
  (and (habilitada? vuelo pista)
       (>= (:longitud pista) (:longitud-minima (m/categoria vuelo)))))

(defn- motivo-no-asignable [vuelo pistas]
  (cond
    (not-any? #(habilitada? vuelo %) pistas) "sin pista habilitada para la operación"
    (not-any? #(compatible? vuelo %) pistas) "sin pista con longitud suficiente"))

(defn no-asignables [vuelos pistas]
  (into [] (keep (fn [vuelo]
                   (when-let [motivo (motivo-no-asignable vuelo pistas)]
                     (m/->NoAsignable vuelo motivo))))
        vuelos))

(defn asignables [vuelos pistas]
  (into [] (remove #(motivo-no-asignable % pistas)) vuelos))

;; ---------- Preparación: 12 filas por (operación, categoría, prioridad)

(defn- armar-filas
  "Todos los vuelos de una fila son compatibles con las mismas pistas: basta mirar el primero."
  [asignables]
  (->> asignables
       (group-by (juxt :operacion (comp :categoria :avion) :prioridad))
       vals
       (mapv #(vec (sort por-hora-y-codigo %)))))

;; ---------- Un paso de la simulación

(defn- quedan-vuelos? [aeropuerto filas i]
  (< (nth (:cabezas aeropuerto) i) (count (nth filas i))))

(defn- primero [aeropuerto filas i]
  (nth (nth filas i) (nth (:cabezas aeropuerto) i)))

(defn- pista-libre
  "La pista libre y compatible de menor id (las pistas ya vienen ordenadas por id)."
  [aeropuerto vuelo pistas]
  (some (fn [j]
          (when (and (<= (nth (:libres aeropuerto) j) (:minuto aeropuerto))
                     (compatible? vuelo (nth pistas j)))
            j))
        (range (count pistas))))

(defn- candidato
  "El primer vuelo de la fila i, si ya espera y tiene una pista libre."
  [aeropuerto filas pistas i]
  (let [vuelo (primero aeropuerto filas i)
        pista (when (<= (:programado vuelo) (:minuto aeropuerto))
                (pista-libre aeropuerto vuelo pistas))]
    (when pista {:fila i :pista pista :vuelo vuelo})))

(defn- mejor-candidato
  "Entre los primeros de cada fila que ya esperan y tienen pista libre, el de mayor prioridad."
  [aeropuerto filas pistas]
  (->> (range (count filas))
       (filter #(quedan-vuelos? aeropuerto filas %))
       (keep #(candidato aeropuerto filas pistas %))
       (sort-by :vuelo por-prioridad)
       first))

(defn- asignar [aeropuerto {:keys [fila pista vuelo]} pistas]
  (let [inicio (:minuto aeropuerto)
        fin (+ inicio (:minutos-ocupacion (m/categoria vuelo)))]
    (-> aeropuerto
        (update-in [:cabezas fila] inc)
        (assoc-in [:libres pista] fin)
        (update :asignadas-en-el-paso conj (m/->OperacionAsignada vuelo (nth pistas pista) inicio fin)))))

(defn- asignar-en-minuto
  "Asigna en el minuto actual mientras haya candidato. Cada asignación ocupa una pista: como mucho k niveles."
  [aeropuerto filas pistas]
  (if-let [c (mejor-candidato aeropuerto filas pistas)]
    (recur (asignar aeropuerto c pistas) filas pistas)
    aeropuerto))

(defn- siguiente-minuto
  "Siguiente evento: el menor minuto futuro en que se libera una pista o llega un vuelo."
  [aeropuerto filas]
  (let [ahora (:minuto aeropuerto)
        futuros (filter #(> % ahora)
                        (concat (:libres aeropuerto)
                                (keep #(when (quedan-vuelos? aeropuerto filas %)
                                         (:programado (primero aeropuerto filas %)))
                                      (range (count filas)))))]
    (if (seq futuros) (reduce min futuros) ahora)))

(defn- paso [aeropuerto filas pistas]
  (let [tras (asignar-en-minuto (assoc aeropuerto :asignadas-en-el-paso []) filas pistas)]
    (assoc tras :minuto (siguiente-minuto tras filas))))

(defn- terminado? [aeropuerto filas]
  (and (empty? (:asignadas-en-el-paso aeropuerto))
       (not-any? #(quedan-vuelos? aeropuerto filas %) (range (count filas)))))

;; ---------- Simulación completa

(defn simular
  "Secuencia perezosa de estados: iterate -> take-while -> mapcat de las asignaciones de cada paso."
  [asignables pistas]
  (let [operativas (vec (sort-by :id (filter #(= :Operativa (:estado %)) pistas)))
        filas (armar-filas asignables)
        inicial (m/->Aeropuerto (if (seq filas) (reduce min (map #(:programado (first %)) filas)) 0)
                                (vec (repeat (count filas) 0))
                                (vec (repeat (count operativas) 0))
                                [])]
    (into []
          (comp (take-while #(not (terminado? % filas)))
                (mapcat :asignadas-en-el-paso))
          (iterate #(paso % filas operativas) inicial))))
