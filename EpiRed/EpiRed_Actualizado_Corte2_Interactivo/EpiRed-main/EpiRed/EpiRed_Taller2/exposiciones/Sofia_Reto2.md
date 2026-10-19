# Sofía explica los municipios críticos

Reto 2. Duración: 4 a 5 minutos con la demo. Objetivo: probar la salida de cada municipio y detectar si divide la red. Las preguntas y la chuleta son apoyo para estudiar.

## Lo que digo al empezar

Buenos días, a mí me correspondió el reto dos. Juan explicó cómo elegir capacidad. Yo voy a mostrar qué pasa si un municipio deja de participar en la red. Mi pregunta es si los demás siguen conectados entre sí.

Un grupo de municipios que pueden alcanzarse es una componente conexa. Si un municipio queda solo, es un aislado. En este reto no sumamos minutos ni capacidades: solo miramos si existen conexiones.

## Lo que digo sobre la versión anterior

En EpiRed-Grafo/grafo.py ya teníamos BFS, RecorridoAnchura y Componentes. La interfaz del Taller 1 permitía quitar G manualmente. Ahora añadimos componentes y DetectarPuntosCriticosDeFalla en epired_taller2.py para ensayar todos los municipios automáticamente. Adaptamos BFS a la matriz del Taller 2, donde inf indica ausencia de enlace.

## Lo que digo sobre el recorrido

BFS usa una cola: saco el primer nodo, reviso sus vecinos y agrego los que todavía no he visitado. Un conjunto de visitados evita repetirlos. Cuando la cola se vacía, tengo un grupo. Si quedan nodos pendientes, comienzo otra búsqueda para obtener los demás grupos.

Primero cuento las componentes originales. Después recorro cada municipio y vuelvo a contar, ignorando ese ID. No borro su fila ni sus enlaces: la búsqueda no lo usa como inicio ni como vecino. Si aparecen más componentes que al principio, lo marco como crítico.

```python
for id in grafo.ids:
    grupos = componentes(grafo, excluido=id)
    aislados = [g[0] for g in grupos if len(g) == 1]
    es_critico = len(grupos) > len(inicial)
    if es_critico:
        criticos.append(id)
```

Esto lo podemos explicar así: el for prueba todos los IDs. componentes calcula los grupos sin ese municipio. Un grupo de un nodo es un aislado. El if compara con la cantidad inicial y guarda los críticos. G y H no están escritos en esta decisión; el algoritmo los encuentra.

## Lo que digo sobre los casos pequeños

La comparación sirve incluso si la red ya estaba desconectada. Si antes había dos grupos y después hay tres, detectamos una nueva división. También separamos los aislados nuevos de los que ya existían.

En un grafo de dos nodos unidos, quitar uno deja un aislado, pero seguimos con una componente. Lo informamos como aislado sin marcarlo crítico, porque seguimos la regla de aumento de componentes. En un grafo vacío o de un solo nodo no aparecen falsos críticos.

<!-- salto -->

## Qué hago y qué digo en la demostración

1. En el menú de python main.py elijo 2. No escribo un ID: el programa prueba los diez municipios.
2. Señalo que al principio existe una sola componente con todos los nodos.
3. Muestro “Sin G: ABCDEF | HI | J”. Digo: “Al retirar Copacabana quedan tres grupos. Medellín a Caldas siguen unidos; Girardota y Barbosa forman otro; Rionegro queda aislado”.
4. Muestro “Sin H: ABCDEFGJ | I”. Digo: “Al retirar Girardota, Barbosa queda aislado. Pasamos de una a dos componentes”.
5. Señalo la lista final G y H. Después elijo 7 para mostrar que los diez nodos, trece conexiones y sus valores siguen iguales.

## Lo que digo al terminar

La función devuelve criticos y también ensayos, con los grupos de cada retiro para poder explicar la respuesta. Como usamos matrices, un BFS completo cuesta O(V²). Lo repetimos para V municipios, por eso el reto completo cuesta O(V³). Guardar los resultados de todos los ensayos ocupa O(V²).

Así comprobamos automáticamente que Copacabana y Girardota son críticos en nuestro ejemplo. La red no necesita restauración porque nunca la modificamos. Ahora Vanessa mostrará las rutas de respaldo y una simulación de costos negativos.

## Preguntas y respuestas cortas

¿Por qué BFS y no Dijkstra? Porque quiero saber quién está conectado, no cuál ruta tarda menos.

¿Por qué comparar con el estado inicial? Porque la red podría estar desconectada desde antes.

¿Tener muchos vecinos hace crítico a un municipio? No necesariamente. Lo que lo demuestra es que su retiro aumente las componentes.

¿Cómo sabemos que el grafo queda intacto? componentes solo lee la matriz; la opción 7 y test_reto2.py comparan el estado completo antes y después.

## Lo que los tres debemos recordar

Juan encuentra A-D-E-F con capacidad 55. Vanessa obtiene primaria A-C-F de 50 min y respaldo A-D-E-F de 62 min, 24 por ciento más. Su reto cuatro usa costos económicos dirigidos, no minutos negativos.

Orden: Juan usa 6 y 1 con A,F; yo, 2 y 7; Vanessa, 3 con A,F, 3 con A,I, 4 y 7. Para comprobar todo: python -m unittest discover -s tests -v.

## Chuleta final

BFS: cola y visitados. Crítico: aumenta el número de componentes al excluirlo.

Sin G: ABCDEF | HI | J. Sin H: ABCDEFGJ | I. Resultado: G y H.

Archivo: epired_taller2.py. Funciones: componentes y DetectarPuntosCriticosDeFalla. Menú: 2 y luego 7.

Frase de enlace: “Vanessa continúa con el respaldo y los costos negativos”.
