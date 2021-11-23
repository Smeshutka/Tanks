import pygame
from tanks import Tank
import numpy as np


class Mob(pygame.sprite.Sprite):
    def __init__(self, x, filename):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load(filename).convert_alpha()
        self.rect=self.image.get_rect(center=(x, 0))
    def triggering(self):
        if (Tank.x-Mob.x)**2+(Tank.x-Mob.x)**2<=2500:
            return True


mob=Mob(50, "greenship3.png.160x120r-removebg-preview")













