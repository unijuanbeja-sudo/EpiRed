import unittest
from math import inf
from epired_taller2 import crear_red
from epired_taller2 import Grafo
from epired_taller2 import RutaMayorCapacidad


class TestCapacidad(unittest.TestCase):
    def test_ejemplo_y_estado(self):
        g = crear_red()
        antes = g.estado()
        self.assertEqual(RutaMayorCapacidad('A', 'F', g), (list('ADEF'), 55))
        self.assertEqual(g.RutaDijkstra(g.Dijkstra('A'), 'F'), list('ACF'))
        self.assertEqual(g.estado(), antes)

    def test_mismo_origen(self):
        self.assertEqual(RutaMayorCapacidad('A', 'A'), (['A'], inf))

    def test_desconectado(self):
        self.assertEqual(RutaMayorCapacidad('A', 'B', Grafo('AB')), ([], 0))

    def test_ids_invalidos(self):
        for a, b in [('X', 'A'), ('A', 'X'), (None, 'A')]:
            with self.subTest(a=a, b=b), self.assertRaises(ValueError):
                RutaMayorCapacidad(a, b)

    def test_capacidades_invalidas_sin_mutacion(self):
        g = Grafo('AB')
        antes = g.estado()
        for c in [0, -1, inf, float('nan'), True, '10', None]:
            with self.subTest(c=c), self.assertRaises(ValueError):
                g.Union('A', 'B', 1, c)
            self.assertEqual(g.estado(), antes)

    def test_desempate_por_id(self):
        g = Grafo('DCBA')
        for a, b in [('A', 'C'), ('A', 'B'), ('C', 'D'), ('B', 'D')]:
            g.Union(a, b, 1, 10)
        self.assertEqual(RutaMayorCapacidad('A', 'D', g), (list('ABD'), 10))

    def test_oraculo_todas_las_rutas_simples(self):
        # Enumeración exhaustiva independiente: compara los 100 pares.
        g = crear_red()
        def buscar(actual, fin, vistos, cuello):
            if actual == fin:
                return cuello
            mejor = 0
            for j, cap in enumerate(g.capacidades[actual]):
                if cap > 0 and j not in vistos:
                    mejor = max(mejor, buscar(j, fin, vistos | {j}, min(cuello, cap)))
            return mejor
        for i, a in enumerate(g.ids):
            for j, b in enumerate(g.ids):
                ruta, cuello = RutaMayorCapacidad(a, b, g)
                self.assertEqual(cuello, buscar(i, j, {i}, inf))
                self.assertEqual((ruta[0], ruta[-1]), (a, b))
                real = min((g.capacidades[g._indice(x)][g._indice(y)]
                            for x, y in zip(ruta, ruta[1:])), default=inf)
                self.assertEqual(cuello, real)
