from PIL import Image
import numpy as np


def cargar_imagen(ruta_imagen):
    # Abrir la imagen
    imagen = Image.open(ruta_imagen)
    # Convertir la imagen a RGB si no lo está
    imagen = imagen.convert("RGB")
    return imagen


def imagen_a_matriz(imagen):
    # Obtener las dimensiones de la imagen
    ancho, alto = imagen.size
    # Crear una matriz vacía con las dimensiones de la imagen
    matriz = np.zeros((alto, ancho, 3), dtype=np.uint8)

    # Rellenar la matriz con los valores de los píxeles
    for y in range(alto):
        for x in range(ancho):
            matriz[y, x] = imagen.getpixel((x, y))

    return matriz


def convertir_color_a_valor(color):
    r, g, b = color
    if g > 150:
        return 1
    elif b > 100:
        return 5
    return 0

def convertir_color_a_humedad(color):
    r, g, b = color
    if b > 100 or b == 0:
        return 1
    return np.random.uniform(0.6, 0.8)

def llenar_matriz_según_color(matriz):
    alto, ancho, _ = matriz.shape
    matriz_valores = np.zeros((alto, ancho), dtype=np.uint8)

    for y in range(alto):
        for x in range(ancho):
            color = matriz[y, x]
            matriz_valores[y, x] = convertir_color_a_valor(color)

    return matriz_valores

def llenar_matriz_humedad(matriz):
    alto, ancho, _ = matriz.shape
    matriz_valores = np.zeros((alto, ancho))

    for y in range(alto):
        for x in range(ancho):
            color = matriz[y, x]
            matriz_valores[y, x] = convertir_color_a_humedad(color)

    return matriz_valores