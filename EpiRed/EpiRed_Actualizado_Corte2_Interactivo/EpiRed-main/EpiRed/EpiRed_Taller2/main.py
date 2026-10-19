"""Consola de exposición. Uso: python main.py [--demo]."""
import argparse
from math import inf

from epired_taller2 import MUNICIPIOS, REPORTES, crear_red, crear_escenario_costos
from epired_taller2 import RutaMayorCapacidad
from epired_taller2 import DetectarPuntosCriticosDeFalla
from epired_taller2 import GenerarRutaConRespaldo
from epired_taller2 import DetectarAnomaliaDeCicloNegativo


def ficha():
    print("EPIRED | PARCIAL CORTE 2\nFICHA DE DOMINIO")
    print("Vértice: municipio del sistema EpiRed (10 municipios).")
    print("Arista: conexión de traslado bidireccional (13 conexiones).")
    print("Peso principal: tiempo ficticio en minutos, separado de la capacidad.")
    print("Capacidad: unidades de suministros médicos por viaje.")
    print("Reto 4: costos económicos dirigidos en unidades monetarias ficticias (UM).")
    print("Reportes epidemiológicos: datos anteriores, sin ponderar rutas.")
    print("Datos académicos ficticios; no son una red hospitalaria real ni recomendaciones sanitarias.")


def ruta_texto(ruta):
    return " -> ".join(f"{v} ({MUNICIPIOS.get(v, v)})" for v in ruta) or "Sin ruta"


def mostrar_capacidad(red, origen, destino):
    ruta, capacidad = RutaMayorCapacidad(origen, destino, red)
    print("\nRETO 1 | Mayor capacidad")
    print(ruta_texto(ruta))
    if capacidad == inf:
        print("Sin traslado: capacidad sin límite de aristas (convención inf).")
    else:
        print(f"Cuello de botella: {capacidad:g} unidades de suministros por viaje.")
    minimo = red.Dijkstra(origen)
    print("Menor tiempo:", ruta_texto(red.RutaDijkstra(minimo, destino)))
    print(f"Costo mínimo: {minimo['distancias'][destino]:g} minutos.")


def mostrar_criticos(red):
    resultado = DetectarPuntosCriticosDeFalla(red)
    print("\nRETO 2 | Puntos críticos de falla")
    print("Componentes iniciales:", resultado["componentes_iniciales"])
    print("Críticos:", ", ".join(f"{v} ({MUNICIPIOS[v]})" for v in resultado["criticos"]) or "Ninguno")
    for id, ensayo in resultado["ensayos"].items():
        grupos = " | ".join("".join(g) for g in ensayo["componentes"])
        print(f"Sin {id}: {grupos}; crítica: {ensayo['es_critico']}; "
              f"nuevos aislados: {ensayo['nuevos_aislados']}")


def mostrar_respaldo(red, origen, destino):
    r = GenerarRutaConRespaldo(origen, destino, red)
    print("\nRETO 3 | Ruta con respaldo")
    print(f"Primaria: {ruta_texto(r['primaria'])}; {r['costo_primario']:g} minutos")
    if r["alerta"]:
        print(r["alerta"])
        return
    print(f"Respaldo: {ruta_texto(r['respaldo'])}; {r['costo_respaldo']:g} minutos")
    print("Diferencia porcentual: " + (f"{r['porcentaje']:g}%" if r["porcentaje"] is not None
                                      else "no definida: costo primario cero."))
    if origen == destino:
        print("Caso trivial sin traslado: ambas rutas no contienen aristas.")


def mostrar_anomalias(red):
    print("\nRETO 4 | Costos dirigidos y subsidio")
    print("Base: 10 UM por arco. Solo A->B recibe bono; B->A sigue en 10 UM.")
    for con_ciclo in (False, True):
        costos = crear_escenario_costos(red, con_ciclo)
        floyd = costos.FloydWarshall()
        r = DetectarAnomaliaDeCicloNegativo(floyd["distancias"], floyd["ids"])
        print(f"A->B = {-35 if con_ciclo else -5} UM; anomalía: {r['hay_anomalia']}")
        print("Diagonal final:", {v: floyd["distancias"][i][i] for i, v in enumerate(floyd["ids"])})
        if r["hay_anomalia"]:
            print("ALERTA: inconsistencia operativa; posible beneficio infinito al repetir un ciclo.")
            print("IDs diagnósticos:", ", ".join(r["ids_diagnosticos"]))
            print("Son evidencia de recorridos cerrados negativos; no identifican el ciclo simple exacto.")
        else:
            print("Sin ciclo negativo: una arista negativa sola no basta para producirlo.")


def verificar_estado(red, esperado):
    if red.estado() != esperado:
        raise AssertionError("La red original fue modificada.")
    print(f"Estado original intacto: {len(red.ids)} municipios y {len(red.Aristas())} conexiones; "
          "IDs, tiempos y capacidades iguales.")


def demo(red):
    original = red.estado()
    mostrar_capacidad(red, "A", "F")
    mostrar_criticos(red)
    mostrar_respaldo(red, "A", "F")
    mostrar_respaldo(red, "A", "I")
    mostrar_anomalias(red)
    verificar_estado(red, original)


def main():
    parser = argparse.ArgumentParser(description="EpiRed: los cuatro retos del parcial.")
    parser.add_argument("--demo", action="store_true", help="demostración completa sin interacción")
    args = parser.parse_args()
    ficha()
    red = crear_red()
    original = red.estado()
    if args.demo:
        demo(red)
        return
    while True:
        print("\n1. Mayor capacidad\n2. Puntos críticos\n3. Ruta con respaldo\n4. Ciclos negativos"
              "\n5. Demo completa\n6. Municipios y reportes\n7. Comprobar estado original"
              "\n8. Ver grafo interactivo\n0. Salir")
        try:
            opcion = input("Opción: ").strip()
            if opcion == "0":
                print("Fin de la exposición. Gracias.")
                return
            if opcion in ("1", "3"):
                origen = input("ID origen: ").strip().upper()
                destino = input("ID destino: ").strip().upper()
                if opcion == "1":
                    mostrar_capacidad(red, origen, destino)
                else:
                    mostrar_respaldo(red, origen, destino)
            elif opcion == "2":
                mostrar_criticos(red)
            elif opcion == "4":
                mostrar_anomalias(red)
            elif opcion == "5":
                demo(red)
            elif opcion == "6":
                for id, nombre in MUNICIPIOS.items():
                    c, r, f = REPORTES[id]
                    print(f"{id}: {nombre}; confirmados {c}, recuperados {r}, fallecidos {f}, activos {c-r-f}")
                print("Reportes ficticios de COVID-19 del mismo corte simulado del Taller 1.")
            elif opcion == "7":
                verificar_estado(red, original)
            elif opcion == "8":
                # Importación local: la consola funciona incluso sin Tkinter.
                try:
                    from grafo_interactivo import abrir_grafo
                except ImportError:
                    print("La vista necesita Tkinter. En Windows, activa Tcl/Tk al instalar Python.")
                    continue
                print("Cierra la ventana del grafo para regresar al menú.")
                abrir_grafo(red)
            else:
                print("Opción no válida. Elige un número de 0 a 8.")
                continue
            verificar_estado(red, original)
        except ValueError as error:
            print("Entrada no válida:", error)
        except (EOFError, KeyboardInterrupt):
            print("\nSesión finalizada.")
            return


if __name__ == "__main__":
    main()
