import random
import tkinter as tk
from tkinter import messagebox
import time
import unidecode


class JuegoAhorcado:
    """
    Clase para el juego del ahorcado.
    """
    def __init__(self, master):
        """
        Inicializa la ventana del juego y los atributos del juego.

        Parameters:
            master (Tk): La ventana principal del juego.
        """
        self.master = master  # Establece la ventana principal del juego
        self.master.title("El Ahorcado")  # Establece el título de la ventana
        self.master.resizable(False, False)  # Evita que se pueda redimensionar la ventana
        # Establecer un tamaño mínimo y máximo para la ventana
        self.master.minsize(400, 250)
        self.master.maxsize(400, 250)

        # Centra la ventana en la pantalla
        self.master.update_idletasks()  # Actualiza la ventana para asegurar que los tamaños sean correctos
        width = self.master.winfo_width()  # Obtiene el ancho actual de la ventana
        height = self.master.winfo_height()  # Obtiene el alto actual de la ventana
        x = (self.master.winfo_screenwidth() // 2) - (width // 2)  # Calcula la posición x para centrar la ventana
        y = (self.master.winfo_screenheight() // 2) - (height // 2)  # Calcula la posición y para centrar la ventana
        self.master.geometry(f"{width}x{height}+{x}+{y}")  # Establece la geometría de la ventana para centrarla en la pantalla

        self.mostrado_bienvenida = False  # Bandera para controlar si se ha mostrado el mensaje de bienvenida
        self.palabra_secreta = self.elegir_palabra()  # Selecciona una palabra al azar para el juego
        self.letras_adivinadas = []  # Lista para almacenar las letras que han sido adivinadas correctamente
        self.letras_falladas = []  # Lista para almacenar las letras que han sido incorrectamente propuestas
        self.fallos = 0  # Contador de los fallos del jugador
        self.puntos = 0  # Puntuación del jugador
        self.acumular_puntos_fallos = 0  # Contador para llevar un registro acumulado de los puntos de los fallos

        # Etiqueta para mostrar la palabra oculta
        self.label_palabra = tk.Label(self.master, text=self.mostrar_palabra_oculta())
        self.label_palabra.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

        # Etiqueta para mostrar el número de fallos
        self.label_fallos = tk.Label(self.master, text=f"Fallos: {self.fallos}/8")
        self.label_fallos.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        # Etiqueta para mostrar las letras falladas
        self.label_letras_falladas = tk.Label(self.master, text="")
        self.label_letras_falladas.grid(row=2, column=0, columnspan=4, padx=10, pady=10)

        # Etiqueta para mostrar los puntos
        self.label_puntos = tk.Label(self.master, text=f"Puntos: {self.puntos}")
        self.label_puntos.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        # Etiqueta para mostrar el tiempo transcurrido
        self.label_tiempo = tk.Label(self.master, text="Tiempo: 1:00")
        self.label_tiempo.grid(row=0, column=3, padx=10, pady=10, sticky="e")

        # Frame para los botones del teclado
        self.frame_teclado = tk.Frame(self.master)
        self.frame_teclado.grid(row=3, column=0, columnspan=4, padx=10, pady=10)

        self.botones_teclado = []  # Lista para almacenar los botones del teclado
        letras = ["QWERTYUIOP", "ASDFGHJKLÑ", "ZXCVBNM"]
        for i, linea in enumerate(letras):
            for j, letra in enumerate(linea):
                # Crea un botón para cada letra del teclado
                boton = tk.Button(self.frame_teclado, text=letra, width=4, command=lambda l=letra: self.adivinar_letra(l))
                boton.grid(row=i, column=j)
                self.botones_teclado.append(boton)

        # Mostrar mensaje de bienvenida si es la primera vez que se ejecuta el juego
        if not self.mostrado_bienvenida:
            self.mostrar_mensaje_bienvenida()
            self.mostrado_bienvenida = True

        # Iniciar contador de tiempo
        self.tiempo_inicio = time.time()
        self.tiempo_transcurrido_total = 0
        self.actualizar_tiempo()

    def mostrar_mensaje_bienvenida(self):
        """
        Muestra un mensaje de bienvenida cuando se inicia el juego.
        """
        messagebox.showinfo("¡Bienvenido!",
                            "Dispones de 8 fallos y 1 minuto para resolver cada palabra.\nLetra acertada suma 1 punto.\nTexto resuelto suma 50 puntos.\n"
                            "+1 punto por segundo restante.\n-3 puntos por fallo.")
    def elegir_palabra(self):
        """
        Elige una palabra al azar de una lista predefinida.

        Returns:
            str: La palabra seleccionada.
        """
        palabras = ["PYTHON", "PROGRAMACIÓN", "COMPUTADORA", "TECLADO", "RATÓN"]
        return random.choice(palabras)

    def mostrar_palabra_oculta(self):
        """
        Crea la representación visual de la palabra oculta, con guiones para las letras no adivinadas.

        Returns:
            str: La palabra oculta con guiones para las letras no adivinadas.
        """
        palabra_oculta = ""  # Inicializa una cadena vacía para la palabra oculta
        for letra in self.palabra_secreta:  # Itera sobre cada letra de la palabra secreta
            letra_normalizada = unidecode.unidecode(letra)  # Normaliza la letra para manejar caracteres especiales
            if letra_normalizada in [unidecode.unidecode(l) for l in self.letras_adivinadas]:  # Comprueba si la letra ha sido adivinada
                palabra_oculta += letra  # Si la letra ha sido adivinada, la agrega a la palabra oculta
            else:
                palabra_oculta += "_"  # Si la letra no ha sido adivinada, agrega un guion bajo a la palabra oculta
        return " ".join(palabra_oculta)  # Retorna la palabra oculta como una cadena con espacios entre cada letra

    def adivinar_letra(self, letra):
        """
        Maneja la lógica cuando el jugador intenta adivinar una letra.

        Parameters:
            letra (str): La letra que el jugador intenta adivinar.
        """
        letra = unidecode.unidecode(letra)  # Normalizar la letra antes de compararla
        if letra in [unidecode.unidecode(l) for l in self.palabra_secreta]:
            # Si la letra está en la palabra secreta, se agrega a las letras adivinadas, se suma 1 punto y se actualiza la interfaz
            self.letras_adivinadas.append(letra)
            self.puntos += 1
            self.actualizar_interfaz()
        else:
            # Si la letra no está en la palabra secreta, se agrega a las letras falladas, se incrementa el contador de fallos
            # y se acumulan los puntos de los fallos, luego se actualiza la interfaz
            self.letras_falladas.append(letra)
            self.fallos += 1
            self.acumular_puntos_fallos += 3
            self.actualizar_interfaz()

        # Desactivar el botón presionado
        for boton in self.botones_teclado:
            if boton["text"] == letra:
                boton.config(state="disabled", bg="lightgray")  # Desactiva el botón y cambia el color de fondo

        # Comprobar si el jugador ha perdido o ganado después de cada intento
        if self.fallos == 8:
            self.perder()  # Llama a la función para manejar la situación de perder
        elif all([unidecode.unidecode(l) in self.letras_adivinadas for l in self.palabra_secreta]):
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
        # Actualiza la etiqueta de puntos con el puntaje actualizado
        self.label_puntos.config(text=f"Puntos: {self.puntos}")

    def perder(self):
        """
        Maneja las acciones cuando el jugador pierde el juego.
        """
        self.tiempo_inicio = None  # Detener el tiempo
        # Muestra un mensaje indicando que el jugador perdió, mostrando la palabra secreta y su puntuación
        if self.puntos == 0:
            messagebox.showinfo("¡Perdiste!", f"La palabra secreta era: {self.palabra_secreta}\nNo has conseguido ningún punto...")
        else:
            # Si el jugador tenía puntos, se resta la acumulación de puntos por fallos de su puntuación total y se muestra un mensaje
            self.puntos -= self.acumular_puntos_fallos
            messagebox.showinfo("¡Perdiste!", f"La palabra secreta era: {self.palabra_secreta}\nHas conseguido un total de: ¡{self.puntos} puntos!")
        # Reinicia la puntuación y el juego
        self.puntos = 0
        self.reset_juego()

    def ganar(self):
        """
        Maneja las acciones cuando el jugador gana el juego.
        """
        self.tiempo_inicio = None  # Detener el tiempo
        # Calcula los puntos ganados por el jugador
        self.puntos += 50 + (60 - self.tiempo_transcurrido_total) - self.acumular_puntos_fallos
        # Muestra un mensaje de felicitación al jugador
        messagebox.showinfo("¡Felicidades!", f"¡Correcto, a por la siguiente palabra!")
        # Reinicia el juego
        self.reset_juego()

    def restaurar_botones(self):
        """
        Restaura los botones del teclado al estado inicial.
        """
        for boton in self.botones_teclado:
            boton.config(state="normal", bg="SystemButtonFace")

    def reset_juego(self):
        """
        Reinicia el juego con una nueva palabra secreta y restablece los atributos del juego.
        """
        self.palabra_secreta = self.elegir_palabra()
        self.letras_adivinadas = []
        self.letras_falladas = []
        self.fallos = 0
        self.acumular_puntos_fallos = 0
        self.actualizar_interfaz()
        self.tiempo_inicio = time.time()
        self.restaurar_botones()

    def actualizar_tiempo(self):
        """
        Actualiza el contador de tiempo y gestiona las acciones cuando se agota el tiempo.
        """
        # Calcula el tiempo transcurrido desde el inicio del juego
        if self.tiempo_inicio is not None:
            tiempo_transcurrido = int(time.time() - self.tiempo_inicio)
            self.tiempo_transcurrido_total = tiempo_transcurrido  # Actualiza el tiempo total transcurrido
        else:
            tiempo_transcurrido = self.tiempo_transcurrido_total  # Si el juego ha terminado, utiliza el tiempo total

        # Calcula el tiempo restante y lo muestra en el formato "minutos:segundos"
        tiempo_restante = max(0, 60 - tiempo_transcurrido)
        minutos = tiempo_restante // 60
        segundos = tiempo_restante % 60
        self.label_tiempo.config(text=f"Tiempo: {minutos}:{segundos:02d}")

        # Si queda tiempo restante, programa una llamada a actualizar_tiempo después de 1 segundo
        if tiempo_restante > 0:
            self.master.after(1000, self.actualizar_tiempo)
        else:
            # Si se agota el tiempo, se llama a la función perder y se programa otra llamada a actualizar_tiempo después de 1 segundo
            self.perder()
            self.master.after(1000, self.actualizar_tiempo)


if __name__ == "__main__":
    root = tk.Tk()
    juego = JuegoAhorcado(root)
    root.mainloop()
