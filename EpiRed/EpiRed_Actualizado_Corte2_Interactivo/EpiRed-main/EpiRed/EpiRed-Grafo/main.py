"""Punto de entrada: ejecutar con python main.py."""

import tkinter as tk
from interfaz import EpiRed


def main():
    ventana = tk.Tk()
    EpiRed(ventana)
    ventana.mainloop()


if __name__ == "__main__":
    main()
