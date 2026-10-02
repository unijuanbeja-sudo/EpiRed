# EpiRed · Taller 2 de caminos mínimos

Una implementación en **un solo archivo Python**, basada en la red del Taller 1. Esta guía sirve para estudiar y exponer: primero la teoría, después el código por bloques.

## 1. Qué entregar y cómo ejecutarlo

- `Informe_Taller2_EpiRed.docx`: solución escrita de las fases 1, 2 y 3.
- `epired_taller2.py`: toda la implementación, demostración y comprobaciones.
- `README.md`: esta guía de estudio.

Requiere Python 3.10 o superior. No hay paquetes externos que instalar. Abre la terminal en esta carpeta:

```console
python epired_taller2.py
python epired_taller2.py A E
python epired_taller2.py I J
python epired_taller2.py --verificar
```

En Windows también puedes usar `py` en lugar de `python`. Es una demostración por consola; usa la terminal para conservar los resultados en pantalla.

## 2. Qué conservamos del Taller 1

Conservamos los 10 municipios, las 13 conexiones y sus pesos de `datos.py`, y adaptamos la matriz, `Union` y la idea de `CaminoMinimo` de `grafo.py`. El Dijkstra anterior devolvía una ruta puntual; ahora devuelve todas las distancias desde un origen y sus predecesores. Añadimos Floyd-Warshall y reconstrucción de caminos.

Concentramos lo necesario para este taller en un archivo. No reproducimos la interfaz gráfica, BFS, DFS ni la edición epidemiológica del anterior. Los tiempos siguen siendo ficticios; no se usan reportes de casos para ponderar las rutas. En la matriz nueva, ausencia de arista = `inf`; diagonal = 0. Esto permite aristas de peso cero.

El enunciado enumera los resultados SSSP y APSP, pero no muestra firmas concretas ni campos. Por eso usamos métodos con nombres claros y diccionarios sencillos; sus campos se explican abajo.

## 3. Teoría antes de mirar código

Un **grafo** representa elementos y sus conexiones. Los vértices son municipios; las aristas son conexiones; el peso es el tiempo de traslado. Un camino mínimo tiene la menor **suma de pesos**, no necesariamente menos conexiones. Una matriz usa una fila y una columna por nodo. `inf` significa que no hay una ruta conocida; `None` significa que no hay predecesor.

**Relajar** es preguntar: “¿Llegar pasando por este nodo cuesta menos?”. Si sí, reemplazamos la distancia y guardamos de dónde llegamos.

### Dijkstra

Resuelve SSSP (caminos mínimos desde una sola fuente). Empieza con distancia 0 en el origen e infinito en los demás. Elige el pendiente más cercano, lo fija y revisa sus vecinos. Repite hasta terminar. Es **voraz** porque toma la mejor opción disponible en cada selección. Con la matriz y búsqueda lineal cuesta O(V²).

No admite pesos negativos: en el ejemplo dirigido A → B = 2, A → C = 5 y C → B = −4, fijaría B demasiado pronto, aunque A → C → B cuesta 1. Nuestro método rechaza cualquier peso negativo antes de comenzar.

### Floyd-Warshall

Resuelve APSP (caminos mínimos entre todos los pares). Para cada intermediario k, pregunta si i → k → j mejora i → j. Es **programación dinámica** porque amplía por etapas el conjunto de intermediarios permitidos y aprovecha soluciones anteriores.

La recurrencia del taller es:

`D^(k)[i][j] = min(D^(k−1)[i][j], D^(k−1)[i][k] + D^(k−1)[k][j])`

Los tres ciclos producen O(V³) tiempo. Las matrices ocupan O(V²) memoria. Admite aristas negativas; si aparece `D[i][i] < 0`, existe un ciclo negativo. Para los pares que pueden aprovechar ese ciclo no hay un mínimo finito. Esta implementación bloquea toda reconstrucción si encuentra uno.

