;; =============================================================================
;;  MÓDULO 5 · REPORTES (RF07 a RF14)
;;  Construye el texto de los tres archivos de salida. Los decimales se calculan con aritmética entera
;;  exacta (centésimas redondeadas HALF_UP), sin números de punto flotante.
;; =============================================================================
(ns simulador.reportes
  (:require [clojure.string :as str]
            [simulador.modelo :as m]))

(def ^:private sin-datos "Sin datos")
(def ^:private umbral-retraso 15)

;; ---------- Formato

(defn- dos-digitos [x]
  (if (< x 10) (str "0" x) (str x)))

(defn- decimal
  "a / b con 2 decimales: c = (200a + b) quot 2b son las centésimas redondeadas."
  [a b]
  (let [c (quot (+ (* 200 a) b) (* 2 b))]
    (str (quot c 100) "." (dos-digitos (rem c 100)))))

(defn- hora [minuto]
  (str "D" (inc (quot minuto 1440)) " "
       (dos-digitos (quot (rem minuto 1440) 60)) ":" (dos-digitos (rem minuto 60))))

(defn- seccion [titulo lineas]
  (concat [(str "== " titulo " ==")] lineas [""]))

(defn- o-sin-datos [lineas vacio]
  (if (seq lineas) lineas [vacio]))

(defn- texto
  "Une las líneas con saltos de línea; el archivo termina con un salto de línea."
  [lineas]
  (str (str/join "\n" lineas) "\n"))

(defn- codigo [operacion] (:codigo (:vuelo operacion)))
(defn- id-pista [operacion] (:id (:pista operacion)))

;; ---------- Archivos CSV

(defn operaciones-csv
  "RF07: una línea por operación, en el orden en que se asignaron."
  [operaciones]
  (texto (cons "codigo,aerolinea,operacion,categoria,prioridad,pista,programada,inicio,fin,retraso"
               (map (fn [{:keys [vuelo inicio fin] :as o}]
                      (str/join "," [(:codigo vuelo) (:aerolinea vuelo) (name (:operacion vuelo))
                                     (name (:categoria (:avion vuelo))) (name (:prioridad vuelo)) (id-pista o)
                                     (hora (:programado vuelo)) (hora inicio) (hora fin) (m/retraso o)]))
                    operaciones))))

(defn errores-csv
  "RF03: primero los errores de pistas y luego los de vuelos."
  [errores]
  (texto (cons "archivo,linea,motivo"
               (map (fn [{:keys [archivo linea motivo]}] (str archivo "," linea "," motivo)) errores))))

;; ---------- Secciones del reporte

(defn- rf03 [d]
  (seccion "RF03 · Validación de datos"
           [(str "Pistas | registros: " (:registros-pistas d) " | válidos: " (count (:pistas d))
                 " | inválidos: " (count (:errores-pistas d)))
            (str "Vuelos | registros: " (:registros-vuelos d) " | válidos: " (:vuelos-validos d)
                 " | inválidos: " (count (:errores-vuelos d)))
            "Detalle de los registros inválidos: errores.csv"]))

(defn- suma-retrasos [ops]
  (reduce + 0 (map m/retraso ops)))

