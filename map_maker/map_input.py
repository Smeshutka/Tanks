import os
import random
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..\..')))
from Tanks.helper import *
from Tanks.constans import *


def map_maker(map):
    for i in range(len(map)):
        for j in range(len(map[i])):
            if map[i][j] == 'g':
                map[i][j] = ([a * j, a * i, 'grass'])
            elif map[i][j] == 'w':
                map[i][j] = ([a * j, a * i, 'water'])
            elif map[i][j] == 'b':
                map[i][j] = ([a * j, a * i, 'bricks'])
            elif map[i][j] == 'S':
                map[i][j] = ([a * j, a * i, 'stone'])
            elif map[i][j] == 's':
                map[i][j] = ([a * j, a * i, 'sand'])
            elif map[i][j] == 'i':
                map[i][j] = ([a * j, a * i, 'ice'])

    return map


def file_reader(input_filename):
    """Cчитывает данные о карте из файла

    Параметры:

    **input_filename** — имя входного файла

    Возвращает:
    (screen_width, screen_height, tiles)
    **screen_width** — необходимая ширина экрана
    **screen_height** — необходимая высота экрана
    **screen_height** — кортеж с элементами вида
        (координата левого верхнего угла по x, координата левого верхнего угла по y, название файла с изображением)
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


# "map_maker/templates/ice and ground/"
# "map_maker/templates/test/"

def key_maker():
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
            par = 4
            up = 0
            for i in range(10):
                if map1[0][i] != map2[9][i]:
                    up += 1
            if up <= par:
                up = True
            else:
                up = False


            down = 0
            for i in range(10):
                if map1[9][i] != map2[0][i]:
                    down +=1
            if down <= par:
                down = True
            else:
                down = False


            left = 0
            for i in range(10):
                if map1[i][0] != map2[i][9]:
                    left += 1
            if left <= par:
                left = True
            else:
                left = False


            right = 0
            for i in range(10):
                if map1[i][9] != map2[i][0]:
                    right += 1
            if right <= par:
                right = True
            else:
                right = False

            list.append([up, down, left, right])

        key.append(list)

    with open('map_maker/templates/key.txt', 'w') as file:
        for i in range(len(key)):
            for j in range(len(key[0])):
                file.write(str(key[i][j]) + '. ')
            file.write('\n')


def key_reader():
    key = []

    with open('map_maker/templates/key.txt', 'r') as input_file:
        for line in input_file:
            line_key = []
            for line_1 in line.split('. '):
                if line_1 != '\n':
                    line_key.append(eval(line_1))
            key.append(line_key.copy())

    return key


def get_complimentary(i, key, direction):
    comp_list = []
    for j in range(len(key[i])):
        if key[i][j][direction]:
            comp_list.append(j)

    return comp_list


def jigsaw_generator(key):
    scale = 7
    map = [[0 for i in range(scale)] for j in range(scale)]
    map[0][0] = random.randint(0, len(key) - 1)
    for j in range(1, len(map[0])):
        map[0][j] = random.choice(get_complimentary(map[0][j - 1], key, 3))
    for i in range(1, len(map)):
        map[i][0] = random.choice(get_complimentary(map[i - 1][0], key, 1))
        for j in range(1, len(map[i])):
            map_a = get_complimentary(map[i - 1][j], key, 1)
            map_b = get_complimentary(map[i][j - 1], key, 3)
            map_c = []
            for first in map_a:
                for second in map_b:
                    if first == second:
                        map_c.append(first)
                        break
            map[i][j] = random.choice(map_c)


    return map


def map_from_jigsaw(scheme):
    map = [[0 for i in range(10 * len(scheme) + 2)] for j in range(10 * len(scheme[0]) + 2)]
    for i in range(len(scheme)):
        for j in range(len(scheme[i])):
            puzzle = file_reader('map_maker/templates/ice and ground/' + str(scheme[i][j]) + '.txt')

            for i_1 in range(len(puzzle)):
                for j_1 in range(len(puzzle[i_1])):
                    if puzzle[i_1][j_1] == 'g':
                        map[10 * i + i_1 + 1][10 * j + j_1 + 1] = ([a * (10 * j + j_1 + 1), a * (10 * i + i_1 + 1), 'grass'])
                    elif puzzle[i_1][j_1] == 'w':
                        map[10 * i + i_1 + 1][10 * j + j_1 + 1] = ([a * (10 * j + j_1 + 1), a * (10 * i + i_1 + 1), 'water'])
                    elif puzzle[i_1][j_1] == 'b':
                        map[10 * i + i_1 + 1][10 * j + j_1 + 1] = ([a * (10 * j + j_1 + 1), a * (10 * i + i_1 + 1), 'bricks'])
                    elif puzzle[i_1][j_1] == 'S':
                        map[10 * i + i_1 + 1][10 * j + j_1 + 1] = ([a * (10 * j + j_1 + 1), a * (10 * i + i_1 + 1), 'stone'])
                    elif puzzle[i_1][j_1] == 's':
                        map[10 * i + i_1 + 1][10 * j + j_1 + 1] = ([a * (10 * j + j_1 + 1), a * (10 * i + i_1 + 1), 'sand'])
                    elif puzzle[i_1][j_1] == 'i':
                        map[10 * i + i_1 + 1][10 * j + j_1 + 1] = ([a * (10 * j + j_1 + 1), a * (10 * i + i_1 + 1), 'ice'])

    for i in range(10 * len(scheme) + 2):
        map[0][i] = ([a * i, a * 0, 'stone'])
        map[10 * len(scheme[0]) + 1][i] = ([a * i, a * (10 * len(scheme[0]) + 1), 'stone'])
    for i in range(10 * len(scheme)):
        map[i+1][0] = ([a * 0, a * (i+1), 'stone'])
        map[i + 1][10 * len(scheme) + 1] = ([a * (10 * len(scheme) + 1), a * (i + 1), 'stone'])

    return map_maker(map)
