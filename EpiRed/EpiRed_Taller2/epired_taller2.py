"""Taller 2 de EpiRed. Python 3.10+, sin paquetes externos.

Adaptación de Grafo, CaminoMinimo y los datos del Taller 1.
Los tiempos son ficticios y se expresan en minutos.
"""

# BLOQUE 1: datos originales y herramientas de Python
from math import inf, isfinite
import sys

MUNICIPIOS = {
    "A": "Medellín", "B": "Bello", "C": "Itagüí", "D": "Envigado",
    "E": "Sabaneta", "F": "Caldas", "G": "Copacabana", "H": "Girardota",
    "I": "Barbosa", "J": "Rionegro",
}
CONEXIONES = [
    ("A", "B", 20), ("A", "C", 15), ("A", "D", 30), ("B", "C", 30),
    ("C", "D", 10), ("D", "E", 12), ("E", "F", 20), ("C", "F", 35),
    ("A", "G", 35), ("B", "G", 20), ("G", "H", 15), ("H", "I", 20),
    ("G", "J", 40),
]


# BLOQUE 2: grafo con matriz de pesos
class Grafo:
    def __init__(self, ids, dirigido=False):
        self.ids = list(ids)
        if len(set(self.ids)) != len(self.ids):
            raise ValueError("No se permiten IDs repetidos.")
        self.dirigido = dirigido
        n = len(self.ids)
        self.matriz = [[0 if i == j else inf for j in range(n)] for i in range(n)]

    def _indice(self, id):
        if id not in self.ids:
            raise ValueError(f"El nodo {id} no existe.")
        return self.ids.index(id)

    def Union(self, origen, destino, peso):
        i, j = self._indice(origen), self._indice(destino)
        peso = float(peso)
        if i == j or not isfinite(peso):
            raise ValueError("Usa nodos diferentes y un peso finito.")
        self.matriz[i][j] = peso
        if not self.dirigido:
            self.matriz[j][i] = peso

    # BLOQUE 3: Dijkstra desde un origen hacia todos
    def Dijkstra(self, origen):
        inicio = self._indice(origen)
        if any(peso < 0 for fila in self.matriz for peso in fila):
            raise ValueError("Dijkstra no admite pesos negativos.")
        n = len(self.ids)
        distancias = [inf] * n
        predecesores = [None] * n
        visitados = [False] * n
        distancias[inicio] = 0
        for _ in range(n):
            actual = None
            for i in range(n):
                if not visitados[i] and (actual is None or distancias[i] < distancias[actual]):
                    actual = i
            if actual is None or distancias[actual] == inf:
                break
            visitados[actual] = True
            for vecino in range(n):
                nuevo = distancias[actual] + self.matriz[actual][vecino]
                if not visitados[vecino] and nuevo < distancias[vecino]:
                    distancias[vecino] = nuevo
                    predecesores[vecino] = self.ids[actual]
        return {"origen": origen, "distancias": dict(zip(self.ids, distancias)),
                "predecesores": dict(zip(self.ids, predecesores))}

    # BLOQUE 4: reconstruir una ruta de Dijkstra
    def RutaDijkstra(self, resultado, destino):
        self._indice(destino)
        if resultado["distancias"][destino] == inf:
            return []
        ruta = []
        actual = destino
        while actual is not None:
            ruta.append(actual)
            actual = resultado["predecesores"][actual]
        return ruta[::-1]

    # BLOQUE 5: Floyd-Warshall para todos los pares
    def FloydWarshall(self):
        n = len(self.ids)
        distancias = [fila[:] for fila in self.matriz]
        predecesores = [[None] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if i != j and distancias[i][j] != inf:
                    predecesores[i][j] = i
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    nuevo = distancias[i][k] + distancias[k][j]
                    if nuevo < distancias[i][j]:
                        distancias[i][j] = nuevo
                        predecesores[i][j] = predecesores[k][j]
        ciclo_negativo = any(distancias[i][i] < 0 for i in range(n))
        return {"ids": self.ids[:], "distancias": distancias,
                "predecesores": predecesores, "ciclo_negativo": ciclo_negativo}

    # BLOQUE 6: reconstruir una ruta de Floyd-Warshall
    def RutaFloyd(self, resultado, origen, destino):
        if resultado["ciclo_negativo"]:
            raise ValueError("Hay un ciclo negativo: no se reconstruyen rutas.")
        i, j = self._indice(origen), self._indice(destino)
        if resultado["distancias"][i][j] == inf:
            return []
        ruta = [destino]
        while j != i:
            j = resultado["predecesores"][i][j]
            ruta.append(self.ids[j])
        return ruta[::-1]


# BLOQUE 7: cargar la misma red del Taller 1
def crear_red():
    grafo = Grafo(MUNICIPIOS)
    for origen, destino, minutos in CONEXIONES:
        grafo.Union(origen, destino, minutos)
    return grafo


# BLOQUE 8: demostración por consola
def mostrar_demo(origen="A", destino="F"):
    grafo = crear_red()
    grafo._indice(origen)
    grafo._indice(destino)
    dijkstra = grafo.Dijkstra(origen)
    floyd = grafo.FloydWarshall()
    print("EPIRED - TALLER 2 (tiempos ficticios en minutos)")
    for id, nombre in MUNICIPIOS.items():
        print(f"{id}: {nombre}")
    print(f"\nDistancias desde {origen}: {dijkstra['distancias']}")
    print(f"Predecesores: {dijkstra['predecesores']}")
    print("Ruta Dijkstra:", " -> ".join(grafo.RutaDijkstra(dijkstra, destino)))
    print("Ruta Floyd:   ", " -> ".join(grafo.RutaFloyd(floyd, origen, destino)))
    print("Costo:", dijkstra["distancias"][destino], "minutos")
    print("\nMatriz final de Floyd-Warshall")
    print("    " + "".join(f"{id:>5}" for id in grafo.ids))
    for id, fila in zip(grafo.ids, floyd["distancias"]):
        print(f"{id:>4}" + "".join(f"{valor:>5g}" for valor in fila))
    print("Ciclo negativo:", floyd["ciclo_negativo"])


# BLOQUE 9: comprobaciones sin otro archivo Python
def verificar():
    grafo = crear_red()
    floyd = grafo.FloydWarshall()
    for i, origen in enumerate(grafo.ids):
        dijkstra = grafo.Dijkstra(origen)
        for j, destino in enumerate(grafo.ids):
            assert dijkstra["distancias"][destino] == floyd["distancias"][i][j]
            for ruta in (grafo.RutaDijkstra(dijkstra, destino),
                         grafo.RutaFloyd(floyd, origen, destino)):
                assert ruta[0] == origen and ruta[-1] == destino
                costo = sum(grafo.matriz[grafo._indice(a)][grafo._indice(b)]
                            for a, b in zip(ruta, ruta[1:]))
                assert costo == dijkstra["distancias"][destino]
    assert grafo.RutaDijkstra(grafo.Dijkstra("A"), "F") == ["A", "C", "F"]
    assert grafo.Dijkstra("A")["distancias"]["F"] == 50
    aislado = Grafo(["A", "B"])
    assert aislado.RutaDijkstra(aislado.Dijkstra("A"), "B") == []
    assert aislado.RutaFloyd(aislado.FloydWarshall(), "A", "B") == []
    aislado.Union("A", "B", 0)
    assert aislado.Dijkstra("A")["distancias"]["B"] == 0
    negativo = Grafo(["A", "B", "C"], dirigido=True)
    negativo.Union("A", "B", 2)
    negativo.Union("A", "C", 5)
    negativo.Union("C", "B", -4)
    resultado = negativo.FloydWarshall()
    assert resultado["distancias"][0][1] == 1
    assert not resultado["ciclo_negativo"]
    assert negativo.RutaFloyd(resultado, "A", "B") == ["A", "C", "B"]
    try:
        negativo.Dijkstra("A")
    except ValueError:
        pass
    else:
        raise AssertionError("Dijkstra debía rechazar el peso negativo.")
    negativo.Union("B", "A", 1)
    resultado = negativo.FloydWarshall()
    assert not resultado["ciclo_negativo"]
    negativo.Union("B", "A", -2)
    resultado = negativo.FloydWarshall()
    assert resultado["ciclo_negativo"]
    try:
        negativo.RutaFloyd(resultado, "A", "B")
    except ValueError:
        pass
    else:
        raise AssertionError("Debía impedir la reconstrucción con ciclo negativo.")
    print("OK: 100 pares, costos de rutas y casos especiales verificados.")


# BLOQUE 10: punto de entrada
if __name__ == "__main__":
    try:
        if sys.argv[1:] == ["--verificar"]:
            verificar()
        elif len(sys.argv) == 1:
            mostrar_demo()
        elif len(sys.argv) == 3:
            mostrar_demo(sys.argv[1].upper(), sys.argv[2].upper())
        else:
            raise ValueError("Uso: python epired_taller2.py [ORIGEN DESTINO | --verificar]")
    except ValueError as error:
        print("Error:", error)
        sys.exit(1)
