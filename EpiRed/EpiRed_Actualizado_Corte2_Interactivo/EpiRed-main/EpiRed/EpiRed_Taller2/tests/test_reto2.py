import unittest
from epired_taller2 import crear_red
from epired_taller2 import Grafo
from epired_taller2 import DetectarPuntosCriticosDeFalla, componentes


class TestCriticos(unittest.TestCase):
    def test_g_h_y_estado(self):
        g = crear_red()
        antes = g.estado()
        r = DetectarPuntosCriticosDeFalla(g)
        self.assertEqual(r['criticos'], ['G', 'H'])
        self.assertEqual(len(r['ensayos']), 10)
        self.assertEqual(r['ensayos']['G']['componentes'], [list('ABCDEF'), list('HI'), ['J']])
        self.assertEqual(r['ensayos']['G']['nuevos_aislados'], ['J'])
        self.assertEqual(r['ensayos']['H']['nuevos_aislados'], ['I'])
        self.assertEqual(g.estado(), antes)

    def test_previamente_desconectado(self):
        g = Grafo('ABCD')
        g.Union('A', 'B', 1)
        g.Union('B', 'C', 1)
        r = DetectarPuntosCriticosDeFalla(g)
        self.assertEqual(len(r['componentes_iniciales']), 2)
        self.assertEqual(r['criticos'], ['B'])
        self.assertEqual(r['ensayos']['B']['nuevos_aislados'], ['A', 'C'])
        self.assertEqual(r['ensayos']['B']['aislados'], ['A', 'C', 'D'])

    def test_vacio_unitario_y_aislados(self):
        for ids in ['', 'A', 'AB']:
            self.assertEqual(DetectarPuntosCriticosDeFalla(Grafo(ids))['criticos'], [])

    def test_dos_nodos_no_es_critico_pero_si_nuevo_aislado(self):
        g = Grafo('AB')
        g.Union('A', 'B', 1)
        r = DetectarPuntosCriticosDeFalla(g)
        self.assertEqual(r['criticos'], [])
        self.assertEqual(r['ensayos']['A']['nuevos_aislados'], ['B'])

    def test_cero_es_arista(self):
        g = Grafo('AB')
        g.Union('A', 'B', 0)
        self.assertEqual(componentes(g), [['A', 'B']])

    def test_entradas_invalidas(self):
        with self.assertRaises(ValueError):
            componentes(Grafo('AB'), 'X')
        with self.assertRaises(ValueError):
            DetectarPuntosCriticosDeFalla(Grafo('AB', dirigido=True))
