from helper import *
from tank_class import *
from map_maker.tiles import *
from map_maker.map_input import *
from win_for_change_size import *
import tkinter
from tkinter.filedialog import *


class Button:
    '''класс кнопок'''

    def __init__(self, screen, x0, y0, a, b, image):
        '''screen: pygame.display
        x0,y0 - координаты левого верхнего угла относительно экрана
        a,b - размеры окна по x,y соотв.
        image - название файла в папке textures формата png'''
        self.screen = screen
        self.size = pos(a, b)
        self.pos = pos(x0, y0)
        self.image = pygame.image.load('textures/' + image + '.png').convert_alpha()

    def draw(self, k):
        x0, y0 = self.pos.x, self.pos.y
        a, b = self.size.x, self.size.y
        pygame.draw.rect(self.screen, (255, 255, 255), (x0, y0, a, b))
        self.screen.blit(update_image(self.image, k, k), (self.pos.x, self.pos.y))

    def check_pressed(self):
        mx, my = pygame.mouse.get_pos()
        x0, y0 = self.pos.x, self.pos.y
        a, b = self.size.x, self.size.y
        if mx >= x0 and my >= y0 and mx <= x0 + a and my <= y0 + b:
            return True
        else:
            return False


class Rotate_button(Button):
    '''класс кнопок для поворота карты при редактировании'''

    def __init__(self, screen, x0, y0, a, b, image, inverse):
        Button.__init__(self, screen, x0, y0, a, b, image)
        self.inverse = inverse

    def draw(self, k):
        pygame.draw.rect(self.screen, (255, 255, 255), (self.pos.x, self.pos.y, self.size.x, self.size.y))
        self.screen.blit(update_image(pygame.transform.flip(self.image, self.inverse, False), k, k),
                         (self.pos.x, self.pos.y))

    def rotate_map(self, map):
        ar = map.tiles_array
        if self.inverse:
            ar = [[ar[i][j] for i in range(len(ar))] for j in range(len(ar[0]) - 1, -1, -1)]
        else:
            for k in range(3):
                ar = [[ar[i][j] for i in range(len(ar))] for j in range(len(ar[0]) - 1, -1, -1)]

        for i in range(len(ar)):
            for j in range(len(ar[0])):
                tile = ar[i][j]
                if tile.type == 'stone':
                    ar[i][j] = 'S'
                else:
                    ar[i][j] = tile.type[0]
        return Map(map_maker(ar), self.screen)


class SaveLoad_Button(Button):
    '''класс кнопок для сохранения или загрузки карт,
    fast_save - функция для сохранения без диалогового окна внуть папки map_maker/templates
    была создана для облегчения создания шаблонов'''

    def load_map(self):
        try:
            # global lt, tiles_array, map
            root = tkinter.Tk()
            new_map = askopenfilename(filetypes=(("Text file", ".txt"),))
            root.destroy()
            if new_map != '':
                chosen_tile = Tile(a * 0, a * 0, "stone", screen)
                map = Map(map_maker(file_reader(new_map)), screen)
                return map
            else:
                return ''

        except tkinter.TclError:
            print('не закрывайте крестиком окно tkinter-а, пожалуйста')
            return ''
        
    def save_map(self, map, tanks_bots):
        """
        map: карта
        
        tanks_bots: группа танков-ботов, в которых обяательно должна иметь:
        tank.list_tile: траектория движения танка (список пар [a,b])
        tank.hp: число жизней
        tank.type: тип танка ('light', 'middle', 'heavy')
        tank.x: координата по оси икс в единицах размера тайла
        tank.y: координата по оси игрек в единицах размера тайла
        tank.ang: начальный угол поворота танка
        
        Возвращает: file
        Стандартным способом кодирует карту,
        затем идет строчка с кодовым словом 'tanks_bots'
        затем в последующих строчках в следующем формате записывается информация:
        [tank.x, tank.y, tank.ang, tank.type, tank.ID, tank.list_tile, tank.hp]
        """
        try:
            root = tkinter.Tk()
            file = asksaveasfilename(filetypes=(("Text file", ".txt"),))
            root.destroy()
            if file != '':
                with open(file, 'w') as file:
                    for i in range(len(map.tiles_array)):
                            for j in range(len(map.tiles_array[0])):
                                tile = map.tiles_array[i][j]
                                if tile.type == 'stone':
                                    text = 'S'
                                elif tile.type == 'finish':
                                    text = 'F'
                                else:
                                    text = tile.type[0]
                                file.write(text)
                            file.write('\n')
                            
                    file.write('tanks_bots\n')
                    
                    ID = 0
                    for tank in tanks_bots:
                        list = [tank.x, tank.y, tank.body_ang, tank.type, str(ID), tank.list_tile, tank.hp]
                        file.write(str(list))
                        file.write('\n')
                        ID += 1
                        
                    
        except tkinter.TclError:
            print('не закрывайте крестиком окно tkinter-а, пожалуйста')

    def fast_save(self, n, map):
        name = 'map_maker/templates/' + str(n) + '.txt'
        file = open(name, 'w')
        for i in range(len(map.tiles_array)):
            for j in range(len(map.tiles_array[0])):
                tile = map.tiles_array[i][j]
                if tile.type == 'stone':
                    text = 'S'
                else:
                    text = tile.type[0]
                file.write(text)
            file.write('\n')
        file.close()


