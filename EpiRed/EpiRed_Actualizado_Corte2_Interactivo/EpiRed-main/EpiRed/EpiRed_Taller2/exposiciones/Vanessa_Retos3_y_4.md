# Vanessa explica el respaldo y los ciclos negativos

Retos 3 y 4. Duración: 5 a 6 minutos con las demos. Objetivo: mostrar una ruta alternativa y detectar un subsidio inconsistente. Las preguntas y la chuleta son apoyo, no parte de la lectura completa.

## Lo que digo al empezar

Buenos días, a mí me correspondieron los retos tres y cuatro. Primero voy a buscar un respaldo para la ruta más rápida. Después mostraré una simulación económica separada. En esta segunda parte los pesos no son minutos de viaje.

## Reto 3 y lo que digo

En epired_taller2.py ya teníamos Grafo.Dijkstra y RutaDijkstra. Añadimos GenerarRutaConRespaldo, que los usa dos veces. Primero obtiene la ruta mínima por tiempo. Después crea una copia, retira solo los enlaces de esa ruta y vuelve a calcular.

```python
copia = grafo.copia()
for a, b in zip(primaria, primaria[1:]):
    copia.BorrarArco(a, b)
segunda = copia.Dijkstra(origen)
respaldo = copia.RutaDijkstra(segunda, destino)
```

Esto lo podemos explicar así: copia crea otra red con filas independientes. zip obtiene los pares consecutivos de la primaria. BorrarArco deshabilita cada enlace en ambos sentidos, porque la red es bidireccional. El segundo Dijkstra y RutaDijkstra encuentran el respaldo con lo que quedó.

Las rutas pueden compartir municipios, pero no enlaces. Para A, Medellín, hasta F, Caldas, la primaria es A-C-F y cuesta cincuenta minutos. El respaldo es A-D-E-F y cuesta sesenta y dos. Calculamos (62-50)/50 por 100: veinticuatro por ciento más.

Seguimos el procedimiento del parcial. No afirmamos optimizar el mejor par global de rutas disjuntas: buscamos la alternativa después de retirar la primaria elegida.

## Qué hago en la demostración del reto 3

1. En python main.py elijo 3, origen A y destino F. Muestro primaria 50 min, respaldo 62 min y diferencia 24 por ciento.
2. Repito 3 con A e I. Muestro A-G-H-I, 70 min, y leo la alerta exacta: “Red no redundante entre origen y destino”.
3. Elijo 7 para confirmar que la red original sigue igual, tanto cuando existe respaldo como cuando no.

Si el costo primario es cero, no calculamos porcentaje para evitar dividir por cero. Si origen y destino coinciden, la ruta es el mismo nodo y no hay traslado. Si no hay primaria, tampoco hay respaldo. Un ID inválido produce un mensaje claro.

<!-- salto -->

## Reto 4 y lo que digo

El Taller 2 ya tenía FloydWarshall y un booleano ciclo_negativo. Ahora añadimos crear_escenario_costos y DetectarAnomaliaDeCicloNegativo en el mismo epired_taller2.py. La primera prepara los datos y la segunda devuelve el booleano y los IDs diagnósticos.

Creamos una versión dirigida con los mismos municipios. Cada conexión original aporta dos arcos de diez unidades monetarias ficticias. Solo A hacia B recibe un subsidio; B hacia A sigue costando diez. No cambiamos la matriz de minutos.

En el control, el bono es quince y A hacia B queda en menos cinco. Volver cuesta diez: la vuelta suma cinco y no aparece ciclo negativo. En el otro escenario, el bono es cuarenta y cinco y A hacia B queda en menos treinta y cinco. A-B-C-A suma menos treinta y cinco más diez más diez: menos quince. Repetir esa vuelta reduciría el costo sin límite dentro del modelo.

## Código real que muestro

Primero ejecutamos Grafo.FloydWarshall. Sus tres bucles prueban si ir de i a j pasando por k mejora el costo. Después revisamos su matriz final:

```python
diagnosticos = [ids[i] for i in range(n) if matriz_distancias[i][i] < 0]
return {"hay_anomalia": bool(diagnosticos), "ids_diagnosticos": diagnosticos}
```

Esto lo podemos explicar así: la diagonal representa volver al mismo nodo. Si alguna casilla es menor que cero, guardo su ID y el booleano resulta verdadero. La función recibe la matriz después de Floyd, no la matriz inicial.

No usamos Dijkstra con pesos negativos. Tampoco interpretamos los resultados de Floyd con ciclo negativo como costos mínimos válidos: el método RutaFloyd ya bloqueaba esas reconstrucciones en el taller.

## Qué hago en la demostración del reto 4

1. Elijo 4. Muestro el control con A hacia B igual a −5 UM: anomalía False y diagonal cero.
2. Muestro el caso de −35 UM: anomalía True y alerta de inconsistencia operativa o beneficio infinito.
3. Señalo que salen los IDs A a J. Digo: “Son evidencia de recorridos cerrados negativos. No significa que todos pertenezcan al ciclo simple exacto A-B-C-A; el efecto se propaga por la red”.
4. Elijo 7 y confirmo que los tiempos originales no cambiaron. Para cerrar la validación, ejecuto python -m unittest discover -s tests -v.

<!-- salto -->

## Preguntas y respuestas cortas

¿Las rutas pueden compartir un municipio? Sí; solo está prohibido compartir aristas. Las pruebas incluyen un vértice interno compartido.

¿Cómo recuperan las aristas retiradas? No tocamos el original: solo retiramos enlaces de una copia.

¿Por qué separar costos y minutos? El subsidio reduce dinero simulado; un viaje no puede durar minutos negativos.

¿Una arista negativa siempre produce un ciclo negativo? No. El control con −5 demuestra que la vuelta completa puede seguir siendo positiva.

¿Los IDs diagnósticos indican el ciclo simple exacto? No. Indican diagonales negativas detectadas; no reconstruyen ese ciclo.

## Lo que digo al cerrar el equipo

El reto tres cuesta O(V²), porque usa dos Dijkstra de matriz, y ocupa O(V²) por la copia. El cuarto cuesta O(V³) por los tres bucles de Floyd y O(V²) de memoria. La inspección de diagonal sola es lineal; nuestra función además valida la matriz.

Con esto terminamos los cuatro retos sobre EpiRed. Juan mostró capacidad, Sofía conectividad y yo respaldo y costos inconsistentes. Conservamos los datos originales, añadimos solo los datos ficticios necesarios y comprobamos los resultados con pruebas. Gracias; quedamos atentos a las preguntas.

## Lo que los tres debemos recordar

Juan: capacidad máxima A-D-E-F, 55 unidades por viaje. Sofía: sin G quedan ABCDEF, HI y J; sin H queda I aislado. Ambos resultados se calculan, no están fijados como respuesta.

Orden: Juan usa 6 y 1 con A,F; Sofía, 2 y 7; yo, 3 con A,F, 3 con A,I, 4 y 7. Para repetir todo sin interacción: python main.py --demo.

## Chuleta final

Reto 3: A-C-F = 50 min; A-D-E-F = 62 min; aumento 24 por ciento. A-I: no hay respaldo.

Reto 4: 10 UM por arco; A→B=−5 sin ciclo o −35 con ciclo. A-B-C-A=−15 UM en la anomalía. IDs diagnósticos A a J.

Archivo: epired_taller2.py. Funciones: GenerarRutaConRespaldo y DetectarAnomaliaDeCicloNegativo. Menú: 3, 4 y 7.

Cierre: “Terminamos los cuatro retos y verificamos que la red sigue intacta. Gracias”.