### Cuál elegir

Para un origen puntual, Dijkstra. Para muchísimas consultas en esta red pequeña y estable, precalcular Floyd una vez y consultar su matriz. Leer una distancia cuesta O(1); reconstruir una ruta cuesta O(L), donde L es su número de nodos. Si cambia el grafo, hay que recalcular. No se midió rendimiento de 100 000 consultas por segundo y no se promete esa capacidad.

### Predecesores

El predecesor es el nodo inmediatamente anterior al destino. Para A → C → D → E, retrocedemos `E ← D ← C ← A` e invertimos. Dijkstra guarda un vector por origen. Floyd guarda una matriz: en `Pi[i][j]`, el origen i queda fijo mientras retrocedemos desde j.

## 4. Traza manual que debes entender

El informe usa A, C, D y E y las aristas A–C = 15, A–D = 30, C–D = 10 y D–E = 12. Es un subgrafo de la red original. El orden de vectores y matrices es **C, D, A, E**, elegido para mostrar mejoras en las primeras dos etapas de Floyd.

| Actual | Visitados | D en orden C,D,A,E | P en orden C,D,A,E |
|---|---|---|---|
| Inicial | {} | ∞, ∞, 0, ∞ | –, –, –, – |
| A | A | 15, 30, 0, ∞ | A, A, –, – |
| C | A,C | 15, 25, 0, ∞ | A, C, –, – |
| D | A,C,D | 15, 25, 0, 37 | A, C, –, D |
| E | A,C,D,E | 15, 25, 0, 37 | A, C, –, D |

Floyd empieza con pesos directos. Con k = 1 (C), A → D y D → A bajan de 30 a 25. Con k = 2 (D), C ↔ E pasa a 22 y A ↔ E a 37. Las matrices completas D y Pi están en el informe. No confundas k = 1 del informe con el índice 1 de Python: Python empieza en 0.

## 5. Contratos de los resultados

```python
grafo = crear_red()
uno = grafo.Dijkstra("A")
print(uno["distancias"]["F"])          # 50.0
print(uno["predecesores"]["F"])       # C
print(grafo.RutaDijkstra(uno, "F"))     # ['A', 'C', 'F']
todos = grafo.FloydWarshall()
print(todos["distancias"][0][5])       # 50.0: A y F
print(grafo.RutaFloyd(todos, "A", "F"))
```

En Floyd, `ids` identifica filas y columnas; `predecesores` contiene índices, no letras. `ciclo_negativo` es un booleano. Los nodos inalcanzables conservan infinito y sus rutas son `[]`. Una ruta al mismo origen devuelve `[origen]` y cuesta 0, siempre que no se bloquee por ciclo negativo. Los resultados deben recalcularse si modificas la red.

## 6. Código explicado por bloques

Los números corresponden al archivo entregado. Los comentarios `BLOQUE` permiten encontrar cada parte aunque después agregues líneas. En los fragmentos, los números de la izquierda son solo una ayuda de lectura: no se copian al programa.

### BLOQUE 1: datos originales y herramientas de Python · líneas 7 a 23

`inf` representa infinito: todavía no existe una ruta conocida. `isfinite` permite rechazar pesos infinitos y NaN. `sys` lee los argumentos de la terminal. `MUNICIPIOS` relaciona IDs con nombres; cada tupla de `CONEXIONES` contiene origen, destino y minutos. Son los mismos 10 nodos y 13 enlaces del Taller 1.

