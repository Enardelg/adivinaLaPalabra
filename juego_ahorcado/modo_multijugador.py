import tkinter as tk
from tkinter import messagebox

from juego_ahorcado.juego_multijugador import JuegoMultijugador


class ModoMultijugador:
    def __init__(self, master):
        self.master = master
        self.master.title("Modo Multijugador")
        self.master.resizable(False, False)
        self.master.geometry("300x150")
        self.centra_ventana()

        self.crear_widgets()

        # Manejar eventos de teclado
        self.master.bind("<Return>", self.manejar_tecla_enter)

    def centra_ventana(self):
        self.master.update_idletasks()
        width = self.master.winfo_width()
        height = self.master.winfo_height()
        x = (self.master.winfo_screenwidth() // 2) - (width // 2)
        y = (self.master.winfo_screenheight() // 2) - (height // 2)
        self.master.geometry(f"{width}x{height}+{x}+{y}")

    def crear_widgets(self):
        lbl_instruccion = tk.Label(self.master, text="Ingresa la palabra para que otro jugador la adivine")
        lbl_instruccion.pack(pady=5)

        self.entry_palabra = tk.Entry(self.master)
        self.entry_palabra.pack(pady=5)

        btn_empezar = tk.Button(self.master, text="Empezar", command=self.iniciar_juego)
        btn_empezar.pack(pady=5)

    def iniciar_juego(self):
        palabra = self.entry_palabra.get()
        if palabra:
            self.master.destroy()  # Cierra la ventana de modo multijugador
            root = tk.Tk()
            JuegoMultijugador(root, palabra=palabra)  # Inicia el juego con la palabra ingresada
            root.mainloop()
        else:
            messagebox.showwarning("Error", "Por favor, ingresa una palabra antes de empezar.")

    def manejar_tecla_enter(self):
        """Maneja el evento de tecla Enter."""
        self.iniciar_juego()
