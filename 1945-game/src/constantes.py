# Titulo del juego

TITLE = "1942"

# Longitudes del tablero

ANCHO = 224
ALTO = 256

COOLDOWN = 5
CADENCIA = 10
CADENCIA_ENEMIGO = 10
COOLDOWN_ENEMIGO = 5

# SPRITE 1942

SPRITE_1942 = (2, 2, 0, 176, 44)
SPRITE_CAPCOM = (2, 0, 50, 62, 13)

# YOU WIN

SPRITE_YOUWIN = (1, 140, 0, 96, 66)

# HUD

SPRITE_ESTRELLA = (0, 130, 0, 15, 12)
SPRITE_ESTRELLA_VACIA = (0, 150, 0, 15, 12)
SPRITE_LOOPS = (0, 170, 0, 10, 15)
SPRITE_LOOPS_VACIO = (0, 185, 0, 10, 15)

# Sprites del avión

AVION_LOOP = ((1, 0, 0, 25, 16), (2, 0, 65, 25, 11),
              (2, 0, 95, 32, 22), (2, 0, 130, 27 ,7))

AVION_SPRITE_1 = (1, 0, 0, 25, 16) # Avión principal
AVION_SPRITE_2 = (1, 0, 130, 25, 16) # Avión hélices giradas
AVION_SPRITE_3 = (2, 0, 65, 25, 11) 
AVION_SPRITE_4 = (2, 0, 95, 32, 22)
AVION_SPRITE_5 = (2, 0, 130, 27 ,7)

ENEMIGO_BASICO_D = (2, 0, 140, 15 , 14)
ENEMIGO_BASICO_U = (2, 0, 155, 15 , 14)

ENEMIGO_ROJO_1 = (2, 0, 195, 14, 15)
ENEMIGO_ROJO_2 = (2, 15, 195, 13, 14)
ENEMIGO_ROJO_3 = (2, 30, 195, 13, 12)
ENEMIGO_ROJO_4 = (2, 45, 195, 16, 12)
ENEMIGO_ROJO_5 = (2, 65, 195, 15, 15)
ENEMIGO_ROJO_6 = (2, 85, 195, 14, 13)
ENEMIGO_ROJO_7 = (2, 100, 195, 13, 12)
ENEMIGO_ROJO_8 = (2, 115, 195, 12, 15)
ENEMIGO_ROJO_9 = (2, 130, 195, 15, 15)
ENEMIGO_ROJO_10 = (2, 150, 195, 14, 15)
ENEMIGO_ROJO_11 = (2, 165, 195, 13, 13)
ENEMIGO_ROJO_12 = (2, 180, 195, 16, 14)
ENEMIGO_ROJO_13 = (2, 200, 195, 15, 15)
ENEMIGO_ROJO_14 = (2, 220, 195, 14, 13)
ENEMIGO_ROJO_15 = (2, 235, 195, 12, 12)
ENEMIGO_ROJO_16 = (2, 0, 215, 13, 16)

BOMBARDERO_U = (0, 122, 20, 54, 42)
BOMBARDERO_D = (0, 122, 65, 54, 42)

SUPER_BOMBARDERO_U = (0, 122, 110, 63, 48)
SUPER_BOMBARDERO_D = (0, 122, 160, 63, 48)


EXPLOSION = (2, 0, 175, 17, 15)

# Imagen de fondo

SPRITE_PORTAVIONES = (0, 0, 0, 121, 256)
SPRITE_ISLA = ((1, 26, 0, 112, 125), 
               (1, 26, 130, 120, 127))


# Popiedades del avion del avión

AVION_VELOCIDAD_X = 4
AVION_VELOCIDAD_Y = 4
AVION_INICIAL = ((ANCHO//2 - AVION_SPRITE_1[3]//2), 200)

# Balas

VELOCIDAD_BALAS = 5
VELOCIDAD_BALAS_ENEMIGO_BOMBARDERO = 1.5
VELOCIDAD_BALAS_ENEMIGO_REGULAR = 2
BALA_INDIVIDUAL = (2, 0, 0, 2, 10)

BALA_REGULAR = (0, 200, 0, 4, 4)
BALA_BOMBARDERO_U = (0, 205, 0, 7, 7)
BALA_BOMBARDERO_D = (0, 215, 0, 8, 7)
