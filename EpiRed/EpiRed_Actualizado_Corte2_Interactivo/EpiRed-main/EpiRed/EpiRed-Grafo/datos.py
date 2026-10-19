"""Datos ficticios para el taller: una enfermedad y un mismo corte de reporte."""

from grafo import Grafo, Vertice

MUNICIPIOS = {
    "A": "Medellín", "B": "Bello", "C": "Itagüí", "D": "Envigado",
    "E": "Sabaneta", "F": "Caldas", "G": "Copacabana", "H": "Girardota",
    "I": "Barbosa", "J": "Rionegro",
}

# Confirmados, recuperados y fallecidos. Los activos se calculan, no se duplican.
# No corresponden a cifras reales ni a una clasificación oficial de riesgo.
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

CAMINOS = ["A C F", "A D E F", "A C D E F"]

# Posiciones de dibujo, no coordenadas geográficas.
POSICIONES = {
    "A": (.44, .36), "B": (.25, .12), "C": (.23, .47),
    "D": (.47, .64), "E": (.34, .87), "F": (.08, .75),
    "G": (.65, .27), "H": (.83, .43), "I": (.90, .77), "J": (.78, .07),
}


def crear_red():
    grafo = Grafo()
    for id, nombre in MUNICIPIOS.items():
        confirmados, recuperados, fallecidos = REPORTES[id]
        grafo.AñadirVertice(Vertice(id, nombre, casos=confirmados,
                                   recuperados=recuperados, fallecidos=fallecidos,
                                   centro_salud=f"Centro de salud {id} (ficticio)"))
    for origen, destino, minutos in CONEXIONES:
        grafo.Union(origen, destino, minutos)
    return grafo
