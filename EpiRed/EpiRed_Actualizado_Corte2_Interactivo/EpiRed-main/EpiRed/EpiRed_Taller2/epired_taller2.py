"""EpiRed Taller 2 ampliado para los cuatro retos del parcial.

Se conservan los municipios, conexiones, Dijkstra y Floyd del taller.
Nuevos bloques: capacidades, fallas, respaldo y subsidio dirigido.
Ejecutar la consola con python main.py. Solo biblioteca estándar.
"""
from collections import deque
from math import inf, isfinite
from numbers import Real

def numero_finito(valor, nombre):
    """Rechaza booleanos, texto, NaN e infinitos antes de cambiar el estado."""
    if isinstance(valor, bool) or not isinstance(valor, Real):
        raise ValueError(f"{nombre} debe ser un número real finito.")
    try:
        valido = isfinite(valor)
    except OverflowError:
        valido = False
    if not valido:
        raise ValueError(f"{nombre} debe ser un número real finito.")
    return valor


def sumar_pesos(a, b):
    """Conserva inf como ausencia y rechaza desbordamientos numéricos."""
    if a == inf or b == inf:
        return inf
    return numero_finito(a + b, "La suma de pesos (fuera del rango permitido)")


class Grafo:
    def __init__(self, ids, dirigido=False, permitir_negativos=False):
        ids = list(ids)
        if any(not isinstance(x, str) or not x.strip() for x in ids):
            raise ValueError("Cada ID debe ser un texto no vacío.")
        if len(set(ids)) != len(ids):
            raise ValueError("No se permiten IDs repetidos.")
        if permitir_negativos and not dirigido:
            raise ValueError("Los costos negativos se reservan al escenario dirigido.")
        self.ids = sorted(ids)  # Desempate estable por ID menor.
        self.dirigido = dirigido
        self.permitir_negativos = permitir_negativos
        n = len(ids)
        self.matriz = [[0 if i == j else inf for j in range(n)] for i in range(n)]
        self.capacidades = [[0 for _ in range(n)] for _ in range(n)]

    def _indice(self, id):
        if id not in self.ids:
            raise ValueError(f"El nodo {id} no existe.")
        return self.ids.index(id)

    def Union(self, origen, destino, peso, capacidad=1):
        """Agrega o actualiza un enlace; valida todo antes de escribir."""
        i, j = self._indice(origen), self._indice(destino)
        peso = numero_finito(peso, "El peso")
        capacidad = numero_finito(capacidad, "La capacidad")
        if i == j or capacidad <= 0:
            raise ValueError("Usa nodos distintos y capacidad positiva.")
        if peso < 0 and not self.permitir_negativos:
            raise ValueError("El tiempo no puede ser negativo.")
        self.matriz[i][j], self.capacidades[i][j] = peso, capacidad
        if not self.dirigido:
            self.matriz[j][i], self.capacidades[j][i] = peso, capacidad

    def BorrarArco(self, origen, destino):
        """Inhabilita el enlace en ambos sentidos si la red es no dirigida."""
        i, j = self._indice(origen), self._indice(destino)
        if i == j or self.matriz[i][j] == inf:
            raise ValueError("No existe esa conexión directa.")
        self.matriz[i][j], self.capacidades[i][j] = inf, 0
        if not self.dirigido:
            self.matriz[j][i], self.capacidades[j][i] = inf, 0

    def copia(self):
        """Copia independiente: ninguna fila queda compartida."""
        copia = Grafo(self.ids, self.dirigido, self.permitir_negativos)
        copia.matriz = [fila[:] for fila in self.matriz]
        copia.capacidades = [fila[:] for fila in self.capacidades]
        return copia

    def estado(self):
        """Fotografía comparable de IDs, atributos y todos los pesos."""
        return (tuple(self.ids), self.dirigido, self.permitir_negativos,
                tuple(map(tuple, self.matriz)), tuple(map(tuple, self.capacidades)))

    def Aristas(self):
        return [(a, b, self.matriz[i][j], self.capacidades[i][j])
                for i, a in enumerate(self.ids) for j, b in enumerate(self.ids)
                if i != j and self.matriz[i][j] != inf and (self.dirigido or i < j)]

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
                nuevo = sumar_pesos(distancias[actual], self.matriz[actual][vecino])
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
                    nuevo = sumar_pesos(distancias[i][k], distancias[k][j])
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


