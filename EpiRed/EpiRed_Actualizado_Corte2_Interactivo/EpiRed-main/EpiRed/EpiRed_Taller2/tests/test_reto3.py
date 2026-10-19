import unittest
from math import inf
from epired_taller2 import crear_red
from epired_taller2 import Grafo
from epired_taller2 import GenerarRutaConRespaldo, ALERTA


def aristas(ruta):
    return {frozenset((a, b)) for a, b in zip(ruta, ruta[1:])}


class TestRespaldo(unittest.TestCase):
    def test_a_f_costos_porcentaje_y_estado(self):
        g = crear_red()
        antes = g.estado()
        r = GenerarRutaConRespaldo('A', 'F', g)
        self.assertEqual(r['primaria'], list('ACF'))
        self.assertEqual(r['respaldo'], list('ADEF'))
        self.assertEqual((r['costo_primario'], r['costo_respaldo'], r['porcentaje']), (50, 62, 24))
        self.assertFalse(aristas(r['primaria']) & aristas(r['respaldo']))
        self.assertEqual(g.estado(), antes)

    def test_sin_respaldo_y_estado(self):
        g = crear_red()
        antes = g.estado()
        r = GenerarRutaConRespaldo('A', 'I', g)
        self.assertEqual(r['alerta'], ALERTA)
        self.assertEqual(r['respaldo'], [])
        self.assertEqual(r['costo_respaldo'], inf)
        self.assertEqual(g.estado(), antes)

    def test_sin_primaria(self):
        r = GenerarRutaConRespaldo('A', 'B', Grafo('AB'))
        self.assertEqual(r['primaria'], [])
        self.assertEqual(r['alerta'], ALERTA)
        self.assertIsNone(r['porcentaje'])

    def test_mismo_origen(self):
        r = GenerarRutaConRespaldo('A', 'A')
        self.assertEqual(r['primaria'], ['A'])
        self.assertEqual(r['respaldo'], ['A'])
        self.assertEqual(r['costo_primario'], 0)
        self.assertIsNone(r['porcentaje'])

    def test_costo_cero_con_extremos_distintos(self):
        g = Grafo('ABC')
        g.Union('A', 'B', 0)
        g.Union('A', 'C', 1)
        g.Union('C', 'B', 1)
        r = GenerarRutaConRespaldo('A', 'B', g)
        self.assertEqual(r['costo_respaldo'], 2)
        self.assertIsNone(r['porcentaje'])

    def test_retirar_solo_aristas_y_ambos_sentidos(self):
        g = crear_red()
        copia = g.copia()
        copia.BorrarArco('A', 'C')
        copia.BorrarArco('C', 'F')
        self.assertEqual(copia.ids, g.ids)
        eliminadas = {frozenset('AC'), frozenset('CF')}
        for i, a in enumerate(g.ids):
            for j, b in enumerate(g.ids):
                if frozenset((a, b)) in eliminadas:
                    self.assertEqual(copia.matriz[i][j], inf)
                    self.assertEqual(copia.capacidades[i][j], 0)
                else:
                    self.assertEqual(copia.matriz[i][j], g.matriz[i][j])
                    self.assertEqual(copia.capacidades[i][j], g.capacidades[i][j])

    def test_respaldo_puede_compartir_vertice_interno(self):
        g = Grafo('ABCDEF')
        for a, b, w in [('A','B',1), ('B','C',1), ('C','F',1),
                        ('A','D',2), ('D','B',2), ('B','E',2), ('E','F',2)]:
            g.Union(a,b,w)
        r = GenerarRutaConRespaldo('A','F',g)
        self.assertEqual(r['primaria'], list('ABCF'))
        self.assertEqual(r['respaldo'], list('ADBEF'))
        self.assertFalse(aristas(r['primaria']) & aristas(r['respaldo']))

    def test_todos_los_pares_sin_aristas_compartidas_y_estado(self):
        g = crear_red()
        antes = g.estado()
        for a in g.ids:
            for b in g.ids:
                r = GenerarRutaConRespaldo(a, b, g)
                self.assertFalse(aristas(r['primaria']) & aristas(r['respaldo']))
                self.assertEqual(g.estado(), antes)
                for clave, costo in [('primaria','costo_primario'), ('respaldo','costo_respaldo')]:
                    if r[clave]:
                        self.assertEqual(sum(g.matriz[g._indice(x)][g._indice(y)]
                                             for x,y in zip(r[clave],r[clave][1:])), r[costo])

    def test_ids_y_red_dirigida(self):
        with self.assertRaises(ValueError):
            GenerarRutaConRespaldo('X', 'F')
        with self.assertRaises(ValueError):
            GenerarRutaConRespaldo('A', 'B', Grafo('AB', dirigido=True))
