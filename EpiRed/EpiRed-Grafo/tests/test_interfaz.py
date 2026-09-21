"""Pruebas de integración de la interfaz; necesitan un escritorio disponible."""

import tkinter as tk
from tkinter import ttk
import unittest
from unittest.mock import patch

from interfaz import EpiRed


class PruebasInterfaz(unittest.TestCase):
    def setUp(self):
        try:
            self.ventana = tk.Tk()
        except tk.TclError:
            self.skipTest("No hay un escritorio disponible para Tkinter.")
        self.ventana.withdraw()
        self.app = EpiRed(self.ventana)
        self.ventana.update_idletasks()

    def tearDown(self):
        if hasattr(self, "app"):
            self.app.cerrar()

    def test_tablas_y_fallas_independientes(self):
        self.assertEqual(len(self.app.matriz_vista.get_children()), 10)
        self.app.simular("nodo")
        self.assertIn("J", self.app.detalle_red.cget("text"))
        self.assertEqual(len(self.app.matriz_vista.get_children()), 9)
        self.app.simular("arista")
        self.assertEqual(len(self.app.grafo.ids), 10)
        self.assertEqual(len(self.app.grafo.Componentes()), 2)
        self.app.restaurar()
        self.assertEqual(len(self.app.grafo.Aristas()), 13)

    def test_camino_minimo_ciclo_e_invalido(self):
        self.app.camino_minimo()
        self.assertEqual(self.app.nodos_marcados, list("ACF"))
        self.app.ruta.set("A → B → C → A")
        self.app.evaluar_camino()
        self.assertIn("Ciclo simple: sí", self.app.detalle_camino.cget("text"))
        self.app.ruta.set("A E F")
        with patch("interfaz.messagebox.showerror") as error:
            self.app.ejecutar(self.app.evaluar_camino)
            error.assert_called_once()
        self.assertEqual(self.app.aristas_marcadas, set())
        self.assertIn("no válido", self.app.detalle_camino.cget("text"))

    def test_dfs_no_dibuja_salto_f_g_y_cancelacion(self):
        self.app.preparar_recorrido("DFS")
        for _ in range(7):
            self.app.siguiente()
        self.assertEqual(self.app.actual, "G")
        self.assertNotIn(frozenset(("F", "G")), self.app.aristas_marcadas)
        self.assertIn(frozenset(("B", "G")), self.app.aristas_marcadas)
        self.app.reproducir()
        self.assertIsNotNone(self.app.temporizador)
        self.app.simular("nodo")
        self.assertIsNone(self.app.temporizador)
        self.assertEqual(self.app.traza, [])

    def test_edicion_actualiza_matriz_y_consultas(self):
        self.app.nuevo_nombre.set("Municipio de prueba")
        self.app.nuevos_casos.set("4")
        self.app.agregar_municipio()
        self.assertEqual(len(self.app.matriz_vista.get_children()), 11)
        self.app.enlace_a.set("J")
        self.app.enlace_b.set("K")
        self.app.minutos.set("8.5")
        self.app.unir()
        self.app.adyacentes()
        self.assertIn("sí tienen", self.app.estado.get())
        self.app.borrar_arco()
        self.assertFalse(self.app.grafo.EsAdyacente("J", "K"))
        self.app.borrar_id.set("K")
        self.app.borrar_municipio()
        self.assertEqual(len(self.app.matriz_vista.get_children()), 10)

    def test_controles_visibles_sin_desplazar_y_edicion_aparte(self):
        self.ventana.geometry("980x620")
        self.ventana.deiconify()
        self.ventana.update()
        self.assertEqual(len(self.app.herramientas.tabs()), 3)
        self.assertFalse(self.app.ventana_tablas.winfo_viewable())
        self.assertFalse(self.app.ventana_editar.winfo_viewable())
        self.app.preparar_recorrido("DFS")
        for _ in range(7):
            self.app.siguiente()
        for i in range(3):
            self.app.herramientas.select(i)
            self.ventana.update()
            tab = self.app.herramientas.nametowidget(self.app.herramientas.select())
            for control in tab.winfo_children():
                self.assertLessEqual(control.winfo_rooty() + control.winfo_height(),
                                     tab.winfo_rooty() + tab.winfo_height())
                if isinstance(control, ttk.Button):
                    self.assertGreaterEqual(control.winfo_height(), control.winfo_reqheight())
        self.app.abrir(self.app.ventana_editar)
        self.ventana.update()
        self.assertTrue(self.app.ventana_editar.winfo_viewable())
        self.app.ventana_editar.withdraw()
        self.app.abrir(self.app.ventana_editar)
        self.ventana.update()
        self.assertTrue(self.app.ventana_editar.winfo_viewable())

    def test_consulta_y_ruta_con_informacion_epidemiologica(self):
        self.app.seleccionar_municipio("C")
        self.assertIn("Activos: 80", self.app.detalle_municipio.cget("text"))
        self.assertIn("Alto", self.app.detalle_municipio.cget("text"))
        self.app.solo_bajo_medio.set(True)
        self.app.camino_minimo()
        self.assertEqual(self.app.nodos_marcados, list("ADEF"))
        with patch("interfaz.messagebox.showinfo") as info:
            self.app.ver_casos_ruta()
            self.assertIn("Medellín: activos 30", info.call_args.args[1])

    def test_reporte_se_actualiza_y_el_color_no_se_pierde_al_recorrer(self):
        self.app.preparar_recorrido("BFS")
        for _ in range(3):
            self.app.siguiente()
        self.assertIn("Itagüí: activos 80", self.app.detalle_recorrido.cget("text"))
        nodo = self.app.canvas.find_withtag("municipio_C")[0]
        self.assertEqual(self.app.canvas.itemcget(nodo, "fill"), "#f5c7c7")
        self.app.grafo.ActualizarReporte("C", 500, 485, 5)
        self.app.actualizar()
        self.app.seleccionar_municipio("C")
        self.assertIn("Activos: 10", self.app.detalle_municipio.cget("text"))
        self.assertEqual(self.app.traza, [])


if __name__ == "__main__":
    unittest.main()
