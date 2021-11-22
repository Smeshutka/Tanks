import pygame
from tiles import Tile
from map_input import *

FPS = 30

SCREEN_WIDTH, SCREEN_HEIGHT, tiles = read_map_data('maps/1.txt')

# Инициализация мира
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

clock = pygame.time.Clock()

# Основной цикл программы
finished = False

while not finished:
    clock.tick(FPS)

    for t in tiles:
        tile = Tile(*t)
        screen.blit(tile.image, tile.rect)


    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            exit()
    pygame.display.update()