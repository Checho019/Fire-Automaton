
import numpy as np
from scipy.signal import convolve2d

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

class que:
    quemado = float(0)
# Función para propagar el valor 2 usando un kernel, con la restricción de solo propagar en valores no 0
def propagar_valor(matriz, kernel, humedad):
    # Crear una matriz donde se propagará el valor
    resultado = matriz.copy()

    # Encontrar las posiciones de los valores 2
    posiciones = np.argwhere(matriz == 2)
    posAux = []
    for pos in posiciones:
        i, j = pos
        if humedad[i][j] <= 0.2:
            posAux.append(pos)

    for (i, j) in posAux:
        # Crear una matriz temporal con un 2 en la posición del 2
        temp = np.zeros_like(matriz)
        temp[i, j] = 2

        # Aplicar la convolución con el kernel
        conv_result = convolve2d(temp, kernel, mode='same', boundary='fill', fillvalue=0)

        # Propagar el valor 2 solo en celdas donde matriz original no sea 0
        mask = (matriz != 0) * humedad
        conv_result = np.where(mask >= 0.65, conv_result, 0)

        # Actualizar el resultado con la propagación válida
        resultado = np.maximum(resultado, conv_result)

    for (i, j) in posiciones:
        if humedad[i, j] != 0:
            resultado[i, j] = 2
            humedad[i, j] = max(0, humedad[i, j] - 0.05)

        if humedad[i, j] == 0:
            resultado[i, j] = 0
            que.quemado += 0.056
            print(que.quemado)
        else:
            resultado[i, j] = 2

    return resultado


def aplicar_agua(matriz, kernel, posicion, fuego):
    tamano_kernel = kernel.shape[0]
    desplazamiento = tamano_kernel // 2
    x, y = posicion
    resultado = matriz.copy()

    # Iterar sobre el kernel y la matriz de salida para aplicar los valores
    for i in range(tamano_kernel):
        for j in range(tamano_kernel):
            if kernel[i, j] == 1:
                nx, ny = x + i - desplazamiento, y + j - desplazamiento
                if 0 <= nx < matriz.shape[0] and 0 <= ny < matriz.shape[1]:
                    if fuego[nx][ny] == 2:
                        fuego[nx][ny] = 0
                        que.quemado += 0.056
                        print(que.quemado)
                    resultado[nx, ny] = 1
    resultado[x][y] = 1

    return resultado