MUNICIPIOS = {
    "A": "Medellín", "B": "Bello", "C": "Itagüí", "D": "Envigado",
    "E": "Sabaneta", "F": "Caldas", "G": "Copacabana", "H": "Girardota",
    "I": "Barbosa", "J": "Rionegro",
}


REPORTES = {
    "A": (300, 268, 2), "B": (140, 126, 2), "C": (500, 415, 5),
    "D": (180, 168, 2), "E": (100, 84, 1), "F": (90, 81, 1),
    "G": (280, 217, 3), "H": (120, 94, 1), "I": (70, 65, 0),
    "J": (220, 173, 2),
}


CONEXIONES = [
    ("A", "B", 20), ("A", "C", 15), ("A", "D", 30), ("B", "C", 30),
    ("C", "D", 10), ("D", "E", 12), ("E", "F", 20), ("C", "F", 35),
    ("A", "G", 35), ("B", "G", 20), ("G", "H", 15), ("H", "I", 20),
    ("G", "J", 40),
]


# Capacidades nuevas: unidades de suministros médicos por viaje.
CAPACIDADES = {
    ("A", "B"): 45, ("A", "C"): 20, ("A", "D"): 70,
    ("B", "C"): 30, ("C", "D"): 25, ("D", "E"): 60,
    ("E", "F"): 55, ("C", "F"): 15, ("A", "G"): 40,
    ("B", "G"): 35, ("G", "H"): 30, ("H", "I"): 25,
    ("G", "J"): 20,
}


def crear_red():
    grafo = Grafo(MUNICIPIOS)
    for a, b, minutos in CONEXIONES:
        grafo.Union(a, b, minutos, CAPACIDADES[a, b])
    return grafo


def crear_escenario_costos(red, con_ciclo=False):
    """Copia dirigida de costos, en unidades monetarias ficticias (UM).

    Cada conexión aporta inicialmente dos arcos de 10 UM. Solo A->B recibe
    bono: 15 UM (neto -5, sin ciclo) o 45 UM (neto -35, con ciclo).
    B->A conserva 10 UM. A->B->C->A suma -15 en el segundo escenario.
    """
    red._indice("A")
    red._indice("B")
    costos = Grafo(red.ids, dirigido=True, permitir_negativos=True)
    for a, b, _, capacidad in red.Aristas():
        costos.Union(a, b, 10, capacidad)
        if not red.dirigido:
            costos.Union(b, a, 10, capacidad)
    i, j = costos._indice("A"), costos._indice("B")
    if costos.capacidades[i][j] == 0:
        raise ValueError("El subsidio requiere la conexión A->B.")
    costos.Union("A", "B", -35 if con_ciclo else -5, costos.capacidades[i][j])
    return costos


def RutaMayorCapacidad(origen, destino, grafo=None):
    """Devuelve (IDs ordenados, cuello). Sin ruta: ([], 0).

    Mismo municipio: ([origen], inf), identidad del mínimo sin aristas;
    no significa que exista un vehículo de capacidad infinita.
    """
    if grafo is None:
        grafo = crear_red()
    inicio, fin = grafo._indice(origen), grafo._indice(destino)
    n = len(grafo.ids)
    mejores, anteriores, visitados = [0] * n, [None] * n, [False] * n
    mejores[inicio] = inf
    for _ in range(n):
        actual = None
        for i in range(n):
            if not visitados[i] and (actual is None or mejores[i] > mejores[actual]):
                actual = i
        if actual is None or mejores[actual] == 0:
            break
        visitados[actual] = True
        if actual == fin:
            break
        for vecino, capacidad in enumerate(grafo.capacidades[actual]):
            candidato = min(mejores[actual], capacidad)
            if not visitados[vecino] and candidato > mejores[vecino]:
                mejores[vecino] = candidato
                anteriores[vecino] = actual
    if mejores[fin] == 0:
        return [], 0
    ruta, actual = [], fin
    while actual is not None:
        ruta.append(grafo.ids[actual])
        actual = anteriores[actual]
    return ruta[::-1], mejores[fin]


