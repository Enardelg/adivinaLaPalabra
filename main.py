import tkinter as tk
from juego_ahorcado.seleccion_modo import SeleccionModo

if __name__ == "__main__":
    root = tk.Tk()
    juego = SeleccionModo(root)
    root.mainloop()
