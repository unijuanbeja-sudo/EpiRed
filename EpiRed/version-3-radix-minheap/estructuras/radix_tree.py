class NodoRadix:
    def __init__(self):
        self.hijos = {}
        self.es_fin = False


class RadixTree:
    def __init__(self):
        self.raiz = NodoRadix()

    def _prefijo_comun(self, texto1, texto2):
        longitud = min(len(texto1), len(texto2))
        indice = 0

        while (
            indice < longitud
            and texto1[indice] == texto2[indice]
        ):
            indice += 1

        return texto1[:indice]

    def insertar(self, palabra):
        palabra = palabra.strip()

        if not palabra:
            return

        nodo = self.raiz
        restante = palabra.lower()

        while restante:
            coincidencia_encontrada = False

            for etiqueta in list(nodo.hijos.keys()):
                prefijo = self._prefijo_comun(
                    restante,
                    etiqueta
                )

                if not prefijo:
                    continue

                coincidencia_encontrada = True
                hijo_actual = nodo.hijos[etiqueta]

                # Caso 1:
                # La etiqueta completa coincide.
                if prefijo == etiqueta:
                    nodo = hijo_actual
                    restante = restante[len(prefijo):]
                    break

                # Caso 2:
                # Hay coincidencia parcial.
                nodo_intermedio = NodoRadix()

                resto_etiqueta = etiqueta[len(prefijo):]

                nodo_intermedio.hijos[
                    resto_etiqueta
                ] = hijo_actual

                del nodo.hijos[etiqueta]

                nodo.hijos[prefijo] = nodo_intermedio

                resto_palabra = restante[len(prefijo):]

                if resto_palabra:
                    nuevo_nodo = NodoRadix()
                    nuevo_nodo.es_fin = True

                    nodo_intermedio.hijos[
                        resto_palabra
                    ] = nuevo_nodo
                else:
                    nodo_intermedio.es_fin = True

                return

            if not coincidencia_encontrada:
                nuevo_nodo = NodoRadix()
                nuevo_nodo.es_fin = True

                nodo.hijos[restante] = nuevo_nodo
                return

        nodo.es_fin = True

    def buscar(self, palabra):
        palabra = palabra.strip().lower()

        nodo = self.raiz
        restante = palabra

        while restante:
            encontrado = False

            for etiqueta, hijo in nodo.hijos.items():

                if restante.startswith(etiqueta):
                    restante = restante[len(etiqueta):]
                    nodo = hijo
                    encontrado = True
                    break

                if etiqueta.startswith(restante):
                    return False

            if not encontrado:
                return False

        return nodo.es_fin

    def autocompletar(self, prefijo):
        prefijo = prefijo.strip().lower()

        if not prefijo:
            return []

        nodo = self.raiz
        restante = prefijo
        construido = ""

        while restante:
            encontrado = False

            for etiqueta, hijo in nodo.hijos.items():

                prefijo_comun = self._prefijo_comun(
                    restante,
                    etiqueta
                )

                if not prefijo_comun:
                    continue

                # El prefijo termina dentro de una etiqueta.
                if etiqueta.startswith(restante):
                    construido += etiqueta

                    resultados = []

                    self._recolectar(
                        hijo,
                        construido,
                        resultados
                    )

                    return resultados

                # La etiqueta completa forma parte del prefijo.
                if restante.startswith(etiqueta):
                    construido += etiqueta
                    restante = restante[len(etiqueta):]
                    nodo = hijo
                    encontrado = True
                    break

                return []

            if not encontrado:
                return []

        resultados = []

        self._recolectar(
            nodo,
            construido,
            resultados
        )

        return resultados

    def _recolectar(
        self,
        nodo,
        palabra_actual,
        resultados
    ):
        if nodo.es_fin:
            resultados.append(palabra_actual)

        for etiqueta, hijo in nodo.hijos.items():
            self._recolectar(
                hijo,
                palabra_actual + etiqueta,
                resultados
            )

    def mostrar(self):
        print("\n--- RADIX TREE ---")
        self._mostrar_nodo(
            self.raiz,
            "",
            0
        )

    def _mostrar_nodo(
        self,
        nodo,
        palabra_actual,
        nivel
    ):
        for etiqueta, hijo in nodo.hijos.items():

            palabra = palabra_actual + etiqueta

            marca = " *" if hijo.es_fin else ""

            print(
                "   " * nivel
                + f"└── {etiqueta}{marca}"
            )

            self._mostrar_nodo(
                hijo,
                palabra,
                nivel + 1
            )