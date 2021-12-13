import pygame
import math
from constans import*


class pos():
    """Класс точка"""
    def __init__(self, x, y):
        self.x = x
        self.y = y


def pos_tile_to_pos_map(dot):
    return pos(dot.x * a + a // 2, dot.y * a + a // 2)


def update_mask(self):
    """Обновляет маску объекта"""
    
    self.mask = pygame.mask.from_surface(self.image)


def update_corner(self):
    """Обновляет положение угла объекта self"""
    
    a, b = self.image.get_size()
    self.corner = pos(self.center.x - a / 2, self.center.y - b / 2)


def meet(self, obj):
    """Проверка на то, встретились ли объект self и объект obj"""
        

    #self.rect = self.image.get_rect()
    self.rect.x, self.rect.y = self.corner.x, self.corner.y
   
    #obj.rect = obj.image.get_rect()
    obj.rect.x, obj.rect.y = obj.corner.x, obj.corner.y
   
    if pygame.sprite.collide_rect(self, obj):
        if pygame.sprite.collide_mask(self, obj):
            return True
    return False


def update_image(image, w, h):
    """
    Меняет исходные размеры картинки
    w, h: новые размеры картинки в размерах тайла (у.е.)
    """
    image = pygame.transform.scale(image, (int(w * a), int(h * a)))
    return image


def convert_ang(ang):
    """Перевод угла ang(в радианах) в полуинтервал [0,2pi)"""
    return ang % (2*math.pi)


class unnamed(pygame.sprite.Sprite):
    """Создает безымянный класс с изображением и маской"""

    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.corner = pos(x, y)
        update_mask(self)
        self.rect = self.image.get_rect()

screen_center = pos(w//2, h//2)
