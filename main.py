import tkinter as tk
from juego_ahorcado.interfaz_grafica import InterfazGrafica

if __name__ == "__main__":
    root = tk.Tk()
    juego = InterfazGrafica(root)
    root.mainloop()
