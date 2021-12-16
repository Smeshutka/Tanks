import pygame
from helper import *
import constans
from game import *
from level_constructor import *

pygame.init()

class Button:
    '''класс кнопок'''

    def __init__(self, screen, x0, y0, a, b, type):
        '''screen: pygame.display
        x0,y0 - координаты левого верхнего угла относительно экрана
        a,b - размеры окна по x,y соотв.
        image - название файла в папке textures формата png'''
        self.screen = screen
        self.size = pos(a, b)
        self.pos = pos(x0, y0)
        self.type = type
        self.image = pygame.image.load('textures/buttons/' + type + '.png').convert_alpha()
        self.image_selected = pygame.image.load('textures/buttons/' + type + '_selected.png').convert_alpha()
        self.pressed = False

    def set_image(self, image):
        self.image = pygame.image.load('textures/buttons/' + image + '.png').convert_alpha()

    def draw(self, k=1):
        x0, y0 = self.pos.x, self.pos.y
        a, b = self.size.x, self.size.y
        pygame.draw.rect(self.screen, (255, 255, 255), (x0, y0, a, b))
        if self.pressed:
            self.screen.blit(update_image(self.image_selected, a * k / constans.a, b * k / constans.a), (self.pos.x, self.pos.y))
        else:
            self.screen.blit(update_image(self.image, a * k / constans.a, b * k / constans.a),
                             (self.pos.x, self.pos.y))

    def check_pressed(self):
        mx, my = pygame.mouse.get_pos()
        x0, y0 = self.pos.x, self.pos.y
        a, b = self.size.x, self.size.y
        if mx >= x0 and my >= y0 and mx <= x0 + a and my <= y0 + b:
            self.pressed = True
        else:
            self.pressed = False

    def trigger(self):
        if self.type == 'new_game':
            game_main()
        elif self.type == 'level_constructor':
            level_constructor_main()
        elif self.type == 'exit_game':
            return True
        else:
            print('penis')
        return False





