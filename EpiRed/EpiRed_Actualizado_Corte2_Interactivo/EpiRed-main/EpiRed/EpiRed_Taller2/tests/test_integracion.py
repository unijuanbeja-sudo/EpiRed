import contextlib
import io
import unittest
from unittest.mock import patch
from epired_taller2 import crear_red, REPORTES, CONEXIONES
from epired_taller2 import Grafo
from main import main, demo, mostrar_respaldo


class TestIntegracion(unittest.TestCase):
    def test_dijkstra_floyd_100_pares(self):
        g = crear_red()
        f = g.FloydWarshall()
        for i, a in enumerate(g.ids):
            d = g.Dijkstra(a)
            for j, b in enumerate(g.ids):
                self.assertEqual(d['distancias'][b], f['distancias'][i][j])
                ruta = g.RutaFloyd(f, a, b)
                self.assertEqual(sum(g.matriz[g._indice(x)][g._indice(y)]
                                     for x,y in zip(ruta,ruta[1:])), d['distancias'][b])

    def test_datos_preservados(self):
        g = crear_red()
        self.assertEqual(len(g.ids), 10)
        self.assertEqual(len(g.Aristas()), 13)
        for a,b,w in CONEXIONES:
            self.assertEqual(g.matriz[g._indice(a)][g._indice(b)], w)
        self.assertEqual([c-r-f for c,r,f in REPORTES.values()], [30,12,80,10,15,8,60,25,5,45])

    def test_validacion_modelo_y_estado(self):
        for ids in [['A','A'], [''], [None]]:
            with self.assertRaises(ValueError):
                Grafo(ids)
        g = crear_red()
        antes = g.estado()
        for peso in [-1, float('inf'), float('nan'), '5', None, True, 10**400]:
            with self.subTest(peso=peso), self.assertRaises(ValueError):
                g.Union('A','B',peso)
        self.assertEqual(g.estado(), antes)
        with self.assertRaises(ValueError):
            g.Union('A','A',1)
        with self.assertRaises(ValueError):
            g.BorrarArco('I','J')

    def test_demo_completa(self):
        salida = io.StringIO()
        with contextlib.redirect_stdout(salida):
            demo(crear_red())
        for texto in ['RETO 1', 'RETO 2', 'RETO 3', 'RETO 4', '24%', 'Estado original intacto']:
            self.assertIn(texto, salida.getvalue())

    def test_desbordamiento_tiene_error_claro(self):
        g = Grafo('ABC')
        g.Union('A', 'B', 1e308)
        g.Union('B', 'C', 1e308)
        antes = g.estado()
        for algoritmo in [lambda: g.Dijkstra('A'), g.FloydWarshall]:
            with self.assertRaisesRegex(ValueError, 'fuera del rango'):
                algoritmo()
        self.assertEqual(g.estado(), antes)

    def test_alerta_exacta_en_consola(self):
        salida = io.StringIO()
        with contextlib.redirect_stdout(salida):
            mostrar_respaldo(crear_red(), 'A', 'I')
        self.assertIn('Red no redundante entre origen y destino', salida.getvalue().splitlines())

    def test_menu_recupera_errores_y_consulta_todas_las_opciones(self):
        entradas = ['9','1','X','F','1','a','f','2','3','A','F','4','5','6','7','0']
        salida = io.StringIO()
        with patch('sys.argv', ['main.py']), patch('builtins.input', side_effect=entradas), contextlib.redirect_stdout(salida):
            main()
        self.assertIn('Entrada no válida', salida.getvalue())
        self.assertIn('Opción no válida', salida.getvalue())
        self.assertIn('Fin de la exposición', salida.getvalue())
