from helper import *
from bullets_class import *
from map_maker.tiles import *
from map_maker.tiles import *
from AI import *

bullets = pygame.sprite.Group()
tanks_bots = pygame.sprite.Group()
tanks = pygame.sprite.Group()


def update_image_for_tank(self):
    """
    Меняет исходный размер катинки танка (image_start)
    k: новая ширина танка в размерах тайла (у.е.)
    """

    k = self.width_in_tiles
    a_body, b_body = self.body_image_start.get_size()
    a_turret, b_turret = self.turret_image_start.get_size()

    self.body_image_start = update_image(self.body_image_start, k, k * b_body / a_body)
    self.turret_image_start = update_image(self.turret_image_start, k * a_turret / a_body, k * b_turret / a_body)


def all_dead():
    for bul in bullets:
        bul.kill()
    for tank in tanks:
        tank.kill()
    for tank in tanks_bots:
        tank.kill()


def create_tank_player(x, y, ang, tank_type, ID, screen):
    x = x * a + a / 2
    y = y * a + a / 2

    tank = Tank(x, y, ang, tank_type, ID, screen)
    tank.add(tanks)
    return tank


def create_tank_bot(x, y, ang, tank_type, ID, screen, list_tile, hp):
    x = x * a + a / 2
    y = y * a + a / 2
    tank = Tank(x, y, ang, tank_type, ID, screen)
    tank.hp = hp
    tank.add(tanks)
    tank.add(tanks_bots)
    tank.update_list_tile(list_tile)
    return tank


