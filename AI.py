from helper import *
import random

def check_meet_dot(dot, tank):
    """Проверка того, доехал ли танк до точки, если да, то обновляем точку, до которой едим"""
    
    if abs(tank.center.x - dot.x) <= 1 and abs(tank.center.y - dot.y) <= 1:
        tank.number_dot += 1
        if tank.number_dot >= len(tank.list_dot):
            tank.number_dot = 0

def update(tank):
    """Обновляет координаты области видимости"""
    
    a, b = tank.vis.image.get_size()
    tank.vis.corner = pos(tank.center.x - a/2, tank.center.y - b/2)
  

def Go_to_dot(dot,tank):
    """Движение tank к точке dot"""
    
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

def move_AI(tank):
    """Алгоритм обработки действий AI, касательно движения"""
    
    dot = tank.list_dot[tank.number_dot]
    Go_to_dot(dot, tank)
    check_meet_dot(dot, tank)
    update(tank)
    

class vision(pygame.sprite.Sprite):
    def __init__(self, owner, screen):

        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.image = pygame.image.load('textures/visibility(1).png').convert_alpha()
        a, b = self.image.get_size()
        self.corner = pos(owner.center.x - a/2, owner.center.y - b/2)
        self.rect = self.image.get_rect()
        
    def draw(self):
        self.screen.blit(self.image, (self.corner.x, self.corner.y))

  
def meet_with_tank(tank, tank_pl):
    """Обработка событий бота, если он замечает игрока tank_pl"""
    
    if meet(tank.vis, tank_pl):
        tank.update_pos_mouse_for_AI(tank_pl.center.x, tank_pl.center.y)

        #Проверка на то, нужно ли стрелять во врага:
        tx, ty = tank.mouse.x, tank.mouse.y

        if tx > tank.center.x:
            tank.wanted_turret_ang = -math.atan((ty-tank.center.y) / (tx-tank.center.x))
        elif tx < tank.center.x:
            tank.wanted_turret_ang = -math.atan((ty-tank.center.y) / (tx-tank.center.x))+math.pi
        else:
            tank.wanted_turret_ang = convert_ang(tank.body_ang)
            
        if tank.wanted_turret_ang < 0:
            tank.wanted_turret_ang += 2*math.pi
        ang = convert_ang(tank.turret_ang) - tank.wanted_turret_ang
        if ang <= -math.pi:
            ang += 2*math.pi
        elif ang > math.pi:
            ang -= 2*math.pi
   
        ang = convert_ang(tank.turret_ang) - tank.wanted_turret_ang
        if ang <= -math.pi:
            ang += 2*math.pi
        elif ang > math.pi:
            ang -= 2*math.pi

        
        if abs(ang) <= math.pi / 6:
            tank.reload_left()
            
    else:
        tank.update_pos_mouse_for_AI(tank.center.x, tank.center.y)