def componentes(grafo, excluido=None):
    """Grupos conexos; ignora un ID sin escribir en el grafo."""
    if grafo.dirigido:
        raise ValueError("Este diagnóstico requiere un grafo no dirigido.")
    if excluido is not None:
        grafo._indice(excluido)
    visitados, grupos = set(), []
    for inicio, id in enumerate(grafo.ids):
        if id == excluido or inicio in visitados:
            continue
        cola, grupo = deque([inicio]), []
        visitados.add(inicio)
        while cola:
            actual = cola.popleft()
            grupo.append(grafo.ids[actual])
            for vecino, peso in enumerate(grafo.matriz[actual]):
                if (vecino not in visitados and grafo.ids[vecino] != excluido
                        and peso != inf):
                    visitados.add(vecino)
                    cola.append(vecino)
        grupos.append(sorted(grupo))
    return grupos


def DetectarPuntosCriticosDeFalla(grafo):
    """Devuelve IDs críticos y evidencia de TODAS las exclusiones."""
    inicial = componentes(grafo)
    aislados_previos = {g[0] for g in inicial if len(g) == 1}
    ensayos, criticos = {}, []
    for id in grafo.ids:
        grupos = componentes(grafo, excluido=id)
        aislados = [g[0] for g in grupos if len(g) == 1]
        es_critico = len(grupos) > len(inicial)
        if es_critico:
            criticos.append(id)
        ensayos[id] = {"componentes": grupos, "aislados": aislados,
                       "nuevos_aislados": [v for v in aislados if v not in aislados_previos],
                       "es_critico": es_critico}
    return {"componentes_iniciales": inicial, "criticos": criticos, "ensayos": ensayos}


ALERTA = "Red no redundante entre origen y destino"


def GenerarRutaConRespaldo(origen, destino, grafo=None):
    """Devuelve rutas, minutos, porcentaje y alerta; nunca modifica el original.

    Porcentaje None si no hay respaldo o si el costo primario es cero.
    Mismo origen/destino: dos rutas triviales de costo cero, sin traslado.
    """
    if grafo is None:
        grafo = crear_red()
    grafo._indice(origen)
    grafo._indice(destino)
    if grafo.dirigido:
        raise ValueError("El respaldo de este parcial usa una red no dirigida.")
    primera = grafo.Dijkstra(origen)
    primaria = grafo.RutaDijkstra(primera, destino)
    costo_primario = primera["distancias"][destino]
    copia = grafo.copia()
    for a, b in zip(primaria, primaria[1:]):
        copia.BorrarArco(a, b)
    segunda = copia.Dijkstra(origen)
    respaldo = copia.RutaDijkstra(segunda, destino)
    costo_respaldo = segunda["distancias"][destino]
    porcentaje = None
    if respaldo and 0 < costo_primario < inf:
        porcentaje = (costo_respaldo - costo_primario) / costo_primario * 100
    return {"primaria": primaria, "respaldo": respaldo,
            "costo_primario": costo_primario, "costo_respaldo": costo_respaldo,
            "porcentaje": porcentaje, "alerta": None if respaldo else ALERTA}


def DetectarAnomaliaDeCicloNegativo(matriz_distancias, ids=None):
    """Recibe la matriz ya calculada por Floyd; no la modifica.

    Sin IDs, asigna A, B, ... para hasta 26 filas. Para otras redes pase IDs
    en el mismo orden que las filas. No reconstruye el ciclo simple exacto.
    """
    if not isinstance(matriz_distancias, (list, tuple)):
        raise ValueError("Se requiere una matriz cuadrada.")
    n = len(matriz_distancias)
    if ids is None:
        if n > 26:
            raise ValueError("Proporciona IDs para matrices de más de 26 filas.")
        ids = [chr(65 + i) for i in range(n)]
    ids = list(ids)
    if (len(ids) != n or any(not isinstance(x, str) or not x.strip() for x in ids)
            or len(set(ids)) != n):
        raise ValueError("Los IDs deben ser únicos y corresponder a las filas.")
    for fila in matriz_distancias:
        if not isinstance(fila, (list, tuple)) or len(fila) != n:
            raise ValueError("Se requiere una matriz cuadrada.")
        for valor in fila:
            if valor != inf:
                numero_finito(valor, "La distancia")
    diagnosticos = [ids[i] for i in range(n) if matriz_distancias[i][i] < 0]
    return {"hay_anomalia": bool(diagnosticos), "ids_diagnosticos": diagnosticos}


if __name__ == "__main__":
    from main import main
    main()
