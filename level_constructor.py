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
def draw_chosen(chosen_tile, screen_center):
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

def change_chosen_type(chosen_tile, tile, new_type):
    tile.update_tile(new_type)
    
def open_map():
    
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
w, h, = 600, 600
screen = pygame.display.set_mode((w, h))
screen_center = pos(w//2, h//2)
clock = pygame.time.Clock()

finished = False
changes = False

#lt = list of tiles
lt = []
for i in range(10):
    lt.append([])
    for j in range(10):
        lt[i].append('g')
        
map = Map(map_maker(lt), screen)
chosen_tile = Tile(a*0,a*0,"stone",screen)

while not finished:
    screen.fill((0,0,0))
    map.draw(screen_center, chosen_tile)
    draw_chosen(chosen_tile,screen_center)
    pygame.display.update()
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                change_pos_chosen(chosen_tile, 0, -1)
            if event.key == pygame.K_a:
                change_pos_chosen(chosen_tile, -1, 0)
            if event.key == pygame.K_s:
                change_pos_chosen(chosen_tile, 0, 1)
            if event.key == pygame.K_d:
                change_pos_chosen(chosen_tile, 1, 0)
            if event.key == pygame.K_1:
                change_chosen_type(chosen_tile, map.tiles_array[chosen_tile.map_pos.y][chosen_tile.map_pos.x], 'grass')
            if event.key == pygame.K_2:
                change_chosen_type(chosen_tile, map.tiles_array[chosen_tile.map_pos.y][chosen_tile.map_pos.x], 'water')
            if event.key == pygame.K_3:
                change_chosen_type(chosen_tile, map.tiles_array[chosen_tile.map_pos.y][chosen_tile.map_pos.x], 'bricks')
            if event.key == pygame.K_4:
                change_chosen_type(chosen_tile, map.tiles_array[chosen_tile.map_pos.y][chosen_tile.map_pos.x], 'stone')
            if event.key == pygame.K_5:
                change_chosen_type(chosen_tile, map.tiles_array[chosen_tile.map_pos.y][chosen_tile.map_pos.x], 'sand')
            if event.key == pygame.K_6:
                change_chosen_type(chosen_tile, map.tiles_array[chosen_tile.map_pos.y][chosen_tile.map_pos.x], 'ice')
            
            if event.key == pygame.K_p:
                save_map()
            if event.key == pygame.K_o:
                map = open_map()
        
pygame.quit()