```text
  7 | # BLOQUE 1: datos originales y herramientas de Python
  8 | from math import inf, isfinite
  9 | import sys
 10 | 
 11 | MUNICIPIOS = {
 12 |     "A": "Medellín", "B": "Bello", "C": "Itagüí", "D": "Envigado",
 13 |     "E": "Sabaneta", "F": "Caldas", "G": "Copacabana", "H": "Girardota",
 14 |     "I": "Barbosa", "J": "Rionegro",
 15 | }
 16 | CONEXIONES = [
 17 |     ("A", "B", 20), ("A", "C", 15), ("A", "D", 30), ("B", "C", 30),
 18 |     ("C", "D", 10), ("D", "E", 12), ("E", "F", 20), ("C", "F", 35),
 19 |     ("A", "G", 35), ("B", "G", 20), ("G", "H", 15), ("H", "I", 20),
 20 |     ("G", "J", 40),
 21 | ]
 22 | 
 23 |
```

### BLOQUE 2: grafo con matriz de pesos · líneas 24 a 47

`__init__` crea el objeto; `self` representa ese grafo. `list(ids)` guarda el orden. `set` sirve para detectar IDs repetidos. La matriz tiene cero cuando `i == j` e infinito en las otras celdas. Las comprensiones construyen una lista nueva por fila. `_indice` traduce un ID a su posición y lanza `ValueError` si no existe. `Union` convierte el peso a número, rechaza bucles y valores no finitos, y escribe la celda. Si el grafo no es dirigido también escribe la celda inversa. Una llamada posterior sobre la misma conexión reemplaza su peso. El modo dirigido se utiliza en los ejemplos de pesos negativos.

```text
 24 | # BLOQUE 2: grafo con matriz de pesos
 25 | class Grafo:
 26 |     def __init__(self, ids, dirigido=False):
 27 |         self.ids = list(ids)
 28 |         if len(set(self.ids)) != len(self.ids):
 29 |             raise ValueError("No se permiten IDs repetidos.")
 30 |         self.dirigido = dirigido
 31 |         n = len(self.ids)
 32 |         self.matriz = [[0 if i == j else inf for j in range(n)] for i in range(n)]
 33 | 
 34 |     def _indice(self, id):
 35 |         if id not in self.ids:
 36 |             raise ValueError(f"El nodo {id} no existe.")
 37 |         return self.ids.index(id)
 38 | 
 39 |     def Union(self, origen, destino, peso):
 40 |         i, j = self._indice(origen), self._indice(destino)
 41 |         peso = float(peso)
 42 |         if i == j or not isfinite(peso):
 43 |             raise ValueError("Usa nodos diferentes y un peso finito.")
 44 |         self.matriz[i][j] = peso
 45 |         if not self.dirigido:
 46 |             self.matriz[j][i] = peso
 47 |
```

### BLOQUE 3: Dijkstra desde un origen hacia todos · líneas 48 a 73

`inicio` es el índice del origen. `any` revisa si existe algún peso negativo y lo rechaza. Las tres listas guardan distancias, predecesores y estados de visita. Solo el origen empieza en cero. El ciclo externo realiza como máximo n selecciones. El primer ciclo interno busca el nodo no visitado de menor distancia; en empate gana el primero en el orden de IDs. Si no queda un nodo alcanzable, `break` termina. Después se marca el actual y se revisa cada posible vecino. `nuevo` suma el costo hasta el actual y el peso hacia el vecino. El `if` exige que el vecino no esté fijado y que haya una mejora estricta. Solo entonces actualiza distancia y predecesor. `zip` une IDs con valores para devolver dos diccionarios. Ejemplo: al procesar C desde A, `nuevo = 15 + 10 = 25`, así que D deja de valer 30.

