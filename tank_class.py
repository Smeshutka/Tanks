from helper import*
from bullets_class import*
from constans import*
from  map_maker.tiles import*

bullets = pygame.sprite.Group()
tanks = pygame.sprite.Group()


class Tank(pygame.sprite.Sprite):
    def __init__(self, x, y, tank_type, screen):
        """
        x,y - положение центра танка
        tank_type - тип танка, возможные: "light", "middle", "heavy"
        sreen - экран на котором будет отображаться танк
        """

        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.center = pos(x,y)
        self.velocity = pos(0,0)
        self.acceleration = pos(0,0)
        self.body_ang = 0
        self.turret_ang = 0
        self.vel_ang = 0
        self.v_ort = 0
        self.v_par = 0
        
        if tank_type == "light":
            self.hp = 5
            self.size = pos(100,50)
            self.body_image_start = pygame.image.load("textures/light_body.png").convert_alpha()
            self.turret_image_start = pygame.image.load("textures/light_turret.png").convert_alpha()
            self.engine_power = 3
            self.ang_speed = 2*math.pi/10
            self.m = 0.25
            self.cooldawn = 1
            self.time_cooldawn = 0
            self.hp = 3
        elif tank_type == "middle":
            self.hp = 5
            self.size = pos(100,50)
            self.body_image_start = pygame.image.load("textures/middle_body.png").convert_alpha()
            self.turret_image_start = pygame.image.load("textures/middle_turret.png").convert_alpha()
            self.engine_power = 2
            self.ang_speed = 2*math.pi/10
            self.m = 0.5
            self.cooldawn = 1
            self.time_cooldawn = 0
            self.hp = 3
        elif tank_type == "heavy":
            self.hp = 5
            self.size = pos(134,82)
            self.body_image_start = pygame.image.load("textures/heavy_body.png").convert_alpha()
            self.turret_image_start = pygame.image.load("textures/heavy_turret.png").convert_alpha()
            self.engine_power = 100
            self.ang_speed = 2*math.pi/10
            self.m = 1
            self.cooldawn = 1
            self.time_cooldawn = 0
            self.hp = 3
            
        self.body_image = self.body_image_start
        self.image = self.body_image
        self.turret_image = self.turret_image_start
        update_corner(self)
        update_mask(self)
        self.rect = self.image.get_rect()
        
    def move(self, fw, fa, fs, fd, k1, k2):
        """
        Отвечает за перемещение и поворот всего танка
        args:
        fw, fa, fs, fd - переменные типа Bool, True если нажата
        кнопка под второй буквой переменной, False если нет
        """
        global dt

        def check_move(self):
            """Проверка на то, может ли танк сюда сдвинутся (врезался ли он с тайлами)"""
            for tile in tiles:
                if tile.type == "bricks" or tile.type == "water":
                    if meet(self, tile):
                        return False
            return True

        def check_turn_turret(self):
            """Проверка на то, может ли танк повернуть свою башню"""
            
            obj = unnamed(self.turret_image, self.corner.x, self.corner.y) #Создается безымяный класс для проверки пересечения со стенками
            for tile in tiles:
                if tile.type == "bricks":
                    if meet(obj, tile):
                        return False
            return True
            
        
        def update_for_check(self):
            """Обновляем предположительно возможное положение танка.
            Нужно для определения того, может ли танк туда попасть или нет"""
            
            self.body_image = pygame.transform.rotate(self.body_image_start, self.body_ang*180/math.pi)
            self.image = self.body_image
            update_corner(self)
            self.rect = self.image.get_rect()
            update_mask(self) #Обновление маски танка
            
        def turn_body(self, fa, fd):
            body_ang = self.body_ang
            
            if fa == True and fd == False:
                self.body_ang += self.ang_speed * dt
            elif fa == False and fd == True:
                self.body_ang -= self.ang_speed * dt

            update_for_check(self)

            if check_move(self):
                pass
            else:
                self.body_ang = body_ang
                update_for_check(self)
                
            
        def turn_turret(self):
            mx , my = pygame.mouse.get_pos()
            #if check_turn_turret(self):
            #   print(mx, my)
            if mx > self.center.x:
                self.turret_ang = -math.atan((my-self.center.y) / (mx-self.center.x))
            elif mx < self.center.x:
                self.turret_ang = -math.atan((my-self.center.y) / (mx-self.center.x))+math.pi
        
        def set_acceleration(self, fw, fs, k1, k2):
            """
            Расчет ускорений танка с учетом действующих сил:
            Сила мотора F = engine_power, соноправлена с танком
            Сила сопротивления среды F = kV^2, противоположна по направлению вектору скорости
            """
            
            self.acceleration.x = 0
            self.acceleration.y = 0
            an = self.body_ang #Угол между горизонтом и направлением танка
            vx = self.velocity.x
            vy = self.velocity.y
            v = (vx**2 + vy**2)**0.5
            
            self.vel_ang = 0 #Угол между вектором скорости и горизонтом
            if vx > 0:
                self.vel_ang = -math.atan(vy/vx)
            elif vx < 0:
                self.vel_ang = -math.atan(vy/vx) + math.pi
                
            #Ускорение за счёт работы двигателя:
            if fw == True and fs == False:
                self.acceleration.x = self.engine_power * math.cos(an) / self.m
                self.acceleration.y = -self.engine_power * math.sin(an) / self.m
            elif fw == False and fs == True:
                self.acceleration.x = -self.engine_power * math.cos(an) / self.m
                self.acceleration.y = self.engine_power * math.sin(an) / self.m
                
            #Ускорение за счёт сопротивления среды:
            self.v_ort = v * math.sin(self.vel_ang-an)
            self.v_par = v * math.cos(self.vel_ang-an)
            self.acceleration.x -= k1 * abs(self.v_par*math.cos(an))* self.v_par*math.cos(an) / self.m
            self.acceleration.y += k1 * abs(self.v_par*math.sin(an))* self.v_par*math.sin(an) / self.m
            self.acceleration.x -= k2 * abs(self.v_ort*math.cos(math.pi/2+an))* self.v_ort*math.cos(math.pi/2+an) / self.m
            self.acceleration.y += k2 * abs(self.v_ort*math.sin(math.pi/2+an))* self.v_ort*math.sin(math.pi/2+an) / self.m

    
        def update_options(self):
            """Движение танка (обновление координат, скоростей)"""
            vx = self.velocity.x 
            vy = self.velocity.y
            x = self.center.x
            y = self.center.y

            #Обновление скоростей и координат
            self.velocity.x += self.acceleration.x * dt
            self.center.x += self.velocity.x * dt
            self.velocity.y += self.acceleration.y * dt
            self.center.y += self.velocity.y * dt
        
            update_for_check(self)

            if check_move(self):
                pass
            else:
                self.center.x = x
                self.center.y = y
                self.velocity.x *= -0.1
                self.velocity.y *= -0.1
            
                update_for_check(self)
                
        def main(self):
            turn_body(self,fa,fd) #Поворот тела танка
            turn_turret(self) #Поворот башни танка
            set_acceleration(self,fw,fs,k1,k2) #Расчет ускорений
            update_options(self) #Движение танка

        main(self)
            
    def draw(self):

        #Рисование тела танка:
        self.screen.blit(self.body_image, (self.corner.x, self.corner.y))
        
        #Рисование башни танка:
        self.turret_image = pygame.transform.rotate(self.turret_image_start, self.turret_ang*180/math.pi)
        a, b = self.turret_image.get_size()
        self.screen.blit(self.turret_image, (self.center.x-a/2, self.center.y-b/2))

        #Рисование cooldawn:
        dx = self.center.x - self.corner.x
        dy = self.center.y - self.corner.y
        x = self.center.x + dx
        y = self.center.y + dy
        pygame.draw.arc(self.screen,(0, 0, 0), (x, y, 20, 20), 0, self.time_cooldawn/self.cooldawn*2*math.pi, width = 6)

        #Рисование жизней:
        sub = pygame.Surface((20,20), pygame.SRCALPHA)
        dots = ((0,5),(5,0),(10,5),(15,0),(20,5),(10,20))
        pygame.draw.polygon(sub, (255,0,0), dots)
        b = self.body_image.get_size()[1]
        for i in range(self.hp):
            self.screen.blit(sub, (self.center.x-50+25*i, self.center.y-b/2-30))
        
    def fire_gun(self, flpk, frpk):
        if flpk == 1 and self.time_cooldawn == 0:
            a, b = self.turret_image_start.get_size()
            x = self.center.x + a / 2 * math.cos(self.turret_ang)
            y = self.center.y - a / 2 * math.sin(self.turret_ang)
            bullet = Bullets(self.screen, "bullet", x, y, self.turret_ang)
            bullet.add(bullets)
            self.time_cooldawn = self.cooldawn
        flpk = 0

        return flpk, frpk
            
          
    def update_cooldawn(self):
        self.time_cooldawn -= 1/FPS
        if self.time_cooldawn <= 0:
            self.time_cooldawn = 0
       
