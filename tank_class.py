import pygame
import math

dt = 1/60


def update(image, w, h, angle):
    """
    Меняет исходные размеры картинки, а затем поворачивает ее
    w, h: новые размеры картинки
    angle: угол поворота картинки
    """

    image = pygame.transform.scale(image, (w, h))
    image = pygame.transform.rotate(image, angle)
    
class pos():
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Tank():
    def __init__(self, x, y, tank_type, screen):
        """
        args: x,y - положение центра танка
        tank_type - тип танка, возможные: "light", "middle", "heavy"
        sreen - экран на котором будет отображаться танквввввв
        """
        self.screen = screen
        self.center = pos(x,y)
        self.velocity = pos(0,0)
        self.acceleration = pos(0,0)
        self.body_ang = 0
        self.turret_ang = 0
        
        
        if tank_type == "light":
            self.hp = 5
            self.size = pos(100,50)
            self.body_image = pygame.image.load("textures/light_body.png").convert_alpha()
            self.turret_image = pygame.image.load("textures/light_turret.png").convert_alpha()
            self.engine_power = 3
            self.ang_speed = 2*math.pi/10
        
        elif tank_type == "middle":
            self.hp = 5
            self.size = pos(100,50)
            self.body_image = pygame.image.load("textures/middle_body.png").convert_alpha()
            self.turret_image = pygame.image.load("textures/middle_turret.png").convert_alpha()
            self.engine_power = 2
            self.ang_speed = 2*math.pi/10
        
        elif tank_type == "heavy":
            self.hp = 5
            self.size = pos(134,82)
            self.body_image = pygame.image.load("textures/heavy_body.png").convert_alpha()
            self.turret_image = pygame.image.load("textures/heavy_turret.png").convert_alpha()
            self.engine_power = 100
            self.ang_speed = 2*math.pi/10
        
        self.corner = pos(self.center.x-self.size.x/2, self.center.y-self.size.y/2)
        
        
    def move(self, fw, fa, fs, fd, k1, k2):
        """
        Отвечает за перемещение и поворот всего танка
        args:
        fw, fa, fs, fd - переменные типа Bool, True если нажата
        кнопка под второй буквой переменной, False если нет
        """
        global dt
        
        def turn(self, fa, fd):
            if fa == True and fd == False:
                self.body_ang += self.ang_speed * dt
            elif fa == False and fd == True:
                self.body_ang -= self.ang_speed * dt
        
        def turn_turret(self):
            mx , my = pygame.mouse.get_pos()
            if mx > self.center.x:
                self.turret_ang = -math.atan((my-self.center.y) / (mx-self.center.x))
            elif mx < self.center.x:
                self.turret_ang = -math.atan((my-self.center.y) / (mx-self.center.x))+math.pi
        
        def set_acceleration(self, fw, fs, k1, k2):
            self.acceleration.x = 0
            self.acceleration.y = 0
            an = self.body_ang
            vx = self.velocity.x
            vy = self.velocity.y
            v = (vx**2 + vy**2)**0.5
            vel_ang = 0
            if vx > 0:
                vel_ang = -math.atan(vy/vx)
            elif vx < 0:
                vel_ang = -math.atan(vy/vx) + math.pi
            #Ускорение за счёт работы двигателя:
            if fw == True and fs == False:
                self.acceleration.x = self.engine_power * math.cos(an)
                self.acceleration.y = -self.engine_power * math.sin(an)
            elif fw == False and fs == True:
                self.acceleration.x = -self.engine_power * math.cos(an)
                self.acceleration.y = self.engine_power * math.sin(an)
            #сопротивление среды
            v_ort = v*math.sin(vel_ang-an)
            v_par = v*math.cos(vel_ang-an)
            self.acceleration.x -= k1 * abs(v_par*math.cos(an))*v_par*math.cos(an)
            self.acceleration.y += k1 * abs(v_par*math.sin(an))*v_par*math.sin(an)
            self.acceleration.x -= k2 * abs(v_ort*math.cos(math.pi/2+an))*v_ort*math.cos(math.pi/2+an)
            self.acceleration.y += k2 * abs(v_ort*math.sin(math.pi/2+an))*v_ort*math.sin(math.pi/2+an)
        turn(self,fa,fd)
        turn_turret(self)
        set_acceleration(self,fw,fs,k1,k2)
        self.velocity.x += self.acceleration.x * dt
        self.center.x += self.velocity.x * dt
        self.velocity.y += self.acceleration.y * dt
        self.center.y += self.velocity.y * dt
        self.corner = pos(self.center.x-self.size.x/2, self.center.y-self.size.y/2)
            
    def draw(self):
        image = pygame.transform.rotate(self.body_image, self.body_ang*180/math.pi)
        a, b = image.get_size()
        self.screen.blit(image, (self.center.x-a/2, self.center.y-b/2))
        image = pygame.transform.rotate(self.turret_image, self.turret_ang*180/math.pi)
        a, b = image.get_size()
        self.screen.blit(image, (self.center.x-a/2, self.center.y-b/2))
    
    def fire_gun(self):
        
                    

# Этот блок здесь для отладки классов
pygame.init()
screen = pygame.display.set_mode((800,800))
tank = Tank(250,250,"heavy",screen)
fw, fa, fs, fd = 0, 0, 0, 0
clock = pygame.time.Clock()
finished = False

while not finished:
    screen.fill((255,255,255))
    tank.draw()
    
    pygame.display.update()
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                fw = 1
            if event.key == pygame.K_a:
                fa = 1
            if event.key == pygame.K_s:
                fs = 1
            if event.key == pygame.K_d:
                fd = 1
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                fw = 0
            if event.key == pygame.K_a:
                fa = 0
            if event.key == pygame.K_s:
                fs = 0
            if event.key == pygame.K_d:
                fd = 0
    
    tank.move(fw,fa,fs,fd,0.01,1)
pygame.quit()