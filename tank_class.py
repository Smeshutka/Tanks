from helper import*
from bullets_class import*
from  map_maker.tiles import*
from AI import*

bullets = pygame.sprite.Group()
tanks_bots = pygame.sprite.Group()
tanks = pygame.sprite.Group()


class Tank(pygame.sprite.Sprite):
    def __init__(self, x, y, angle, tank_type, screen):
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
        self.body_ang = angle
        self.turret_ang = angle
        self.vel_ang = 0
        self.v_ort = 0
        self.v_par = 0
        self.flpk = 0
        self.frpk = 0
        self.fw = 0
        self.fa = 0
        self.fs = 0
        self.fd = 0
        self.turret_rotate_speed = 1
        self.number_dot = 0
        self.mouse = pos(x, y)
        self.vis = vision(self, screen)
        self.wanted_turret_ang = self.body_ang
        
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
        self.add(tanks)
        
    def update_list_dot(self, list_dot):
        """
        list_dot: список координат точек траектории танка
        элементами списка являются объекты класса pos
        pos(x, y): точка с координатами (x, y)
        """
        
        self.list_dot = list_dot

    def update_list_tile(self, list_tile):
        """
        list_tile: список тайлов, по которым хочется, чтобы двигался танк.
        элементами списка являются объекты класса pos
        pos(n, m): тайл с номером (n, m)
        Этот список преобразуется в список точек, по которым будет двигаться танк
        Самая левая ячейка карты имеет координаты (0, 0)
        """
        
        list_dot = []
        for i in range(len(list_tile)):
            list_tile[i] = pos_tile_to_pos_map(list_tile[i])
        self.list_dot = list_tile

    def update_pos_mouse_for_player(self):
        """Обновляет положение мыши для игрока"""
        x, y = pygame.mouse.get_pos()
        self.mouse = pos(x, y)


    def update_pos_mouse_for_AI(self, x, y):
        """Обновляет положение мыши у бота"""
        self.mouse = pos(x, y)
    
    def turn_turret(self):
        tx, ty = self.mouse.x, self.mouse.y

        if tx > self.center.x:
            self.wanted_turret_ang = -math.atan((ty-self.center.y) / (tx-self.center.x))
        elif tx < self.center.x:
            self.wanted_turret_ang = -math.atan((ty-self.center.y) / (tx-self.center.x))+math.pi
        else:
            self.wanted_turret_ang = convert_ang(self.body_ang)
            
        if self.wanted_turret_ang < 0:
            self.wanted_turret_ang += 2*math.pi
        ang = convert_ang(self.turret_ang) - self.wanted_turret_ang
        if ang <= -math.pi:
            ang += 2*math.pi
        elif ang > math.pi:
            ang -= 2*math.pi
        if ang < 0:
            self.turret_ang += self.turret_rotate_speed * dt
        elif ang > 0:
            self.turret_ang -= self.turret_rotate_speed * dt


    def move(self):
        """
        Отвечает за перемещение и поворот всего танка
        args:
        fw, fa, fs, fd - переменные типа Bool, True если нажата
        кнопка под второй буквой переменной, False если нет
        """
        global dt

        def get_mu(self):
            """Возвращает коэффициент трения тайла, находящегося в центре танка"""
            tile = return_tile_ower_pos(self.center.x, self.center.y)
            return tile.k1, tile.k2
        
        def tiles_near(self):
            """
            Возвращает группу тайлов, находящихся поблизости танка
            tiles_array[i][j]: i - номер строчки, j - номер столбца
            """
            tiles_n = pygame.sprite.Group()
            x1, y1, x2, y2 = self.corner.x, self.corner.y, 2 * self.center.x - self.corner.x, 2 * self.center.y - self.corner.y
            x1 = max(int(x1) // a - 2, 0)
            x2 = min(int(x2) // a + 2, len(tiles_array[0]) - 1)
            y1 = max(int(y1) // a - 2, 0)
            y2 = min(int(y2) // a + 2, len(tiles_array) - 1)
            for i in range(x1, x2):
                for j in range(y1, y2):
                    if j >= 0 and j < len(tiles_array) and i >= 0 and i < len(tiles_array[0]):
                        tiles_array[j][i].add(tiles_n)
            return tiles_n

        def check_move_tanks(self):
            """Проверка на то, может ли танк сюда сдвинутся (врезался ли он с танками)"""
            for tank in tanks:
                if tank != self:
                    if meet(self, tank):
                        return False
            return True
        
        def check_move_tiles(self):
            """Проверка на то, может ли танк сюда сдвинутся (врезался ли он с тайлами)"""
            for tile in tiles_near(self):
                if tile.type == "bricks" or tile.type == "water":
                    if meet(self, tile):
                        return False
            return True

        def check_move(self):
            """Проверка на то, может ли танк сюда сдвинутся (врезался ли он с тайлами или танком)"""
            return check_move_tanks(self) and check_move_tiles(self)

        def check_turn_turret(self):
            """Проверка на то, может ли танк повернуть свою башню"""
            
            obj = unnamed(self.turret_image, self.corner.x, self.corner.y) #Создается безымяный класс для проверки пересечения со стенками
            for tile in tiles_near(self):
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
            
        def turn_body(self):
            body_ang = self.body_ang
            
            if self.fa == True and self.fd == False:
                self.body_ang += self.ang_speed * dt
                self.turret_ang += self.ang_speed * dt
            elif self.fa == False and self.fd == True:
                self.body_ang -= self.ang_speed * dt
                self.turret_ang -= self.ang_speed * dt

            update_for_check(self)

            if check_move(self):
                pass
            else:
                self.body_ang = body_ang
                update_for_check(self)


        def set_acceleration(self, k1, k2):
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
            self.turn_turret() #Поворот башни танка
            v = (vx**2 + vy**2)**0.5
            
            self.vel_ang = 0 #Угол между вектором скорости и горизонтом
            if vx > 0:
                self.vel_ang = -math.atan(vy/vx)
            elif vx < 0:
                self.vel_ang = -math.atan(vy/vx) + math.pi
                
            #Ускорение за счёт работы двигателя:
            if self.fw == True and self.fs == False:
                self.acceleration.x = self.engine_power * math.cos(an) / self.m
                self.acceleration.y = -self.engine_power * math.sin(an) / self.m
            elif self.fw == False and self.fs == True:
                self.acceleration.x = -self.engine_power * math.cos(an) / self.m
                self.acceleration.y = self.engine_power * math.sin(an) / self.m
                
            #Ускорение за счёт сопротивления среды:
            self.v_ort = v * math.sin(self.vel_ang-an)
            self.v_par = v * math.cos(self.vel_ang-an)


            if abs(self.v_par*math.cos(an)) > 10:
                self.acceleration.x -= k1 * abs(self.v_par*math.cos(an))* self.v_par*math.cos(an) / self.m
            elif abs(self.v_par*math.cos(an)) > 5:
                self.acceleration.x -= k1 * 10 * self.v_par*math.cos(an) / self.m
            elif abs(self.v_par*math.cos(an)) > 0:
                self.acceleration.x -= k1*25 * self.v_par*math.cos(an)/abs(self.v_par*math.cos(an))
            else:
                pass

            if abs(self.v_par * math.sin(an)) > 10:
                self.acceleration.y += k1 * abs(self.v_par*math.sin(an))* self.v_par*math.sin(an) / self.m
            elif abs(self.v_par * math.sin(an)) > 5:
                self.acceleration.y += k2 * 10 * self.v_par*math.sin(an) / self.m
            elif abs(self.v_par*math.sin(an)) > 0:
                self.acceleration.y += k2*25 * self.v_par*math.sin(an)/abs(self.v_par*math.sin(an))
            else:
                pass


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
            k1, k2 = get_mu(self)
            turn_body(self) #Поворот тела танка
            self.turn_turret() #Поворот башни танка
            set_acceleration(self, k1, k2) #Расчет ускорений
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

    def reload_left(self):
        self.flpk = 1

    def reload_right(self):
        self.frpk = 1

    def fire_gun(self):
        if self.flpk == 1 and self.time_cooldawn == 0:
            a, b = self.turret_image_start.get_size()
            x = self.center.x + a / 2 * math.cos(self.turret_ang)
            y = self.center.y - a / 2 * math.sin(self.turret_ang)
            bullet = Bullets(self.screen, "bullet", x, y, self.turret_ang, self)
            bullet.add(bullets)
            self.time_cooldawn = self.cooldawn
        self.flpk = 0

          
    def update_cooldawn(self):
        self.time_cooldawn -= 1/FPS
        if self.time_cooldawn <= 0:
            self.time_cooldawn = 0
       
    def meet_with_bullet(self, obj):
        if meet(self, obj):
            if obj.owner != self:
                self.hp -= obj.damage
                obj.kill()
                if self.hp == 0:
                    self.kill()