(defn- retrasados [ops]
  (count (filter #(> (m/retraso %) umbral-retraso) ops)))

(defn- promedio [ops]
  (if (seq ops) (str (decimal (suma-retrasos ops) (count ops)) " min") sin-datos))

(defn- porcentaje-retrasados [ops]
  (if (seq ops) (str (decimal (* 100 (retrasados ops)) (count ops)) "%") sin-datos))

(defn- rf08 [ops]
  (seccion "RF08 · Resumen de retrasos"
           [(str "Operaciones asignadas: " (count ops))
            (str "Retraso promedio: " (promedio ops))
            (str "Retraso máximo: " (if (seq ops) (str (reduce max (map m/retraso ops)) " min") sin-datos))
            (str "Vuelos retrasados (más de " umbral-retraso " min): "
                 (if (seq ops) (str (retrasados ops) " (" (porcentaje-retrasados ops) ")") sin-datos))]))

(defn- por-retraso
  "De mayor a menor retraso; si empatan, por código."
  [x y]
  (let [c (compare (m/retraso y) (m/retraso x))]
    (if (zero? c) (compare (codigo x) (codigo y)) c)))

(defn- rf09 [ops]
  (seccion "RF09 · 5 vuelos más retrasados"
           (o-sin-datos (map-indexed (fn [i o]
                                       (str (inc i) ". " (codigo o) " | retraso: " (m/retraso o) " min | "
                                            (name (:operacion (:vuelo o))) " | " (id-pista o)))
                                     (take 5 (sort por-retraso ops)))
                        sin-datos)))

(defn- uso-de-pistas [ops pistas]
  (let [inicio (reduce min (map #(:programado (:vuelo %)) ops))
        fin (reduce max (map :fin ops))
        por-pista (group-by id-pista ops)]
    (cons (str "Período simulado: " (hora inicio) " a " (hora fin) " (" (- fin inicio) " min)")
          (map (fn [pista]
                 (let [suyas (get por-pista (:id pista) [])
                       ocupada (reduce + 0 (map #(- (:fin %) (:inicio %)) suyas))]
                   (str (:id pista) " | " (name (:estado pista)) " | operaciones: " (count suyas)
                        " | ocupada: " ocupada " min | ocupación: " (decimal (* 100 ocupada) (- fin inicio)) "%")))
               (sort-by :id pistas)))))

(defn- rf10 [ops pistas]
  (seccion "RF10 · Uso de pistas"
           (if (and (seq ops) (seq pistas)) (uso-de-pistas ops pistas) [sin-datos])))

(defn- por-promedio
  "RF11: de mayor a menor promedio (comparando fracciones exactas); si empatan, por nombre."
  [x y]
  (let [c (compare (* (:suma y) (:cantidad x)) (* (:suma x) (:cantidad y)))]
    (if (zero? c) (compare (:nombre x) (:nombre y)) c)))

(defn- aerolineas [ops]
  (->> (group-by #(:aerolinea (:vuelo %)) ops)
       (map (fn [[nombre suyas]] {:nombre nombre :suma (suma-retrasos suyas) :cantidad (count suyas)}))
       (sort por-promedio)))

(defn- rf11 [lista]
  (seccion "RF11 · Retraso promedio por aerolínea"
           (o-sin-datos (map (fn [{:keys [nombre suma cantidad]}]
                               (str nombre " | retraso promedio: " (decimal suma cantidad) " min | operaciones: " cantidad))
                             lista)
                        sin-datos)))

(defn- rf12 [no-asignables]
  (seccion "RF12 · Vuelos no asignables"
           (o-sin-datos (map (fn [{:keys [vuelo motivo]}]
                               (str (:codigo vuelo) " | " (name (:operacion vuelo)) " | "
                                    (name (:categoria (:avion vuelo))) " | " motivo))
                             no-asignables)
                        "Ninguno")))

(defn- rf13 [ops]
  (seccion "RF13 · Operaciones por tipo y categoría"
           (concat (map (fn [tipo] (str (name tipo) ": " (count (filter #(= tipo (:operacion (:vuelo %))) ops))))
                        [:Aterrizaje :Despegue])
                   (map (fn [categoria] (str categoria ": " (count (filter #(= (keyword categoria) (:categoria (:avion (:vuelo %))))
                                                                           ops))))
                        m/nombres-categoria))))

(defn- pista-mas-usada [ops pistas]
  (let [usos (frequencies (map id-pista ops))
        usos-de #(get usos (:id %) 0)
        mas-usada (first (sort (fn [x y]
                                 (let [c (compare (usos-de y) (usos-de x))]
                                   (if (zero? c) (compare (:id x) (:id y)) c)))
                               pistas))]
    (if (and (seq ops) mas-usada)
      (str (:id mas-usada) " (operaciones: " (usos-de mas-usada) ")")
      sin-datos)))

(defn- rf14 [d lista]
  (let [ops (:operaciones d)]
    ["== RF14 · Resumen ejecutivo =="
     (str "Vuelos cargados: " (:registros-vuelos d))
     (str "Vuelos válidos: " (:vuelos-validos d))
     (str "Vuelos inválidos: " (count (:errores-vuelos d)))
     (str "Vuelos asignados: " (count ops))
     (str "Vuelos no asignables: " (count (:no-asignables d)))
     (str "Retraso promedio: " (promedio ops))
     (str "Vuelos retrasados: " (porcentaje-retrasados ops))
     (str "Pista más usada: " (pista-mas-usada ops (:pistas d)))
     (str "Aerolínea con mayor retraso promedio: "
          (if-let [{:keys [nombre suma cantidad]} (first lista)]
            (str nombre " (" (decimal suma cantidad) " min)")
            sin-datos))]))

(defn reporte
  "reporte.txt completo (RF03 y RF08 a RF14)."
  [d]
  (let [ops (:operaciones d)
        lista (aerolineas ops)]
    (texto (concat ["SIMULADOR DE OPERACIONES AEROPORTUARIAS · REPORTE" ""]
                   (rf03 d) (rf08 ops) (rf09 ops) (rf10 ops (:pistas d))
                   (rf11 lista) (rf12 (:no-asignables d)) (rf13 ops) (rf14 d lista)))))
