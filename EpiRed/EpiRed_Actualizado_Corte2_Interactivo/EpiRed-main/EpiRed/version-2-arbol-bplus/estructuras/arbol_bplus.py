class NodoBPlus:
    def __init__(self, es_hoja=False):
        self.es_hoja = es_hoja
        self.claves = []
        self.hijos = []
        self.siguiente = None


class ArbolBPlus:
    def __init__(self, orden=4):
        self.orden = orden
        self.raiz = NodoBPlus(es_hoja=True)

    def buscar(self, clave):
        nodo = self.raiz

        while not nodo.es_hoja:
            indice = 0

            while (
                indice < len(nodo.claves)
                and clave >= nodo.claves[indice]
            ):
                indice += 1

            nodo = nodo.hijos[indice]

        for i, clave_actual in enumerate(nodo.claves):
            if clave_actual == clave:
                return nodo.hijos[i]

        return None

    def insertar(self, clave, registro):
        raiz = self.raiz

        if len(raiz.claves) >= self.orden - 1:
            nueva_raiz = NodoBPlus(es_hoja=False)
            nueva_raiz.hijos.append(raiz)

            self._dividir_hijo(nueva_raiz, 0)

            self.raiz = nueva_raiz

            self._insertar_no_lleno(
                nueva_raiz,
                clave,
                registro
            )

        else:
            self._insertar_no_lleno(
                raiz,
                clave,
                registro
            )

    def _insertar_no_lleno(self, nodo, clave, registro):
        if nodo.es_hoja:
            indice = 0

            while (
                indice < len(nodo.claves)
                and nodo.claves[indice] < clave
            ):
                indice += 1

            nodo.claves.insert(indice, clave)
            nodo.hijos.insert(indice, registro)

        else:
            indice = 0

            while (
                indice < len(nodo.claves)
                and clave >= nodo.claves[indice]
            ):
                indice += 1

            hijo = nodo.hijos[indice]

            if len(hijo.claves) >= self.orden - 1:
                self._dividir_hijo(nodo, indice)

                if clave >= nodo.claves[indice]:
                    indice += 1

            self._insertar_no_lleno(
                nodo.hijos[indice],
                clave,
                registro
            )

    def _dividir_hijo(self, padre, indice):
        nodo = padre.hijos[indice]

        nuevo = NodoBPlus(
            es_hoja=nodo.es_hoja
        )

        mitad = len(nodo.claves) // 2

        if nodo.es_hoja:
            nuevo.claves = nodo.claves[mitad:]
            nuevo.hijos = nodo.hijos[mitad:]

            nodo.claves = nodo.claves[:mitad]
            nodo.hijos = nodo.hijos[:mitad]

            nuevo.siguiente = nodo.siguiente
            nodo.siguiente = nuevo

            clave_promovida = nuevo.claves[0]

            padre.claves.insert(
                indice,
                clave_promovida
            )

            padre.hijos.insert(
                indice + 1,
                nuevo
            )

        else:
            clave_promovida = nodo.claves[mitad]

            nuevo.claves = nodo.claves[mitad + 1:]
            nuevo.hijos = nodo.hijos[mitad + 1:]

            nodo.claves = nodo.claves[:mitad]
            nodo.hijos = nodo.hijos[:mitad + 1]

            padre.claves.insert(
                indice,
                clave_promovida
            )

            padre.hijos.insert(
                indice + 1,
                nuevo
            )

    def buscar_rango(self, clave_inicio, clave_fin):
        resultados = []

        nodo = self.raiz

        while not nodo.es_hoja:
            indice = 0

            while (
                indice < len(nodo.claves)
                and clave_inicio >= nodo.claves[indice]
            ):
                indice += 1

            nodo = nodo.hijos[indice]

        while nodo is not None:
            for i, clave in enumerate(nodo.claves):

                if clave_inicio <= clave <= clave_fin:
                    resultados.append(
                        nodo.hijos[i]
                    )

                if clave > clave_fin:
                    return resultados

            nodo = nodo.siguiente

        return resultados

    def mostrar(self, nodo=None, nivel=0):
        if nodo is None:
            nodo = self.raiz

        tipo = (
            "HOJA"
            if nodo.es_hoja
            else "INTERNO"
        )

        print(
            "   " * nivel
            + f"[{tipo}] {nodo.claves}"
        )

        if not nodo.es_hoja:
            for hijo in nodo.hijos:
                self.mostrar(
                    hijo,
                    nivel + 1
                )