from estructuras.arbol_bplus import ArbolBPlus
from casos_epidemiologicos import CasoEpidemiologico


print("==============================================")
print("            EPIRED - VERSION 2")
print("==============================================")
print("Version anterior:")
print("- Arbol n-ario para organizar departamentos,")
print("  municipios, centros de salud y enfermedades.")
print()
print("Nueva version:")
print("- Se incorpora un Arbol B+.")
print("- Se indexan casos epidemiologicos.")
print("- Se permiten busquedas exactas y por rango.")
print("==============================================")


# -------------------------------------------------
# CREACION DEL ARBOL B+
# -------------------------------------------------

# Se usa orden 4 para que sea facil ver las divisiones
# durante la demostracion.
arbol_bplus = ArbolBPlus(orden=4)


# -------------------------------------------------
# CREACION DE CASOS EPIDEMIOLOGICOS
# -------------------------------------------------

casos = [
    CasoEpidemiologico(
        "CASO0001",
        "2026-09-01",
        "Dengue",
        "Medellin",
        "Hospital Central",
        18,
        "Alto"
    ),

    CasoEpidemiologico(
        "CASO0002",
        "2026-09-02",
        "Tuberculosis",
        "Bogota",
        "Hospital San Jose",
        6,
        "Medio"
    ),

    CasoEpidemiologico(
        "CASO0003",
        "2026-09-03",
        "Malaria",
        "Cali",
        "Hospital Universitario",
        11,
        "Alto"
    ),

    CasoEpidemiologico(
        "CASO0004",
        "2026-09-04",
        "Sarampion",
        "Medellin",
        "Clinica Norte",
        4,
        "Medio"
    ),

    CasoEpidemiologico(
        "CASO0005",
        "2026-09-05",
        "COVID-19",
        "Bogota",
        "Hospital San Jose",
        22,
        "Alto"
    ),

    CasoEpidemiologico(
        "CASO0006",
        "2026-09-06",
        "Dengue",
        "Bello",
        "Hospital Marco Fidel Suarez",
        9,
        "Medio"
    ),

    CasoEpidemiologico(
        "CASO0007",
        "2026-09-07",
        "Tuberculosis",
        "Medellin",
        "Hospital Central",
        5,
        "Medio"
    ),

    CasoEpidemiologico(
        "CASO0008",
        "2026-09-08",
        "Malaria",
        "Cali",
        "Hospital Universitario",
        14,
        "Alto"
    )
]


# -------------------------------------------------
# INSERCION DE LOS CASOS EN EL ARBOL B+
# -------------------------------------------------

for caso in casos:
    arbol_bplus.insertar(
        caso.id_caso,
        caso
    )


# -------------------------------------------------
# MENU PRINCIPAL
# -------------------------------------------------

while True:
    print("\n==============================================")
    print("              MENU EPIRED")
    print("==============================================")
    print("1. Mostrar Arbol B+")
    print("2. Buscar caso por ID")
    print("3. Buscar casos por rango de ID")
    print("4. Mostrar todos los casos")
    print("5. Salir")

    opcion = input("\nSeleccione una opcion: ")

    if opcion == "1":

        print("\n--- ESTRUCTURA DEL ARBOL B+ ---")
        arbol_bplus.mostrar()

    elif opcion == "2":

        id_buscar = input(
            "Ingrese el ID del caso: "
        ).upper()

        resultado = arbol_bplus.buscar(
            id_buscar
        )

        if resultado is not None:
            print("\nCaso encontrado:")
            print(resultado)
        else:
            print(
                "\nNo se encontro un caso con ese ID."
            )

    elif opcion == "3":

        inicio = input(
            "Ingrese el ID inicial: "
        ).upper()

        fin = input(
            "Ingrese el ID final: "
        ).upper()

        resultados = arbol_bplus.buscar_rango(
            inicio,
            fin
        )

        if len(resultados) > 0:
            print("\nCasos encontrados:")

            for caso in resultados:
                print(caso)

        else:
            print(
                "\nNo se encontraron casos "
                "en ese rango."
            )

    elif opcion == "4":

        print("\n--- CASOS EPIDEMIOLOGICOS ---")

        for caso in casos:
            print(caso)

    elif opcion == "5":

        print("\nSaliendo de EpiRed...")
        break

    else:

        print("\nOpcion no valida.")