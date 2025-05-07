import copy
import random
import time
import tkinter as tk
from tkinter import messagebox

import unidecode

from juego_ahorcado.clasificacion import SistemaClasificacion
from juego_ahorcado.dialogo_nombre import NombreDialog
from juego_ahorcado.palabras import CATEGORIAS_PALABRAS, CATEGORIAS_PALABRAS_ORIGINALES


class JuegoAhorcado:
    def obtener_arte_ascii(self):
        return (
            " _   _                                          \n"
            "| | | |                                         \n"
            "| |_| | __ _ _ __   __ _ _ __ ___   __ _ _ __  \n"
            "|  _  |/ _` | '_ \\ / _` | '_ ` _ \\ / _` | '_ \\ \n"
            "| | | | (_| | | | | (_| | | | | | | (_| | | | |\n"
            "\\_| |_/\\__,_|_| |_|\\__, |_| |_| |_|\\__,_|_| |_|\n"
            "                    __/ |                      \n"
        )

    def __init__(self, master, con_tiempo):
        """
        Inicializa la ventana del juego y los atributos del juego.

        Parameters:
            master (Tk): La ventana principal del juego.
            con_tiempo (bool): Indica el juego con tiempo (True) o sin tiempo (False).
        """
        self.master = master  # Establece la ventana principal del juego
        self.inicializar_ventana()

        self.mostrado_bienvenida = False  # Bandera para controlar si se ha mostrado el mensaje de bienvenida
        self.con_tiempo = con_tiempo
        self.categoria_actual, self.palabra_secreta = self.elegir_palabra()  # Selecciona una palabra al azar para el juego
        self.letras_adivinadas = []  # Lista para almacenar las letras que han sido adivinadas correctamente
        self.letras_falladas = []  # Lista para almacenar las letras que han sido incorrectamente propuestas
        self.letra_desbloqueada = False
        self.fallos = 0  # Contador de los fallos del jugador
        self.puntos = 0  # Puntuación del jugador
        self.acumular_puntos_fallos = 0  # Contador para llevar un registro acumulado de los puntos de los fallos
        # Inicializar el sistema de clasificación
        self.sistema_clasificacion = SistemaClasificacion()
        # Cargar las puntuaciones guardadas
        self.sistema_clasificacion.cargar_puntuaciones()

        self.configurar_interfaz()

        # Mostrar mensaje de bienvenida si es la primera vez que se ejecuta el juego
        if not self.mostrado_bienvenida:
            self.mostrar_mensaje_bienvenida()
            self.mostrado_bienvenida = True

        if self.con_tiempo:
            # Iniciar contador de tiempo
            self.tiempo_inicio = time.time()
            self.tiempo_transcurrido_total = 0
            self.tiempo_limite = 60  # Tiempo límite en segundos
            self.actualizar_tiempo()  # Llamar a la función de actualización del tiempo inicialmente
        else:
            # Sin tiempo estrablecer a 0 para no sumar puntos extra al acertar las palabras
            self.tiempo_transcurrido_total = 0
            self.tiempo_limite = 0

    def inicializar_ventana(self):
        self.master.title("Adivina la Palabra")
        self.master.resizable(False, False)
        self.master.minsize(400, 460)
        self.centra_ventana()

    def centra_ventana(self):
    # Primero define las figuras del ahorcado
        self.figuras_ahorcado = [
        """
         +---+
         |   |
             |
             |
             |
             |
        =========""",
        """
         +---+
         |   |
         O   |
             |
             |
             |
        =========""",
        """
         +---+
         |   |
         O   |
         |   |
             |
             |
        =========""",
        """
         +---+
         |   |
         O   |
        /|   |
             |
             |
        =========""",
        """
         +---+
         |   |
         O   |
        /|\  |
             |
             |
        =========""",
        """
         +---+
         |   |
         O   |
        /|\  |
        /    |
             |
        =========""",
        """
         +---+
         |   |
         O   |
        /|\  |
        / \  |
             |
        =========""",
        """
         +---+
         |   |
        [O   |
        /|\  |
        / \  |
             |
        ========="""
    ]
    
    # Luego crea el label con la figura inicial
        self.label_figura = tk.Label(
            self.master, 
            text=self.figuras_ahorcado[0], 
            font=("Courier New", 12),
            justify="center",
            anchor="nw"
        )
        self.label_figura.grid(row=3, column=0, columnspan=4, sticky="nw", padx=20, pady=10)
    
    # Configuración del tamaño y posición de la ventana
        initial_width = 400
        initial_height = 550
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        x = (screen_width // 2) - (initial_width // 2)
        y = (screen_height // 2) - (initial_height // 2)
        self.master.geometry(f"{initial_width}x{initial_height}+{x}+{y}")
        
    def configurar_interfaz(self):
        # Etiqueta para mostrar los puntos
        self.label_puntos = tk.Label(self.master, text=f"Puntos: {self.puntos}")
        self.label_puntos.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        # Etiqueta para mostrar la categoría
        self.label_categoria = tk.Label(self.master, text="Categoría - " + self.categoria_actual)
        self.label_categoria.grid(row=0, column=0, columnspan=4, padx=10, pady=5)

        if self.con_tiempo:
            # Etiqueta para mostrar el tiempo transcurrido
            self.label_tiempo = tk.Label(self.master, text="Tiempo: 1:00")
            self.label_tiempo.grid(row=0, column=3, padx=10, pady=10, sticky="e")

        # Etiqueta para mostrar el número de fallos
        self.label_fallos = tk.Label(self.master, text=f"Fallos: {self.fallos}/8")
        self.label_fallos.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        # Etiqueta para mostrar la palabra oculta
        self.label_palabra = tk.Label(self.master, text=self.mostrar_palabra_oculta())
        self.label_palabra.grid(row=1, column=0, columnspan=4, padx=10, pady=10)

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

        self.label_arte = tk.Label(self.master, text=self.obtener_arte_ascii(), font=("Courier", 8), justify="left")
        self.label_arte.grid(row=6, column=0, columnspan=4)
        self.master.after(3000, self.label_arte.destroy)

        # Botón de ayuda
        self.boton_ayuda = tk.Button(self.master, text="Ayuda", command=self.mostrar_ayuda)
        self.boton_ayuda.grid(row=5, column=0, columnspan=4, pady=10)

        # Manejar eventos de teclado
        self.master.bind("<KeyPress>", self.manejar_evento_teclado)

    def mostrar_ayuda(self):
        equivalencias = {
            'Á': 'A',
            'É': 'E',
            'Í': 'I',
            'Ó': 'O',
            'Ú': 'U',
        }

        if self.puntos < 25:
            messagebox.showinfo("Ayuda", "No tienes suficientes puntos para obtener ayuda.")
            return

        # Seleccionar una letra aleatoria que no haya sido adivinada aún
        letras_disponibles = [letra for letra in self.palabra_secreta if letra not in self.letras_adivinadas]
        letras_disponibles_sin_espacio = [letra for letra in letras_disponibles if letra != " "]  # Filtrar los espacios

        letras_desbloquear = []  # Lista para almacenar todas las letras a desbloquear

        # Convertir todas las letras disponibles a su forma sin tilde
        letras_disponibles_sin_tilde = [unidecode.unidecode(letra) for letra in letras_disponibles_sin_espacio]

        if letras_disponibles_sin_tilde:
            letra_ayuda_sin_tilde = random.choice(letras_disponibles_sin_tilde)
            # Encontrar la letra original correspondiente con tilde
            letra_ayuda = letras_disponibles_sin_espacio[letras_disponibles_sin_tilde.index(letra_ayuda_sin_tilde)]

            # Si la letra desbloqueada tiene tilde, también desbloquea la correspondiente sin tilde
            if letra_ayuda in equivalencias:
                letra_sin_tilde = equivalencias[letra_ayuda]
                if letra_sin_tilde in self.palabra_secreta and letra_sin_tilde not in self.letras_adivinadas:
                    letras_desbloquear.append(letra_sin_tilde)
            # Si la letra desbloqueada es una vocal sin tilde, desbloquea también la vocal con tilde
            elif letra_ayuda in equivalencias.values():
                letra_con_tilde = list(equivalencias.keys())[list(equivalencias.values()).index(letra_ayuda)]
                if letra_con_tilde in self.palabra_secreta and letra_con_tilde not in self.letras_adivinadas:
                    letras_desbloquear.append(letra_con_tilde)
        else:
            letra_ayuda = random.choice(letras_disponibles)

        # Actualizar la lista de letras adivinadas y la interfaz gráfica
        self.letras_adivinadas.append(letra_ayuda)
        for letra in letras_desbloquear:
            self.letras_adivinadas.append(letra)
        self.actualizar_interfaz()

        # Descontar 25 puntos
        self.puntos -= 25
        self.label_puntos.config(text=f"Puntos: {self.puntos}")

        # Marcar que se ha desbloqueado una letra para esta palabra
        self.letra_desbloqueada = True

        # Deshabilitar el botón correspondiente a la letra desbloqueada
        if letra_ayuda in self.teclas_botones:
            boton_desbloqueado = self.teclas_botones[letra_ayuda]
            boton_desbloqueado.config(state="disabled", bg="lightgray")

        if self.letra_desbloqueada:
            self.boton_ayuda.config(state="disabled", bg="lightgray")

        if len(self.letras_adivinadas) == len(set(self.palabra_secreta)):
            self.ganar()
            return

        print(f"Se ha desbloqueado la letra '{letra_ayuda}' a cambio de 25 puntos.")

    def manejar_evento_teclado(self, evento):
        """
        Maneja el evento de teclado: simula un clic en el botón correspondiente a la tecla presionada.
        """
        tecla = evento.char.upper()  # Obtiene la tecla presionada (en mayúsculas)
        if tecla in self.teclas_botones:
            boton = self.teclas_botones[tecla]
            boton.invoke()  # Simula un clic en el botón

    def guardar_puntuacion(self):
        nombre_jugador = self.obtener_nombre_jugador()
        if nombre_jugador is not None:  # Verifica si se proporcionó un nombre
            self.sistema_clasificacion.agregar_puntuacion(nombre_jugador, self.puntos, self.con_tiempo)
            self.sistema_clasificacion.guardar_puntuaciones()

    def obtener_nombre_jugador(self):
        dialog = NombreDialog(self.master)  # Crea una instancia del diálogo personalizado
        return dialog.result  # Devuelve el resultado después de que se cierra el diálogo

    def mostrar_clasificacion(self):
        clasificacion = self.sistema_clasificacion.obtener_clasificacion(self.con_tiempo)
        clasificacion_str = "\n".join(f"{i + 1}. {nombre}: {puntos}" for i, (nombre, puntos) in enumerate(clasificacion))
        messagebox.showinfo("Tabla de Clasificación", f"Tabla de Clasificación:\n{clasificacion_str}")

    def mostrar_mensaje_bienvenida(self):
        """
        Muestra un mensaje de bienvenida cuando se inicia el juego.
        """
        if self.con_tiempo:
            messagebox.showinfo("¡Bienvenido!",
                                "Dispones de 8 fallos y 1 minuto para resolver cada palabra.\nLetra acertada suma 1 punto."
                                "\nTexto resuelto suma 50 puntos.\n+1 punto por segundo restante.\n-3 puntos por fallo.")
        else:
            messagebox.showinfo("¡Bienvenido!",
                                "Dispones de 8 fallos.\nLetra acertada suma 1 punto.\nTexto resuelto suma 50 puntos."
                                "\n-3 puntos por fallo.")

    def elegir_palabra(self):
        """
        Elige una palabra al azar de una categoría predefinida.

        Returns:
            str: La categoría seleccionada.
            str: La palabra seleccionada.
        """
        # Selección aleatoria de una categoría
        categoria = random.choice(list(CATEGORIAS_PALABRAS.keys()))
        # Selección aleatoria de una palabra de la categoría seleccionada
        palabra = random.choice(CATEGORIAS_PALABRAS[categoria]).upper()
        return categoria, palabra

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
            # Si la letra está en la palabra secreta, se agrega a las letras adivinadas, se suma 1 punto y se actualiza la interfaz
            self.letras_adivinadas.append(letra)

            # Sumar puntos adicionales por cada aparición de la letra en la palabra secreta
            puntos_adicionales = letras_secretas.count(letra)
            self.puntos += puntos_adicionales
        else:
            letra_original = letra  # Conserva la letra original antes de normalizarla
            # Normaliza la letra y las letras de la palabra secreta
            letra_normalizada = unidecode.unidecode(letra_original)
            letras_secretas_normalizadas = [unidecode.unidecode(l) for l in letras_secretas]

            # Si la letra es "Ñ" o su versión normalizada no está en las letras secretas normalizadas:
            if letra == "Ñ" or letra_normalizada not in letras_secretas_normalizadas:
                self.letras_falladas.append(letra)
                self.fallos += 1
                self.acumular_puntos_fallos += 3

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
                    self.puntos += 1

        self.actualizar_interfaz()
        self.label_figura.config(text=self.figuras_ahorcado[min(self.fallos, len(self.figuras_ahorcado)-1)])

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
        # Actualiza la etiqueta de puntos con el puntaje actualizado
        self.label_puntos.config(text=f"Puntos: {self.puntos}")

    def perder(self):
        """
        Maneja las acciones cuando el jugador pierde el juego.
        """
        self.tiempo_inicio = None  # Detener el tiempo
        total_puntos = self.puntos - self.acumular_puntos_fallos

        # Muestra un mensaje indicando que el jugador perdió y su puntuación
        if self.tiempo_transcurrido_total >= 10 and total_puntos <= 0:
            self.puntos = 0
            # Actualiza la interfaz gráfica
            self.actualizar_interfaz()
            messagebox.showinfo("¡Perdiste!", f"Fin del juego\nSe ha agotado el tiempo\n"f"No has conseguido ningún punto...")
        elif self.tiempo_transcurrido_total >= 10 and total_puntos > 0:
            # Si el jugador tenía puntos, se resta la acumulación de puntos por fallos de su puntuación total y se muestra un mensaje
            self.puntos -= self.acumular_puntos_fallos
            # Actualiza la interfaz gráfica
            self.actualizar_interfaz()
            messagebox.showinfo("¡Perdiste!", f"Fin del juego\nSe ha agotado el tiempo\n"f"Has conseguido un total de: ¡{self.puntos} puntos!")
        elif total_puntos <= 0 < self.fallos >= 8:
            self.puntos = 0
            # Actualiza la interfaz gráfica
            self.actualizar_interfaz()
            messagebox.showinfo("¡Perdiste!", f"Fin del juego\nHas superado los fallos permitidos\nNo has conseguido ningún punto...")
        elif total_puntos > 0 < self.fallos >= 8:
            # Si el jugador tenía puntos, se resta la acumulación de puntos por fallos de su puntuación total y se muestra un mensaje
            self.puntos -= self.acumular_puntos_fallos
            # Actualiza la interfaz gráfica
            self.actualizar_interfaz()
            messagebox.showinfo("¡Perdiste!", f"Fin del juego\nHas superado los fallos permitidos\nHas conseguido un total de: ¡{self.puntos} puntos!")

        if self.puntos > 0:
            clasificacion = self.sistema_clasificacion.obtener_clasificacion(self.con_tiempo)
            if clasificacion:
                puntajes_actuales = [puntuacion for _, puntuacion in self.sistema_clasificacion.obtener_clasificacion(self.con_tiempo)]
                peor_puntaje = min(puntajes_actuales)
                if self.puntos > peor_puntaje or len(puntajes_actuales) < self.sistema_clasificacion.max_puntuaciones:
                    self.guardar_puntuacion()  # Guardar la puntuación cuando el jugador gana puntos
                else:
                    messagebox.showinfo("¡Puntos insuficientes!", "No tienes suficientes puntos para entrar en el top 10.")
                self.mostrar_clasificacion()  # Mostrar la tabla de clasificación cuando el jugador ha ganado puntos
            else:
                self.guardar_puntuacion()  # Guarda la puntuación cuando no hay ninguna puntuación en la clasificación
                self.mostrar_clasificacion()  # Muestra la tabla de clasificación vacía
        # Reinicia la puntuación y el juego
        self.puntos = 0

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
        self.tiempo_inicio = None  # Detener el tiempo
        # Calcula los puntos ganados por el jugador
        self.puntos += 50 + (self.tiempo_limite - self.tiempo_transcurrido_total) - self.acumular_puntos_fallos
        # Actualiza la interfaz gráfica
        self.actualizar_interfaz()
        # Muestra un mensaje de felicitación al jugador
        messagebox.showinfo("¡Felicidades!", f"¡Correcto, a por la siguiente palabra!")
        # Reinicia el juego
        self.continuar_juego()

    def restaurar_botones(self):
        """
        Restaura los botones del teclado al estado inicial.
        """
        for boton in self.botones_teclado:
            boton.config(state="normal", bg="SystemButtonFace")

    def continuar_juego(self):
        """
        Continúa el juego con una nueva palabra secreta y restablece los atributos del juego.
        """
    # Convierte la primera letra de cada palabra de la palabra secreta en mayúscula
        palabras_secreta_lista = self.palabra_secreta.split()
        palabras_secreta_minuscula = [palabra[0].upper() + palabra[1:].lower() for palabra in palabras_secreta_lista]
        palabra_secreta_minuscula = " ".join(palabras_secreta_minuscula)
        
    # Elimina la palabra acertada del diccionario de categorías
        try:
            CATEGORIAS_PALABRAS[self.categoria_actual].remove(palabra_secreta_minuscula)
            # Si no hay más palabras en la categoría, elimina la categoría del diccionario
            if not CATEGORIAS_PALABRAS[self.categoria_actual]:
                del CATEGORIAS_PALABRAS[self.categoria_actual]
            if not CATEGORIAS_PALABRAS:
                messagebox.showinfo("Fin del juego", "¡Todas las palabras se han agotado! Gracias por jugar.")
                if self.sistema_clasificacion.puntuaciones_con_tiempo:
                    puntajes_actuales = [puntuacion for _, puntuacion in self.sistema_clasificacion.obtener_clasificacion(self.con_tiempo)]
                    peor_puntaje = min(puntajes_actuales)
                    if self.puntos > peor_puntaje or len(puntajes_actuales) < self.sistema_clasificacion.max_puntuaciones:
                        self.guardar_puntuacion()
                    else:
                        messagebox.showinfo("¡Puntos insuficientes!", "No tienes suficientes puntos para entrar en el top 10.")
                    self.mostrar_clasificacion()
                self.reiniciar_juego()
                return
        except ValueError as e:
            print(f"Error: {e}. La palabra '{palabra_secreta_minuscula}' no está en la lista de la categoría '{self.categoria_actual}'.")

    # Reiniciar variables del juego
        self.letras_adivinadas = []
        self.letras_falladas = []
        self.letra_desbloqueada = False
        self.fallos = 0
        self.acumular_puntos_fallos = 0
        
        # Reiniciar la figura del ahorcado
        self.label_figura.config(text=self.figuras_ahorcado[0])
        
        # Obtener nueva palabra
        self.categoria_actual, self.palabra_secreta = self.elegir_palabra()
        
        # Reiniciar tiempo si es modo con tiempo
        if self.con_tiempo:
            self.tiempo_inicio = time.time()
        
        # Actualizar interfaz
        self.actualizar_interfaz()
        self.boton_ayuda.config(state="normal", bg="SystemButtonFace")
        self.restaurar_botones()
        self.label_categoria.config(text="Categoría - " + self.categoria_actual)

    def reiniciar_juego(self):
        """
        Reinicia el juego con todas las palabras y categorías nuevamente.
        """
        # Reiniciar variables del juego
        self.letras_adivinadas = []
        self.letras_falladas = []
        self.letra_desbloqueada = False
        self.fallos = 0
        self.puntos = 0
        self.acumular_puntos_fallos = 0
        
        # Reiniciar la figura del ahorcado
        self.label_figura.config(text=self.figuras_ahorcado[0])
        
        # Reiniciar sistema de clasificación
        self.sistema_clasificacion = SistemaClasificacion()
        self.sistema_clasificacion.cargar_puntuaciones()
        
        # Reiniciar tiempo
        if self.con_tiempo:
            self.tiempo_inicio = time.time()
        
        # Restaurar palabras originales
        categorias_palabras_originales_copia = copy.deepcopy(CATEGORIAS_PALABRAS_ORIGINALES)
        CATEGORIAS_PALABRAS.clear()
        CATEGORIAS_PALABRAS.update(categorias_palabras_originales_copia)
        
        # Obtener nueva palabra
        self.categoria_actual, self.palabra_secreta = self.elegir_palabra()
        
        # Actualizar interfaz
        self.actualizar_interfaz()
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
        tiempo_restante = max(0, self.tiempo_limite - tiempo_transcurrido)
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