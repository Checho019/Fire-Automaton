import math

import pygame
import numpy as np
from modelos.arboles import Arboles
from utils.utileria import propagar_valor, K_V0, K_V290, K_V145, K_V190

## Determina un bosque aleatorio
def inicializacion(x):
    if x <= 0.6:
        return 1
    else:
        return 0

def get_color(value):
    assert 0 <= value <= 1, "El valor debe estar entre 0 y 1"

    blue = np.array([0, 0, 255])
    white = np.array([255, 255, 255])

    color = value * blue + (1 - value) * white
    return color


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    alive_color = (69, 220, 118)
    dead_color = (0, 0, 0)
    burning_color = (227, 82, 82)
    wings_color = (0, 0, 0)
    wet_color = (0, 0, 255)

    colores = {
        0: dead_color,
        1: alive_color,
        2: burning_color,
        3: wings_color,
        4: wet_color,
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
    grid = np.random.rand(grid_size[0], grid_size[1])
    grid = vect_inicializacion(grid)
    estado_inicial = grid.copy()
    humedad_grid = np.random.rand(grid_size[0], grid_size[1])
    # definir los colores de las células


    # definir la duración de cada imagen en el GIF en milisegundos
    duration = 1000

    # ejecutar el bucle principal del juego
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
                    posx = math.floor((y / 10))
                    posy = math.floor((x / 10))
                    grid[posx][posy] = 2

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused
                elif event.key == pygame.K_r:
                    grid = estado_inicial.copy()
                elif event.key == pygame.K_LSHIFT:
                    humedad_view = not humedad_view
                elif event.key == pygame.K_v:
                    viento_view = not viento_view

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
        next_grid = propagar_valor(grid, K_V290, humedad_grid)
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
