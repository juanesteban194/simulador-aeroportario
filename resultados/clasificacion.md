# Clasificación automática

Generado por `experimento/clasificar.py` con los criterios de `docs/04_criterios.md`.

## Posiciones

| Posición | Lenguaje | Tiempo (25%) | Memoria (20%) | Rendimiento (20%) | Calidad (15%) | Confiabilidad (10%) | Uso funcional (10%) | **Final** |
|---|---|---|---|---|---|---|---|---|
| 1 | Java | 95.74 | 88.53 | 100.00 | 86.22 | 100.00 | 87.77 | **93.35** |
| 2 | Scala | 88.87 | 95.70 | 86.66 | 85.06 | 100.00 | 100.00 | **91.45** |
| 3 | Clojure | 78.64 | 75.97 | 58.71 | 72.78 | 100.00 | 81.35 | **75.65** |

## Por qué cada lenguaje quedó en su posición

**1.º Java** (93.35 puntos). Es el mejor en Tiempo, Rendimiento, Calidad. Los tres empatan en Confiabilidad. Pierde 7.2 puntos en Memoria (le restan 1.43 al final); 12.2 puntos en Uso funcional (le restan 1.22 al final).

**2.º Scala** (91.45 puntos). Es el mejor en Memoria, Uso funcional. Los tres empatan en Confiabilidad. Pierde 13.3 puntos en Rendimiento (le restan 2.67 al final); 6.9 puntos en Tiempo (le restan 1.72 al final); 1.2 puntos en Calidad (le restan 0.17 al final).

**3.º Clojure** (75.65 puntos). No es el mejor en ningún criterio. Los tres empatan en Confiabilidad. Pierde 41.3 puntos en Rendimiento (le restan 8.26 al final); 17.1 puntos en Tiempo (le restan 4.27 al final); 19.7 puntos en Memoria (le restan 3.94 al final); 13.4 puntos en Calidad (le restan 2.02 al final); 18.7 puntos en Uso funcional (le restan 1.87 al final).

## Prueba de solidez

La clasificación se recalcula con pesos iguales y quitando un criterio a la vez (su peso se reparte entre los demás en proporción a sus pesos).

| Variante | 1.º | 2.º | 3.º | Puntaje del 1.º |
|---|---|---|---|---|
| Pesos del proyecto | Java | Scala | Clojure | 93.35 |
| Pesos iguales | Java | Scala | Clojure | 93.04 |
| Sin Tiempo | Java | Scala | Clojure | 92.55 |
| Sin Memoria | Java | Scala | Clojure | 94.56 |
| Sin Rendimiento | Scala | Java | Clojure | 92.64 |
| Sin Calidad | Java | Scala | Clojure | 94.61 |
| Sin Confiabilidad | Java | Scala | Clojure | 92.61 |
| Sin Uso funcional | Java | Scala | Clojure | 93.97 |

**Java gana en 6 de las 7 variantes.** La decisión depende en parte de los pesos: ver las variantes en las que cambia el ganador.