class Change_size_button(Button):
    def call_tk(self):
        create_dialog_window()

    def read_new_size(self):
        self.call_tk()
        file = open('new_size.txt', 'r')
        data = file.read()
        file.close()
        if data != '':
            return data.split()[0], data.split()[1]

    def change_map_size(self, map, screen):
        a, b = self.read_new_size()
        a, b = int(a), int(b)
        if b > 0 and a > 0:
            lt = []
            for i in range(b):
                lt.append([])
                for j in range(a):
                    lt[i].append('g')
            return Map(map_maker(lt), screen)
        else:
            return ''


class Generate_button(Button):
    def call_tk(self):
        create_dialog_window_for_generator()

    def read_new_size(self):
        self.call_tk()
        file = open('new_size.txt', 'r')
        data = file.read()
        file.close()
        if data != '':
            return data.split()[0], data.split()[1]

    def generate(self):
        a, b = self.read_new_size()
        a, b = int(a), int(b)
        if b > 0 and a > 0:
            lt = []
            for i in range(b):
                lt.append([])
                for j in range(a):
                    lt[i].append('g')
            return Map((map_from_jigsaw(jigsaw_generator(key_reader(), a, b))), screen)
        else:
            return ''


class Change_menu_mode_button(Button):
    def change_mode(self, menu):
        for i in range(len(menu.all_modes)):
            if menu.mode == menu.all_modes[i]:
                menu.mode = menu.all_modes[i - 1]
                break
        if menu.mode == 'tiles':
            menu.chosen_type = 'grass'
        elif menu.mode == 'tanks':
            menu.chosen_type = 'light'

class HP_button(Button):
    def __init__(self, screen, x0, y0, a, b, image, plus):
        Button.__init__(self, screen, x0, y0, a, b, image)
        self.plus = plus
    
    def change_tank_hp(self, menu):
        if self.plus:
            menu.tank_hp += 1
        else:
            menu.tank_hp -= 1

