import os
import random
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..\..')))
from Tanks.helper import *
from Tanks.constans import *


def map_maker(map):
    """
    Параметры:
    map: карта, в ячейках которых тайлы-буквы: g, w, b, S, s, i, F
    
    Возвращает:
    map: карта, в ячейках которых лежит: map[row][col] = [a * col, a * row, name_tile]
    """
    
    for row in range(len(map)):
        for col in range(len(map[row])):
            list = [a * col, a * row]
            name_tile = None
            
            if map[row][col] == 'g':
                name_tile = 'grass'
            elif map[row][col] == 'w':
                name_tile = 'water'
            elif map[row][col] == 'b':
                name_tile = 'bricks'
            elif map[row][col] == 'S':
                name_tile = 'stone'
            elif map[row][col] == 's':
                name_tile = 'sand'
            elif map[row][col] == 'i':
                name_tile = 'ice'
            elif map[row][col] == 'F':
               name_tile = 'finish'
            if name_tile != None:
                list.append(name_tile)
            else:
                list = map[row][col]
                
            map[row][col] = list
            
    return map


def file_reader(input_filename):
    """Cчитывает данные о карте из файла

    Параметры:
    **input_filename** — имя входного файла

    Возвращает:
    map, в ячейках которых лежит:
        map[row][col] = name_tile: вид тайла, состоящий из одной буквы
    """

    map = []

    with open(input_filename) as input_file:
        for line in input_file:
            line_tiles = []
            for line_1 in line.split():
                for char in line_1:
                    line_tiles.append(char)
            map.append(line_tiles.copy())
            
    return map


def file_reader_level(input_filename):
    """Cчитывает данные об УРОВНЕ из файла

    Параметры:
    **input_filename** — имя входного файла

    Возвращает: [map, tanks_bots_list, tank_player]
    
    map: карта, в ячейках которых лежит: map[row][col] = [a * col, a * row, name_tile]
    
    tanks_bots_list: список, элементами которого являются:
        [tank.x, tank.y, tank.ang, tank.type, tank.ID, tank.list_tile, tank.hp]
    tank_player (игрок):
        [tank_player.x, tank_player.y, tank_player.body_ang, ID]
    
    """

    map = []
    tanks_bots_list = []
    tanks_player = []
    
    flag = 'map'
    with open(input_filename) as input_file:
        for line in input_file:
            if line[0:10] == 'tanks_bots':
                flag = 'tanks_bots'
            elif line[0:11] == 'tank_player':
                flag = 'tank_player'
            elif flag == 'map':
                line_tiles = []
                for line_1 in line.split():
                    for char in line_1:
                        line_tiles.append(char)
                map.append(line_tiles.copy())
            elif flag == 'tanks_bots':
                list = eval(line)
                list_tile = list[5]
                for i in range(len(list_tile)):
                    list_tile[i] = pos(list_tile[i][0], list_tile[i][1])
                list[5] = list_tile
                tanks_bots_list.append(list) #list = [tank.x, tank.y, tank.ang, tank.type, tank.ID, tank.list_tile, tank.hp]
            elif flag == 'tank_player':
                tank_player = eval(line) #list = [tank_player.x, tank_player.y, tank_player.body_ang, ID]
                tanks_player.append(tank_player)
                
    return [map_maker(map), tanks_bots_list, tanks_player]


# "map_maker/templates/ice and ground/"
# "map_maker/templates/test/"

def key_maker():
    """
    По шаблонам 10*10 генерирует ключ-соответсвие: двумерный массив
    key[map1][map2] = [up, down, left, right],
    можно ли сверху, снизу, слева, справа относительно map1 поставить map2.
    Данный ключ записывается в файл key.txt
    
    par: число тайлов, которые могут не состыковаться
    """
    par = 4
    key = []
    path = "map_maker/templates/ice and ground/"
    files = os.listdir(path=path)
    
    for i_file in range(len(files)):
        list = []
        file1 = str(i_file)
        map1 = file_reader(path + file1 + '.txt')
        for j_file in range(len(files)):
            file2 = str(j_file)
            map2 = file_reader(path + file2 + '.txt')
            
            up = 0
            for col in range(10):
                if map1[0][col] != map2[9][col]:
                    up += 1
            if up <= par:
                up = True
            else:
                up = False

            down = 0
            for col in range(10):
                if map1[9][col] != map2[0][col]:
                    down += 1
            if down <= par:
                down = True
            else:
                down = False

            left = 0
            for row in range(10):
                if map1[row][0] != map2[row][9]:
                    left += 1
            if left <= par:
                left = True
            else:
                left = False

            right = 0
            for row in range(10):
                if map1[row][9] != map2[row][0]:
                    right += 1
            if right <= par:
                right = True
            else:
                right = False
                
            list_n =  [up, down, left, right]
            list.append(list_n)
        key.append(list)

    with open('map_maker/templates/key.txt', 'w') as file:
        for i in range(len(key)):
            for j in range(len(key[0])):
                file.write(str(key[i][j]) + '. ')
            file.write('\n')


