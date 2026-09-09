class CasoEpidemiologico:
    def __init__(
        self,
        id_caso,
        fecha,
        enfermedad,
        municipio,
        centro_salud,
        cantidad,
        nivel_riesgo
    ):
        self.id_caso = id_caso
        self.fecha = fecha
        self.enfermedad = enfermedad
        self.municipio = municipio
        self.centro_salud = centro_salud
        self.cantidad = cantidad
        self.nivel_riesgo = nivel_riesgo

    def __str__(self):
        return (
            f"ID: {self.id_caso} | "
            f"Fecha: {self.fecha} | "
            f"Enfermedad: {self.enfermedad} | "
            f"Municipio: {self.municipio} | "
            f"Centro: {self.centro_salud} | "
            f"Casos: {self.cantidad} | "
            f"Riesgo: {self.nivel_riesgo}"
        )