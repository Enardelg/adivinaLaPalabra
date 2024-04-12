import json


class SistemaClasificacion:
    def __init__(self, max_puntuaciones=10):
        self.max_puntuaciones = max_puntuaciones
        self.puntuaciones = []

    def agregar_puntuacion(self, nombre, puntuacion):
        """
        Agrega una nueva puntuación al sistema de clasificación.

        Parameters:
            nombre (str): El nombre del jugador.
            puntuacion (int): La puntuación del jugador.
        """
        self.puntuaciones.append((nombre, puntuacion))
        self.puntuaciones.sort(key=lambda x: x[1], reverse=True)
        self.puntuaciones = self.puntuaciones[:self.max_puntuaciones]  # Limita la lista a las 10 puntuaciones más altas

    def obtener_clasificacion(self):
        """
        Obtiene la clasificación actual.

        Returns:
            list: Una lista de tuplas (nombre, puntuacion) ordenadas por puntuación descendente.
        """
        return self.puntuaciones

    def guardar_puntuaciones(self, archivo="puntuaciones.json"):
        """
        Guarda las puntuaciones en un archivo JSON.

        Parameters:
            archivo (str): El nombre del archivo donde se guardarán las puntuaciones.
        """
        with open(archivo, "w") as f:
            json.dump(self.puntuaciones, f)

    def cargar_puntuaciones(self, archivo="puntuaciones.json"):
        """
        Carga las puntuaciones desde un archivo JSON.

        Parameters:
            archivo (str): El nombre del archivo desde donde se cargarán las puntuaciones.
        """
        try:
            with open(archivo, "r") as f:
                self.puntuaciones = json.load(f)
        except FileNotFoundError:
            # Si el archivo no existe, se crea una lista vacía de puntuaciones
            self.puntuaciones = []