```text
 48 |     # BLOQUE 3: Dijkstra desde un origen hacia todos
 49 |     def Dijkstra(self, origen):
 50 |         inicio = self._indice(origen)
 51 |         if any(peso < 0 for fila in self.matriz for peso in fila):
 52 |             raise ValueError("Dijkstra no admite pesos negativos.")
 53 |         n = len(self.ids)
 54 |         distancias = [inf] * n
 55 |         predecesores = [None] * n
 56 |         visitados = [False] * n
 57 |         distancias[inicio] = 0
 58 |         for _ in range(n):
 59 |             actual = None
 60 |             for i in range(n):
 61 |                 if not visitados[i] and (actual is None or distancias[i] < distancias[actual]):
 62 |                     actual = i
 63 |             if actual is None or distancias[actual] == inf:
 64 |                 break
 65 |             visitados[actual] = True
 66 |             for vecino in range(n):
 67 |                 nuevo = distancias[actual] + self.matriz[actual][vecino]
 68 |                 if not visitados[vecino] and nuevo < distancias[vecino]:
 69 |                     distancias[vecino] = nuevo
 70 |                     predecesores[vecino] = self.ids[actual]
 71 |         return {"origen": origen, "distancias": dict(zip(self.ids, distancias)),
 72 |                 "predecesores": dict(zip(self.ids, predecesores))}
 73 |
```

### BLOQUE 4: reconstruir una ruta de Dijkstra · líneas 74 a 85

Primero valida el destino. Si su distancia es infinito, devuelve `[]`. En caso contrario empieza en el destino y agrega sus predecesores hasta llegar a `None`, que corresponde al origen. `ruta[::-1]` invierte la lista. Para E, construye E, D, C, A y devuelve A, C, D, E. Si origen y destino coinciden, devuelve una lista con ese único nodo.

```text
 74 |     # BLOQUE 4: reconstruir una ruta de Dijkstra
 75 |     def RutaDijkstra(self, resultado, destino):
 76 |         self._indice(destino)
 77 |         if resultado["distancias"][destino] == inf:
 78 |             return []
 79 |         ruta = []
 80 |         actual = destino
 81 |         while actual is not None:
 82 |             ruta.append(actual)
 83 |             actual = resultado["predecesores"][actual]
 84 |         return ruta[::-1]
 85 |
```

### BLOQUE 5: Floyd-Warshall para todos los pares · líneas 86 a 105

`fila[:]` copia cada fila para no modificar la matriz original. La matriz de predecesores empieza en `None`; si hay arista directa de i a j, su predecesor es i. El orden de los tres ciclos es fundamental: k (intermedio), i (origen), j (destino). `nuevo` compara la ruta i → k → j con la distancia actual. Cuando mejora, se copia el predecesor de k → j, porque interesa el último nodo antes de j. El cálculo con infinito no crea rutas falsas: infinito más un peso finito sigue siendo infinito. La diagonal negativa activa `ciclo_negativo`. Se devuelven matrices y el orden de sus índices. La actualización sobre la misma matriz es la versión habitual de Floyd; sin ciclos negativos conserva la recurrencia por etapas.

```text
 86 |     # BLOQUE 5: Floyd-Warshall para todos los pares
 87 |     def FloydWarshall(self):
 88 |         n = len(self.ids)
 89 |         distancias = [fila[:] for fila in self.matriz]
 90 |         predecesores = [[None] * n for _ in range(n)]
 91 |         for i in range(n):
 92 |             for j in range(n):
 93 |                 if i != j and distancias[i][j] != inf:
 94 |                     predecesores[i][j] = i
 95 |         for k in range(n):
 96 |             for i in range(n):
 97 |                 for j in range(n):
 98 |                     nuevo = distancias[i][k] + distancias[k][j]
 99 |                     if nuevo < distancias[i][j]:
100 |                         distancias[i][j] = nuevo
101 |                         predecesores[i][j] = predecesores[k][j]
102 |         ciclo_negativo = any(distancias[i][i] < 0 for i in range(n))
103 |         return {"ids": self.ids[:], "distancias": distancias,
104 |                 "predecesores": predecesores, "ciclo_negativo": ciclo_negativo}
105 |
```

### BLOQUE 6: reconstruir una ruta de Floyd-Warshall · líneas 106 a 119

Si hay un ciclo negativo, lanza un error antes de reconstruir: esta versión bloquea todas las rutas por sencillez, aunque algunos pares podrían no estar afectados. Convierte IDs a índices, comprueba si el destino es alcanzable y retrocede por la fila del origen en la matriz de predecesores. Finalmente invierte la ruta. Este método debe recibir un resultado calculado para la misma red, sin modificarla después.