class Tank(pygame.sprite.Sprite):

    def __init__(self, x, y, angle, tank_type, ID, screen):
        """
        x,y - положение центра танка
        tank_type - тип танка, возможные: "light", "middle", "heavy"
        sreen - экран на котором будет отображаться танк
        """

        pygame.sprite.Sprite.__init__(self)
        self.ID = ID
        self.screen = screen
        self.center = pos(x, y)
        self.velocity = pos(0, 0)
        self.acceleration = pos(0, 0)
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
        self.flag_at = 0
        self.dot = pos(0, 0)
        self.dx = 0
        self.dy = 0
        self.ai = 0
        self.dist = 300
        self.type = tank_type
        self.alive = True
        self.win = False

        if tank_type == "light":
            self.body_image_start = pygame.image.load("textures/light_body.png").convert_alpha()
            self.turret_image_start = pygame.image.load("textures/light_turret(4).png").convert_alpha()
            self.engine_power = 100
            self.ang_speed = 3 * math.pi / 10
            self.m = 0.25
            self.cooldawn = 1
            self.time_cooldawn = 0
            self.hp = 3
            self.ai = 1
            self.k_turret_draw = 0.0
            self.width_in_tiles = 3.5

        elif tank_type == "middle":
            self.body_image_start = pygame.image.load("textures/middle_body.png").convert_alpha()
            self.turret_image_start = pygame.image.load("textures/middle_turret.png").convert_alpha()
            self.engine_power = 80
            self.ang_speed = 2 * math.pi / 10
            self.m = 0.5
            self.cooldawn = 1
            self.time_cooldawn = 0
            self.hp = 4
            self.ai = 2
            self.k_turret_draw = 0.0
            self.width_in_tiles = 3.5

        elif tank_type == "heavy":
            self.body_image_start = pygame.image.load("textures/heavy_body.png").convert_alpha()
            self.turret_image_start = pygame.image.load("textures/heavy_turret.png").convert_alpha()
            self.engine_power = 60
            self.ang_speed = 1.5 * math.pi / 10
            self.m = 1
            self.cooldawn = 1
            self.time_cooldawn = 0
            self.hp = 5
            self.ai = 3
            self.k_turret_draw = 0.3
            self.width_in_tiles = 3.5

        update_image_for_tank(self)

        self.body_image = self.body_image_start
        self.image = self.body_image
        self.turret_image = self.turret_image_start
        update_corner(self)
        update_mask(self)
        self.rect = self.image.get_rect()

        a_body, b_body = self.body_image_start.get_size()
        self.s = b_body * self.k_turret_draw

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

        if tx > self.center_visible.x - self.s * math.cos(self.body_ang):
            self.wanted_turret_ang = -math.atan((ty - self.center_visible.y - self.s * math.sin(self.body_ang)) / (
                    tx - self.center_visible.x + self.s * math.cos(self.body_ang)))
        elif tx < self.center_visible.x - self.s * math.cos(self.body_ang):
            self.wanted_turret_ang = -math.atan((ty - self.center_visible.y - self.s * math.sin(self.body_ang)) / (
                    tx - self.center_visible.x + self.s * math.cos(self.body_ang))) + math.pi
        else:
            self.wanted_turret_ang = convert_ang(self.body_ang)

        if self.wanted_turret_ang < 0:
            self.wanted_turret_ang += 2 * math.pi
        ang = convert_ang(self.turret_ang) - self.wanted_turret_ang
        if ang <= -math.pi:
            ang += 2 * math.pi
        elif ang > math.pi:
            ang -= 2 * math.pi
        if ang < 0:
            self.turret_ang += self.turret_rotate_speed * dt
        elif ang > 0:
            self.turret_ang -= self.turret_rotate_speed * dt

    def move(self, map):
        """
        Отвечает за перемещение и поворот всего танка
        args:
        fw, fa, fs, fd - переменные типа Bool, True если нажата
        кнопка под второй буквой переменной, False если нет
        """
        global dt

        def get_mu(self, map):
            """Возвращает коэффициент трения тайла, находящегося в центре танка"""
            tile = return_tile_ower_pos(self.center.x, self.center.y, map)
            return tile.k1, tile.k2

        def tiles_near(self, map):
            """
            Возвращает группу тайлов, находящихся поблизости танка
            tiles_array[i][j]: i - номер строчки, j - номер столбца
            """
            tiles_n = pygame.sprite.Group()
            x1, y1, x2, y2 = self.corner.x, self.corner.y, 2 * self.center.x - self.corner.x, 2 * self.center.y - self.corner.y
            x1 = max(int(x1) // a - 2, 0)
            x2 = min(int(x2) // a + 2, len(map.tiles_array[0]))
            y1 = max(int(y1) // a - 2, 0)
            y2 = min(int(y2) // a + 2, len(map.tiles_array))
            for i in range(x1, x2):
                for j in range(y1, y2):
                    if j >= 0 and j <= len(map.tiles_array) and i >= 0 and i <= len(map.tiles_array[0]):
                        map.tiles_array[j][i].add(tiles_n)
            return tiles_n

        def check_move_tanks(self):
            """Проверка на то, может ли танк сюда сдвинутся (врезался ли он с танками)"""
            for tank in tanks:
                if tank != self:
                    if meet(self, tank):
                        return False
            return True

        def check_move_tiles(self, map):
            """Эта функция выполняет две задачи:
                1) если танк врезался в bricks, water, stone: возвращает False (ехать нельзя) или True (можно)
                2) если танк попал на финиш, то запускается соответсвующая функция"""

            FLAG = True
            for tile in tiles_near(self, map):
                if tile.type == "bricks" or tile.type == "water" or tile.type == "stone":
                    if meet(self, tile):
                        FLAG = False
                elif tile.type == "finish" and not (self is tanks_bots):
                    if meet(self, tile):
                        self.win = True
            return FLAG

        def check_move(self, map):
            """Проверка на то, может ли танк сюда сдвинутся (врезался ли он с тайлами или танком)"""
            return check_move_tanks(self) and check_move_tiles(self, map)

        def check_turn_turret(self, map):
            """Проверка на то, может ли танк повернуть свою башню"""

            obj = unnamed(self.turret_image, self.corner.x,
                          self.corner.y)  # Создается безымяный класс для проверки пересечения со стенками
            for tile in tiles_near(self, map):
                if tile.type == "bricks":
                    if meet(obj, tile):
                        return False
            return True

        def update_for_check(self):
            """Обновляем предположительно возможное положение танка.
            Нужно для определения того, может ли танк туда попасть или нет"""

            self.body_image = pygame.transform.rotate(self.body_image_start, self.body_ang * 180 / math.pi)
            self.image = self.body_image
            update_corner(self)
            self.rect = self.image.get_rect()
            update_mask(self)  # Обновление маски танка

        def turn_body(self, map):
            body_ang = self.body_ang

            if self.fa == True and self.fd == False:
                self.body_ang += self.ang_speed * dt
                self.turret_ang += self.ang_speed * dt
            elif self.fa == False and self.fd == True:
                self.body_ang -= self.ang_speed * dt
                self.turret_ang -= self.ang_speed * dt

            update_for_check(self)

            if check_move(self, map):
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
            an = self.body_ang  # Угол между горизонтом и направлением танка
            vx = self.velocity.x
            vy = self.velocity.y
            self.turn_turret()  # Поворот башни танка
            v = (vx ** 2 + vy ** 2) ** 0.5

            self.vel_ang = 0  # Угол между вектором скорости и горизонтом
            if vx > 0:
                self.vel_ang = -math.atan(vy / vx)
            elif vx < 0:
                self.vel_ang = -math.atan(vy / vx) + math.pi

            # Ускорение за счёт работы двигателя:
            if self.fw == True and self.fs == False:
                self.acceleration.x = dt ** 2 * self.engine_power * math.cos(an) / self.m
                self.acceleration.y = dt ** 2 * -self.engine_power * math.sin(an) / self.m
            elif self.fw == False and self.fs == True:
                self.acceleration.x = dt ** 2 * -self.engine_power * math.cos(an) / self.m
                self.acceleration.y = dt ** 2 * self.engine_power * math.sin(an) / self.m
            # Ускорение за счёт сопротивления среды:
            if v < 15 * dt:
                v = 15 * dt
            self.v_ort = v * math.sin(self.vel_ang - an)
            self.v_par = v * math.cos(self.vel_ang - an)

            self.acceleration.x -= dt ** 2 * k1 * abs(self.v_par * math.cos(an)) * self.v_par * math.cos(an) / self.m
            self.acceleration.y += dt ** 2 * k1 * abs(self.v_par * math.sin(an)) * self.v_par * math.sin(an) / self.m
            self.acceleration.x -= dt ** 2 * k2 * abs(self.v_ort * math.cos(math.pi / 2 + an)) * self.v_ort * math.cos(
                math.pi / 2 + an) / self.m
            self.acceleration.y += dt ** 2 * k2 * abs(self.v_ort * math.sin(math.pi / 2 + an)) * self.v_ort * math.sin(
                math.pi / 2 + an) / self.m

        def update_options(self, map):
            """Движение танка (обновление координат, скоростей)"""
            self.velocity.x *= dt
            self.velocity.y *= dt

            vx = self.velocity.x
            vy = self.velocity.y
            v = (vx ** 2 + vy ** 2) ** 0.5
            x = self.center.x
            y = self.center.y

            # Обновление скоростей и координат
            if v <= 1 * dt and (self.fw + self.fs) % 2 == 0:
                self.velocity.x = 0
                self.velocity.y = 0
            else:
                self.velocity.x += self.acceleration.x
                self.velocity.y += self.acceleration.y

            self.center.x += self.velocity.x
            self.center.y += self.velocity.y
            self.velocity.x /= dt
            self.velocity.y /= dt

            update_for_check(self)

            if check_move(self, map):
                pass
            else:
                self.center.x = x
                self.center.y = y
                self.velocity.x *= -0.1
                self.velocity.y *= -0.1

                update_for_check(self)

        def main(self, map):
            k1, k2 = get_mu(self, map)
            turn_body(self, map)  # Поворот тела танка
            self.turn_turret()  # Поворот башни танка
            set_acceleration(self, k1, k2)  # Расчет ускорений
            update_options(self, map)  # Движение танка

        if self.hp > 0:
            main(self, map)

    def before_draw(self, observating_point):
        self.center_visible = pos(screen_center.x + self.center.x - observating_point.x,
                                  screen_center.y + self.center.y - observating_point.y)
        self.corner_visible = pos(screen_center.x + self.corner.x - observating_point.x,
                                  screen_center.y + self.corner.y - observating_point.y)

    def draw(self, observating_point, k=1):
        # Рисование тела танка:
        self.body_image = pygame.transform.rotate(self.body_image_start, self.body_ang * 180 / math.pi)
        self.screen.blit(self.body_image, (self.corner_visible.x, self.corner_visible.y))

        # Рисование cooldawn:
        dx = self.center.x - self.corner.x
        dy = self.center.y - self.corner.y
        x = self.center_visible.x + dx
        y = self.center_visible.y + dy
        pygame.draw.arc(self.screen, (0, 0, 0), (x, y, 20, 20), 0, self.time_cooldawn / self.cooldawn * 2 * math.pi,
                        width=6)

        # Рисование жизней:
        sub = pygame.Surface((20, 20), pygame.SRCALPHA)
        dots = ((0, 5), (5, 0), (10, 5), (15, 0), (20, 5), (10, 20))
        pygame.draw.polygon(sub, (255, 0, 0), dots)
        b = self.body_image.get_size()[1]
        for i in range(self.hp):
            self.screen.blit(sub, (self.center_visible.x - 50 + 25 * i, self.center_visible.y - b / 2 - 30))

    def draw_turret(self):
        # Рисование башни танка:
        self.turret_image = pygame.transform.rotate(self.turret_image_start, self.turret_ang * 180 / math.pi)
        a, b = self.turret_image.get_size()

        self.screen.blit(self.turret_image, (self.center_visible.x - a / 2 - self.s * math.cos(self.body_ang),
                                             self.center_visible.y - b / 2 + self.s * math.sin(self.body_ang)))

    def draw_tank_for_constructor(self, observating_point, k):
        self.center_visible = pos(screen_center.x + self.center.x * k - observating_point.x * k,
                                  screen_center.y + self.center.y * k - observating_point.y * k)
        self.corner_visible = pos(screen_center.x + self.corner.x * k - observating_point.x * k,
                                  screen_center.y + self.corner.y * k - observating_point.y * k)

        self.body_image = pygame.transform.rotate(self.body_image_start, self.body_ang * 180 / math.pi)
        a, b = self.body_image.get_size()
        self.body_image = pygame.transform.scale(self.body_image, (a * k, b * k))
        a, b = self.body_image.get_size()
        self.screen.blit(self.body_image, (self.center_visible.x - a / 2, self.center_visible.y - b / 2))
        # hp
        sub = pygame.Surface((20, 20), pygame.SRCALPHA)
        dots = ((0, 5), (5, 0), (10, 5), (15, 0), (20, 5), (10, 20))
        pygame.draw.polygon(sub, (255, 0, 0), dots)
        sub = pygame.transform.scale(sub, (20 * k, 20 * k))
        b = self.body_image.get_size()[1]
        for i in range(self.hp):
            self.screen.blit(sub, (self.center_visible.x - 50 * k + 25 * k * i, self.center_visible.y - b / 2 - 30 * k))
        # turret
        self.turret_image = pygame.transform.rotate(self.turret_image_start, self.turret_ang * 180 / math.pi)
        a, b = self.turret_image.get_size()
        self.turret_image = pygame.transform.scale(self.turret_image, (a * k, b * k))
        a, b = self.turret_image.get_size()
        self.screen.blit(self.turret_image, (self.center_visible.x - a / 2 - self.s * math.cos(self.body_ang),
                                             self.center_visible.y - b / 2 + self.s * math.sin(self.body_ang)))

    def reload_left(self):
        if self.hp > 0:
            self.flpk = 1

    def reload_right(self):
        if self.hp > 0:
            self.frpk = 1

    def fire_gun(self):
        if self.flpk == 1 and self.time_cooldawn == 0:
            a, b = self.turret_image_start.get_size()

            x = self.center.x + a / 2 * math.cos(self.turret_ang) - self.s * math.cos(self.body_ang)
            y = self.center.y - a / 2 * math.sin(self.turret_ang) + self.s * math.sin(self.body_ang)
            bullet = Bullets(self.screen, "bullet", x, y, self.turret_ang, self)
            bullet.add(bullets)
            self.time_cooldawn = self.cooldawn

        self.flpk = 0

    def update_cooldawn(self):
        self.time_cooldawn -= 1 / FPS
        if self.time_cooldawn <= 0:
            self.time_cooldawn = 0

    def dead(self):
        self.body_image_start = pygame.image.load("textures/" + self.type + "_body_crash.png").convert_alpha()
        self.turret_image_start = pygame.image.load("textures/" + self.type + "_turret_crash.png").convert_alpha()
        update_image_for_tank(self)

    def life_before_death(self):
        self.kill()

    def meet_with_bullet(self, obj):
        if meet(self, obj):
            if not (obj.owner is self):
                self.hp -= obj.damage
                obj.kill()
                if self.hp == 0:
                    self.dead()
                if self.hp == -1:
                    self.life_before_death()

    def game_over(self):
        if self.hp <= 0 and self.alive:
            self.alive = False
            return True
        else:
            return False

    def game_win(self):
        if self.win:
            return True
        else:
            return False