class Tiles_menu:
    '''Меню на котором отображаются все имеющиеся виды тайлов слева,
    хранит выбранный тип тайлов, и визуально отмечает его'''

    def __init__(self, screen, w, h, chosen_type='stone'):
        self.screen = screen
        self.screen_size = pos(w, h)
        self.k = 5
        self.chosen_type = chosen_type
        self.y0 = 0
        self.all_modes = ['tiles', 'tanks']
        self.mode = 'tiles'
        self.tile_types = ['grass', 'water', 'bricks', 'stone', 'sand', 'ice', 'finish']
        self.tank_types = ['light', 'middle', 'heavy']
        self.tank_y = []
        self.tank_hp = 3

    def create_sur_tiles_type(self):
        def draw_chosen(self):
            sur = pygame.Surface((a * (self.k - 2), a * (self.k - 2)), pygame.SRCALPHA)
            pygame.draw.line(sur, (0, 0, 0), (a * (self.k - 2) // 2, 0), (a * (self.k - 2) // 2, a * (self.k - 2)),
                             a // 4)
            pygame.draw.line(sur, (0, 0, 0), (0, a * (self.k - 2) // 2), (a * (self.k - 2), a * (self.k - 2) / 2),
                             a // 4)
            # pygame.draw.line(sur, (0,0,0), (),(), a/4)
            return sur

        sur = pygame.Surface((a * self.k, self.screen_size.y), pygame.SRCALPHA)
        tile = Tile(a, a, 'stone', sur)

        for ttype in self.tile_types:
            tile.update_tile(ttype)
            tile.corner_visible = tile.corner
            tile.draw(self.k - 2)
            if ttype == self.chosen_type:
                sur.blit(draw_chosen(self), (tile.corner.x, tile.corner.y))
            tile.corner = pos(tile.corner.x, tile.corner.y + a * (self.k - 1))
        return sur

    def create_sur_tanks_type(self):
        l = a * self.k - a
        sur = pygame.Surface((a * self.k, self.screen_size.y), pygame.SRCALPHA)
        tank_chosen = ["textures/buttons/tank_light_selected.png", "textures/buttons/tank_middle_selected.png",
                       "textures/buttons/tank_heavy_selected.png"]
        c = a
        for tank_type in self.tank_types:
            if self.chosen_type == tank_type:
                path = "textures/buttons/tank_" + tank_type + "_selected.png"
            else:
                path = "textures/buttons/tank_" + tank_type + ".png"
            image = pygame.image.load(path).convert_alpha()
            a_image, b_image = image.get_size()
            a_needed = int(l - a)
            image = pygame.transform.scale(image, (a_needed, int(b_image * a_needed / a_image)))
            sur.blit(image, (a, c))
            self.tank_y.append(c)
            c += b_image * a_needed / a_image + a
        self.tank_y.append(c)
        return sur

    def draw_work_space(self):
        pygame.draw.rect(self.screen, (255, 255, 255),
                         (self.screen_size.x - a * self.k, 0, a * self.k, self.screen_size.y))

    def draw_tiles_type(self):
        self.screen.blit(self.create_sur_tiles_type(), (self.screen_size.x - a * self.k, self.y0))

    def draw_tanks_type(self):
        self.screen.blit(self.create_sur_tanks_type(), (self.screen_size.x - a * self.k, self.y0))

    def draw_tank_hp(self):
        sub = pygame.Surface((a, a), pygame.SRCALPHA)
        dots = ((0, a/4), (a/4, 0), (a/2, a/4), (a*3/4, 0), (a, a/4), (a/2, a))
        pygame.draw.polygon(sub, (255, 0, 0), dots)
        for i in range(self.tank_hp):
            c = i // self.k
            b = i % self.k
            self.screen.blit(sub, (w - a*self.k + a * b, h - 3*a - c*a - 5))
    
    def draw(self):
        self.draw_work_space()
        # рамка рисуется не так как надо
        # pygame.draw.rect(self.screen, (255,255,0),(self.screen_size.x - a*self.k, 0, a*self.k, self.screen_size.y), a)
        if self.mode == 'tiles':
            self.draw_tiles_type()
        elif self.mode == 'tanks':
            self.draw_tanks_type()
            self.draw_tank_hp()

    def check_pressed(self):
        mx, my = pygame.mouse.get_pos()
        if mx >= self.screen_size.x - a * self.k + a and mx <= self.screen_size.x - a:
            if self.mode == 'tiles':
                for i in range(len(self.tile_types)):
                    if my + self.y0 <= (self.k - 1) * a + a * i * (self.k - 1) and my + self.y0 >= a + a * i * (
                            self.k - 1):
                        return self.tile_types[i]
            elif self.mode == 'tanks':
                for i in range(len(self.tank_types)):
                    if my >= self.tank_y[i] and my <= self.tank_y[i + 1] - a:
                        return self.tank_types[i]
        return ''