```text
106 |     # BLOQUE 6: reconstruir una ruta de Floyd-Warshall
107 |     def RutaFloyd(self, resultado, origen, destino):
108 |         if resultado["ciclo_negativo"]:
109 |             raise ValueError("Hay un ciclo negativo: no se reconstruyen rutas.")
110 |         i, j = self._indice(origen), self._indice(destino)
111 |         if resultado["distancias"][i][j] == inf:
112 |             return []
113 |         ruta = [destino]
114 |         while j != i:
115 |             j = resultado["predecesores"][i][j]
116 |             ruta.append(self.ids[j])
117 |         return ruta[::-1]
118 | 
119 |
```

### BLOQUE 7: cargar la misma red del Taller 1 · líneas 120 a 127

`Grafo(MUNICIPIOS)` toma las claves del diccionario en su orden A a J. El ciclo desempaqueta cada tupla en tres variables y llama a `Union`. Como la red es no dirigida, cada enlace se escribe en ambos sentidos. `return` entrega la red lista. Esta función reemplaza la carga distribuida entre varios archivos del Taller 1.

```text
120 | # BLOQUE 7: cargar la misma red del Taller 1
121 | def crear_red():
122 |     grafo = Grafo(MUNICIPIOS)
123 |     for origen, destino, minutos in CONEXIONES:
124 |         grafo.Union(origen, destino, minutos)
125 |     return grafo
126 | 
127 |
```

### BLOQUE 8: demostración por consola · líneas 128 a 149

Los parámetros por defecto son A y F. La función crea la red, valida los IDs y ejecuta los dos algoritmos. `print` muestra los resultados; `join` une los IDs con flechas de texto. Los ciclos finales imprimen las filas de la matriz. Los formatos `>5` y `>5g` alinean columnas; no forman parte del algoritmo. Esta demostración recalcula Floyd en cada ejecución: no es un servidor que atienda 100 000 consultas por segundo. Para muchas consultas dentro de un mismo proceso se guarda su resultado una vez y se reutiliza.

```text
128 | # BLOQUE 8: demostración por consola
129 | def mostrar_demo(origen="A", destino="F"):
130 |     grafo = crear_red()
131 |     grafo._indice(origen)
132 |     grafo._indice(destino)
133 |     dijkstra = grafo.Dijkstra(origen)
134 |     floyd = grafo.FloydWarshall()
135 |     print("EPIRED - TALLER 2 (tiempos ficticios en minutos)")
136 |     for id, nombre in MUNICIPIOS.items():
137 |         print(f"{id}: {nombre}")
138 |     print(f"\nDistancias desde {origen}: {dijkstra['distancias']}")
139 |     print(f"Predecesores: {dijkstra['predecesores']}")
140 |     print("Ruta Dijkstra:", " -> ".join(grafo.RutaDijkstra(dijkstra, destino)))
141 |     print("Ruta Floyd:   ", " -> ".join(grafo.RutaFloyd(floyd, origen, destino)))
142 |     print("Costo:", dijkstra["distancias"][destino], "minutos")
143 |     print("\nMatriz final de Floyd-Warshall")
144 |     print("    " + "".join(f"{id:>5}" for id in grafo.ids))
145 |     for id, fila in zip(grafo.ids, floyd["distancias"]):
146 |         print(f"{id:>4}" + "".join(f"{valor:>5g}" for valor in fila))
147 |     print("Ciclo negativo:", floyd["ciclo_negativo"])
148 | 
149 |
```

### BLOQUE 9: comprobaciones sin otro archivo Python · líneas 150 a 199

