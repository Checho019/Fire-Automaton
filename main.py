import math

import pygame
import numpy as np
from utils.utileria import propagar_valor, K_V0, K_V290, K_V145, K_V190, K_V245, aplicar_agua
from utils.image_loader import cargar_imagen, imagen_a_matriz, llenar_matriz_según_color, llenar_matriz_humedad

## Determina un bosque aleatorio
def inicializacion(x):
    if x <= 0.6:
        return 1
    else:
        return 0


def obtener_click(x, y):
    posx = math.floor((y / 10))
    posy = math.floor((x / 10))
    return posx, posy


def get_color(value):
    assert 0 <= value <= 1, "El valor debe estar entre 0 y 1"

    blue = np.array([0, 0, 255])
    white = np.array([255, 255, 255])

    color = value * blue + (1 - value) * white
    return color


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    alive_color = (112, 168, 19)
    dead_color = (0, 0, 0)
    burning_color = (255, 0, 0)
    wings_color = (0, 0, 0)
    wet_color = (0, 113, 254)
    water_color = (0, 0, 255)

    ruta_imagen = 'nuevo.jpg'  # Cambia esto por la ruta a tu imagen
    imagen = cargar_imagen(ruta_imagen)
    matriz_colores = imagen_a_matriz(imagen)
    matriz_valores = llenar_matriz_según_color(matriz_colores)

    colores = {
        0: dead_color,
        1: alive_color,
        2: burning_color,
        3: wings_color,
        4: wet_color,
        5: water_color
    }

    # inicializar Pygame
    pygame.init()

    # definir las dimensiones de la ventana
    width = 1200
    height = 700

    # crear la ventana
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Incendio :(')

    # definir el tamaño de la cuadrícula
    grid_size = [height // 10, width // 10]

    # crear una matriz aleatoria para la cuadrícula
    vect_inicializacion = np.vectorize(inicializacion)
    #grid = np.random.rand(grid_size[0], grid_size[1])
    #grid = vect_inicializacion(grid)
    grid = matriz_valores
    estado_inicial = grid.copy()
    #humedad_grid = np.random.rand(grid_size[0], grid_size[1])
    humedad_grid = llenar_matriz_humedad(matriz_colores)

    # Definir vainas
    kernel = K_V0
    velocidad = 0

    # definir la duración de cada imagen en el GIF en milisegundos
    duration = 1000

    # ejecutar el bucle principal del juego
    water_mode = False
    viento_view = False
    humedad_view = False
    paused = False
    running = True
    while running:
        # manejar los eventos de Pygame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    x, y = event.pos
                    posx, posy = obtener_click(x, y)
                    if not water_mode:
                        grid[posx][posy] = 2
                    else:
                        humedad_grid = aplicar_agua(humedad_grid, kernel, (posx, posy), grid)

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused
                elif event.key == pygame.K_r:
                    grid = estado_inicial.copy()
                elif event.key == pygame.K_LSHIFT:
                    humedad_view = not humedad_view
                elif event.key == pygame.K_v:
                    viento_view = not viento_view
                elif event.key == pygame.K_a:
                    water_mode = not water_mode

                # Eventos de la velocidad del viento
                elif event.key == pygame.K_0:
                    velocidad = 0
                    kernel = K_V0
                elif event.key == pygame.K_1:
                    velocidad = 1
                elif event.key == pygame.K_2:
                    velocidad = 2

                ## Direccionamiento del viento
                keys = pygame.key.get_pressed()
                if keys[pygame.K_UP] and keys[pygame.K_LEFT]:
                    print("xd")
                elif keys[pygame.K_UP] and keys[pygame.K_RIGHT]:
                    kernel = K_V145 if velocidad == 1 else K_V245
                elif keys[pygame.K_DOWN] and keys[pygame.K_LEFT]:
                    print("Abajo-izquierda")
                elif keys[pygame.K_DOWN] and keys[pygame.K_RIGHT]:
                    print("Abajo-derecha")
                elif keys[pygame.K_UP]:
                    kernel = np.rot90(K_V190, k=1) if velocidad == 1 else np.rot90(K_V290, k=1)
                elif keys[pygame.K_DOWN]:
                    kernel = np.rot90(K_V190, k=-1) if velocidad == 1 else np.rot90(K_V290, k=-1)
                elif keys[pygame.K_LEFT]:
                    kernel = np.rot90(K_V190, k=2) if velocidad == 1 else np.rot90(K_V290, k=2)
                elif keys[pygame.K_RIGHT]:
                    kernel = K_V190 if velocidad == 1 else K_V290

        ## Pausa
        if paused:
            overlay = pygame.Surface((width, height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 1))
            screen.blit(overlay, (0, 0))

            # Mostrar el texto "PAUSA" en la mitad de la pantalla
            font = pygame.font.Font(None, 72)
            text = font.render("PAUSA", True, (255, 255, 255))
            text_rect = text.get_rect(center=(width // 2, height // 2))
            screen.blit(text, text_rect)
            pygame.display.flip()
            continue

        if humedad_view:
            screen.fill((255, 255, 255))
            for x in range(grid_size[0]):
                for y in range(grid_size[1]):
                    rect = pygame.Rect(y * width // grid_size[1], x * height // grid_size[0], width // grid_size[1],
                                       height // grid_size[0])
                    pygame.draw.rect(screen, get_color(humedad_grid[x, y]), rect)
            pygame.display.update()
            continue

        # actualizar la cuadrícula
        next_grid = propagar_valor(grid, kernel, humedad_grid)
        grid = next_grid

        # dibujar la cuadrícula en la pantalla
        screen.fill(dead_color)
        for x in range(grid_size[0]):
            for y in range(grid_size[1]):
                if grid[x, y] != 0:
                    rect = pygame.Rect(y * width // grid_size[1], x * height // grid_size[0], width // grid_size[1],
                                       height // grid_size[0])
                    pygame.draw.rect(screen, colores[grid[x, y]], rect)


        # actualizar la pantalla
        pygame.display.update()
