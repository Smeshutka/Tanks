import pygame
from tiles import *
from map_input import *

FPS = 30

# SCREEN_WIDTH, SCREEN_HEIGHT, tiles = file_reader('maps/1.txt')
SCREEN_WIDTH, SCREEN_HEIGHT, tiles = map_generator(35, 70)

# Инициализация мира
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

clock = pygame.time.Clock()

tile_grass = pygame.image.load('images/tile_grass1.png').convert_alpha()
tile_water = pygame.image.load('images/tile_water1.png').convert_alpha()
tile_bricks = pygame.image.load('images/tile_bricks1.png').convert_alpha()


# Основной цикл программы
finished = False

while not finished:
    clock.tick(FPS)

    for t in tiles:
        tile = Tile(t[0], t[1], eval(t[2]))
        screen.blit(tile.image, tile.rect)

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            exit()
    pygame.display.update()