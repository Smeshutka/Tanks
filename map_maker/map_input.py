import random

def map_maker(map):
    screen_width = 20 * len(map[0])
    screen_height = 20 * len(map)
    tiles = []

    for i in range(len(map)):
        for j in range(len(map[i])):
            if map[i][j] == 'g':
                tiles.append([20 * j, 20 * i, 'grass'])
            elif map[i][j] == 'w':
                tiles.append([20 * j, 20 * i, 'water'])
            elif map[i][j] == 'b':
                tiles.append([20 * j, 20 * i, 'bricks'])

    return (screen_width, screen_height, tiles)

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

    return map_maker(map)

def map_generator(a, b):
    """Генерирует карту размером a * b тайлов.

    Возвращает:
    (screen_width, screen_height, tiles)
    **screen_width** — необходимая ширина экрана
    **screen_height** — необходимая высота экрана
    **screen_height** — кортеж с элементами вида
        (координата левого верхнего угла по x, координата левого верхнего угла по y, название файла с изображением)
    """
    map = [['g' for i in range(b)] for j in range(a)]

    m, n = random.randint(0, a-1), random.randint(0, b-1)
    for i in range(a*b):
        x = random.randint(0, 3)
        if x == 0:
            if m < a-1:
                m += 1
        elif x == 1:
            if m > 0:
                m -= 1
        elif x == 2:
            if n < b-1:
                n += 1
        elif x == 3:
            if n > 0:
                n -= 1
        map[m][n] = 'w'

    m, n = random.randint(0, a - 1), random.randint(0, b - 1)
    for i in range(a*b//10):
        x = random.randint(0, 3)
        if x == 0:
            if m < a-1:
                m += 1
        elif x == 1:
            if m > 0:
                m -= 1
        elif x == 2:
            if n < b-1:
                n += 1
        elif x == 3:
            if n > 0:
                n -= 1
        map[m][n] = 'b'

    return map_maker(map)
