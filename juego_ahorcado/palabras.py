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
    "Superhéroes": ["Superman", "Batman", "Spiderman", "Wonder woman", "Iron man", "Capitán américa", "Thor", "Hulk", "Flash", "Aquaman"],
    "Marcas comerciales": ["Apple", "Samsung", "Microsoft", "Google", "Amazon", "Facebook", "Tesla", "Nike", "Coca-cola", "Disney"]
}

CATEGORIAS_PALABRAS_ORIGINALES = copy.deepcopy(CATEGORIAS_PALABRAS)