`assert` comprueba que una condición sea verdadera. Se recorren los 100 pares y se comparan distancias y costos de rutas. La suma sobre `zip(ruta, ruta[1:])` recorre parejas consecutivas del camino. Luego se prueban resultados conocidos y casos especiales. Los bloques `try/except/else` comprueban que se produzcan los errores esperados. En el ejemplo negativo, primero se prueba una arista negativa sin ciclo negativo; después se añade B → A = 1 y finalmente se cambia a −2 para producir el ciclo negativo. Ejecuta las pruebas sin la opción `-O` de Python, porque esa opción desactiva los `assert`.

```text
150 | # BLOQUE 9: comprobaciones sin otro archivo Python
151 | def verificar():
152 |     grafo = crear_red()
153 |     floyd = grafo.FloydWarshall()
154 |     for i, origen in enumerate(grafo.ids):
155 |         dijkstra = grafo.Dijkstra(origen)
156 |         for j, destino in enumerate(grafo.ids):
157 |             assert dijkstra["distancias"][destino] == floyd["distancias"][i][j]
158 |             for ruta in (grafo.RutaDijkstra(dijkstra, destino),
159 |                          grafo.RutaFloyd(floyd, origen, destino)):
160 |                 assert ruta[0] == origen and ruta[-1] == destino
161 |                 costo = sum(grafo.matriz[grafo._indice(a)][grafo._indice(b)]
162 |                             for a, b in zip(ruta, ruta[1:]))
163 |                 assert costo == dijkstra["distancias"][destino]
164 |     assert grafo.RutaDijkstra(grafo.Dijkstra("A"), "F") == ["A", "C", "F"]
165 |     assert grafo.Dijkstra("A")["distancias"]["F"] == 50
166 |     aislado = Grafo(["A", "B"])
167 |     assert aislado.RutaDijkstra(aislado.Dijkstra("A"), "B") == []
168 |     assert aislado.RutaFloyd(aislado.FloydWarshall(), "A", "B") == []
169 |     aislado.Union("A", "B", 0)
170 |     assert aislado.Dijkstra("A")["distancias"]["B"] == 0
171 |     negativo = Grafo(["A", "B", "C"], dirigido=True)
172 |     negativo.Union("A", "B", 2)
173 |     negativo.Union("A", "C", 5)
174 |     negativo.Union("C", "B", -4)
175 |     resultado = negativo.FloydWarshall()
176 |     assert resultado["distancias"][0][1] == 1
177 |     assert not resultado["ciclo_negativo"]
178 |     assert negativo.RutaFloyd(resultado, "A", "B") == ["A", "C", "B"]
179 |     try:
180 |         negativo.Dijkstra("A")
181 |     except ValueError:
182 |         pass
183 |     else:
184 |         raise AssertionError("Dijkstra debía rechazar el peso negativo.")
185 |     negativo.Union("B", "A", 1)
186 |     resultado = negativo.FloydWarshall()
187 |     assert not resultado["ciclo_negativo"]
188 |     negativo.Union("B", "A", -2)
189 |     resultado = negativo.FloydWarshall()
190 |     assert resultado["ciclo_negativo"]
191 |     try:
192 |         negativo.RutaFloyd(resultado, "A", "B")
193 |     except ValueError:
194 |         pass
195 |     else:
196 |         raise AssertionError("Debía impedir la reconstrucción con ciclo negativo.")
197 |     print("OK: 100 pares, costos de rutas y casos especiales verificados.")
198 | 
199 |
```

### BLOQUE 10: punto de entrada · líneas 200 a 213

La condición `__name__ == "__main__"` ejecuta la demostración solo al abrir este archivo como programa. `sys.argv` contiene las palabras escritas en la terminal. `--verificar` ejecuta las comprobaciones; sin argumentos muestra A → F; con dos argumentos consulta esos IDs y los convierte a mayúsculas. Una entrada inválida imprime el error y termina con código 1.

