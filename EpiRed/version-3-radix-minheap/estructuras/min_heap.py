class AlertaEpidemiologica:
    def __init__(
        self,
        prioridad,
        mensaje,
        municipio,
        enfermedad
    ):
        self.prioridad = prioridad
        self.mensaje = mensaje
        self.municipio = municipio
        self.enfermedad = enfermedad

    def __str__(self):
        return (
            f"Prioridad: {self.prioridad} | "
            f"Municipio: {self.municipio} | "
            f"Enfermedad: {self.enfermedad} | "
            f"Alerta: {self.mensaje}"
        )


class MinHeap:
    def __init__(self):
        self.elementos = []

    def _padre(self, indice):
        return (indice - 1) // 2

    def _hijo_izquierdo(self, indice):
        return 2 * indice + 1

    def _hijo_derecho(self, indice):
        return 2 * indice + 2

    def insertar(self, alerta):
        self.elementos.append(alerta)

        indice = len(self.elementos) - 1

        self._subir(indice)

    def _subir(self, indice):
        while indice > 0:
            padre = self._padre(indice)

            if (
                self.elementos[indice].prioridad
                >=
                self.elementos[padre].prioridad
            ):
                break

            self.elementos[indice], self.elementos[padre] = (
                self.elementos[padre],
                self.elementos[indice]
            )

            indice = padre

    def extraer_minimo(self):
        if not self.elementos:
            return None

        if len(self.elementos) == 1:
            return self.elementos.pop()

        minimo = self.elementos[0]

        self.elementos[0] = self.elementos.pop()

        self._bajar(0)

        return minimo

    def _bajar(self, indice):
        tamaño = len(self.elementos)

        while True:
            izquierdo = self._hijo_izquierdo(indice)
            derecho = self._hijo_derecho(indice)

            menor = indice

            if (
                izquierdo < tamaño
                and
                self.elementos[izquierdo].prioridad
                <
                self.elementos[menor].prioridad
            ):
                menor = izquierdo

            if (
                derecho < tamaño
                and
                self.elementos[derecho].prioridad
                <
                self.elementos[menor].prioridad
            ):
                menor = derecho

            if menor == indice:
                break

            self.elementos[indice], self.elementos[menor] = (
                self.elementos[menor],
                self.elementos[indice]
            )

            indice = menor

    def ver_minimo(self):
        if not self.elementos:
            return None

        return self.elementos[0]

    def esta_vacio(self):
        return len(self.elementos) == 0

    def mostrar(self):
        print("\n--- MIN-HEAP DE ALERTAS ---")

        if not self.elementos:
            print("No hay alertas pendientes.")
            return

        for indice, alerta in enumerate(self.elementos):
            print(
                f"[{indice}] {alerta}"
            )