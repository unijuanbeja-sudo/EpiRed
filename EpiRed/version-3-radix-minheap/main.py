from estructuras.radix_tree import RadixTree
from estructuras.min_heap import MinHeap, AlertaEpidemiologica


print("==============================================")
print("            EPIRED - VERSION 3")
print("==============================================")
print("Versiones anteriores:")
print("- Arbol n-ario para estructura territorial.")
print("- Arbol B+ para indexacion de casos.")
print()
print("Nueva version:")
print("- Radix Tree para autocompletado.")
print("- Min-Heap para alertas epidemiologicas.")
print("==============================================")


# -------------------------------------------------
# RADIX TREE
# -------------------------------------------------

radix = RadixTree()

datos_radix = [
    # Municipios
    "Medellin",
    "Bogota",
    "Bello",
    "Cali",

    # Centros de salud
    "Hospital Central",
    "Clinica Norte",
    "Hospital San Jose",
    "Hospital Universitario",
    "Hospital Marco Fidel Suarez",

    # Enfermedades
    "Dengue",
    "Tuberculosis",
    "Malaria",
    "Sarampion",
    "COVID-19"
]

for dato in datos_radix:
    radix.insertar(dato)


# -------------------------------------------------
# MIN-HEAP
# -------------------------------------------------

min_heap = MinHeap()

alertas_iniciales = [
    AlertaEpidemiologica(
        2,
        "Aumento de casos de tuberculosis",
        "Bogota",
        "Tuberculosis"
    ),

    AlertaEpidemiologica(
        1,
        "Brote critico de dengue",
        "Medellin",
        "Dengue"
    ),

    AlertaEpidemiologica(
        3,
        "Seguimiento de casos de malaria",
        "Cali",
        "Malaria"
    )
]

for alerta in alertas_iniciales:
    min_heap.insertar(alerta)


# -------------------------------------------------
# FUNCIONES DEL MENU
# -------------------------------------------------

def mostrar_resultados(resultados):
    if resultados:
        print("\nCoincidencias encontradas:")

        for resultado in resultados:
            print("-", resultado.title())

    else:
        print("\nNo se encontraron coincidencias.")


def explicar_prioridad():
    print("\nNiveles de prioridad:")
    print("1 = Critica")
    print("2 = Alta")
    print("3 = Media")
    print("4 = Baja")


# -------------------------------------------------
# MENU
# -------------------------------------------------

while True:
    print("\n==============================================")
    print("              MENU EPIRED")
    print("==============================================")
    print("1. Autocompletar municipio")
    print("2. Autocompletar centro de salud")
    print("3. Autocompletar enfermedad")
    print("4. Mostrar Radix Tree")
    print("5. Registrar alerta epidemiologica")
    print("6. Procesar alerta mas prioritaria")
    print("7. Mostrar Min-Heap")
    print("8. Ver siguiente alerta")
    print("9. Salir")

    opcion = input("\nSeleccione una opcion: ")

    if opcion == "1":
        prefijo = input(
            "Ingrese el inicio del municipio: "
        )

        resultados = radix.autocompletar(prefijo)

        mostrar_resultados(resultados)

    elif opcion == "2":
        prefijo = input(
            "Ingrese el inicio del centro de salud: "
        )

        resultados = radix.autocompletar(prefijo)

        mostrar_resultados(resultados)

    elif opcion == "3":
        prefijo = input(
            "Ingrese el inicio de la enfermedad: "
        )

        resultados = radix.autocompletar(prefijo)

        mostrar_resultados(resultados)

    elif opcion == "4":
        radix.mostrar()

    elif opcion == "5":
        explicar_prioridad()

        try:
            prioridad = int(
                input("Ingrese la prioridad: ")
            )

            if prioridad < 1 or prioridad > 4:
                print(
                    "\nLa prioridad debe estar entre 1 y 4."
                )
                continue

        except ValueError:
            print(
                "\nLa prioridad debe ser un numero."
            )
            continue

        mensaje = input(
            "Descripcion de la alerta: "
        )

        municipio = input(
            "Municipio: "
        )

        enfermedad = input(
            "Enfermedad: "
        )

        nueva_alerta = AlertaEpidemiologica(
            prioridad,
            mensaje,
            municipio,
            enfermedad
        )

        min_heap.insertar(nueva_alerta)

        print(
            "\nAlerta registrada correctamente."
        )

    elif opcion == "6":
        alerta = min_heap.extraer_minimo()

        if alerta is None:
            print(
                "\nNo hay alertas pendientes."
            )

        else:
            print(
                "\nAlerta procesada:"
            )

            print(alerta)

    elif opcion == "7":
        min_heap.mostrar()

    elif opcion == "8":
        alerta = min_heap.ver_minimo()

        if alerta is None:
            print(
                "\nNo hay alertas pendientes."
            )

        else:
            print(
                "\nSiguiente alerta a procesar:"
            )

            print(alerta)

    elif opcion == "9":
        print(
            "\nSaliendo de EpiRed..."
        )
        break

    else:
        print(
            "\nOpcion no valida."
        )