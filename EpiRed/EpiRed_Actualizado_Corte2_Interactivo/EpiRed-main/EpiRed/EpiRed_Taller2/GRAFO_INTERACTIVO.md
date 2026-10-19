# Grafo interactivo de EpiRed

## 1. Abrir la visualización

1. Extrae el ZIP completo.
2. En VS Code abre la carpeta `EpiRed-main/EpiRed/EpiRed_Taller2`.
3. Abre **Terminal → Nueva terminal** y ejecuta:

```powershell
python main.py
```

4. Escribe **8** y presiona Enter. Se abre una ventana con los 10 municipios y las 13 conexiones.
5. Cierra esa ventana para volver al menú de la consola.

También puedes abrir solo la visualización:

```powershell
python grafo_interactivo.py
```

Usa Python 3.10 o superior con Tkinter. No requiere internet ni paquetes de pip. En la instalación habitual de Python para Windows, Tkinter viene incluido; si falta, modifica la instalación y activa **Tcl/Tk e IDLE**. Si `python` no se reconoce, prueba `py -3`.

## 2. Qué puedes hacer

- **Mover municipios:** mantén presionado el botón izquierdo sobre un círculo y arrástralo. Sus conexiones se mueven con él.
- **Consultar datos:** haz clic en un círculo para ver el nombre y los reportes ficticios debajo del dibujo.
- **Cambiar las etiquetas:** elige tiempo en minutos o capacidad en unidades por viaje.
- **Consultar rutas:** selecciona los IDs de origen y destino y pulsa **Más rápida**, **Mayor capacidad** o **Respaldo**. Después de cambiar los IDs, pulsa de nuevo el botón para actualizar el resultado.
- **Ver puntos críticos:** pulsa ese botón para marcar G y H en naranja. Este análisis usa toda la red, independientemente del origen y destino seleccionados.
- **Restablecer:** recupera las posiciones iniciales y quita los resaltados.

El azul resalta la ruta consultada o primaria; el verde, el respaldo. El resultado escrito debajo del dibujo indica la ruta y sus valores. El dibujo representa conexiones, no ubicaciones geográficas reales. Las líneas que se cruzan no crean nuevos municipios.

## 3. Ejemplo breve para exponer

1. Selecciona **A** y **F**. Pulsa **Más rápida**: aparece **A → C → F**, de **50 minutos**.
2. Pulsa **Mayor capacidad**: aparece **A → D → E → F**, con **55 unidades por viaje**. La capacidad es el menor valor de los enlaces de esa ruta.
3. Pulsa **Respaldo**: la primaria queda azul y el respaldo verde. El respaldo tarda **62 minutos**, un **24 %** más.
4. Pulsa **Puntos críticos**: se resaltan **G y H**.
5. Cambia el destino a **I** y pulsa **Respaldo**: se muestra la alerta **Red no redundante entre origen y destino**.
6. Arrastra un municipio y explica: “Solo cambia su posición en el dibujo; los tiempos, capacidades y conexiones siguen iguales”.

Para mantener la exposición de 25 minutos, usa estos botones como apoyo visual durante los ejemplos ya asignados a cada estudiante. El reto 4 se sigue demostrando con la opción 4 de la consola: utiliza costos dirigidos, mientras que esta ventana muestra la red de traslados bidireccional.

## 4. Código que se añadió

- `grafo_interactivo.py`: usa un `Canvas` de Tkinter para dibujar las conexiones como líneas y los municipios como círculos.
- `dibujar()`: lee las aristas del mismo grafo; muestra tiempos o capacidades y aplica los colores.
- `seleccionar()`, `mover()` y `soltar()`: permiten consultar y arrastrar los nodos.
- Los botones llaman a los algoritmos existentes en `epired_taller2.py`; no contienen nuevas implementaciones de esos algoritmos.
- En `main.py` se añadió la opción 8 para abrir la ventana. Al cerrarla, la consola comprueba que la red original sigue intacta.

Las posiciones se guardan en un diccionario separado de las matrices. Por eso mover un círculo no modifica el grafo. El botón Restablecer recupera ese diccionario inicial.
