# Simulador de operaciones aeroportuarias · Comparativo Java · Scala · Clojure

Proyecto final de **Lenguajes y Paradigmas de Programación** · Universidad de Medellín · Profesor: JuanGui

**Integrantes:** Sebastián Villa · Miguel Guarnizo · Juan Esteban Echavarría

## Objetivo

Implementar el **mismo simulador de operaciones aeroportuarias** en tres lenguajes (Java, Scala y Clojure),
con los mismos requisitos y los mismos resultados, aplicando los principios de la programación funcional.
Sobre esas tres versiones se ejecuta un **experimento**: las mismas cargas de trabajo y las mismas condiciones
para los tres lenguajes. Con las métricas obtenidas, un mecanismo **determina automáticamente** cuál lenguaje
se comporta mejor para este problema.

**El simulador:** gestiona vuelos, asigna pistas, organiza despegues y aterrizajes y controla retrasos.
Entidades: Avión, Vuelo, Pista, Aeropuerto y TorreControl. Además, asigna las pistas automáticamente
según prioridades y disponibilidad.

## Criterios de comparación (definidos por el profesor)

| Criterio | Peso |
|---|---|
| Tiempo de ejecución | 25 % |
| Consumo de memoria | 20 % |
| Rendimiento (operaciones por unidad de tiempo) | 20 % |
| Calidad de código | 15 % |
| Confiabilidad | 10 % |
| Uso funcional | 10 % |

## Estado del trabajo

El proyecto avanza por bloques. Antes de pasar al siguiente bloque se toman y registran todas las decisiones
del anterior ([método de trabajo](docs/00_metodo_de_trabajo.md) · [registro de decisiones](docs/decisiones.md)).

| # | Bloque | Estado |
|---|---|---|
| 0 | Marco: repo, herramientas y equipo | ✅ |
| 1 | Requerimientos ([01_requerimientos.md](docs/01_requerimientos.md)) | ✅ |
| 2 | Modelo y contrato ([02_modelo_y_contrato.md](docs/02_modelo_y_contrato.md)) | 🔍 en revisión |
| 3 | Diseño del experimento | — |
| 4 | Criterios y clasificación | — |
| 5 | Implementación (Scala → Java → Clojure) | — |
| 6 | Ejecución y medición | — |
| 7 | Consolidación y ranking automático | — |
| 8 | Informe técnico y sustentación | — |

## Estructura (se completa por bloques)

```
simulador-aeroportuario/
├── README.md
├── docs/            método de trabajo, decisiones, requerimientos, contrato, experimento, criterios, informe
├── herramientas/    instalación del entorno
├── datos/           generador de datos, escenarios y salidas esperadas
├── java/            versión Java
├── scala/           versión Scala
├── clojure/         versión Clojure
├── experimento/     ejecutar, medir, consolidar y clasificar
└── resultados/      datos crudos, consolidado, clasificación y gráficos
```

## Entorno

Las tres versiones se ejecutan sobre **la misma JVM (JDK 21)**, empaquetadas como `.jar` y lanzadas con
`java -jar` con las mismas opciones.

| Herramienta | Uso |
|---|---|
| JDK 21 (Temurin u OpenJDK) | Compilar y ejecutar Java; JVM común para los tres |
| Scala CLI | Compilar y empaquetar la versión Scala |
| Leiningen | Compilar por adelantado (AOT) y empaquetar la versión Clojure |
| IntelliJ IDEA + plugin Cursive | Editar los tres lenguajes en un mismo IDE |

**macOS:** `bash herramientas/instalar_entorno.sh` instala y verifica todo. Se puede ejecutar varias veces.
