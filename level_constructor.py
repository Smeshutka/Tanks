from helper import *
from tank_class import*
from map_maker.tiles import*
from map_maker.map_input import*
import tkinter
from tkinter.filedialog import *

'''
Этот модуль позволяет создавать карту
управление: wasd - перемещение выделенного тайла
1 - замена выделенного тайла на траву
2 - на воду
3 - на кирпич
4 - на камень
5 - на песок
6 - на лёд
o - вызов диалогового окна для открытия файла карты
p - вызов диалогового окна для сохранения карты в файл, необходимо прописывать расширение .txt
'''
class Button:
    def __init__(self, screen, x0, y0, a, b, text):
        self.screen = screen
        self.size = pos(a,b)
        self.pos = pos(x0,y0)
        self.text = text
    def draw(self):
        pygame.draw.rect(self.screen, (255,255,255), (x0,y0,a,b))
        f = pygame.font.Font(None, 36)
        text = f.render(self.text, 1, (180, 0, 0))
        self.screen.blit(text, (250, 20))
        
class Rotate_button(Button):
    def __init__(self, screen, x0, y0, a, b, inverse):
        self.screen = screen
        self.size = pos(a,b)
        self.pos = pos(x0,y0)
        self.image = pygame.image.load('textures/rotate_icon.png').convert_alpha()
        self.inverse = inverse
        
    def draw(self,k):
        pygame.draw.rect(self.screen, (255,255,255), (self.pos.x,self.pos.y,self.size.x,self.size.y))
        self.screen.blit(update_image(pygame.transform.flip(self.image,self.inverse,False), k, k), (self.pos.x, self.pos.y))
    
    def check_pressed(self):
        mx,my = pygame.mouse.get_pos()
        x0, y0 = self.pos.x, self.pos.y
        a,b = self.size.x, self.size.y
        if mx >= x0 and my >= y0 and mx <= x0+a and my <= y0+b:
            return True
        else: return False
        
    def rotate_map(self, map):
        ar = map.tiles_array
        if self.inverse:
            ar = [[ar[i][j] for i in range(len(ar))] for j in range(len(ar[0])-1,-1,-1)]
        else:
            for k in range(3):
                ar = [[ar[i][j] for i in range(len(ar))] for j in range(len(ar[0])-1,-1,-1)]
        
        for i in range(len(ar)):
            for j in range(len(ar[0])):
                tile = ar[i][j]
                if tile.type == 'stone':
                    ar[i][j] = 'S'
                else:
                    ar[i][j] = tile.type[0]
        return Map(map_maker(ar),self.screen)

