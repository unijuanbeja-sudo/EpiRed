"""Grafo no dirigido con matriz de adyacencia. No usa librerías externas."""

from collections import deque
from dataclasses import dataclass, replace
from math import isfinite


@dataclass
class Vertice:
    id: str
    nombre: str
    departamento: str = "Antioquia"
    casos: int | None = None  # Confirmados; None significa que no se suministraron datos.
    recuperados: int | None = None
    fallecidos: int | None = None
    enfermedad: str = "COVID-19"
    corte: str = "Corte simulado del taller"
    centro_salud: str = "Sin registrar"

    def __post_init__(self):
        self.id = self.id.strip().upper()
        self.nombre = self.nombre.strip()
        if not self.id or not self.id.isalnum() or len(self.id) > 8:
            raise ValueError("El ID debe tener entre 1 y 8 letras o números.")
        if not self.nombre:
            raise ValueError("Escribe el nombre del municipio.")
        for valor in (self.casos, self.recuperados, self.fallecidos):
            if valor is not None and (type(valor) is not int or valor < 0):
                raise ValueError("Las cantidades deben ser enteros mayores o iguales a cero.")
        registrados = [n for n in (self.recuperados, self.fallecidos) if n is not None]
        if self.casos is None and registrados:
            raise ValueError("Registra los confirmados antes de indicar recuperados o fallecidos.")
        if self.casos is not None and sum(registrados) > self.casos:
            raise ValueError("Recuperados y fallecidos no pueden superar los confirmados.")

    @property
    def activos(self):
        # Todos corresponden a la misma enfermedad y al mismo corte del ejemplo.
        if None in (self.casos, self.recuperados, self.fallecidos):
            return None
        return self.casos - self.recuperados - self.fallecidos

    @property
    def nivel_riesgo(self):
        """Clasificación didáctica, no una medida de probabilidad de contagio."""
        if self.activos is None:
            return "Sin datos"
        if self.activos < 20:
            return "Bajo"
        if self.activos < 50:
            return "Medio"
        return "Alto"


