from estructuras.arbol_nario import ArbolNario


arbol = ArbolNario("EpiRed Colombia")

# Departamentos
arbol.agregar_nodo("EpiRed Colombia", "Antioquia")
arbol.agregar_nodo("EpiRed Colombia", "Cundinamarca")
arbol.agregar_nodo("EpiRed Colombia", "Valle del Cauca")

# Municipios
arbol.agregar_nodo("Antioquia", "Medellín")
arbol.agregar_nodo("Antioquia", "Bello")

arbol.agregar_nodo("Cundinamarca", "Bogotá")

arbol.agregar_nodo("Valle del Cauca", "Cali")

# Centros de salud
arbol.agregar_nodo("Medellín", "Hospital Central")
arbol.agregar_nodo("Medellín", "Clínica Norte")

arbol.agregar_nodo("Bello", "Hospital Marco Fidel Suárez")

arbol.agregar_nodo("Bogotá", "Hospital San José")

arbol.agregar_nodo("Cali", "Hospital Universitario")

# Enfermedades
arbol.agregar_nodo("Hospital Central", "Dengue")
arbol.agregar_nodo("Hospital Central", "Tuberculosis")

arbol.agregar_nodo("Clínica Norte", "Sarampión")

arbol.agregar_nodo("Hospital Marco Fidel Suárez", "Dengue")

arbol.agregar_nodo("Hospital San José", "Tuberculosis")
arbol.agregar_nodo("Hospital San José", "COVID-19")

arbol.agregar_nodo("Hospital Universitario", "Dengue")
arbol.agregar_nodo("Hospital Universitario", "Malaria")


arbol.mostrar_arbol()

while True:
    print("\n==============================")
    print("            EPIRED")
    print("==============================")
    print("1. Mostrar estructura")
    print("2. Buscar enfermedad")
    print("3. Agregar enfermedad")
    print("4. Eliminar enfermedad")
    print("5. Salir")

    opcion = input("\nSeleccione una opción: ")

    if opcion == "1":
        print("\n--- ESTRUCTURA EPIDEMIOLÓGICA ---")
        arbol.mostrar_arbol()

    elif opcion == "2":
        nombre = input("Ingrese el nombre de la enfermedad: ")

        resultado = arbol.buscar_nodo(arbol.raiz, nombre)

        if resultado is not None:
            print("Enfermedad encontrada:", resultado.nombre)
        else:
            print("La enfermedad no fue encontrada.")

    elif opcion == "3":
        centro_salud = input("Ingrese el centro de salud: ")
        enfermedad = input("Ingrese la enfermedad: ")

        agregado = arbol.agregar_nodo(centro_salud, enfermedad)

        if agregado:
            print("Enfermedad agregada correctamente.")
        else:
            print("No se encontró el centro de salud.")

    elif opcion == "4":
        enfermedad = input("Ingrese la enfermedad que desea eliminar: ")

        eliminado = arbol.eliminar_nodo(arbol.raiz, enfermedad)

        if eliminado:
            print("Enfermedad eliminada correctamente.")
        else:
            print("La enfermedad no fue encontrada.")

    elif opcion == "5":
        print("Saliendo de EpiRed...")
        break

    else:
        print("Opción no válida.")