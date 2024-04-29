import tkinter as tk
from tkinter import messagebox

from juego_ahorcado.clasificacion import SistemaClasificacion
from juego_ahorcado.juego import JuegoAhorcado


class SeleccionModo:
    def __init__(self, master):
        self.master = master
        self.master.title("Selección de Modo de Juego")
        self.master.resizable(False, False)
        self.master.geometry("300x250")
        self.centra_ventana(self.master)

        self.crear_widgets()

    def centra_ventana(self, ventana):
        ventana.update_idletasks()
        width = ventana.winfo_width()
        height = ventana.winfo_height()
        x = (ventana.winfo_screenwidth() // 2) - (width // 2)
        y = (ventana.winfo_screenheight() // 2) - (height // 2)
        ventana.geometry(f"{width}x{height}+{x}+{y}")

    def crear_widgets(self):
        # Etiqueta para mostrar el texto "Escoge el modo de juego"
        lbl_modo_juego = tk.Label(self.master, text="Selecciona el modo de juego")
        lbl_modo_juego.pack(pady=5)

        # Botones para seleccionar el modo de juego
        btn_un_jugador = tk.Button(self.master, text="Un Jugador", command=self.mostrar_opciones_un_jugador)
        btn_un_jugador.pack(pady=10)

        btn_multijugador = tk.Button(self.master, text="Multijugador (Próximamente)", command=self.iniciar_juego_multijugador)
        btn_multijugador.pack(pady=10)

        btn_clasificacion = tk.Button(self.master, text="Clasificación con tiempo", command=self.mostrar_clasificacion_con_tiempo)
        btn_clasificacion.pack(pady=10)

        btn_clasificacion = tk.Button(self.master, text="Clasificación sin tiempo", command=self.mostrar_clasificacion_sin_tiempo)
        btn_clasificacion.pack(pady=10)

    def mostrar_opciones_un_jugador(self):
        self.master.withdraw()  # Oculta la ventana principal
        opciones_un_jugador = tk.Toplevel(self.master)
        opciones_un_jugador.title("Opciones Un Jugador")
        opciones_un_jugador.geometry("300x150")
        opciones_un_jugador.resizable(False, False)
        # Centra la ventana secundaria después de que se ha creado
        self.centra_ventana(opciones_un_jugador)

        lbl_opciones = tk.Label(opciones_un_jugador, text="Selecciona las opciones de juego")
        lbl_opciones.pack(pady=5)

        btn_con_tiempo = tk.Button(opciones_un_jugador, text="Con Tiempo", command=lambda: self.iniciar_juego_un_jugador(con_tiempo=True))
        btn_con_tiempo.pack(pady=5)

        btn_sin_tiempo = tk.Button(opciones_un_jugador, text="Sin Tiempo", command=lambda: self.iniciar_juego_un_jugador(con_tiempo=False))
        btn_sin_tiempo.pack(pady=5)

    def iniciar_juego_un_jugador(self, con_tiempo):
        self.master.destroy()  # Cierra la ventana de selección de modo de juego
        root = tk.Tk()
        JuegoAhorcado(root, con_tiempo)
        root.mainloop()

    def iniciar_juego_multijugador(self):
        messagebox.showinfo("Próximamente", "La opción Multijugador estará disponible en futuras versiones.")

    def mostrar_clasificacion_con_tiempo(self):
        sistema_clasificacion = SistemaClasificacion()
        sistema_clasificacion.cargar_puntuaciones()

        clasificacion = sistema_clasificacion.obtener_clasificacion(con_tiempo=True)
        if clasificacion:
            clasificacion_str = "\n".join(f"{i + 1}. {nombre}: {puntos}" for i, (nombre, puntos) in enumerate(clasificacion))
            messagebox.showinfo("Tabla de Clasificación", f"Tabla de Clasificación:\n{clasificacion_str}")
        else:
            messagebox.showinfo("Tabla de Clasificación", "Aún no hay puntuaciones para mostrar.")

    def mostrar_clasificacion_sin_tiempo(self):
        sistema_clasificacion = SistemaClasificacion()
        sistema_clasificacion.cargar_puntuaciones()

        clasificacion = sistema_clasificacion.obtener_clasificacion(con_tiempo=False)
        if clasificacion:
            clasificacion_str = "\n".join(f"{i + 1}. {nombre}: {puntos}" for i, (nombre, puntos) in enumerate(clasificacion))
            messagebox.showinfo("Tabla de Clasificación", f"Tabla de Clasificación:\n{clasificacion_str}")
        else:
            messagebox.showinfo("Tabla de Clasificación", "Aún no hay puntuaciones para mostrar.")