class Tiles_menu:
    def __init__(self, screen, w, h, chosen_type = 'stone'):
        self.screen = screen
        self.screen_size = pos(w, h)
        self.k = 5
        self.chosen_type = chosen_type
        self.y0 = 0
        self.all_types = ['grass', 'water', 'bricks', 'stone', 'sand', 'ice']
        
    def create_sur_ttype(self):
        def draw_chosen(self):
            sur = pygame.Surface((a*(self.k-2),a*(self.k-2)), pygame.SRCALPHA)
            pygame.draw.line(sur, (0,0,0), (a*(self.k-2)//2,0), (a*(self.k-2)//2,a*(self.k-2)), a//4)
            pygame.draw.line(sur, (0,0,0), (0,a*(self.k-2)//2), (a*(self.k-2),a*(self.k-2)/2), a//4)
            #pygame.draw.line(sur, (0,0,0), (),(), a/4) 
            return sur
        
        
        sur = pygame.Surface((a*self.k, self.screen_size.y), pygame.SRCALPHA)
        tile = Tile(a, a,'stone',sur)
        
        for ttype in self.all_types:
            tile.update_tile(ttype)
            tile.corner_visible = tile.corner
            tile.draw(self.k-2)
            if ttype == self.chosen_type:
                sur.blit(draw_chosen(self), (tile.corner.x, tile.corner.y))
            tile.corner = pos(tile.corner.x, tile.corner.y+a*(self.k-1))
        return sur
                
    def draw_work_space(self):
        pygame.draw.rect(self.screen, (255,255,255),
                             (self.screen_size.x - a*self.k, 0, a*self.k, self.screen_size.y))
        
    def draw_tiles_type(self):
        self.screen.blit(self.create_sur_ttype(), (self.screen_size.x - a*self.k, self.y0))
        
    def draw(self):   
        self.draw_work_space()
        #рамка рисуется не так как надо
        #pygame.draw.rect(self.screen, (255,255,0),(self.screen_size.x - a*self.k, 0, a*self.k, self.screen_size.y), a)
        self.draw_tiles_type()
        
    def check_pressed(self):
        mx,my = pygame.mouse.get_pos()
        if mx>=self.screen_size.x - a*self.k + a and mx<=self.screen_size.x - a:
            for i in range(len(self.all_types)):
                if my+self.y0<=(self.k-1)*a+a*i*(self.k-1) and my+self.y0>= a+a*i*(self.k-1):
                    return self.all_types[i]
        return ''
        

def draw_chosen(chosen_tile):
    sur = pygame.Surface((a,a), pygame.SRCALPHA)
    pygame.draw.rect(sur, (255,255,255), (a/4,a/4,a/2,a/2))
    
    chosen_tile.corner_visible = pos(screen_center.x + chosen_tile.corner.x - chosen_tile.center.x,
                                  screen_center.y + chosen_tile.corner.y - chosen_tile.center.y)
    chosen_tile.screen.blit(sur,(chosen_tile.corner_visible.x, chosen_tile.corner_visible.y))

def change_pos_chosen(chosen_tile, cx, cy):
    '''cx,cy - на сколько тайлов переместить по x,y. Может быть -1,0,1'''
    chosen_tile.corner.x += cx*a
    chosen_tile.corner.y += cy*a
    chosen_tile.center = pos(chosen_tile.corner.x+a//2, chosen_tile.corner.y+a//2)
    chosen_tile.map_pos = pos(chosen_tile.corner.x//a, chosen_tile.corner.y//a)

def change_chosen_type(chosen_tile, tile, new_type,menu):
    tile.update_tile(new_type)
    #chosen_tile.type = new_type
    menu.chosen_type = new_type
    
def calculate_map_pressed(map):
    mx,my = pygame.mouse.get_pos()
    map_b = len(map.tiles_array)
    map_a = len(map.tiles_array[0])
    ma = (mx - map.tiles_array[0][0].corner_visible.x)//a
    mb = (my - map.tiles_array[0][0].corner_visible.y)//a
    if ma< map_a and ma>=0 and mb< map_b and mb>=0:
        return ma, mb
    else: return -1, -1

def draw_highlighting(ma_start, mb_start, screen,map):
    mx,my = pygame.mouse.get_pos()
    x0,y0 = map.tiles_array[mb_start][ma_start].corner_visible.x + a//2, map.tiles_array[mb_start][ma_start].corner_visible.y + a//2
    if mx < x0:
        mx, x0 = x0, mx
    if my < y0:
        my, y0 = y0, my
    pygame.draw.rect(screen, (0,0,0), (x0,y0,mx-x0,my-y0), 2)

def open_map():
    #global lt, tiles_array, map
    
    root = tkinter.Tk()
    
    new_map = askopenfilename(filetypes=(("Text file", ".txt"),))
    root.destroy()
    chosen_tile = Tile(a*0,a*0,"stone",screen)
    map = Map(file_reader(new_map), screen)
    return map
    
def save_map():
    root = tkinter.Tk()
    file = asksaveasfilename(filetypes=(("Text file", ".txt"),))
    root.destroy()
    with open(file, 'w') as file:
        for i in range(len(map.tiles_array)):
            for j in range(len(map.tiles_array[0])):
                tile = map.tiles_array[i][j]
                if tile.type == 'stone':
                    text = 'S'
                else:
                    text = tile.type[0]
                file.write(text)
            file.write('\n')
    
    
pygame.init()
screen = pygame.display.set_mode((w, h))
clock = pygame.time.Clock()

finished = False
mouse_pressed = False


#lt = list of tiles
lt = []
for i in range(10):
    lt.append([])
    for j in range(10):
        lt[i].append('g')
        
map = Map(map_maker(lt), screen)
chosen_tile = Tile(a*0,a*0,"stone",screen)

menu = Tiles_menu(screen, w,h)
rotate_clockwise_button = Rotate_button(screen, w-a*menu.k-a*2, 0, a*2, a*2, False)
rotate_counterclockwise_button = Rotate_button(screen, w-a*menu.k-a*4, 0, a*2, a*2, True)

while not finished:
    screen.fill((0,0,0))
    map.draw(chosen_tile.center)
    draw_chosen(chosen_tile)
    menu.draw()
    if mouse_pressed:
        draw_highlighting(ma_start, mb_start, screen,map)
    rotate_clockwise_button.draw(2)
    rotate_counterclockwise_button.draw(2)
    pygame.display.update()
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w or event.key == pygame.K_UP:
                change_pos_chosen(chosen_tile, 0, -1)
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                change_pos_chosen(chosen_tile, -1, 0)
            if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                change_pos_chosen(chosen_tile, 0, 1)
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                change_pos_chosen(chosen_tile, 1, 0)
            if event.key == pygame.K_1:
                change_chosen_type(chosen_tile, map.tiles_array[chosen_tile.map_pos.y][chosen_tile.map_pos.x], 'grass',menu)
            if event.key == pygame.K_2:
                change_chosen_type(chosen_tile, map.tiles_array[chosen_tile.map_pos.y][chosen_tile.map_pos.x], 'water',menu)
            if event.key == pygame.K_3:
                change_chosen_type(chosen_tile, map.tiles_array[chosen_tile.map_pos.y][chosen_tile.map_pos.x], 'bricks',menu)
            if event.key == pygame.K_4:
                change_chosen_type(chosen_tile, map.tiles_array[chosen_tile.map_pos.y][chosen_tile.map_pos.x], 'stone',menu)
            if event.key == pygame.K_5:
                change_chosen_type(chosen_tile, map.tiles_array[chosen_tile.map_pos.y][chosen_tile.map_pos.x], 'sand',menu)
            if event.key == pygame.K_6:
                change_chosen_type(chosen_tile, map.tiles_array[chosen_tile.map_pos.y][chosen_tile.map_pos.x], 'ice',menu)
            
            if event.key == pygame.K_p:
                save_map()
            if event.key == pygame.K_o:
                map = open_map()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if menu.check_pressed()!= '':
                    menu.chosen_type = menu.check_pressed()
                elif rotate_clockwise_button.check_pressed():
                    map = rotate_clockwise_button.rotate_map(map)
                elif rotate_counterclockwise_button.check_pressed():
                    map = rotate_counterclockwise_button.rotate_map(map)
                else:
                    ma_start,mb_start = calculate_map_pressed(map)
                    if ma_start!=-1 and mb_start!=-1:
                        mouse_pressed = True
                        
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if mouse_pressed:
                    mouse_pressed = False
                    ma_end, mb_end = calculate_map_pressed(map)
                    if ma_end != -1 and mb_end != -1:
                        mb_end += 1
                        ma_end += 1
                        for i in range(abs(mb_end-mb_start)):
                            for j in range(abs(ma_end-ma_start)):
                                if ma_end < ma_start:
                                    ma_end, ma_start = ma_start, ma_end
                                if mb_end < mb_start:
                                    mb_end, mb_start = mb_start, mb_end
                                map.tiles_array[mb_start+i][ma_start+j].update_tile(menu.chosen_type)
                    
                    
