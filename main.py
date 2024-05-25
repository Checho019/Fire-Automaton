import math

import pygame
import numpy as np
from modelos.arboles import Arboles
from utils.utileria import propagar_valor, K_V0, K_V245

## Determina un bosque aleatorio
def inicializacion(x):
    if x <= 0.67:
        return 1
    else:
        return 0


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    vect_inicializacion = np.vectorize(inicializacion)
    arbolito = Arboles(1.5, 1.5, 1.5)
    arbolito.mostrar_arbol()

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
    grid = np.random.rand(grid_size[0], grid_size[1])
    grid = vect_inicializacion(grid)
    estado_inicial = grid.copy()

    # definir los colores de las células
    alive_color = (69, 220, 118)
    dead_color = (0, 0, 0)
    burning_color = (227, 82, 82)

    # definir la duración de cada imagen en el GIF en milisegundos
    duration = 1000

    # ejecutar el bucle principal del juego
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
                    print("Hola mundo")

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


        # actualizar la cuadrícula
        # next_grid = np.ones_like(grid)
        next_grid = propagar_valor(grid, K_V245)
        '''
        for x in range(grid_size[0]):
            for y in range(grid_size[1]):
                if grid[x, y] == 2:
                    # continue
                    next_grid = propagar_valor(grid, K_V0)
                    #grid_value = next_grid[min(x + 1, grid_size[0] - 1), y]
                    #next_grid[min(x + 1, grid_size[0] - 1), y] = 2 if grid_value != 0 else 0
                    #grid_value = next_grid[x, min(y + 1, grid_size[1] - 1)]
                    #next_grid[x, min(y + 1, grid_size[1] - 1)] = 2 if grid_value != 0 else 0
                    #grid_value = next_grid[max(x - 1, 0), y]
                    #next_grid[max(x - 1, 0), y] = 2 if grid_value != 0 else 0
                    #grid_value = next_grid[x, max(y - 1, 0)]
                    #next_grid[x, max(y - 1, 0)] = 2 if grid_value != 0 else 0
                    next_grid[x, y] = 0
                elif grid[x, y] == 0:
                    next_grid[x, y] = 0
'''
        grid = next_grid

        # dibujar la cuadrícula en la pantalla
        screen.fill(dead_color)
        for x in range(grid_size[0]):
            for y in range(grid_size[1]):
                if grid[x, y] != 0:
                    rect = pygame.Rect(y * width // grid_size[1], x * height // grid_size[0], width // grid_size[1],
                                       height // grid_size[0])
                    if grid[x, y] == 1:
                        pygame.draw.rect(screen, alive_color, rect)
                    else:
                        pygame.draw.rect(screen, burning_color, rect)

        # actualizar la pantalla
        pygame.display.update()
