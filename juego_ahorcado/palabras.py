import copy

CATEGORIAS_PALABRAS = {
    "Animales": ["León", "Elefante", "Tigre", "Jirafa", "Ballena", "Delfín", "Cebra", "Cocodrilo", "Águila", "Serpiente"],
    "Frutas": ["Manzana", "Plátano", "Pera", "Uva", "Fresa", "Piña", "Mango", "Melón", "Sandía", "Naranja"],
    "Países": ["Estados Unidos", "Canadá", "México", "Brasil", "Argentina", "España", "Francia", "Alemania", "Italia", "China"],
    "Colores": ["Rojo", "Azul", "Verde", "Amarillo", "Blanco", "Negro", "Rosa", "Morado", "Naranja", "Gris"],
    "Profesiones": ["Médico", "Maestro", "Bombero", "Policía", "Ingeniero", "Arquitecto", "Abogado", "Músico", "Actor", "Cocinero"],
    "Deportes": ["Fútbol", "Baloncesto", "Tenis", "Béisbol", "Natación", "Atletismo", "Voleibol", "Rugby", "Golf", "Hockey"],
    "Instrumentos musicales": ["Guitarra", "Piano", "Violín", "Batería", "Saxofón", "Trompeta", "Flauta", "Clarinete", "Acordeón", "Contrabajo"],
    "Cuerpo humano": ["Cabeza", "Brazo", "Pierna", "Mano", "Pie", "Ojo", "Nariz", "Boca", "Oreja", "Dedo"],
    "Transportes": ["Coche", "Avión", "Barco", "Tren", "Bicicleta", "Moto", "Camión", "Helicóptero", "Autobús", "Submarino"],
    "Comida": ["Pizza", "Hamburguesa", "Pasta", "Sushi", "Ensalada", "Sopa", "Tacos", "Kebab", "Paella", "Empanada"],
    "Objetos": ["Lápiz", "Libro", "Teléfono", "Cámara", "Reloj", "Televisión", "Lámpara", "Silla", "Mesa", "Cuchillo"],
    "Vegetales": ["Zanahoria", "Lechuga", "Tomate", "Cebolla", "Pimiento", "Pepino", "Calabaza", "Espinaca", "Patata", "Brócoli"],
    "Materiales": ["Madera", "Metal", "Plástico", "Vidrio", "Aluminio", "Acero", "Cartón", "Papel", "Titanio", "Cerámica"],
    "Superhéroes": ["Superman", "Batman", "Spiderman", "Wonder Woman", "Iron Man", "Capitán América", "Thor", "Hulk", "Flash", "Aquaman"],
    "Marcas comerciales": ["Apple", "Samsung", "Microsoft", "Google", "Amazon", "Facebook", "Tesla", "Nike", "Coca-cola", "Disney"],
    "Elementos químicos": ["Oxígeno", "Hidrógeno", "Carbono", "Nitrógeno", "Hierro", "Cobre", "Aluminio", "Plata", "Oro", "Uranio"],
    "Música clásica": ["Mozart", "Beethoven", "Bach", "Chopin", "Vivaldi", "Tchaikovsky", "Strauss", "Wagner", "Mendelssohn", "Haydn"],
    "Bebidas": ["Café", "Té", "Agua", "Cerveza", "Vino", "Refresco", "Jugo", "Whisky", "Ron", "Ginebra"],
    "Juegos de mesa": ["Ajedrez", "Damas", "Monopoly", "Risk", "Scrabble", "Catan", "Dominó", "Jenga", "Pictionary", "Trivial"],
    "Géneros cinematográficos": ["Acción", "Comedia", "Drama", "Ciencia Ficción", "Terror", "Aventura", "Romance", "Animación", "Fantasía", "Thriller"],
    "Ciudades del mundo": ["Nueva York", "Tokio", "Londres", "París", "Roma", "Pekín", "Sídney", "Moscú", "Dubái", "Los Ángeles"],
    "Científicos famosos": ["Albert Einstein", "Isaac Newton", "Marie Curie", "Charles Darwin", "Galileo Galilei", "Stephen Hawking", "Nikola Tesla", "Richard Feynman", "Jane Goodall", "Carl Sagan"],
    "Personajes de cuentos de hadas": ["Cenicienta", "Blancanieves", "Caperucita Roja", "Pulgarcito", "Rapunzel", "Hansel Y Gretel", "Peter Pan", "Alicia", "El Patito Feo", "Ricitos De Oro"],
    "Partes de un automóvil": ["Motor", "Rueda", "Parabrisas", "Volante", "Cinturón De Seguridad", "Freno", "Acelerador", "Marcha", "Faros", "Espejo Retrovisor"],
    "Tecnologías emergentes": ["Inteligencia Artificial", "Blockchain", "Realidad Virtual", "Internet De Las Cosas", "Seguridad Cibernética", "Vehículos Autónomos", "Computación Cuántica", "Robótica", "Nanotecnología", "Biometría"],
    "Mitos y leyendas": ["Medusa", "Minotauro", "Sirena", "Kraken", "Cíclope", "Quimera", "Hidra", "Fénix", "Naga", "Esfinge"],
    "Artistas renombrados": ["Leonardo Da Vinci", "Vincent van Gogh", "Pablo Picasso", "Michelangelo Buonarroti", "Rembrandt Van Rijn", "Claude Monet", "Edvard Munch", "Salvador Dalí", "Frida Kahlo", "Andy Warhol"]
}

CATEGORIAS_PALABRAS_ORIGINALES = copy.deepcopy(CATEGORIAS_PALABRAS)
