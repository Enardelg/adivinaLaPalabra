import json


class SistemaClasificacion:
    def __init__(self, max_puntuaciones=10):
        self.max_puntuaciones = max_puntuaciones
        self.puntuaciones_con_tiempo = []
        self.puntuaciones_sin_tiempo = []

    def agregar_puntuacion(self, nombre, puntuacion, con_tiempo):
        """
        Agrega una nueva puntuación al sistema de clasificación.

        Parameters:
            nombre (str): El nombre del jugador.
            puntuacion (int): La puntuación del jugador.
            con_tiempo (bool): Indica si la puntuación fue obtenida en un juego con tiempo (True) o sin tiempo (False).
        """
        if con_tiempo:
            lista_puntuaciones = self.puntuaciones_con_tiempo
        else:
            lista_puntuaciones = self.puntuaciones_sin_tiempo

        lista_puntuaciones.append((nombre, puntuacion))
        lista_puntuaciones.sort(key=lambda x: x[1], reverse=True)
        lista_puntuaciones = lista_puntuaciones[:self.max_puntuaciones]  # Limita la lista a las 10 puntuaciones más altas

        if con_tiempo:
            self.puntuaciones_con_tiempo = lista_puntuaciones
        else:
            self.puntuaciones_sin_tiempo = lista_puntuaciones

    def obtener_clasificacion(self, con_tiempo):
        """
        Obtiene la clasificación actual.

        Returns:
            list: Una lista de tuplas (nombre, puntuacion) ordenadas por puntuación descendente.
        """
        if con_tiempo:
            return self.puntuaciones_con_tiempo
        else:
            return self.puntuaciones_sin_tiempo

    def guardar_puntuaciones(self, archivo="puntuaciones.json"):
        """
        Guarda las puntuaciones en un archivo JSON.

        Parameters:
            archivo (str): El nombre del archivo donde se guardarán las puntuaciones.
        """
        with open(archivo, "w") as f:
            json.dump((self.puntuaciones_con_tiempo, self.puntuaciones_sin_tiempo), f)

    def cargar_puntuaciones(self, archivo="puntuaciones.json"):
        """
        Carga las puntuaciones desde un archivo JSON.

        Parameters:
            archivo (str): El nombre del archivo desde donde se cargarán las puntuaciones.
        """
        try:
            with open(archivo, "r") as f:
                self.puntuaciones_con_tiempo, self.puntuaciones_sin_tiempo = json.load(f)
        except FileNotFoundError:
            # Si el archivo no existe, se crea una lista vacía de puntuaciones
            self.puntuaciones_con_tiempo = []
            self.puntuaciones_sin_tiempo = []
