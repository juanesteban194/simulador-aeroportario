# Resumen de la medición

Mediana de las rondas medidas (sin el calentamiento). Entre corchetes: mínimo – máximo; RIC = rango intercuartílico. Detalle por ejecución en `crudos/`.

## V1 · 1.000 vuelos

| Lenguaje | t_operaciones (ms) | t_proceso (ms) | Vuelos/s | Memoria máx. (MB) | Correctas |
|---|---|---|---|---|---|
| java | 285 [238 – 331] RIC 65 | 365 [326 – 423] RIC 56 | 2741 [2363 – 3068] RIC 413 | 62 [60 – 76] RIC 14 | 10/10 |
| scala | 339 [291 – 379] RIC 17 | 539 [484 – 590] RIC 31 | 1855 [1695 – 2065] RIC 103 | 78 [77 – 92] RIC 2 | 10/10 |
| clojure | 212 [183 – 251] RIC 37 | 838 [760 – 929] RIC 63 | 1193 [1077 – 1316] RIC 90 | 106 [102 – 111] RIC 3 | 10/10 |

## V2 · 10.000 vuelos

| Lenguaje | t_operaciones (ms) | t_proceso (ms) | Vuelos/s | Memoria máx. (MB) | Correctas |
|---|---|---|---|---|---|
| java | 665 [619 – 888] RIC 89 | 775 [727 – 999] RIC 83 | 12909 [10015 – 13754] RIC 1336 | 171 [146 – 172] RIC 9 | 10/10 |
| scala | 755 [638 – 843] RIC 35 | 961 [883 – 1073] RIC 63 | 10408 [9322 – 11326] RIC 666 | 151 [132 – 169] RIC 30 | 10/10 |
| clojure | 759 [666 – 823] RIC 41 | 1429 [1336 – 1482] RIC 68 | 6999 [6745 – 7487] RIC 333 | 185 [175 – 203] RIC 6 | 10/10 |

## V3 · 100.000 vuelos

| Lenguaje | t_operaciones (ms) | t_proceso (ms) | Vuelos/s | Memoria máx. (MB) | Correctas |
|---|---|---|---|---|---|
| java | 2419 [2280 – 2627] RIC 136 | 2594 [2460 – 2805] RIC 123 | 38553 [35652 – 40657] RIC 1833 | 741 [660 – 759] RIC 41 | 10/10 |
| scala | 2554 [2342 – 2905] RIC 66 | 2839 [2600 – 3188] RIC 40 | 35222 [31370 – 38468] RIC 498 | 599 [576 – 627] RIC 26 | 10/10 |
| clojure | 3311 [3103 – 3566] RIC 116 | 4041 [3884 – 4462] RIC 128 | 24747 [22414 – 25745] RIC 772 | 659 [604 – 955] RIC 34 | 10/10 |

## V4 · 1.000.000 vuelos

| Lenguaje | t_operaciones (ms) | t_proceso (ms) | Vuelos/s | Memoria máx. (MB) | Correctas |
|---|---|---|---|---|---|
| java | 12047 [11183 – 12907] RIC 412 | 12819 [11953 – 13751] RIC 390 | 78012 [72722 – 83660] RIC 2390 | 3065 [2865 – 3347] RIC 195 | 10/10 |
| scala | 13001 [12286 – 14062] RIC 992 | 13921 [13194 – 14903] RIC 1042 | 71833 [67101 – 75792] RIC 5429 | 3238 [2630 – 3532] RIC 282 | 10/10 |
| clojure | 19806 [19155 – 20428] RIC 489 | 21329 [20785 – 21952] RIC 558 | 46884 [45553 – 48113] RIC 1237 | 3883 [3765 – 4033] RIC 120 | 10/10 |

## C1 · 100.000 vuelos

| Lenguaje | t_operaciones (ms) | t_proceso (ms) | Vuelos/s | Memoria máx. (MB) | Correctas |
|---|---|---|---|---|---|
| java | 2529 [2312 – 3093] RIC 137 | 2692 [2482 – 3282] RIC 136 | 37145 [30474 – 40288] RIC 1835 | 738 [696 – 755] RIC 40 | 10/10 |
| scala | 2585 [2357 – 2930] RIC 182 | 2852 [2612 – 3256] RIC 154 | 35062 [30710 – 38285] RIC 1934 | 597 [578 – 620] RIC 19 | 10/10 |
| clojure | 3288 [3080 – 3798] RIC 312 | 4044 [3759 – 4636] RIC 324 | 24729 [21571 – 26600] RIC 1889 | 823 [637 – 921] RIC 209 | 10/10 |

## X1 · 100.000 vuelos

| Lenguaje | t_operaciones (ms) | t_proceso (ms) | Vuelos/s | Memoria máx. (MB) | Correctas |
|---|---|---|---|---|---|
| java | 2408 [2204 – 2572] RIC 65 | 2599 [2378 – 2779] RIC 53 | 38483 [35985 – 42046] RIC 778 | 734 [682 – 750] RIC 32 | 10/10 |
| scala | 2475 [2418 – 2525] RIC 84 | 2769 [2711 – 2839] RIC 67 | 36116 [35226 – 36893] RIC 874 | 596 [575 – 619] RIC 14 | 10/10 |
| clojure | 3280 [2859 – 3646] RIC 233 | 4083 [3585 – 4370] RIC 298 | 24494 [22886 – 27897] RIC 1820 | 813 [601 – 1006] RIC 276 | 10/10 |
