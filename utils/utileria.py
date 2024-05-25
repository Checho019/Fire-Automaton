import numpy as np
from scipy.signal import convolve2d
import time

# Definir los kernels
K_V0 = np.array([[0, 0, 0, 0, 0],
                 [0, 0, 1, 0, 0],
                 [0, 1, 0, 1, 0],
                 [0, 0, 1, 0, 0],
                 [0, 0, 0, 0, 0]])

K_V145 = np.array([[0, 0, 0, 0, 0],
                   [0, 1, 1, 1, 0],
                   [0, 0, 0, 1, 0],
                   [0, 0, 0, 1, 0],
                   [0, 0, 0, 0, 0]])

K_V190 = np.array([[0, 0, 0, 0, 0],
                   [0, 0, 1, 1, 0],
                   [0, 0, 0, 1, 0],
                   [0, 0, 1, 1, 0],
                   [0, 0, 0, 0, 0]])

K_V245 = np.array([[0, 0, 1, 1, 1],
                   [0, 0, 1, 1, 1],
                   [0, 0, 0, 1, 1],
                   [0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0]])

K_V290 = np.array([[0, 0, 0, 0, 0],
                   [0, 0, 1, 1, 1],
                   [0, 0, 0, 1, 1],
                   [0, 0, 1, 1, 1],
                   [0, 0, 0, 0, 0]])

# Función para propagar el valor 2 usando un kernel, con la restricción de solo propagar en valores no 0
def propagar_valor(matriz, kernel):
    # Crear una matriz donde se propagará el valor
    resultado = matriz.copy()

    # Encontrar las posiciones de los valores 2
    posiciones = np.argwhere(matriz == 2)
    for (i, j) in posiciones:
        # Crear una matriz temporal con un 2 en la posición del 2
        temp = np.zeros_like(matriz)
        temp[i, j] = 2

        # Aplicar la convolución con el kernel
        conv_result = convolve2d(temp, kernel, mode='same', boundary='fill', fillvalue=0)

        # Propagar el valor 2 solo en celdas donde matriz original no sea 0
        mask = matriz != 0
        conv_result = conv_result * mask

        resultado[i, j] = 0
        conv_result[i, j] = 0
        # Actualizar el resultado con la propagación válida
        resultado = np.maximum(resultado, conv_result)

    for (i, j) in posiciones:
        resultado[i, j] = 0

    return resultado
