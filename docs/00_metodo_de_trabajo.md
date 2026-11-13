# Método de trabajo

## Ciclo de cada bloque

1. **Propuesta:** se plantean las decisiones del bloque (máximo 3 a 5), cada una con sus opciones,
   una recomendación y su justificación.
2. **Decisión:** el equipo elige.
3. **Entregable:** se produce el documento o el código del bloque.
4. **Revisión:** el equipo lo revisa y se corrige.
5. **Cierre:** se sube al repositorio y se registra en [decisiones.md](decisiones.md).

## Reglas

- No se abre un bloque si quedan decisiones pendientes del anterior.
- No se escribe código hasta cerrar los Bloques 1 a 4: primero se documenta qué se construye y cómo se mide.
- Toda decisión queda en [decisiones.md](decisiones.md), con las opciones, lo elegido y la razón.

## Bloques

| # | Bloque | Qué se decide | Entregable | Qué cubre del enunciado |
|---|---|---|---|---|
| 0 | Marco | Repo, herramientas, equipo | Repo con README inicial | Entregable 11 |
| 1 | Requerimientos | Qué hace el simulador: vuelos, pistas, despegues y aterrizajes, retrasos, prioridades | `01_requerimientos.md` | Condición 2 |
| 2 | Modelo y contrato | Entidades como datos inmutables, algoritmo de asignación de pistas, formato exacto de entrada y salida | `02_modelo_y_contrato.md` y un diagrama | Condiciones 2 y 3 · Uso funcional |
| 3 | Diseño del experimento | Escenarios y volúmenes, repeticiones, protocolo, instrumentos | `03_experimento.md` | Condiciones 4, 5 y 6 · Tiempo, Memoria, Rendimiento |
| 4 | Criterios y clasificación | Fórmula de cada criterio, normalización, pesos, desempate | `04_criterios.md` | Condiciones 7, 8 y 9 · Calidad, Confiabilidad, Uso funcional |
| 5 | Implementación | Orden de trabajo (Scala → Java → Clojure) y estructura del código | Tres proyectos, generador de datos, pruebas de equivalencia | Condiciones 1, 2 y 3 · Entregables 11 y 12 |
| 6 | Ejecución y medición | Se ejecuta el diseño del Bloque 3 | `resultados/crudos/` | Condiciones 5 y 6 · Entregable 13 |
| 7 | Consolidación y ranking | Se aplica la fórmula del Bloque 4 | `consolidado.csv`, `clasificacion.md`, gráficos | Condiciones 7, 8 y 9 · Entregable 14 |
| 8 | Informe y sustentación | Estructura del informe y guion | `05_informe_tecnico.md` y guion | Condición 10 · Entregables 15 y 16 |

## Cómo se cubren los criterios de evaluación

| Criterio | Peso | Se diseña en | Se mide o se verifica en |
|---|---|---|---|
| Tiempo de ejecución | 25 % | Bloque 3 | Bloque 6 |
| Consumo de memoria | 20 % | Bloque 3 | Bloque 6 |
| Rendimiento | 20 % | Bloque 3 | Bloque 6 |
| Calidad de código | 15 % | Bloque 4 | Bloque 5 (código) y Bloque 7 (cálculo) |
| Confiabilidad | 10 % | Bloque 2 (salidas esperadas y errores) | Bloque 5 (pruebas) |
| Uso funcional | 10 % | Bloque 2 (diseño) y Bloque 4 (reglas) | Bloque 7 (revisión automática) |

## Principios de equidad

Lo que se compara son los lenguajes, no la calidad de cada implementación. Por eso:

1. **Mismo diseño** en los tres: los mismos módulos y funciones, con nombres equivalentes.
2. **Misma complejidad algorítmica:** ninguna versión usa un algoritmo más costoso que las otras.
3. **Solo biblioteca estándar** de cada lenguaje.
4. **Mismas entradas** (generadas con semilla fija) y **la misma salida**, verificada carácter por carácter.
5. **Misma plataforma de ejecución:** el mismo equipo, el mismo JDK 21, `java -jar` con las mismas opciones
   y Clojure compilado por adelantado (AOT).
6. **Ejecuciones intercaladas y repetidas:** se reporta la mediana.
7. **Mismo instrumento por métrica** para los tres lenguajes.
