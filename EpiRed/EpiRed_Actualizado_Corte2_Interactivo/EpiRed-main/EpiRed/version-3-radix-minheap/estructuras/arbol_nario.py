class Nodo:
    def __init__(self, nombre):
        self.nombre = nombre
        self.hijos = []

    def agregar_hijo(self, nodo):
        self.hijos.append(nodo)


class ArbolNario:
    def __init__(self, nombre_raiz):
        self.raiz = Nodo(nombre_raiz)

    def agregar_nodo(self, nombre_padre, nombre_hijo):
        padre = self.buscar_nodo(self.raiz, nombre_padre)

        if padre is not None:
            padre.agregar_hijo(Nodo(nombre_hijo))
            return True

        return False

    def buscar_nodo(self, nodo_actual, nombre):
        if nodo_actual.nombre.lower() == nombre.lower():
            return nodo_actual

        for hijo in nodo_actual.hijos:
            encontrado = self.buscar_nodo(hijo, nombre)

            if encontrado is not None:
                return encontrado

        return None

    def mostrar_arbol(self, nodo=None, nivel=0):
        if nodo is None:
            nodo = self.raiz

        print("   " * nivel + "└── " + nodo.nombre)

        for hijo in nodo.hijos:
            self.mostrar_arbol(hijo, nivel + 1)

    def eliminar_nodo(self, nodo_actual, nombre):
        for hijo in nodo_actual.hijos:
            if hijo.nombre.lower() == nombre.lower():
                nodo_actual.hijos.remove(hijo)
                return True

            eliminado = self.eliminar_nodo(hijo, nombre)

            if eliminado:
                return True

        return False