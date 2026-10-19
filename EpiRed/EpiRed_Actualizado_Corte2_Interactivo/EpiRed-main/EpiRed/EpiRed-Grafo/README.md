# EpiRed — Taller de grafos

Aplicación sencilla en Python para mostrar el taller. Tiene 10 municipios y 13 conexiones. Los casos, los niveles y los minutos son ficticios.

Abre **iniciar.bat** en Windows, o ejecuta `python main.py`. Necesitas Python 3.10 o superior con Tkinter. No requiere instalar paquetes adicionales.

## Para mostrarlo en clase

1. **Municipios:** pulsa un círculo. A la derecha aparecen sus casos, su grado y sus vecinos.
2. **Caminos:** elige uno de los ejemplos y pulsa **Mostrar camino**. Verás la ruta en naranja, sus conexiones y su costo. También puedes escribir un camino propio con los IDs separados por espacios.
3. **Recorridos:** elige el inicio, pulsa **Iniciar BFS** o **Iniciar DFS** y luego **Siguiente paso**. El borde azul indica dónde estás. **Ver tabla de pasos** abre la cola de BFS o la rama de DFS.

Debajo del grafo hay tres botones:

- **Ver matriz:** abre la matriz completa. La segunda pestaña muestra casos y grados.
- **Probar fallas:** permite quitar G o la conexión G–H. Cada prueba empieza con la red original.
- **Editar red:** permite agregar o quitar municipios y conexiones, cambiar pesos y comprobar adyacencia.

**Reiniciar ejemplo** recupera todos los datos iniciales. Los cambios duran mientras la aplicación esté abierta. Las ventanas auxiliares se cierran con la X y pueden volver a abrirse.

## Ejemplos del taller

| Prueba | Resultado original |
| --- | --- |
| A C F | 2 conexiones, 50 minutos; es el mínimo sin filtro. |
| A D E F | 3 conexiones, 62 minutos. |
| A C D E F | 4 conexiones, 57 minutos. |
| A B C A | Ciclo de 3 conexiones, 65 minutos. |
| A E F | Inválido: A–E no existe. |
| Quitar G | Tres grupos: ABCDEF, HI y J. J queda aislado. |
| Quitar G–H | Dos grupos: ABCDEFGJ y HI. No hay aislados. |
| BFS desde A | A, B, C, D, G, F, E, H, J, I. |
| DFS desde A | A, B, C, D, E, F, G, H, I, J. |

En DFS, después de F se retrocede hasta B antes de visitar G. No existe una conexión directa F–G. BFS recorre por cantidad de conexiones, no por minutos.

## Datos epidemiológicos

Activos = confirmados − recuperados − fallecidos. Si falta una cifra necesaria, aparece **Sin datos**. El nivel del ejercicio es bajo de 0 a 19 activos, medio de 20 a 49 y alto desde 50. No es una clasificación oficial de riesgo.

**Cambiar cifras** permite modificar el municipio elegido. En **Caminos → Buscar el camino más corto…** puedes elegir origen y destino. La casilla opcional admite solo niveles bajo y medio y excluye también los municipios sin datos. No garantiza una ruta segura.

Por ejemplo, A–C–F cuesta 50 minutos. Con filtro aparece A–D–E–F, con 62 minutos. Si cambias los recuperados de C a 485, quedan 10 activos y el filtro vuelve a permitir A–C–F. **Ver casos de esta ruta** muestra los datos de sus municipios.

## Archivos

`main.py` abre la ventana, `grafo.py` contiene los algoritmos, `datos.py` carga el ejemplo e `interfaz.py` muestra los controles. Se conservan las operaciones del taller y la matriz de adyacencia. BFS usa una cola; DFS, recursión; Dijkstra busca el camino de menor tiempo.

En docs/ están el informe original versión 1, sin modificaciones, y la guía de uso en PDF. Para subir este proyecto a GitHub, descomprime el ZIP y sube las carpetas y archivos que contiene. Para abrir el aplicativo, ejecuta iniciar.bat.

Para comprobar el funcionamiento: `python -m unittest discover -s tests -v`. Las pruebas de interfaz necesitan un escritorio disponible. Los cambios están guardados en un repositorio Git local.
