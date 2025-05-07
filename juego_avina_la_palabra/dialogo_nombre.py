import tkinter as tk
from tkinter import simpledialog


class NombreDialog(tk.simpledialog.Dialog):
    def body(self, master):
        """
        Crea el cuerpo del diálogo que solicita al usuario su nombre.

        Args:
            master (tk.Tk): La ventana principal donde se mostrará el diálogo.

        Returns:
            tk.Entry: El widget de entrada donde el usuario ingresará su nombre.
        """
        tk.Label(master, text="Introduce tu nombre:").grid(row=0)
        self.entry = tk.Entry(master)
        self.entry.grid(row=0, column=1)
        return self.entry

    def apply(self):
        """
        Obtiene el nombre ingresado por el usuario cuando se cierra el diálogo.
        """
        self.result = self.entry.get()  # Obtiene el texto ingresado por el usuario
