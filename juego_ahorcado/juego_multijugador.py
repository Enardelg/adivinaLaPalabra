import tkinter as tk
from tkinter import messagebox

import unidecode


class JuegoMultijugador:
    def __init__(self, master, palabra):
        self.master = master  # Establece la ventana principal del juego
        self.inicializar_ventana()

        self.palabra_secreta = palabra.upper()
        self.letras_adivinadas = []  # Lista para almacenar las letras que han sido adivinadas correctamente
        self.letras_falladas = []  # Lista para almacenar las letras que han sido incorrectamente propuestas
        self.fallos = 0  # Contador de los fallos del jugador

        self.configurar_interfaz()

    def inicializar_ventana(self):
        self.master.title("El Ahorcado - Multijugador")
        self.master.resizable(False, False)
        self.master.minsize(400, 250)
        self.master.maxsize(400, 250)
        self.centra_ventana()

    def centra_ventana(self):
        self.master.update_idletasks()
        width = self.master.winfo_width()
        height = self.master.winfo_height()
        x = (self.master.winfo_screenwidth() // 2) - (width // 2)
        y = (self.master.winfo_screenheight() // 2) - (height // 2)
        self.master.geometry(f"{width}x{height}+{x}+{y}")

    def configurar_interfaz(self):
        # Etiqueta para mostrar la palabra oculta
        self.label_palabra = tk.Label(self.master, text=self.mostrar_palabra_oculta())
        self.label_palabra.grid(row=1, column=0, columnspan=4, padx=10, pady=10)

        # Etiqueta para mostrar el número de fallos
        self.label_fallos = tk.Label(self.master, text=f"Fallos: {self.fallos}/8")
        self.label_fallos.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        # Etiqueta para mostrar las letras falladas
        self.label_letras_falladas = tk.Label(self.master, text="")
        self.label_letras_falladas.grid(row=2, column=0, columnspan=4, padx=10, pady=10)

        # Frame para los botones del teclado
        self.frame_teclado = tk.Frame(self.master)
        self.frame_teclado.grid(row=4, column=0, columnspan=4, padx=10, pady=10)

        self.botones_teclado = []  # Lista para almacenar los botones del teclado
        letras = ["QWERTYUIOP", "ASDFGHJKLÑ", "ZXCVBNM"]
        self.teclas_botones = {}  # Diccionario para asociar teclas con botones
        for i, linea in enumerate(letras):
            for j, letra in enumerate(linea):
                # Crea un botón para cada letra del teclado
                boton = tk.Button(self.frame_teclado, text=letra, width=4, command=lambda l=letra: self.adivinar_letra(l))
                boton.grid(row=i, column=j)
                self.botones_teclado.append(boton)
                self.teclas_botones[letra] = boton  # Asocia la tecla con el botón correspondiente

        # Manejar eventos de teclado
        self.master.bind("<KeyPress>", self.manejar_evento_teclado)

    def manejar_evento_teclado(self, evento):
        """
        Maneja el evento de teclado: simula un clic en el botón correspondiente a la tecla presionada.
        """
        tecla = evento.char.upper()  # Obtiene la tecla presionada (en mayúsculas)
        if tecla in self.teclas_botones:
            boton = self.teclas_botones[tecla]
            boton.invoke()  # Simula un clic en el botón

    def mostrar_palabra_oculta(self):
        """
        Crea la representación visual de la palabra oculta, con guiones para las letras no adivinadas.

        Returns:
            str: La palabra oculta con guiones para las letras no adivinadas.
        """
        palabra_oculta = ""  # Inicializa una cadena vacía para la palabra oculta
        for letra in self.palabra_secreta:  # Itera sobre cada letra de la palabra secreta
            if letra == "Ñ":  # Si la letra es "Ñ", verifica si "Ñ" está adivinada
                if "Ñ" in self.letras_adivinadas:
                    palabra_oculta += letra
                else:
                    palabra_oculta += "_"  # Si "Ñ" no está adivinada, muestra un guion bajo
            elif letra in self.letras_adivinadas or unidecode.unidecode(letra) in self.letras_adivinadas:  # Comprueba si la letra ha sido adivinada
                palabra_oculta += letra  # Si la letra ha sido adivinada, la agrega a la palabra oculta
            else:
                if letra == " ":  # Si la letra es un espacio, agrega un espacio a la palabra oculta
                    palabra_oculta += " "
                elif letra == "-":
                    palabra_oculta += "-"
                else:
                    palabra_oculta += "_"  # Si la letra no ha sido adivinada, agrega un guion bajo a la palabra oculta
        return " ".join(palabra_oculta)  # Retorna la palabra oculta como una cadena con espacios entre cada letra

    def adivinar_letra(self, letra):
        """
        Maneja la lógica cuando el jugador intenta adivinar una letra.

        Parameters:
            letra (str): La letra que el jugador intenta adivinar.
        """
        letras_secretas = self.palabra_secreta  # Lista de letras de la palabra secreta

        if letra in letras_secretas:
            # Si la letra está en la palabra secreta, se agrega a las letras adivinadas
            self.letras_adivinadas.append(letra)
        else:
            letra_original = letra  # Conserva la letra original antes de normalizarla
            # Normaliza la letra y las letras de la palabra secreta
            letra_normalizada = unidecode.unidecode(letra_original)
            letras_secretas_normalizadas = [unidecode.unidecode(l) for l in letras_secretas]

            # Si la letra es "Ñ" o su versión normalizada no está en las letras secretas normalizadas
            if letra == "Ñ" or letra_normalizada not in letras_secretas_normalizadas:
                self.letras_falladas.append(letra)
                self.fallos += 1

        # Desactivar el botón presionado
        for boton in self.botones_teclado:
            if boton["text"] == letra:
                boton.config(state="disabled", bg="lightgray")  # Desactiva el botón y cambia el color de fondo

        # Verifica si la letra actual es una vocal sin tilde (A, E, I, O, U).
        # Si la letra con tilde (l) es igual a la letra actual y aún no ha sido adivinada,
        # la agrega a las letras adivinadas para mostrarla correctamente en la palabra oculta.
        for l in letras_secretas:
            if letra in ["A", "E", "I", "O", "U"]:
                if unidecode.unidecode(l) == letra and l not in self.letras_adivinadas:
                    self.letras_adivinadas.append(l)

        self.actualizar_interfaz()

        # Comprobar si el jugador ha perdido o ganado después de cada intento
        if self.fallos == 8:
            self.perder()  # Llama a la función para manejar la situación de perder
        elif all(l in self.letras_adivinadas or l == " " or l == "-" for l in self.palabra_secreta):
            self.ganar()  # Llama a la función para manejar la situación de ganar

    def actualizar_interfaz(self):
        """
        Actualiza la interfaz gráfica con la información más reciente del juego.
        """
        # Actualiza la etiqueta de la palabra oculta con la representación visual actualizada
        self.label_palabra.config(text=self.mostrar_palabra_oculta())
        # Actualiza la etiqueta de fallos con el conteo actualizado de fallos
        self.label_fallos.config(text=f"Fallos: {self.fallos}/8")
        # Actualiza la etiqueta de letras falladas con la lista actualizada de letras falladas
        self.label_letras_falladas.config(text=" ".join(self.letras_falladas))

    def perder(self):
        """
        Maneja las acciones cuando el jugador pierde el juego.
        """
        # Actualiza la interfaz gráfica
        self.actualizar_interfaz()

        # Muestra un mensaje indicando que el jugador perdió
        if self.fallos >= 8:
            messagebox.showinfo("¡Perdiste!", f"Fin del juego\nHas superado los fallos permitidos\nLa palabara era: {self.palabra_secreta}")

        # Cierra la ventana del juego actual
        self.master.destroy()

        # Crea una nueva ventana de selección de modo de juego
        root = tk.Tk()
        from juego_ahorcado.seleccion_modo import SeleccionModo
        SeleccionModo(root)
        root.mainloop()

    def ganar(self):
        """
        Maneja las acciones cuando el jugador gana el juego.
        """
        # Actualiza la interfaz gráfica
        self.actualizar_interfaz()
        # Muestra un mensaje de felicitación al jugador
        messagebox.showinfo("¡Felicidades!", f"¡Correcto, la palabra era: {self.palabra_secreta}!")

        # Cierra la ventana del juego actual
        self.master.destroy()

        # Crea una nueva ventana de selección de modo de juego
        root = tk.Tk()
        from juego_ahorcado.seleccion_modo import SeleccionModo
        SeleccionModo(root)
        root.mainloop()
