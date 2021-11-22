def read_map_data(input_filename):
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

    screen_width = 100 * len(map[0])
    screen_height = 100 * len(map)
    tiles = []

    for i in range(len(map)):
        for j in range(len(map[i])):
            if map[i][j] == 'g':
                tiles.append((100 * j, 100 * i, 'images/tile_grass.png'))
            elif map[i][j] == 'w':
                tiles.append((100 * j, 100 * i, 'images/tile_water.png'))
            elif map[i][j] == 'b':
                tiles.append((100 * j, 100 * i, 'images/tile_bricks.png'))

    return (screen_width, screen_height, tiles)