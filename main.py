import tkinter as tk
from juego_ahorcado.juego import JuegoAhorcado

if __name__ == "__main__":
    root = tk.Tk()
    juego = JuegoAhorcado(root)
    root.mainloop()
