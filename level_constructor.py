from classes_for_constructor import *

'''
Этот модуль позволяет создавать карту
управление: wasd - быстрое перемещение выделенного тайла
на стрелочки - медленное перемещение
1 - замена выделенного тайла на траву
2 - на воду
3 - на кирпич
4 - на камень
5 - на песок
6 - на лёд
left_ctrl + o - вызов диалогового окна для открытия файла карты
left_ctrl + s - вызов диалогового окна для сохранения карты в файл,
                                необходимо прописывать расширение .txt
Backspace - возвращение в левый верхний угол карты
масштабирование карты по колёсику мыши
также поддерживает работу с мышкой
'''


# def call_n_for_fast_save():
#    return int(input())
def draw_run_line(k, c):
    sur = pygame.Surface((a * k, a * k), pygame.SRCALPHA)
    pygame.draw.line(sur, (255, 255, 255), (-2 * a * k / 3 + c, 0), (-a * k / 3 + c, 0), 2)
    pygame.draw.line(sur, (255, 255, 255), (c, 0), (a * k / 3 + c, 0), 2)
    pygame.draw.line(sur, (255, 255, 255), (2 * a * k / 3 + c, 0), (a * k + c, 0), 2)
    return sur


def draw_chosen(chosen_tile, k, time):
    '''рисует прямоугольник на месте выбранного тайла и
    рассчитывает его координаты для корректного центрирования вида на нём'''
    sur = pygame.Surface((a * k, a * k), pygame.SRCALPHA)
    c = time / (2 * FPS) * 2 * a * k / 3
    sur.blit(pygame.transform.rotate(draw_run_line(k, c), 0), (0, 0))
    sur.blit(pygame.transform.rotate(draw_run_line(k, c - a * k / 3), 90), (0, 0))
    sur.blit(pygame.transform.rotate(draw_run_line(k, c), 90 * 2), (0, 0))
    sur.blit(pygame.transform.rotate(draw_run_line(k, c - a * k / 3), 90 * 3), (0, 0))

    chosen_tile.corner_visible = pos(w // 2, h // 2)
    chosen_tile.screen.blit(sur, (chosen_tile.corner_visible.x - a * k / 2, chosen_tile.corner_visible.y - a * k / 2))


def change_pos_chosen(chosen_tile, cx, cy, k):
    '''Меняет положение выбранного тайла
    cx,cy - на сколько тайлов переместить по x,y. Может быть -1,0,1'''
    chosen_tile.corner.x += cx * a
    chosen_tile.corner.y += cy * a
    chosen_tile.center = pos(chosen_tile.corner.x + a // 2, chosen_tile.corner.y + a // 2)
    chosen_tile.map_pos = pos(chosen_tile.corner.x // a, chosen_tile.corner.y // a)


def change_chosen_type(chosen_tile, map, new_type, menu):
    '''изменяет тип выбранного файла'''

    ca, cb = chosen_tile.map_pos.x, chosen_tile.map_pos.y
    map_b = len(map.tiles_array)
    map_a = len(map.tiles_array[0])
    if ca >= 0 and ca < map_a and cb >= 0 and cb < map_b:
        tile = map.tiles_array[chosen_tile.map_pos.y][chosen_tile.map_pos.x]
        tile.update_tile(new_type)
        # chosen_tile.type = new_type
        menu.chosen_type = new_type


def calculate_map_pressed(map, chosen_tile, k):
    '''Возвращает координаты тайла на карте при щелчке мыши'''
    mx, my = pygame.mouse.get_pos()
    map_b = len(map.tiles_array)
    map_a = len(map.tiles_array[0])

    ma = (mx + chosen_tile.center.x * k - w // 2) / a / k
    mb = (my + chosen_tile.center.y * k - h // 2) / a / k
    ma = int(ma)
    mb = int(mb)

    if ma < map_a and ma >= 0 and mb < map_b and mb >= 0:
        return ma, mb
    else:
        return -1, -1


def draw_highlighting(ma_start, mb_start, screen, map, k):
    '''рисует рамочку выделения выбранных тайлов при зажатии мыши
    из центра начального выбранного тайла до положения мыши'''
    mx, my = pygame.mouse.get_pos()
    x0, y0 = map.tiles_array[mb_start][ma_start].corner_visible.x + k * a / 2, map.tiles_array[mb_start][
        ma_start].corner_visible.y + k * a / 2
    x0 = int(x0)
    y0 = int(y0)
    if mx < x0:
        mx, x0 = x0, mx
    if my < y0:
        my, y0 = y0, my
    pygame.draw.rect(screen, (0, 0, 0), (x0, y0, mx - x0, my - y0), 2)

def put_tank_on_map(tanks, ma, mb, menu):
    tank = Tank(ma*a + a/2, mb*a + a/2, math.pi/2, menu.chosen_type, '0', menu.screen)
    tank.add(tanks)

def level_constructor_main():
    # print('Please, print start number')
    # n = call_n_for_fast_save()

    pygame.init()
    screen = pygame.display.set_mode((w, h))
    clock = pygame.time.Clock()
    tanks = pygame.sprite.Group()
    
    finished = False
    mouse_pressed = False

    fa, fw, fs, fd, fo, f_ctrl = 0, 0, 0, 0, 0, 0
    scale = 1
    time = 0
    # lt = list of tiles
    lt = []
    for i in range(10):
        lt.append([])
        for j in range(10):
            lt[i].append('g')

    map = Map(map_maker(lt), screen)
    chosen_tile = Tile(a * 0, a * 0, "stone", screen)

    tiles_menu = Tiles_menu(screen, w, h)
    rotate_clockwise_button = Rotate_button(screen, w - a * tiles_menu.k - a * 2, 0, a * 2, a * 2, 'rotate_icon', False)
    rotate_counterclockwise_button = Rotate_button(screen, w - a * tiles_menu.k - a * 4, 0, a * 2, a * 2, 'rotate_icon',
                                                   True)
    save_button = SaveLoad_Button(screen, w - a * tiles_menu.k - a * 6, 0, a * 2, a * 2, 'save')
    load_button = SaveLoad_Button(screen, w - a * tiles_menu.k - a * 8, 0, a * 2, a * 2, 'load')
    size_button = Change_size_button(screen, w - a * tiles_menu.k - a * 10, 0, a * 2, a * 2, 'size')
    generator = Generate_button(screen, w - a * tiles_menu.k - a * 12, 0, a * 2, a * 2, 'dices')
    change_menu_button = Change_menu_mode_button(screen, w - a * tiles_menu.k - a * 2, h-a*2, a * 2, a * 2, 'cycle')
    # fast_save_button = SaveLoad_Button(screen, 0, 0, a*2,a*2, 'save')

    while not finished:
        screen.fill((0, 0, 0))
        map.draw_level_constructor(chosen_tile.center, scale)
        draw_chosen(chosen_tile, scale, time)
        tiles_menu.draw()
        if mouse_pressed:
            draw_highlighting(ma_start, mb_start, screen, map, scale)
        rotate_clockwise_button.draw(2)
        rotate_counterclockwise_button.draw(2)
        save_button.draw(2)
        load_button.draw(2)
        size_button.draw(2)
        generator.draw(2)
        change_menu_button.draw(2)
        
        for tank in tanks:
            tank.draw_tank_for_constructor(chosen_tile.center, scale)
        # fast_save_button.draw(2)
        pygame.display.update()

        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    fw = 1
                elif event.key == pygame.K_a:
                    fa = 1
                elif event.key == pygame.K_s:
                    fs = 1
                elif event.key == pygame.K_d:
                    fd = 1
                elif event.key == pygame.K_o:
                    fo = 1
                elif event.key == pygame.K_LCTRL:
                    f_ctrl = 1
                elif event.key == pygame.K_RCTRL:
                    create_dialog_window()
                elif event.key == pygame.K_BACKSPACE:
                    change_pos_chosen(chosen_tile, -chosen_tile.map_pos.x, -chosen_tile.map_pos.y, scale)
                elif event.key == pygame.K_UP:
                    change_pos_chosen(chosen_tile, 0, -1, scale)
                elif event.key == pygame.K_LEFT:
                    change_pos_chosen(chosen_tile, -1, 0, scale)
                elif event.key == pygame.K_DOWN:
                    change_pos_chosen(chosen_tile, 0, 1, scale)
                elif event.key == pygame.K_RIGHT:
                    change_pos_chosen(chosen_tile, 1, 0, scale)
                elif event.key == pygame.K_1:
                    change_chosen_type(chosen_tile, map, 'grass', tiles_menu)
                elif event.key == pygame.K_2:
                    change_chosen_type(chosen_tile, map, 'water', tiles_menu)
                elif event.key == pygame.K_3:
                    change_chosen_type(chosen_tile, map, 'bricks', tiles_menu)
                elif event.key == pygame.K_4:
                    change_chosen_type(chosen_tile, map, 'stone', tiles_menu)
                elif event.key == pygame.K_5:
                    change_chosen_type(chosen_tile, map, 'sand', tiles_menu)
                elif event.key == pygame.K_6:
                    change_chosen_type(chosen_tile, map, 'ice', tiles_menu)
                # if event.key == pygame.K_f:
                # fast_save_button.fast_save(n, map)
                # n += 1
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    fw = 0
                elif event.key == pygame.K_a:
                    fa = 0
                elif event.key == pygame.K_s:
                    fs = 0
                elif event.key == pygame.K_d:
                    fd = 0
                elif event.key == pygame.K_o:
                    fo = 1
                elif event.key == pygame.K_LCTRL:
                    f_ctrl = 0
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if tiles_menu.check_pressed() != '':
                        tiles_menu.chosen_type = tiles_menu.check_pressed()
                    elif rotate_clockwise_button.check_pressed():
                        map = rotate_clockwise_button.rotate_map(map)
                    elif rotate_counterclockwise_button.check_pressed():
                        map = rotate_counterclockwise_button.rotate_map(map)
                    elif save_button.check_pressed():
                        save_button.save_map(map)
                    elif load_button.check_pressed():
                        new_map = load_button.load_map()
                        if new_map != '':
                            map = new_map
                    elif size_button.check_pressed():
                        new_map = size_button.change_map_size(map, screen)
                        if new_map != '':
                            map = new_map
                    elif change_menu_button.check_pressed():
                        change_menu_button.change_mode(tiles_menu)
                    elif generator.check_pressed():
                        try:
                            new_map = generator.generate()
                        except IndexError:
                            print('Ошибка генерации. Попробуйте уменьшить количество шаблонов')
                            new_map = ''
                        if new_map != '':
                            map = new_map
                    #                elif fast_save_button.check_pressed():
                    #                    fast_save_button.fast_save(n, map)
                    #                    n += 1
                    else:
                        if tiles_menu.mode == 'tiles':
                            ma_start, mb_start = calculate_map_pressed(map, chosen_tile, scale)
                            if ma_start != -1 and mb_start != -1:
                                mouse_pressed = True
                        elif tiles_menu.mode == 'tanks':
                            ma, mb = calculate_map_pressed(map, chosen_tile, scale)
                            if ma != -1 and mb != -1:
                                put_tank_on_map(tanks, ma, mb, tiles_menu)
                if event.button == 4:
                    scale += 0.3
                if event.button == 5 and scale > 0.3:
                    scale -= 0.3

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if mouse_pressed:
                        mouse_pressed = False
                        ma_end, mb_end = calculate_map_pressed(map, chosen_tile, scale)
                        if ma_end != -1 and mb_end != -1:
                            if ma_end < ma_start:
                                ma_end, ma_start = ma_start, ma_end
                            if mb_end < mb_start:
                                mb_end, mb_start = mb_start, mb_end
                            mb_end += 1
                            ma_end += 1
                            for i in range(abs(mb_end - mb_start)):
                                for j in range(abs(ma_end - ma_start)):
                                    map.tiles_array[mb_start + i][ma_start + j].update_tile(tiles_menu.chosen_type)
        if f_ctrl == 1 and fs == 1:
            save_button.save_map(map)
        if f_ctrl == 1 and fo == 1:
            new_map = load_button.load_map()
            if new_map != '':
                map = new_map
        if fa == 1 and fd == 0:
            change_pos_chosen(chosen_tile, -1, 0, scale)
        elif fa == 0 and fd == 1:
            change_pos_chosen(chosen_tile, 1, 0, scale)
        if fw == 1 and fs == 0:
            change_pos_chosen(chosen_tile, 0, -1, scale)
        elif fw == 0 and fs == 1:
            change_pos_chosen(chosen_tile, 0, 1, scale)

        time += 1
        if time >= 2 * FPS:
            time = 0
