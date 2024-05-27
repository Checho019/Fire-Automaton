import pygame
from componentes.kernels import *
from componentes.escenario import espacio_aleatorio, espacio_imagen, cargar_imagen
from componentes.utilidades import *
from componentes.celulas import estados

# Metodo main
if __name__ == '__main__':
    # inicializar Pygame
    pygame.init()

    # definir las dimensiones de la ventana
    width = 1200
    height = 700

    # crear la ventana
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Fire Automaton')

    # definir el tamaño de la cuadrícula
    grid_size = [height // 10, width // 10]

    # crear una matriz aleatoria para la cuadrícula
    # grid, humedad_grid = espacio_aleatorio(grid_size)

    # Crear matriz a partir de una imagen
    grid, humedad_grid = espacio_imagen(cargar_imagen('nuevo.jpg'))

    # Guardar estados iniciales
    estado_inicial = grid.copy()
    humedad_inicial = humedad_grid.copy()

    # Vecindario y velocidad de propagación
    kernel = K_V0
    velocidad = 0

    # ejecutar el bucle principal del juego
    water_mode = False
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
                    humedad_grid = humedad_inicial.copy()
                    que.quemado = 0
                elif event.key == pygame.K_LSHIFT:
                    humedad_view = not humedad_view
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
                    kernel = np.rot90(K_V145, k=1) if velocidad == 1 else np.rot90(K_V245, k=1)
                elif keys[pygame.K_UP] and keys[pygame.K_RIGHT]:
                    kernel = K_V145 if velocidad == 1 else K_V245
                elif keys[pygame.K_DOWN] and keys[pygame.K_LEFT]:
                    kernel = np.rot90(K_V145, k=2) if velocidad == 1 else np.rot90(K_V245, k=2)
                elif keys[pygame.K_DOWN] and keys[pygame.K_RIGHT]:
                    kernel = np.rot90(K_V145, k=-1) if velocidad == 1 else np.rot90(K_V245, k=-1)
                elif keys[pygame.K_UP]:
                    kernel = np.rot90(K_V190, k=1) if velocidad == 1 else np.rot90(K_V290, k=1)
                elif keys[pygame.K_DOWN]:
                    kernel = np.rot90(K_V190, k=-1) if velocidad == 1 else np.rot90(K_V290, k=-1)
                elif keys[pygame.K_LEFT]:
                    kernel = np.rot90(K_V190, k=2) if velocidad == 1 else np.rot90(K_V290, k=2)
                elif keys[pygame.K_RIGHT]:
                    kernel = K_V190 if velocidad == 1 else K_V290

        # Pausa
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
        if not humedad_view:
            next_grid = propagar_valor(grid, kernel, humedad_grid)
            grid = next_grid

        # dibujar la cuadrícula en la pantalla
        screen.fill((0, 0, 0) if not humedad_view else (255, 255, 255))
        for x in range(grid_size[0]):
            for y in range(grid_size[1]):
                if grid[x, y] != 0 if not humedad_view else True:
                    rect = pygame.Rect(y * width // grid_size[1], x * height // grid_size[0], width // grid_size[1],
                                       height // grid_size[0])
                    if not humedad_view:
                        pygame.draw.rect(screen, estados[grid[x, y]], rect)
                    else:
                        val = humedad_grid[x, y]
                        if val == 0:
                            val = 1
                        elif val == 1:
                            val = 0
                        pygame.draw.rect(screen, get_color(val), rect)

        # actualizar la pantalla
        pygame.display.update()