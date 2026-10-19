# Juan explica la capacidad y abre la exposición

Reto 1 e integración. Duración: 4 a 5 minutos con la demo. Objetivo: explicar la ruta que transporta más suministros. Estudia el guion; las preguntas y la chuleta son apoyo, no hay que leerlas todas en clase.

## Lo que digo al empezar

Buenos días. Somos Juan, Sofía y Vanessa. Nuestro proyecto es EpiRed, del área de salud y epidemiología. Conservamos diez municipios y trece conexiones del taller. Vamos a mostrar los cuatro retos del parcial. Los datos son ficticios y no representan una red hospitalaria real.

Buenos días, a mí me correspondió el reto uno y unir la solución. Cada nodo representa un municipio y cada arista una conexión en ambos sentidos. El peso sigue siendo el tiempo en minutos. Para mi reto añadimos la capacidad: unidades de suministros médicos por viaje. Los reportes epidemiológicos se conservan, pero no se usan para calcular las rutas.

## Lo que digo sobre lo que cambiamos

Trabajamos sobre epired_taller2.py, que ya estaba en nuestro ZIP. Conservamos su clase Grafo y los métodos Dijkstra, RutaDijkstra, FloydWarshall y RutaFloyd. Añadimos las cuatro funciones del parcial en ese mismo archivo y un main.py con el menú.

En el Taller 1, cero significaba que no había conexión. Elegimos la representación del Taller 2: infinito para ausencia y cero en la diagonal. Los tiempos originales siguen en matriz; las capacidades nuevas van en capacidades. Union recibe ambos datos y evita valores no permitidos.

## Lo que digo sobre mi algoritmo

La ruta más rápida no siempre transporta más. De A, Medellín, a F, Caldas, A-C-F tarda cincuenta minutos. Sus capacidades son veinte y quince, así que toda la ruta queda limitada a quince unidades por viaje.

Mi función RutaMayorCapacidad busca el cuello de botella más grande. Empieza con infinito en el origen, porque aún no atravesamos ningún enlace, y cero en los demás. Elige el pendiente con mayor capacidad, revisa sus vecinos y guarda una mejora cuando la encuentra.

```python
for vecino, capacidad in enumerate(grafo.capacidades[actual]):
    candidato = min(mejores[actual], capacidad)
    if not visitados[vecino] and candidato > mejores[vecino]:
        mejores[vecino] = candidato
        anteriores[vecino] = actual
```

Esto lo podemos explicar así: min calcula el límite al agregar la siguiente arista. El if pregunta si ese límite mejora lo que teníamos. Si mejora, guardamos la capacidad y el nodo anterior para reconstruir la ruta. No sumamos capacidades. Los empates se resuelven de forma estable por el orden de los IDs.

<!-- salto -->

## Qué hago y qué digo en la demostración

1. Abro la terminal en EpiRed/EpiRed_Taller2 y ejecuto python main.py. Leo brevemente la ficha de dominio y elijo 6 para mostrar IDs y nombres.
2. Elijo 1, escribo A y luego F. Señalo A-D-E-F: Medellín, Envigado, Sabaneta y Caldas.
3. Digo: “Las capacidades son 70, 60 y 55. min(70,60)=60 y min(60,55)=55. El cuello de botella es 55 unidades por viaje. Esta ruta tarda 62 minutos; la mínima por tiempo es A-C-F y tarda 50”.
4. Elijo 7. Digo: “El programa compara IDs, tiempos y capacidades: la red original sigue intacta”.

## Lo que digo al terminar

En main.py reunimos las cuatro consultas para no ejecutar un archivo distinto por reto. Mi parte usa O(V²) de tiempo: para cada nodo revisamos pendientes y vecinos en una matriz. Usa O(V) de memoria adicional. Ahora Sofía va a mostrar qué municipios pueden dividir la red cuando fallan.

## Preguntas y respuestas cortas

¿Por qué no basta Dijkstra normal? Porque busca la menor suma de tiempos; aquí buscamos el mayor mínimo de capacidad.

¿De dónde salen las capacidades? Las añadimos para el parcial y están en CAPACIDADES. Son ficticias y no se deducen de los minutos.

¿Qué pasa si no hay ruta? Devuelve lista vacía y capacidad cero. Si el ID no existe, el menú muestra el error.

¿Y si origen y destino coinciden? Devuelve ese ID e inf como convención sin aristas. No significa transporte físico infinito.

## Lo que los tres debemos recordar

Sofía obtiene G y H como críticos. Vanessa obtiene respaldo A-D-E-F de 62 minutos, un 24 por ciento más que la primaria; después detecta costos económicos negativos con Floyd. Todos trabajamos sobre la misma base, sin mezclar minutos con capacidades ni subsidios.

Orden: Juan usa 6 y 1 con A,F; Sofía, 2 y 7; Vanessa, 3 con A,F, 3 con A,I, 4 y 7. Para repetir todo: python main.py --demo. Las pruebas se ejecutan con python -m unittest discover -s tests -v.

## Chuleta final

Idea: máximo de los mínimos. Ejemplo: A-D-E-F, capacidad 55. A-C-F es más rápida, 50 min, pero su capacidad es 15.

Archivo: epired_taller2.py. Función: RutaMayorCapacidad. Integración: main.py. Menú: 1, A, F; luego 7.

Frase de enlace: “Ahora Sofía explica los municipios críticos”.
