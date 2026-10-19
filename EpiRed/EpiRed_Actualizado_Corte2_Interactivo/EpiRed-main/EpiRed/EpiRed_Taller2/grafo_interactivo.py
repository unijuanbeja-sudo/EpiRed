"""Vista sencilla con Tkinter. Los algoritmos siguen en epired_taller2.py."""
import tkinter as tk
from tkinter import ttk

from epired_taller2 import (
    MUNICIPIOS, REPORTES, crear_red, RutaMayorCapacidad,
    GenerarRutaConRespaldo, DetectarPuntosCriticosDeFalla,
)


# Posiciones de dibujo, no coordenadas geográficas.
POSICIONES = {
    "A": (180, 240), "B": (340, 40), "C": (180, 100),
    "D": (340, 350), "E": (500, 350), "F": (500, 100),
    "G": (650, 240), "H": (780, 240), "I": (900, 240),
    "J": (650, 370),
}


class VistaGrafo:
    def __init__(self, ventana, red):
        self.red = red
        self.posiciones = POSICIONES.copy()
        self.rutas = []
        self.criticos = []
        self.arrastrado = None
        ventana.title("EpiRed | Grafo interactivo")
        ventana.minsize(1000, 620)

        tk.Label(ventana, text="EpiRed · Red de municipios", font=("Arial", 18, "bold")).pack(pady=8)
        tk.Label(ventana, text="Arrastra los nodos para moverlos. Haz clic en un municipio para ver sus datos.",
                 font=("Arial", 11)).pack()
        controles = ttk.Frame(ventana)
        controles.pack(pady=10)
        self.origen = tk.StringVar(value="A")
        self.destino = tk.StringVar(value="F")
        self.peso = tk.StringVar(value="Tiempo (min)")
        for titulo, variable in (("Origen", self.origen), ("Destino", self.destino)):
            ttk.Label(controles, text=titulo).pack(side="left", padx=5)
            ttk.Combobox(controles, textvariable=variable, values=red.ids,
                         state="readonly", width=4).pack(side="left")
        ttk.Label(controles, text="Etiquetas").pack(side="left", padx=5)
        selector = ttk.Combobox(controles, textvariable=self.peso, width=21,
                               values=["Tiempo (min)", "Capacidad (u./viaje)"], state="readonly")
        selector.pack(side="left")
        selector.bind("<<ComboboxSelected>>", lambda evento: self.dibujar())
        for titulo, accion in (("Más rápida", self.rapida), ("Mayor capacidad", self.capacidad),
                               ("Respaldo", self.respaldo), ("Puntos críticos", self.fallas),
                               ("Restablecer", self.restablecer)):
            ttk.Button(controles, text=titulo, command=accion).pack(side="left", padx=3)

        self.canvas = tk.Canvas(ventana, width=980, height=450, bg="#f4f7fb", highlightthickness=0)
        self.canvas.pack(padx=12, pady=5)
        self.canvas.bind("<Button-1>", self.seleccionar)
        self.canvas.bind("<B1-Motion>", self.mover)
        self.canvas.bind("<ButtonRelease-1>", self.soltar)
        tk.Label(ventana, text="Azul: municipio / ruta primaria o consultada   |   Verde: respaldo   |   Naranja: punto crítico",
                 font=("Arial", 10)).pack()
        self.mensaje = tk.StringVar(value="10 municipios · 13 conexiones bidireccionales · Datos ficticios. Diagrama sin escala geográfica.")
        tk.Label(ventana, textvariable=self.mensaje, font=("Arial", 11), wraplength=950).pack(pady=8)
        self.detalle = tk.StringVar(value="Selecciona un municipio para consultar sus reportes.")
        tk.Label(ventana, textvariable=self.detalle, font=("Arial", 10), wraplength=950).pack(pady=(0, 10))
        self.dibujar()

    def dibujar(self):
        """Primero dibuja conexiones y después municipios sobre ellas."""
        self.canvas.delete("all")
        for a, b, minutos, capacidad in self.red.Aristas():
            color, grosor = "#9aa9bc", 2
            for ruta, tono in self.rutas:
                if any({a, b} == {x, y} for x, y in zip(ruta, ruta[1:])):
                    color, grosor = tono, 5
            x1, y1 = self.posiciones[a]
            x2, y2 = self.posiciones[b]
            self.canvas.create_line(x1, y1, x2, y2, fill=color, width=grosor, tags="arista")
            valor = minutos if self.peso.get() == "Tiempo (min)" else capacidad
            self.canvas.create_text((x1+x2)/2, (y1+y2)/2-10, text=str(valor),
                                    fill="#27384e", font=("Arial", 10, "bold"), tags="peso")
        for id, (x, y) in self.posiciones.items():
            color = "#a94b08" if id in self.criticos else "#2463a6"
            self.canvas.create_oval(x-22, y-22, x+22, y+22, fill=color, outline="white", width=2, tags="nodo")
            self.canvas.create_text(x, y, text=id, fill="white", font=("Arial", 12, "bold"))
            self.canvas.create_text(x, y+34, text=MUNICIPIOS[id], fill="#27384e", font=("Arial", 10))

    def seleccionar(self, evento):
        self.arrastrado = None
        # Orden inverso: si se superponen, seleccionar el que está encima.
        for id in reversed(self.red.ids):
            x, y = self.posiciones[id]
            if (evento.x-x)**2 + (evento.y-y)**2 <= 22**2:
                self.arrastrado = id
                c, r, f = REPORTES[id]
                self.detalle.set(f"{id} · {MUNICIPIOS[id]}: confirmados {c}, recuperados {r}, fallecidos {f}, activos {c-r-f}.")
                break

    def mover(self, evento):
        if self.arrastrado is not None:
            # Mantener el nodo y su nombre dentro del área visible.
            x = max(65, min(915, evento.x))
            y = max(30, min(400, evento.y))
            self.posiciones[self.arrastrado] = (x, y)
            self.dibujar()

    def soltar(self, evento):
        self.arrastrado = None

    def rapida(self):
        a, b = self.origen.get(), self.destino.get()
        resultado = self.red.Dijkstra(a)
        ruta = self.red.RutaDijkstra(resultado, b)
        self.rutas, self.criticos = [(ruta, "#2463a6")], []
        self.mensaje.set(f"Más rápida: {' → '.join(ruta)} · {resultado['distancias'][b]:g} minutos.")
        self.dibujar()

    def capacidad(self):
        ruta, capacidad = RutaMayorCapacidad(self.origen.get(), self.destino.get(), self.red)
        self.rutas, self.criticos = [(ruta, "#2463a6")], []
        detalle = ("Sin traslado; no se recorren aristas." if len(ruta) == 1
                   else f"Cuello de botella: {capacidad:g} unidades por viaje.")
        self.mensaje.set(f"Mayor capacidad: {' → '.join(ruta)} · {detalle}")
        self.dibujar()

    def respaldo(self):
        r = GenerarRutaConRespaldo(self.origen.get(), self.destino.get(), self.red)
        self.rutas = [(r['primaria'], "#2463a6"), (r['respaldo'], "#15803d")]
        self.criticos = []
        texto = f"Primaria: {' → '.join(r['primaria'])} ({r['costo_primario']:g} min). "
        if r['alerta']:
            texto += r['alerta']
        elif self.origen.get() == self.destino.get():
            texto += "Sin traslado; ambas rutas tienen cero aristas."
        else:
            texto += f"Respaldo: {' → '.join(r['respaldo'])} ({r['costo_respaldo']:g} min)."
            if r['porcentaje'] is not None:
                texto += f" Diferencia: {r['porcentaje']:g} %."
        self.mensaje.set(texto)
        self.dibujar()

    def fallas(self):
        self.criticos = DetectarPuntosCriticosDeFalla(self.red)['criticos']
        self.rutas = []
        self.mensaje.set("Puntos críticos: " + ", ".join(f"{id} ({MUNICIPIOS[id]})" for id in self.criticos))
        self.dibujar()

    def restablecer(self):
        self.posiciones = POSICIONES.copy()
        self.rutas, self.criticos = [], []
        self.mensaje.set("Vista restablecida. Mover los nodos solo cambia el dibujo; los datos del grafo siguen iguales.")
        self.dibujar()


def abrir_grafo(red=None):
    ventana = tk.Tk()
    VistaGrafo(ventana, crear_red() if red is None else red)
    ventana.mainloop()


if __name__ == "__main__":
    abrir_grafo()
