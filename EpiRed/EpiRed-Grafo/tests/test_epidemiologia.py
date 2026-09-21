import unittest

from datos import crear_red
from grafo import Vertice


class PruebasEpidemiologia(unittest.TestCase):
    def setUp(self):
        self.grafo = crear_red()

    def test_reportes_y_resumen_del_ejemplo(self):
        self.assertEqual([v.activos for v in self.grafo.vertices], [30, 12, 80, 10, 15, 8, 60, 25, 5, 45])
        self.assertEqual(self.grafo.ResumenEpidemiologico(), {
            "reportes_completos": 10, "activos": 290, "mas_activos": "C",
            "menos_activos": "I", "mas_recuperados": "C"})
        self.assertEqual(self.grafo.ConsultarMunicipio("C").nivel_riesgo, "Alto")

    def test_limites_de_clasificacion_didactica(self):
        for activos, nivel in [(0, "Bajo"), (19, "Bajo"), (20, "Medio"), (49, "Medio"), (50, "Alto")]:
            v = Vertice("K", "Ejemplo", casos=100, recuperados=100 - activos, fallecidos=0)
            self.assertEqual(v.nivel_riesgo, nivel)

    def test_desconocido_no_equivale_a_cero(self):
        for datos in [dict(), dict(casos=40), dict(casos=40, recuperados=30),
                      dict(casos=40, fallecidos=0)]:
            v = Vertice("K", "Ejemplo", **datos)
            self.assertIsNone(v.activos)
            self.assertEqual(v.nivel_riesgo, "Sin datos")
        self.grafo.ActualizarReporte("C", 500, 415, None)
        resumen = self.grafo.ResumenEpidemiologico()
        self.assertEqual(resumen["activos"], 210)
        self.assertEqual(resumen["reportes_completos"], 9)

    def test_ruta_filtrada_y_ruta_rapida_son_distintas(self):
        self.assertEqual(self.grafo.CaminoMinimo("A", "F"), (list("ACF"), 50))
        self.assertEqual(self.grafo.CaminoMinimo("A", "F", True), (list("ADEF"), 62))
        # Aplicar el filtro no borra C ni modifica conexiones.
        self.assertEqual(len(self.grafo.ids), 10)
        self.assertEqual(len(self.grafo.Aristas()), 13)

    def test_filtro_tambien_revisa_extremos_y_datos_desconocidos(self):
        self.assertEqual(self.grafo.CaminoMinimo("C", "F", True), ([], None))
        self.assertEqual(self.grafo.CaminoMinimo("A", "C", True), ([], None))
        self.grafo.ActualizarReporte("D", 180, None, None)
        self.assertEqual(self.grafo.CaminoMinimo("A", "F", True), ([], None))
        self.assertEqual(self.grafo.CaminoMinimo("A", "F"), (list("ACF"), 50))

    def test_cambiar_reporte_recalcula_ruta_sin_cambiar_pesos(self):
        matriz = [fila[:] for fila in self.grafo.matriz]
        self.grafo.ActualizarReporte("C", 500, 485, 5)
        self.assertEqual(self.grafo.ConsultarMunicipio("C").activos, 10)
        self.assertEqual(self.grafo.ConsultarMunicipio("C").nivel_riesgo, "Bajo")
        self.assertEqual(self.grafo.CaminoMinimo("A", "F", True), (list("ACF"), 50))
        self.assertEqual(self.grafo.matriz, matriz)

    def test_reportes_invalidos_no_sustituyen_los_datos(self):
        anterior = self.grafo.ConsultarMunicipio("A")
        for cifras in [(10, 9, 2), (10, 11, None), (None, 1, None),
                       (10, -1, 0), (10, 2.5, 0), (10, 2, True)]:
            with self.assertRaises(ValueError):
                self.grafo.ActualizarReporte("A", *cifras)
            self.assertIs(self.grafo.ConsultarMunicipio("A"), anterior)

    def test_informacion_epidemiologica_de_una_ruta(self):
        datos = self.grafo.InformacionRuta(list("ACF"))
        self.assertEqual([(v.nombre, v.activos, v.nivel_riesgo) for v in datos],
                         [("Medellín", 30, "Medio"), ("Itagüí", 80, "Alto"), ("Caldas", 8, "Bajo")])
        with self.assertRaises(ValueError):
            self.grafo.InformacionRuta(list("AEF"))
