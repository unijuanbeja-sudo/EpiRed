"""Resultados esperados del informe y casos que pueden romper la estructura."""

import unittest

from datos import crear_red
from grafo import Grafo, Vertice


class PruebasGrafo(unittest.TestCase):
    def setUp(self):
        self.grafo = crear_red()

    def test_matriz_completa_del_informe(self):
        esperada = [
            [0, 20, 15, 30, 0, 0, 35, 0, 0, 0],
            [20, 0, 30, 0, 0, 0, 20, 0, 0, 0],
            [15, 30, 0, 10, 0, 35, 0, 0, 0, 0],
            [30, 0, 10, 0, 12, 0, 0, 0, 0, 0],
            [0, 0, 0, 12, 0, 20, 0, 0, 0, 0],
            [0, 0, 35, 0, 20, 0, 0, 0, 0, 0],
            [35, 20, 0, 0, 0, 0, 0, 15, 0, 40],
            [0, 0, 0, 0, 0, 0, 15, 0, 20, 0],
            [0, 0, 0, 0, 0, 0, 0, 20, 0, 0],
            [0, 0, 0, 0, 0, 0, 40, 0, 0, 0],
        ]
        self.assertEqual(self.grafo.matriz, esperada)
        self.assertEqual(self.grafo.Componentes(), [list("ABCDEFGHIJ")])

    def test_grados_y_desempates(self):
        self.assertEqual([self.grafo.CalcularGrado(id) for id in self.grafo.ids],
                         [4, 3, 4, 3, 2, 2, 4, 2, 1, 1])
        self.assertEqual(self.grafo.ObtenerGradosExtremos(), ("A", "I"))

    def test_falla_del_nodo_critico(self):
        self.grafo.BorrarVertice("G")
        self.assertEqual(self.grafo.Componentes(), [list("ABCDEF"), list("HI"), ["J"]])
        self.assertEqual(self.grafo.CalcularGrado("J"), 0)
        self.assertEqual(len(self.grafo.Aristas()), 9)
        self.assertEqual(len(self.grafo.matriz), 9)
        self.assertTrue(all(len(fila) == 9 for fila in self.grafo.matriz))

    def test_falla_de_arista_sin_nodos_aislados(self):
        self.grafo.BorrarArco("G", "H")
        self.assertEqual(self.grafo.Componentes(), [list("ABCDEFGJ"), list("HI")])
        self.assertEqual(len(self.grafo.Aristas()), 12)
        self.assertTrue(all(self.grafo.CalcularGrado(id) > 0 for id in self.grafo.ids))
        self.assertFalse(self.grafo.EsAdyacente("H", "G"))

    def test_tres_caminos_y_minimo_global(self):
        for camino, esperado in [("ACF", (2, 50)), ("ADEF", (3, 62)), ("ACDEF", (4, 57))]:
            self.assertEqual(self.grafo.CalcularCostoCamino(list(camino)), esperado)
        self.assertEqual(self.grafo.CaminoMinimo("A", "F"), (list("ACF"), 50))

    def test_minimo_se_recalcula_al_editar_pesos(self):
        self.grafo.Union("C", "F", 100)
        self.assertEqual(self.grafo.CaminoMinimo("A", "F"), (list("ACDEF"), 57))
        self.assertEqual(len(self.grafo.Aristas()), 13)

    def test_rutas_invalidas_ciclos_y_un_solo_nodo(self):
        for ruta in [[], list("AEF"), list("AZF")]:
            self.assertFalse(self.grafo.EsCaminoValido(ruta))
            with self.assertRaises(ValueError):
                self.grafo.CalcularCostoCamino(ruta)
        self.assertEqual(self.grafo.CalcularCostoCamino(["A"]), (0, 0))
        self.assertEqual(self.grafo.CaminoMinimo("A", "A"), (["A"], 0))
        self.assertTrue(self.grafo.EsCiclo(list("ABCA")))
        self.assertTrue(self.grafo.EsCiclo(list("CDEFC")))
        for ruta in [list("ABA"), list("ABCBCA"), list("AEFA"), ["A"], []]:
            self.assertFalse(self.grafo.EsCiclo(ruta))

    def test_bfs_y_colas_del_informe(self):
        self.assertEqual(self.grafo.RecorridoAnchura("A"), list("ABCDGFEHJI"))
        traza = self.grafo.TrazaAnchura("A")
        self.assertEqual([p["cola"] for p in traza],
                         [list(s) for s in ["BCDG", "CDG", "DGF", "GFE", "FEHJ",
                                           "EHJ", "HJ", "JI", "I", ""]])
        self.assertEqual([p["nivel"] for p in traza], [0, 1, 1, 1, 1, 2, 2, 2, 2, 3])

    def test_dfs_con_retrocesos_reales(self):
        self.assertEqual(self.grafo.RecorridoProfundidad("A"), list("ABCDEFGHIJ"))
        traza = self.grafo.TrazaProfundidad("A")
        self.assertEqual(traza[6]["rama"], list("ABG"))
        self.assertEqual(traza[9]["rama"], list("ABGJ"))
        for paso in traza:
            self.assertTrue(self.grafo.EsCaminoValido(paso["rama"]))

    def test_red_desconectada_y_recorridos_parciales(self):
        self.grafo.BorrarVertice("G")
        self.assertEqual(self.grafo.CaminoMinimo("A", "J"), ([], None))
        self.assertEqual(self.grafo.RecorridoAnchura("H"), list("HI"))
        self.assertEqual(self.grafo.RecorridoProfundidad("J"), ["J"])

    def test_insertar_en_medio_preserva_conexiones(self):
        self.grafo.AñadirVertice(Vertice("AA", "Municipio de prueba"))
        self.assertEqual(self.grafo.ids[:3], ["A", "AA", "B"])
        self.assertEqual(self.grafo.CalcularCostoCamino(list("ACF")), (2, 50))
        self.assertEqual(self.grafo.CalcularGrado("AA"), 0)
        self.grafo.Union("AA", "J", 7.5)
        self.assertEqual(self.grafo.CalcularCostoCamino(["J", "AA"]), (1, 7.5))
        self.grafo.BorrarVertice("AA")
        self.assertEqual(self.grafo.matriz, crear_red().matriz)

    def test_entradas_invalidas_no_modifican_la_red(self):
        original = [fila[:] for fila in self.grafo.matriz]
        for peso in [0, -1, "hola", float("nan"), float("inf"), -float("inf")]:
            with self.assertRaises(ValueError):
                self.grafo.Union("A", "B", peso)
        for accion in [lambda: self.grafo.Union("A", "A", 10),
                       lambda: self.grafo.Union("A", "Z", 10),
                       lambda: self.grafo.BorrarArco("A", "E"),
                       lambda: self.grafo.BorrarVertice("Z"),
                       lambda: self.grafo.AñadirVertice(Vertice("A", "Duplicado"))]:
            with self.assertRaises(ValueError):
                accion()
        self.assertEqual(self.grafo.matriz, original)

    def test_red_vacia_y_ultimo_municipio(self):
        grafo = Grafo()
        self.assertEqual(grafo.Componentes(), [])
        self.assertEqual(grafo.ObtenerGradosExtremos(), (None, None))
        with self.assertRaises(ValueError):
            grafo.RecorridoAnchura("A")
        grafo.AñadirVertice(Vertice("A", "Único"))
        self.assertEqual(grafo.Componentes(), [["A"]])
        self.assertEqual(grafo.CalcularGrado("A"), 0)
        grafo.BorrarVertice("A")
        self.assertEqual(grafo.matriz, [])

    def test_datos_del_vertice(self):
        self.assertEqual(Vertice(" k ", " Prueba ", casos=2).id, "K")
        for datos in [("", "Prueba", None), ("A-B", "Prueba", None),
                      ("K", "", None), ("K", "Prueba", -1), ("K", "Prueba", 1.5)]:
            with self.assertRaises(ValueError):
                Vertice(datos[0], datos[1], casos=datos[2])


if __name__ == "__main__":
    unittest.main()
