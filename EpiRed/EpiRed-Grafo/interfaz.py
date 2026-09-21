"""Interfaz de escritorio con Tkinter; la lógica del grafo está en grafo.py."""

import math
import tkinter as tk
from tkinter import messagebox, ttk

from datos import CAMINOS, POSICIONES, crear_red
from grafo import Vertice


class EpiRed:
    def __init__(self, ventana):
        self.ventana = ventana
        self.grafo = crear_red()
        self.combos = []
        self.nodos_marcados = []
        self.aristas_marcadas = set()
        self.actual = None
        self.traza = []
        self.paso = 0
        self.temporizador = None
        ventana.title("EpiRed | Taller — interfaz sencilla")
        ventana.geometry("1100x680")
        ventana.minsize(980, 620)
        ventana.protocol("WM_DELETE_WINDOW", self.cerrar)
        estilo = ttk.Style()
        estilo.theme_use("clam")
        estilo.configure("TLabel", font=("Segoe UI", 11))
        estilo.configure("TButton", font=("Segoe UI", 11), padding=(10, 8))
        estilo.configure("TNotebook.Tab", font=("Segoe UI", 11), padding=(10, 9))
        estilo.configure("Treeview", font=("Segoe UI", 10), rowheight=27)
        estilo.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))

        cabecera = ttk.Frame(ventana, padding=(18, 12))
        cabecera.pack(fill="x")
        ttk.Label(cabecera, text="EpiRed · Taller de grafos",
                  font=("Segoe UI", 18, "bold")).pack(side="left")
        ttk.Button(cabecera, text="Reiniciar ejemplo", command=self.restaurar).pack(side="right")
        self.estado = tk.StringVar(value="Para empezar, haz clic en un municipio.")
        ttk.Label(ventana, textvariable=self.estado, padding=(18, 10),
                  wraplength=920).pack(side="bottom", fill="x")
        cuerpo = ttk.Frame(ventana, padding=(18, 0, 18, 0))
        cuerpo.pack(fill="both", expand=True)
        cuerpo.columnconfigure(0, weight=1)
        cuerpo.columnconfigure(1, minsize=340)
        cuerpo.rowconfigure(0, weight=1)
        panel = ttk.Frame(cuerpo)
        panel.grid(row=0, column=0, sticky="nsew", padx=(0, 18))
        self.resumen = ttk.Label(panel)
        self.resumen.pack(anchor="w", pady=(0, 10))
        self.canvas = tk.Canvas(panel, background="white", highlightthickness=1,
                                highlightbackground="#cccccc", width=550, height=370)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Configure>", lambda event: self.dibujar())
        ttk.Label(panel, text="Círculo = municipio · Línea = conexión · Número = minutos",
                  font=("Segoe UI", 10)).pack(anchor="w", pady=(10, 3))
        ttk.Label(panel, text="Nivel: verde bajo · amarillo medio · rojo alto · gris sin datos",
                  font=("Segoe UI", 10)).pack(anchor="w")
        acciones = ttk.Frame(panel)
        acciones.pack(fill="x", pady=(12, 0))
        self.herramientas = ttk.Notebook(cuerpo, width=340)
        self.herramientas.grid(row=0, column=1, sticky="nsew")
        for nombre, construir in [("Municipios", self.panel_red), ("Caminos", self.panel_caminos),
                                   ("Recorridos", self.panel_recorridos)]:
            tab = ttk.Frame(self.herramientas, padding=12)
            self.herramientas.add(tab, text=nombre)
            construir(tab)
        self.herramientas.bind("<<NotebookTabChanged>>", lambda event: self.pausar())

        # Las tablas y formularios se muestran solo cuando se necesitan.
        self.ventana_tablas = self.crear_ventana("Matriz y datos", "850x450")
        self.tablas = ttk.Notebook(self.ventana_tablas)
        self.tablas.pack(fill="both", expand=True, padx=12, pady=12)
        matriz, datos = ttk.Frame(self.tablas), ttk.Frame(self.tablas)
        self.tablas.add(matriz, text="Matriz de adyacencia")
        self.tablas.add(datos, text="Casos y grados")
        self.matriz_vista = self.tabla(matriz)
        self.municipios_vista = self.tabla(datos)

        self.ventana_fallas = self.crear_ventana("Probar fallas", "420x410")
        fallas = ttk.Frame(self.ventana_fallas, padding=18)
        fallas.pack(fill="both", expand=True)
        self.texto(fallas, "Cada prueba empieza con la red original.")
        self.boton(fallas, "1. Quitar G (Copacabana)", lambda: self.simular("nodo"))
        self.boton(fallas, "2. Quitar la conexión G–H", lambda: self.simular("arista"))
        self.detalle_red = self.texto(fallas, "")
        self.boton(fallas, "Restaurar la red", self.restaurar)

        self.ventana_editar = self.crear_ventana("Editar la red", "440x500")
        self.panel_editar(self.ventana_editar)
        for nombre, dialogo in [("Ver matriz", self.ventana_tablas),
                                ("Probar fallas", self.ventana_fallas),
                                ("Editar red", self.ventana_editar)]:
            ttk.Button(acciones, text=nombre, command=lambda d=dialogo: self.abrir(d)).pack(
                side="left", padx=(0, 8))
        self.actualizar()

    def crear_ventana(self, titulo, tamaño):
        dialogo = tk.Toplevel(self.ventana)
        dialogo.withdraw()
        dialogo.title(titulo)
        dialogo.geometry(tamaño)
        dialogo.transient(self.ventana)
        dialogo.protocol("WM_DELETE_WINDOW", dialogo.withdraw)
        return dialogo

    def abrir(self, dialogo):
        self.pausar()
        dialogo.deiconify()
        dialogo.lift()

    def tabla(self, padre):
        padre.rowconfigure(0, weight=1)
        padre.columnconfigure(0, weight=1)
        vista = ttk.Treeview(padre, show="headings", height=6)
        vista.grid(row=0, column=0, sticky="nsew")
        vertical = ttk.Scrollbar(padre, orient="vertical", command=vista.yview)
        horizontal = ttk.Scrollbar(padre, orient="horizontal", command=vista.xview)
        vertical.grid(row=0, column=1, sticky="ns")
        horizontal.grid(row=1, column=0, sticky="ew")
        vista.configure(yscrollcommand=vertical.set, xscrollcommand=horizontal.set)
        return vista

    def llenar_tabla(self, vista, columnas, filas, anchos):
        vista.delete(*vista.get_children())
        vista.configure(columns=list(range(len(columnas))))
        for i, (nombre, ancho) in enumerate(zip(columnas, anchos)):
            vista.heading(i, text=nombre)
            vista.column(i, width=ancho, minwidth=ancho, stretch=True, anchor="center")
        for fila in filas:
            vista.insert("", "end", values=fila)

    def titulo(self, padre, texto):
        ttk.Label(padre, text=texto, font=("Segoe UI", 11, "bold")).pack(
            anchor="w", pady=(8, 5))

    def texto(self, padre, texto):
        etiqueta = ttk.Label(padre, text=texto, wraplength=310, justify="left")
        etiqueta.pack(anchor="w", fill="x", pady=5)
        return etiqueta

    def entrada(self, padre, etiqueta, valor="", combo=False):
        ttk.Label(padre, text=etiqueta).pack(anchor="w", pady=(7, 3))
        variable = tk.StringVar(value=valor)
        if combo:
            widget = ttk.Combobox(padre, textvariable=variable, state="readonly")
            self.combos.append((widget, variable))
        else:
            widget = ttk.Entry(padre, textvariable=variable)
        widget.pack(fill="x")
        return variable

    def boton(self, padre, texto, funcion):
        ttk.Button(padre, text=texto, command=lambda: self.ejecutar(funcion)).pack(
            fill="x", pady=(7, 0))

    def ejecutar(self, funcion):
        try:
            funcion()
        except ValueError as error:
            messagebox.showerror("Revisa los datos", str(error), parent=self.ventana)

    def panel_red(self, tab):
        self.titulo(tab, "1. Elige un municipio")
        self.texto(tab, "Haz clic en un círculo del grafo.")
        self.consulta_id = tk.StringVar(value="A")
        self.detalle_municipio = self.texto(tab, "")
        self.boton(tab, "Cambiar cifras", self.editar_reporte)
        self.texto(tab, "Activos = confirmados − recuperados − fallecidos.")
        self.texto(tab, "Datos ficticios del taller. Los colores son una regla de práctica.")

    def panel_caminos(self, tab):
        self.titulo(tab, "2. Muestra un camino")
        self.texto(tab, "Elige un ejemplo o escribe los IDs separados por espacios.")
        self.ruta = tk.StringVar(value="A C F")
        ttk.Combobox(tab, textvariable=self.ruta,
                     values=CAMINOS + ["A B C A", "C D E F C"]).pack(fill="x", pady=5)
        self.boton(tab, "Mostrar camino", self.evaluar_camino)
        self.boton(tab, "Buscar el camino más corto…", lambda: self.abrir(self.ventana_ruta))
        self.detalle_camino = self.texto(tab, "Pulsa Mostrar camino para verlo en naranja.")
        self.boton(tab, "Ver casos de esta ruta", self.ver_casos_ruta)

        self.ventana_ruta = self.crear_ventana("Buscar camino", "400x350")
        marco = ttk.Frame(self.ventana_ruta, padding=18)
        marco.pack(fill="both", expand=True)
        self.origen = self.entrada(marco, "Desde", "A", combo=True)
        self.destino = self.entrada(marco, "Hasta", "F", combo=True)
        self.solo_bajo_medio = tk.BooleanVar(value=False)
        ttk.Checkbutton(marco, text="Solo niveles bajo y medio (opcional)",
                        variable=self.solo_bajo_medio).pack(anchor="w", pady=(14, 5))
        self.texto(marco, "El filtro excluye niveles altos y sin datos. No indica que una ruta sea segura.")
        self.boton(marco, "Buscar y mostrar", self.buscar_y_mostrar)

    def buscar_y_mostrar(self):
        self.camino_minimo()
        self.ventana_ruta.withdraw()
        self.herramientas.select(1)

    def ver_casos_ruta(self):
        if not self.nodos_marcados or self.traza:
            raise ValueError("Primero muestra o busca un camino.")
        messagebox.showinfo("Municipios de la ruta", "\n\n".join(
            self.texto_epidemiologico(id) for id in self.nodos_marcados), parent=self.ventana)

    def panel_recorridos(self, tab):
        self.titulo(tab, "3. Recorre paso a paso")
        self.inicio = self.entrada(tab, "Empezar en", "A", combo=True)
        self.texto(tab, "BFS: por niveles. DFS: por ramas.\nAzul: actual · Borde verde: visitado.")
        fila = ttk.Frame(tab)
        fila.pack(fill="x", pady=5)
        for modo in ("BFS", "DFS"):
            ttk.Button(fila, text="Iniciar " + modo, command=lambda m=modo: self.ejecutar(
                lambda: self.preparar_recorrido(m))).pack(side="left", expand=True, fill="x")
        self.siguiente_boton = ttk.Button(tab, text="Siguiente paso", command=self.siguiente)
        self.siguiente_boton.pack(fill="x", pady=10)
        self.detalle_recorrido = self.texto(tab, "Elige BFS o DFS para empezar.")
        self.boton(tab, "Ver tabla de pasos", lambda: self.abrir(self.ventana_traza))

        self.ventana_traza = self.crear_ventana("Pasos de BFS / DFS", "650x440")
        marco = ttk.Frame(self.ventana_traza, padding=12)
        marco.pack(fill="both", expand=True)
        self.traza_vista = self.tabla(marco)
        self.traza_vista.tag_configure("actual", background="#cde8fa")
        self.llenar_tabla(self.traza_vista, ["Paso", "Nodo", "Cola / rama"], [], [55, 55, 430])

    def panel_editar(self, ventana):
        pestañas = ttk.Notebook(ventana)
        pestañas.pack(fill="both", expand=True, padx=12, pady=12)
        municipios, conexiones = ttk.Frame(pestañas, padding=12), ttk.Frame(pestañas, padding=12)
        pestañas.add(municipios, text="Municipios")
        pestañas.add(conexiones, text="Conexiones")
        self.nuevo_id = self.entrada(municipios, "ID nuevo", "K")
        self.nuevo_nombre = self.entrada(municipios, "Nombre")
        self.nuevo_departamento = tk.StringVar(value="Antioquia")
        self.nuevos_casos = tk.StringVar(value="")
        self.boton(municipios, "Agregar municipio", self.agregar_municipio)
        self.borrar_id = self.entrada(municipios, "Municipio que quieres quitar", "G", combo=True)
        self.boton(municipios, "Quitar municipio", self.borrar_municipio)
        self.texto(municipios, "Al quitar un municipio también se quitan sus conexiones.")
        self.enlace_a = self.entrada(conexiones, "Primer municipio", "A", combo=True)
        self.enlace_b = self.entrada(conexiones, "Segundo municipio", "C", combo=True)
        self.minutos = self.entrada(conexiones, "Minutos", "15")
        self.boton(conexiones, "Guardar conexión", self.unir)
        self.boton(conexiones, "Quitar conexión", self.borrar_arco)
        self.boton(conexiones, "¿Tienen conexión directa?", self.adyacentes)

    def limpiar_recorrido(self):
        self.pausar()
        self.traza = []
        self.paso = 0
        self.nodos_marcados = []
        self.aristas_marcadas = set()
        self.actual = None
        self.traza_vista.delete(*self.traza_vista.get_children())
        self.detalle_recorrido.configure(text="Selecciona BFS o DFS para comenzar.")
        self.siguiente_boton.configure(state="disabled")

    def actualizar(self):
        self.limpiar_recorrido()
        self.detalle_camino.configure(text="Consulta una ruta para ver sus minutos y la situación de cada municipio.")
        for combo, variable in self.combos:
            combo.configure(values=self.grafo.ids)
            if variable.get() not in self.grafo.ids:
                variable.set(self.grafo.ids[0] if self.grafo.ids else "")
        componentes = self.grafo.Componentes()
        aislados = [id for id in self.grafo.ids if self.grafo.CalcularGrado(id) == 0]
        etiqueta = "componente" if len(componentes) == 1 else "componentes"
        self.resumen.configure(text=f"{len(self.grafo.ids)} municipios  ·  "
                               f"{len(self.grafo.Aristas())} conexiones  ·  "
                               f"{len(componentes)} {etiqueta}")
        tipo = "Red vacía" if not componentes else "Conexa" if len(componentes) == 1 else "No conexa"
        grupos = "\n".join("{" + ", ".join(grupo) + "}" for grupo in componentes) or "Ninguno"
        mayor, menor = self.grafo.ObtenerGradosExtremos()
        extremos = ""
        if mayor:
            extremos = (f"\nGrado máx.: {mayor} = {self.grafo.CalcularGrado(mayor)} · "
                        f"mín.: {menor} = {self.grafo.CalcularGrado(menor)}")
        self.detalle_red.configure(text=f"{tipo} · {len(componentes)} {etiqueta}\n{grupos}\n"
                                  f"Aislados: {', '.join(aislados) or 'ninguno'}{extremos}")
        self.llenar_tabla(self.matriz_vista, ["ID"] + self.grafo.ids,
                         [[id] + [f"{n:g}" for n in fila]
                          for id, fila in zip(self.grafo.ids, self.grafo.matriz)],
                         [46] * (len(self.grafo.ids) + 1))
        self.llenar_tabla(self.municipios_vista,
                         ["ID", "Municipio", "Confirm.", "Recuperados", "Fallecidos", "Activos", "Nivel", "Grado"],
                         [[v.id, v.nombre, self.numero(v.casos), self.numero(v.recuperados),
                           self.numero(v.fallecidos), self.numero(v.activos), v.nivel_riesgo,
                           self.grafo.CalcularGrado(v.id)] for v in self.grafo.vertices],
                         [35, 110, 70, 85, 75, 65, 80, 50])
        self.actualizar_ficha()
        self.dibujar()

    def dibujar(self):
        self.canvas.delete("all")
        ancho, alto = self.canvas.winfo_width(), self.canvas.winfo_height()
        posiciones = POSICIONES.copy()
        if any(id not in POSICIONES for id in self.grafo.ids):
            # Para municipios nuevos se usa un círculo sencillo, sin instalar librerías.
            posiciones = {id: (.5 + .40 * math.cos(2 * math.pi * i / len(self.grafo.ids)),
                               .46 + .36 * math.sin(2 * math.pi * i / len(self.grafo.ids)))
                          for i, id in enumerate(self.grafo.ids)}
        puntos = {id: (45 + x * max(ancho - 100, 1), 30 + y * max(alto - 85, 1))
                  for id, (x, y) in posiciones.items() if id in self.grafo.ids}
        for a, b, peso in self.grafo.Aristas():
            x1, y1 = puntos[a]
            x2, y2 = puntos[b]
            marcada = frozenset((a, b)) in self.aristas_marcadas
            color = ("#288269" if self.traza else "#d1770d") if marcada else "#aabcc2"
            self.canvas.create_line(x1, y1, x2, y2, fill=color, width=4 if marcada else 2)
            x, y = (x1 + x2) / 2, (y1 + y2) / 2
            if a == "A" and b == "D":
                x += 42
            elif a == "B" and b == "C":
                x -= 25
            elif a == "H" and b == "I":
                x += 32
            elif (a, b) in (("D", "E"), ("G", "J")):
                x -= 24
                y -= 8
            self.canvas.create_rectangle(x - 17, y - 10, x + 17, y + 10, fill="white", outline="")
            self.canvas.create_text(x, y, text=f"{peso:g}", fill="#334d56", font=("Segoe UI", 10))
        colores = {"Bajo": "#ccebd7", "Medio": "#fff0b3", "Alto": "#f5c7c7", "Sin datos": "#e5e7eb"}
        for v in self.grafo.vertices:
            x, y = puntos[v.id]
            color = colores[v.nivel_riesgo]
            borde, grosor = "#40656d", 2
            if v.id in self.nodos_marcados:
                borde, grosor = ("#288269" if self.traza else "#d1770d"), 4
            if v.id == self.actual:
                borde, grosor = "#2372b3", 5
            etiqueta = "municipio_" + v.id
            self.canvas.create_oval(x - 19, y - 19, x + 19, y + 19, fill=color,
                                    outline=borde, width=grosor, tags=(etiqueta,))
            self.canvas.create_text(x, y, text=v.id, font=("Segoe UI", 11, "bold"),
                                    fill="#163b40", tags=(etiqueta,))
            # En una ventana baja los nombres siguen disponibles en la tabla.
            if alto >= 240:
                desplazamiento = -22 if v.id == "A" else 0
                self.canvas.create_text(x + desplazamiento, y + 32, text=v.nombre, width=115,
                                        font=("Segoe UI", 9), fill="#203c45", tags=(etiqueta,))
            self.canvas.tag_bind(etiqueta, "<Button-1>", lambda event, id=v.id: self.seleccionar_municipio(id))
        if not self.grafo.ids:
            self.canvas.create_text(ancho / 2, alto / 2, text="Red vacía. Agrega un municipio o restaura el ejemplo.",
                                    fill="#526970", font=("Segoe UI", 12))

    def restaurar(self):
        self.grafo = crear_red()
        self.solo_bajo_medio.set(False)
        self.actualizar()
        self.estado.set("Ejemplo restaurado: 10 municipios, sus reportes ficticios y 13 conexiones.")

    def simular(self, tipo):
        self.grafo = crear_red()
        if tipo == "nodo":
            self.grafo.BorrarVertice("G")
            mensaje = "Sin G: quedan 3 componentes; J está aislado."
        else:
            self.grafo.BorrarArco("G", "H")
            mensaje = "Sin G–H: quedan 2 componentes; H e I se separan del resto. No hay aislados."
        self.actualizar()
        self.estado.set(mensaje)

    def consultar(self):
        id = self.consulta_id.get()
        vecinos = self.grafo.Vecinos(id)
        self.actualizar_ficha()
        self.estado.set(f"{id}: grado {len(vecinos)}. Vecinos: {', '.join(vecinos) or 'ninguno'}.")

    @staticmethod
    def numero(valor):
        return "Sin datos" if valor is None else str(valor)

    def actualizar_ficha(self):
        if not self.grafo.ids:
            self.detalle_municipio.configure(text="No hay municipios registrados.")
            return
        if self.consulta_id.get() not in self.grafo.ids:
            self.consulta_id.set(self.grafo.ids[0])
        v = self.grafo.ConsultarMunicipio(self.consulta_id.get())
        self.detalle_municipio.configure(text=(
            f"{v.id} · {v.nombre}\n\n"
            f"Confirmados: {self.numero(v.casos)}\nRecuperados: {self.numero(v.recuperados)}\n"
            f"Fallecidos: {self.numero(v.fallecidos)}\nActivos: {self.numero(v.activos)}\n"
            f"Nivel del ejemplo: {v.nivel_riesgo}\n\n"
            f"Conexiones (grado): {self.grafo.CalcularGrado(v.id)}\n"
            f"Vecinos: {', '.join(self.grafo.Vecinos(v.id)) or 'ninguno'}"))

    def seleccionar_municipio(self, id):
        self.consulta_id.set(id)
        self.herramientas.select(0)
        self.consultar()

    def editar_reporte(self):
        v = self.grafo.ConsultarMunicipio(self.consulta_id.get())
        dialogo = tk.Toplevel(self.ventana)
        dialogo.title(f"Reporte de {v.nombre}")
        dialogo.transient(self.ventana)
        dialogo.grab_set()
        marco = ttk.Frame(dialogo, padding=18)
        marco.pack(fill="both", expand=True)
        self.texto(marco, f"{v.enfermedad} · {v.corte}\nDeja en blanco las cifras desconocidas.")
        variables = [self.entrada(marco, nombre, "" if valor is None else str(valor))
                     for nombre, valor in [("Confirmados", v.casos), ("Recuperados", v.recuperados),
                                           ("Fallecidos", v.fallecidos)]]

        def guardar():
            try:
                cifras = [int(x.get()) if x.get().strip() else None for x in variables]
            except ValueError:
                raise ValueError("Escribe números enteros o deja el campo en blanco.") from None
            self.grafo.ActualizarReporte(v.id, *cifras)
            dialogo.destroy()
            self.actualizar()
            self.estado.set(f"Reporte de {v.nombre} actualizado. Los activos y el nivel se recalcularon.")

        self.boton(marco, "Guardar cifras", guardar)

    def texto_epidemiologico(self, id):
        v = self.grafo.ConsultarMunicipio(id)
        return (f"{v.id} {v.nombre}: activos {self.numero(v.activos)}, "
                f"recuperados {self.numero(v.recuperados)}, nivel {v.nivel_riesgo}")

    def mostrar_camino(self, secuencia, costo):
        self.limpiar_recorrido()
        self.nodos_marcados = secuencia
        self.aristas_marcadas = {frozenset((a, b)) for a, b in zip(secuencia, secuencia[1:])}
        texto = (f"{' → '.join(secuencia)}\nLongitud: {len(secuencia) - 1} conexiones"
                 f"\nCosto total: {costo:g} minutos\n"
                 f"Ciclo simple: {'sí' if self.grafo.EsCiclo(secuencia) else 'no'}")
        self.detalle_camino.configure(text=texto)
        self.estado.set(f"{' → '.join(secuencia)} · {len(secuencia) - 1} conexiones · {costo:g} minutos.")
        self.dibujar()

    def evaluar_camino(self):
        secuencia = self.ruta.get().upper().replace("->", " ").replace("→", " ").replace(",", " ").split()
        # Quitar un resultado anterior antes de validar una nueva solicitud.
        self.limpiar_recorrido()
        self.dibujar()
        self.detalle_camino.configure(text="Camino no válido. Revisa los IDs y las conexiones.")
        self.estado.set("Camino no válido. Revisa los IDs y las conexiones.")
        _, costo = self.grafo.CalcularCostoCamino(secuencia)
        self.mostrar_camino(secuencia, costo)

    def camino_minimo(self):
        self.limpiar_recorrido()
        self.dibujar()
        self.detalle_camino.configure(text="Selecciona un origen y un destino válidos.")
        camino, costo = self.grafo.CaminoMinimo(self.origen.get(), self.destino.get(),
                                               self.solo_bajo_medio.get())
        if camino:
            self.mostrar_camino(camino, costo)
        else:
            mensaje = ("No hay ruta que cumpla el filtro. Revisa también el nivel del origen y destino."
                       if self.solo_bajo_medio.get() else "No hay un camino entre esos municipios en la red actual.")
            self.detalle_camino.configure(text=mensaje)
            self.estado.set(mensaje)

    def preparar_recorrido(self, modo):
        self.limpiar_recorrido()
        self.modo = modo
        inicio = self.inicio.get()
        self.traza = (self.grafo.TrazaAnchura(inicio) if modo == "BFS"
                      else self.grafo.TrazaProfundidad(inicio))
        for i, paso in enumerate(self.traza, 1):
            estado = (", ".join(paso["cola"]) or "Vacía") if modo == "BFS" else " → ".join(paso["rama"])
            self.traza_vista.insert("", "end", values=(i, paso["nodo"], estado))
        self.siguiente_boton.configure(state="normal")
        self.detalle_recorrido.configure(text=f"{modo} desde {inicio}. Pulsa Siguiente paso.")
        self.estado.set(f"{modo} listo. Se visitan únicamente los nodos alcanzables desde {inicio}.")
        self.dibujar()

    def siguiente(self):
        if self.paso >= len(self.traza):
            return
        paso = self.traza[self.paso]
        self.actual = paso["nodo"]
        self.nodos_marcados.append(self.actual)
        if paso["padre"] is not None:
            self.aristas_marcadas.add(frozenset((paso["padre"], self.actual)))
        self.paso += 1
        for i, item in enumerate(self.traza_vista.get_children()):
            self.traza_vista.item(item, tags=("actual",) if i == self.paso - 1 else ())
            if i == self.paso - 1:
                self.traza_vista.see(item)
        detalle = (f"Nivel: {paso['nivel']}. Cola: {', '.join(paso['cola']) or 'vacía'}"
                   if self.modo == "BFS" else f"Rama activa: {' → '.join(paso['rama'])}")
        self.detalle_recorrido.configure(text=f"Paso {self.paso}/{len(self.traza)} · Nodo {self.actual}\n{detalle}\n"
                                         + self.texto_epidemiologico(self.actual))
        self.estado.set(f"{self.modo}: {' → '.join(self.nodos_marcados)}")
        if self.paso == len(self.traza):
            self.pausar()
            self.siguiente_boton.configure(state="disabled")
            self.estado.set(self.estado.get() + "  ·  Recorrido terminado.")
        self.dibujar()

    def reproducir(self):
        self.pausar()
        self.avanzar_automatico()

    def avanzar_automatico(self):
        self.temporizador = None
        self.siguiente()
        if self.paso < len(self.traza):
            self.temporizador = self.ventana.after(700, self.avanzar_automatico)

    def pausar(self):
        if self.temporizador is not None:
            self.ventana.after_cancel(self.temporizador)
            self.temporizador = None

    def agregar_municipio(self):
        try:
            casos = int(self.nuevos_casos.get()) if self.nuevos_casos.get().strip() else None
        except ValueError:
            raise ValueError("Los casos deben ser un número entero, o dejarse en blanco.") from None
        self.grafo.AñadirVertice(Vertice(self.nuevo_id.get(), self.nuevo_nombre.get(),
                                        self.nuevo_departamento.get().strip(), casos))
        self.actualizar()
        self.estado.set("Municipio agregado. Abre Conexiones para unirlo a la red.")

    def borrar_municipio(self):
        id = self.borrar_id.get()
        self.grafo.BorrarVertice(id)
        self.actualizar()
        self.estado.set(f"Municipio {id} y sus conexiones eliminados.")

    def unir(self):
        self.grafo.Union(self.enlace_a.get(), self.enlace_b.get(), self.minutos.get())
        self.actualizar()
        self.estado.set("Conexión guardada en ambos sentidos.")

    def borrar_arco(self):
        self.grafo.BorrarArco(self.enlace_a.get(), self.enlace_b.get())
        self.actualizar()
        self.estado.set("Conexión eliminada. Los municipios se conservan.")

    def adyacentes(self):
        a, b = self.enlace_a.get(), self.enlace_b.get()
        existe = self.grafo.EsAdyacente(a, b)
        self.estado.set(f"{a} y {b}: {'sí tienen' if existe else 'no tienen'} conexión directa.")

    def cerrar(self):
        self.pausar()
        self.ventana.destroy()
