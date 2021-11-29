from tank_class import *
from helper import *

def Go_to_dot(dot,tank):
    tank.fw,tank.fa,tank.fs,tank.fd = 0,0,0,0
    alpha = 0
    if dot.x > tank.center.x:
        alpha = -math.atan((dot.y-tank.center.y) / (dot.x-tank.center.x))
    elif dot.x < tank.center.x:
        alpha = -math.atan((dot.y-tank.center.y) / (dot.x-tank.center.x))+math.pi
    if alpha < 0:
        alpha += 2*math.pi
    beta = convert_ang(tank.body_ang)
    ang = alpha - beta
    if ang <= -math.pi:
        ang += 2*math.pi
    elif ang > math.pi:
        ang -= 2*math.pi
    
    if abs(ang) < math.pi/3:
        tank.fw = 1 
    elif abs(ang) > math.pi/3:
        tank.fs = 1
    if ang > 0:
        tank.fa = 1
    elif ang < 0:
        tank.fd = 1


class vision(pygame.sprite.Sprite):
    def __init__(self, owner, screen):
        """
        owner - тот, танк, чьё это поле зрения
        """

        pygame.sprite.Sprite.__init__(self)
        self.owner = owner
        self.screen = screen
        self.image = pygame.image.load('textures/visibility.png').convert_alpha()
        a, b = self.image.get_size()
        self.corner = pos(self.owner.center.x - a/2, self.owner.center.y - b/2)
        self.rect = self.image.get_rect()

    def draw(self):
        self.screen.blit(self.image, (self.corner.x, self.corner.y))

    def meet_with_tank(self, tank):
        """Обработка пересечения с игроком"""
        if meet(tank, self):
            self.owner.turn_turret(tank.center.x, tank.center.y)
            self.owner.reload_left()
            self.owner.fire_gun()
