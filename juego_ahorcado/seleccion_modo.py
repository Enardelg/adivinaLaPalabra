import tkinter as tk
from tkinter import messagebox

from juego_ahorcado.clasificacion import SistemaClasificacion
from juego_ahorcado.juego import JuegoAhorcado


class SeleccionModo:
    def __init__(self, master):
        self.master = master
        self.master.title("Selección de Modo de Juego")
        self.master.resizable(False, False)
        self.master.geometry("400x200")
        self.centra_ventana()

        self.crear_widgets()

    def centra_ventana(self):
        self.master.update_idletasks()
        width = self.master.winfo_width()
        height = self.master.winfo_height()
        x = (self.master.winfo_screenwidth() // 2) - (width // 2)
        y = (self.master.winfo_screenheight() // 2) - (height // 2)
        self.master.geometry(f"{width}x{height}+{x}+{y}")

    def crear_widgets(self):
        # Etiqueta para mostrar el texto "Escoge el modo de juego"
        lbl_modo_juego = tk.Label(self.master, text="Selecciona el modo de juego")
        lbl_modo_juego.pack(pady=5)

        # Botones para seleccionar el modo de juego
        btn_un_jugador = tk.Button(self.master, text="Un Jugador", command=self.iniciar_juego_un_jugador)
        btn_un_jugador.pack(pady=10)

        btn_multijugador = tk.Button(self.master, text="Multijugador (Próximamente)", command=self.iniciar_juego_multijugador)
        btn_multijugador.pack(pady=10)

        btn_clasificacion = tk.Button(self.master, text="Clasificación", command=self.mostrar_clasificacion)
        btn_clasificacion.pack(pady=10)

    def iniciar_juego_un_jugador(self):
        self.master.destroy()  # Cierra la ventana de selección de modo de juego
        root = tk.Tk()
        JuegoAhorcado(root)
        root.mainloop()

    def iniciar_juego_multijugador(self):
        messagebox.showinfo("Próximamente", "La opción Multijugador estará disponible en futuras versiones.")

    def mostrar_clasificacion(self):
        sistema_clasificacion = SistemaClasificacion()
        sistema_clasificacion.cargar_puntuaciones()

        clasificacion = sistema_clasificacion.obtener_clasificacion()
        if clasificacion:
            clasificacion_str = "\n".join(f"{i + 1}. {nombre}: {puntos}" for i, (nombre, puntos) in enumerate(clasificacion))
            messagebox.showinfo("Tabla de Clasificación", f"Tabla de Clasificación:\n{clasificacion_str}")
        else:
            messagebox.showinfo("Tabla de Clasificación", "Aún no hay puntuaciones para mostrar.")
