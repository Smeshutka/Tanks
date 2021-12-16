import pygame
from helper import *
from button_class import *


def menu_main():
    pygame.init()
    screen = pygame.display.set_mode((w, h))
    clock = pygame.time.Clock()

    finished = False
    mouse_pressed = False

    button1 = Button(screen, 250, 75, 300, 100, 'new_game')
    button2 = Button(screen, 250, 195, 300, 100, 'level_constructor')
    button3 = Button(screen, 250, 315, 300, 100, 'settings')
    button4 = Button(screen, 250, 435, 300, 100, 'exit_game')
    buttons = [button1, button2, button3, button4]

    while not finished:
        screen.fill((0, 0, 0))

        for button in buttons:
            button.check_pressed()
            button.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    for button in buttons:
                        if button.pressed:
                            finished = button.trigger()

        pygame.display.update()

        clock.tick(FPS)

menu_main()