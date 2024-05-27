# Utilidades generales del sistema
import math
import numpy as np

# Generación aleatoria de un bosque con un 60% de bosque
def inicializacion(x):
    return 1 if x <= 0.6 else 0


# Obtener la celda de matriz a travez de un click
def obtener_click(x, y):
    posx = math.floor((y / 10))
    posy = math.floor((x / 10))
    return posx, posy


# Obtener el gradiente de color Azul-Blanco para graficar la humedad
def get_color(value):
    assert 0 <= value <= 1, "El valor debe estar entre 0 y 1"

    blue = np.array([0, 0, 255])
    white = np.array([255, 255, 255])

    color = value * white + (1 - value) * blue
    return color
