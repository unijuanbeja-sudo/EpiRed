import unittest
from copy import deepcopy
from math import inf
from epired_taller2 import crear_red, crear_escenario_costos
from epired_taller2 import Grafo
from epired_taller2 import DetectarAnomaliaDeCicloNegativo as detectar


class TestCiclos(unittest.TestCase):
    def test_negativo_sin_ciclo_y_original_intacto(self):
        g = crear_red()
        antes = g.estado()
        c = crear_escenario_costos(g, False)
        self.assertEqual(c.matriz[0][1], -5)
        self.assertEqual(c.matriz[1][0], 10)
        estado_costos = c.estado()
        f = c.FloydWarshall()
        self.assertEqual(detectar(f['distancias'], f['ids']),
                         {'hay_anomalia': False, 'ids_diagnosticos': []})
        self.assertEqual(c.estado(), estado_costos)
        self.assertEqual(g.estado(), antes)

    def test_con_ciclo_y_matriz_intacta(self):
        g = crear_red()
        antes = g.estado()
        c = crear_escenario_costos(g, True)
        self.assertEqual(c.matriz[0][1] + c.matriz[1][2] + c.matriz[2][0], -15)
        f = c.FloydWarshall()
        matriz = deepcopy(f['distancias'])
        r = detectar(f['distancias'], f['ids'])
        self.assertTrue(r['hay_anomalia'])
        self.assertIn('A', r['ids_diagnosticos'])
        self.assertIn('B', r['ids_diagnosticos'])
        self.assertEqual(f['distancias'], matriz)
        self.assertEqual(g.estado(), antes)
        with self.assertRaises(ValueError):
            c.RutaFloyd(f, 'A', 'F')

    def test_dijkstra_rechaza_negativos(self):
        for ciclo in [False, True]:
            with self.assertRaises(ValueError):
                crear_escenario_costos(crear_red(), ciclo).Dijkstra('A')

    def test_ciclo_desconectado(self):
        g = Grafo('ABCD', dirigido=True, permitir_negativos=True)
        g.Union('C', 'D', -3)
        g.Union('D', 'C', 1)
        r = detectar(g.FloydWarshall()['distancias'], g.ids)
        self.assertEqual(r['ids_diagnosticos'], ['C', 'D'])

    def test_vacio_unitario_y_diagonal_negativa(self):
        self.assertFalse(detectar([])['hay_anomalia'])
        self.assertFalse(detectar([[0]])['hay_anomalia'])
        self.assertEqual(detectar([[-1]])['ids_diagnosticos'], ['A'])

    def test_matrices_e_ids_invalidos(self):
        for m in [None, [[0,1]], [[float('nan')]], [[-inf]], [['x']], [[True]]]:
            with self.subTest(m=m), self.assertRaises(ValueError):
                detectar(m)
        for ids in [['A'], ['A','A'], ['A',None]]:
            with self.subTest(ids=ids), self.assertRaises(ValueError):
                detectar([[0,inf],[inf,0]], ids)

    def test_ids_personalizados(self):
        self.assertEqual(detectar([[-1]], ['Medellin'])['ids_diagnosticos'], ['Medellin'])