```text
200 | # BLOQUE 10: punto de entrada
201 | if __name__ == "__main__":
202 |     try:
203 |         if sys.argv[1:] == ["--verificar"]:
204 |             verificar()
205 |         elif len(sys.argv) == 1:
206 |             mostrar_demo()
207 |         elif len(sys.argv) == 3:
208 |             mostrar_demo(sys.argv[1].upper(), sys.argv[2].upper())
209 |         else:
210 |             raise ValueError("Uso: python epired_taller2.py [ORIGEN DESTINO | --verificar]")
211 |     except ValueError as error:
212 |         print("Error:", error)
213 |         sys.exit(1)
```

## 7. Guion corto para exponer

1. **Presentar la red:** “Continuamos EpiRed con 10 municipios y 13 conexiones; los pesos son minutos ficticios”.
2. **Explicar el problema:** “Queremos minimizar la suma de minutos, no contar conexiones”.
3. **Explicar Dijkstra:** muestra la mejora de D, de 30 a 25, al pasar por C. Explica distancia, visitados y predecesores.
4. **Explicar Floyd:** muestra k = C y k = D; relaciona los tres ciclos con origen, destino e intermediario.
5. **Ejecutar:** `python epired_taller2.py A F`. Ambos dan A → C → F y 50 minutos.
6. **Mostrar otra consulta:** `python epired_taller2.py A E`, con 37 minutos. Después ejecuta `--verificar`.
7. **Cerrar:** “Dijkstra sirve desde una fuente; Floyd deja lista toda la tabla. Los predecesores recuperan las rutas”.

## 8. Preguntas que pueden hacerte

**¿Por qué infinito y no cero para una arista ausente?** Cero puede ser un peso válido. Infinito expresa que no se puede cruzar directamente.

**¿Por qué copiar filas en Floyd?** Para conservar los pesos originales y trabajar en una matriz de distancias independiente.

**¿Por qué se copia `predecesores[k][j]` y no simplemente k?** Porque el último tramo k → j puede tener más nodos; el predecesor inmediato de j puede ser otro.

**¿Puede una distancia final ser negativa?** Sí, con aristas negativas en un grafo dirigido sin ciclos negativos. Lo problemático es poder disminuirla indefinidamente repitiendo un ciclo.

**¿La ruta más rápida evita contagios?** El algoritmo solo minimiza los tiempos ficticios. No mide riesgo epidemiológico.

**¿Qué significa O(V³)?** Al aumentar el número de vértices, el trabajo crece aproximadamente como su cubo por los tres ciclos anidados. No significa exactamente V³ segundos.

**¿Se conservó toda la aplicación anterior?** Se conservó y adaptó la base necesaria para este taller, en una versión por consola enfocada en caminos mínimos.

## 9. Resultados y comprobaciones

| Consulta | Ruta | Minutos |
|---|---|---:|
| A a F | A → C → F | 50 |
| A a E | A → C → D → E | 37 |
| A a J | A → G → J | 75 |
| I a J | I → H → G → J | 75 |

`--verificar` revisa los 100 pares, costos de rutas, nodos aislados, peso cero, negativos sin ciclo, rechazo de Dijkstra y ciclo negativo. Se ejecutó correctamente al preparar esta entrega. No utiliza bibliotecas que resuelvan los algoritmos por nosotros.

## 10. Subir a GitHub

Descomprime la entrega. En tu repositorio puedes crear una carpeta `Taller2` para conservar separado el Taller 1 y subir allí el `.py`, este README, el informe y `.gitignore`. No necesitas subir archivos temporales ni `__pycache__`. La entrega está preparada para subir; no se publicó automáticamente en un repositorio.

## Referencias del curso

- `ENO LINEALES C2 TALLER2 GRAFOS.pdf`, páginas 1 y 2.
- `GRAFOS P2 26-2.pdf`, diapositivas 43–80, 81 y 85.
- ZIP de EpiRed Taller 1: `datos.py`, `grafo.py` y `README.md`.