class Grafo:
    def __init__(self):
        self.vertices = []
        self.matriz = []

    @property
    def ids(self):
        return [v.id for v in self.vertices]

    def _indice(self, id):
        if id not in self.ids:
            raise ValueError(f"El municipio {id} no existe en la red.")
        return self.ids.index(id)

    def ConsultarMunicipio(self, id):
        return self.vertices[self._indice(id)]

    def ActualizarReporte(self, id, confirmados, recuperados, fallecidos):
        i = self._indice(id)
        # replace valida el nuevo reporte antes de sustituir el anterior.
        self.vertices[i] = replace(self.vertices[i], casos=confirmados,
                                   recuperados=recuperados, fallecidos=fallecidos)

    def InformacionRuta(self, secuencia):
        if not self.EsCaminoValido(secuencia):
            raise ValueError("El camino no es válido: revisa sus nodos y conexiones.")
        return [self.ConsultarMunicipio(id) for id in secuencia]

    def ResumenEpidemiologico(self):
        completos = [v for v in self.vertices if v.activos is not None]
        recuperados = [v for v in self.vertices if v.recuperados is not None]
        return {
            "reportes_completos": len(completos),
            "activos": sum(v.activos for v in completos) if completos else None,
            "mas_activos": max(completos, key=lambda v: v.activos).id if completos else None,
            "menos_activos": min(completos, key=lambda v: v.activos).id if completos else None,
            "mas_recuperados": max(recuperados, key=lambda v: v.recuperados).id if recuperados else None,
        }

    def AñadirVertice(self, vertice):
        if vertice.id in self.ids:
            raise ValueError(f"Ya existe el municipio con ID {vertice.id}.")
        # Insertar en orden de ID mantiene la matriz y los recorridos ordenados.
        posicion = sorted(self.ids + [vertice.id]).index(vertice.id)
        self.vertices.insert(posicion, vertice)
        for fila in self.matriz:
            fila.insert(posicion, 0)
        self.matriz.insert(posicion, [0] * len(self.vertices))

    def BorrarVertice(self, id):
        i = self._indice(id)
        self.vertices.pop(i)
        self.matriz.pop(i)
        for fila in self.matriz:
            fila.pop(i)

    def Union(self, origen, destino, peso):
        i, j = self._indice(origen), self._indice(destino)
        if i == j:
            raise ValueError("Esta red no permite conectar un municipio consigo mismo.")
        try:
            peso = float(peso)
        except (TypeError, ValueError):
            raise ValueError("El tiempo debe ser un número positivo.") from None
        if not isfinite(peso) or peso <= 0:
            raise ValueError("El tiempo debe ser un número finito mayor que cero.")
        # Una conexión ya existente se actualiza; no se crean aristas repetidas.
        self.matriz[i][j] = self.matriz[j][i] = peso

    def BorrarArco(self, origen, destino):
        i, j = self._indice(origen), self._indice(destino)
        if self.matriz[i][j] == 0:
            raise ValueError("No existe esa conexión directa.")
        self.matriz[i][j] = self.matriz[j][i] = 0

    def EsAdyacente(self, origen, destino):
        i, j = self._indice(origen), self._indice(destino)
        return self.matriz[i][j] > 0

    def Vecinos(self, id):
        fila = self.matriz[self._indice(id)]
        return [v.id for v, peso in zip(self.vertices, fila) if peso > 0]

    def Aristas(self):
        # Solo la mitad superior: cada arista bidireccional se cuenta una vez.
        return [(a, b, self.matriz[i][j])
                for i, a in enumerate(self.ids)
                for j, b in enumerate(self.ids) if j > i and self.matriz[i][j] > 0]

    def CalcularGrado(self, id):
        return len(self.Vecinos(id))

    def ObtenerGradosExtremos(self):
        if not self.vertices:
            return None, None
        # Los empates se resuelven por ID, igual que en el informe.
        mayor = max(self.ids, key=self.CalcularGrado)
        menor = min(self.ids, key=self.CalcularGrado)
        return mayor, menor

    def EsCaminoValido(self, secuencia):
        if not secuencia or any(id not in self.ids for id in secuencia):
            return False
        return all(self.EsAdyacente(a, b) for a, b in zip(secuencia, secuencia[1:]))

    def CalcularCostoCamino(self, secuencia):
        if not self.EsCaminoValido(secuencia):
            raise ValueError("El camino no es válido: revisa sus nodos y conexiones.")
        costo = sum(self.matriz[self._indice(a)][self._indice(b)]
                    for a, b in zip(secuencia, secuencia[1:]))
        return len(secuencia) - 1, costo

    def EsCiclo(self, secuencia):
        return (len(secuencia) >= 4 and self.EsCaminoValido(secuencia)
                and secuencia[0] == secuencia[-1]
                and len(set(secuencia[:-1])) == len(secuencia) - 1)

    def TrazaAnchura(self, inicio):
        self._indice(inicio)
        cola = deque([inicio])
        visitados = {inicio}
        niveles = {inicio: 0}
        padres = {inicio: None}
        traza = []
        while cola:
            actual = cola.popleft()
            for vecino in self.Vecinos(actual):
                if vecino not in visitados:
                    visitados.add(vecino)
                    niveles[vecino] = niveles[actual] + 1
                    padres[vecino] = actual
                    cola.append(vecino)
            traza.append({"nodo": actual, "nivel": niveles[actual],
                          "cola": list(cola), "padre": padres[actual]})
        return traza

    def RecorridoAnchura(self, inicio):
        return [paso["nodo"] for paso in self.TrazaAnchura(inicio)]

    def TrazaProfundidad(self, inicio):
        self._indice(inicio)
        visitados, traza = set(), []

        def visitar(actual, rama):
            visitados.add(actual)
            rama = rama + [actual]
            traza.append({"nodo": actual, "rama": rama,
                          "padre": rama[-2] if len(rama) > 1 else None})
            for vecino in self.Vecinos(actual):
                if vecino not in visitados:
                    visitar(vecino, rama)

        visitar(inicio, [])
        return traza

    def RecorridoProfundidad(self, inicio):
        return [paso["nodo"] for paso in self.TrazaProfundidad(inicio)]

    def Componentes(self):
        pendientes = set(self.ids)
        componentes = []
        while pendientes:
            componente = sorted(self.RecorridoAnchura(min(pendientes)))
            componentes.append(componente)
            pendientes.difference_update(componente)
        return componentes

    def CaminoMinimo(self, origen, destino, solo_bajo_medio=False):
        """Dijkstra sencillo: permite comprobar el mínimo incluso al editar la red."""
        self._indice(origen)
        self._indice(destino)
        distancias = {id: float("inf") for id in self.ids}
        anteriores = {}
        pendientes = {v.id for v in self.vertices
                      if not solo_bajo_medio or v.nivel_riesgo in ("Bajo", "Medio")}
        if origen not in pendientes or destino not in pendientes:
            return [], None
        distancias[origen] = 0
        while pendientes:
            actual = min(pendientes, key=lambda id: (distancias[id], id))
            if distancias[actual] == float("inf"):
                break
            pendientes.remove(actual)
            if actual == destino:
                camino = [destino]
                while camino[-1] != origen:
                    camino.append(anteriores[camino[-1]])
                return list(reversed(camino)), distancias[destino]
            fila = self.matriz[self._indice(actual)]
            for j, peso in enumerate(fila):
                if peso == 0:
                    continue
                vecino = self.vertices[j].id
                nuevo_costo = distancias[actual] + peso
                if vecino in pendientes and nuevo_costo < distancias[vecino]:
                    distancias[vecino] = nuevo_costo
                    anteriores[vecino] = actual
        return [], None