def key_reader():
    """
    Считывает файл key.txt, в котором лежит ключ.
    
    Возвращает двумерный массив, в котором:
    key[map1][map2] = {'up':bool, 'down':bool, 'left':bool, 'right':bool}:
    можно ли сверху, снизу, слева, справа от map1 поставить map2
    """
    
    key = []

    with open('map_maker/templates/key.txt', 'r') as input_file:
        for line in input_file:
            line_key = []
            for line_1 in line.split('. '):
                if line_1 != '\n':
                    line1 = eval(line_1)
                    dict =  {'up':False, 'down':False, 'left':False, 'right':False}
                    dict['up'] = line1[0]
                    dict['down'] = line1[1]
                    dict['left'] = line1[2]
                    dict['right'] = line1[3]
                    
                    line_key.append(dict)
            
            key.append(line_key)
    return key


def get_complimentary(row, key, direction):
    """
    Принимаются:
    row: строчка, соответсвующая данному шаблону (шаблон №row)
    key: ключ, соответсвующий данному набору шаблонов
    direction: направление
    
    По ключу key возвращает список шаблонов, которые
    могут контактироваться с данным по направлению direction
    """
    
    comp_list = []
    for col in range(len(key[row])):
        if key[row][col][direction]:
            comp_list.append(col)

    return comp_list


def jigsaw_generator(key, scale_y, scale_x):
    """
    Параметры:
    key: ключ, необходим для генерации
    scale_x: число столбцов (размер по оси икс)
    scale_y: число строк (размер по оси игрек)
    
    Возвращает:
    map: карта, но в ячейках лежат не тайлы, а шаблоны
    map[row][col]: номер шаблона, который тут будет находиться
    """
    
    map = [[0 for col in range(scale_x)] for row in range(scale_y)]
    map[0][0] = random.randint(0, len(key) - 1)
    for col in range(1, len(map[0])):
        map[0][col] = random.choice(get_complimentary(map[0][col - 1], key, 'right'))
        
    for row in range(1, len(map)):
        map[row][0] = random.choice(get_complimentary(map[row - 1][0], key, 'down'))
        for col in range(1, len(map[row])):
            map_a = get_complimentary(map[row - 1][col], key, 'down')
            map_b = get_complimentary(map[row][col - 1], key, 'right')
            map_c = []
            for first in map_a:
                for second in map_b:
                    if first == second:
                        map_c.append(first)
                        break
            map[row][col] = random.choice(map_c)

    return map


def map_from_jigsaw(scheme):
    """
    Принимает:
    scheme: схема расставления шаблонов
    
    Возвращает:
    map: готовую карту по этим шаблонам
    """
    
    map = [[0 for i in range(10 * len(scheme[0]) + 2)] for j in range(10 * len(scheme) + 2)]
    for i in range(len(scheme)):
        for j in range(len(scheme[i])):
            puzzle = file_reader('map_maker/templates/ice and ground/' + str(scheme[i][j]) + '.txt')

            for i_1 in range(len(puzzle)):
                for j_1 in range(len(puzzle[i_1])):
                    if puzzle[i_1][j_1] == 'g':
                        map[10 * i + i_1 + 1][10 * j + j_1 + 1] = (
                        [a * (10 * j + j_1 + 1), a * (10 * i + i_1 + 1), 'grass'])
                    elif puzzle[i_1][j_1] == 'w':
                        map[10 * i + i_1 + 1][10 * j + j_1 + 1] = (
                        [a * (10 * j + j_1 + 1), a * (10 * i + i_1 + 1), 'water'])
                    elif puzzle[i_1][j_1] == 'b':
                        map[10 * i + i_1 + 1][10 * j + j_1 + 1] = (
                        [a * (10 * j + j_1 + 1), a * (10 * i + i_1 + 1), 'bricks'])
                    elif puzzle[i_1][j_1] == 'S':
                        map[10 * i + i_1 + 1][10 * j + j_1 + 1] = (
                        [a * (10 * j + j_1 + 1), a * (10 * i + i_1 + 1), 'stone'])
                    elif puzzle[i_1][j_1] == 's':
                        map[10 * i + i_1 + 1][10 * j + j_1 + 1] = (
                        [a * (10 * j + j_1 + 1), a * (10 * i + i_1 + 1), 'sand'])
                    elif puzzle[i_1][j_1] == 'i':
                        map[10 * i + i_1 + 1][10 * j + j_1 + 1] = (
                        [a * (10 * j + j_1 + 1), a * (10 * i + i_1 + 1), 'ice'])

    for i in range(10 * len(scheme[0]) + 2):
        map[0][i] = ([a * i, a * 0, 'stone'])
        map[10 * len(scheme) + 1][i] = ([a * i, a * (10 * len(scheme) + 1), 'stone'])
    for i in range(10 * len(scheme)):
        map[i + 1][0] = ([a * 0, a * (i + 1), 'stone'])
        map[i + 1][10 * len(scheme[0]) + 1] = ([a * (10 * len(scheme[0]) + 1), a * (i + 1), 'stone'])

    return map_maker(map)
