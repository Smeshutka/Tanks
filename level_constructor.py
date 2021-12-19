from classes_for_constructor import *
import button_class

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
def draw_run_line(k, c, color):
    sur = pygame.Surface((a * k, a * k), pygame.SRCALPHA)
    pygame.draw.line(sur, color, (-2 * a * k / 3 + c, 0), (-a * k / 3 + c, 0), 2)
    pygame.draw.line(sur, color, (c, 0), (a * k / 3 + c, 0), 2)
    pygame.draw.line(sur, color, (2 * a * k / 3 + c, 0), (a * k + c, 0), 2)
    return sur


def draw_chosen(k, time, color = (255,255,255)):
    '''рисует прямоугольник на месте выбранного тайла и
    рассчитывает его координаты для корректного центрирования вида на нём'''
    sur = pygame.Surface((a * k, a * k), pygame.SRCALPHA)
    c = time / (2 * FPS) * 2 * a * k / 3
    sur.blit(pygame.transform.rotate(draw_run_line(k, c,color), 0), (0, 0))
    sur.blit(pygame.transform.rotate(draw_run_line(k, c - a * k / 3,color), 90), (0, 0))
    sur.blit(pygame.transform.rotate(draw_run_line(k, c,color), 90 * 2), (0, 0))
    sur.blit(pygame.transform.rotate(draw_run_line(k, c - a * k / 3,color), 90 * 3), (0, 0))
    return sur

def draw_chosen_tile(chosen_tile,k,time):
    sur = draw_chosen(k,time)
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


def put_tank_on_map(tanks, ma, mb, menu, n):
    tank = Tank(ma*a + a/2, mb*a + a/2, math.pi/2, menu.chosen_type, str(n), menu.screen)
    tank.hp = menu.tank_hp
    tank.x = ma
    tank.y = mb
    tank.list_tile = [[ma,mb]]
    tank.add(tanks)
    return tank

def draw_dots_from_list_tile(screen, tanks, map, observating_point, k):
    sur = pygame.Surface((a * k, a * k), pygame.SRCALPHA)
    pygame.draw.rect(sur, (255,255,255), (a*k/4, a*k/4, a*k/2, a*k/2))
    for tank in tanks:
        ar_for_lines = []
        for dot in tank.list_tile:
            b,c = dot[0], dot[1]
            t = map.tiles_array[c][b]
            t.corner_visible = pos(screen_center.x + t.corner.x * k - observating_point.x * k,
                                       screen_center.y + t.corner.y * k - observating_point.y * k)
            ar_for_lines.append([t.corner_visible.x + a/2*k, t.corner_visible.y + a/2*k])
            screen.blit(sur, (t.corner_visible.x, t.corner_visible.y))
        for i in range(len(ar_for_lines)-1):
            pygame.draw.line(screen, (255,255,255), (ar_for_lines[i][0], ar_for_lines[i][1]),
                             (ar_for_lines[i+1][0],ar_for_lines[i+1][1]))

def draw_flag(screen, flag, map, observating_point, k):
    t = map.tiles_array[flag[1]][flag[0]]
    t.corner_visible = pos(screen_center.x + t.corner.x * k - observating_point.x * k,
                                       screen_center.y + t.corner.y * k - observating_point.y * k)
    image = pygame.image.load('textures/flag.png').convert_alpha()
    screen.blit(update_image(image, k, k), (t.corner_visible.x, t.corner_visible.y))

def del_all_in_tile(ma,mb,tanks,pl_flags):
    for tank in tanks:
        if tank.x == ma and tank.y == mb:
            tank.kill()
        else:
            for dot in tank.list_tile:
                if dot[0] == ma and dot[1] == mb:
                    tank.list_tile.remove(dot)
    for flag in pl_flags:
        if flag[0] == ma and flag[1] == mb:
            pl_flags.remove(flag)

def level_constructor_main():
    # print('Please, print start number')
    # n = call_n_for_fast_save()

    pygame.init()
    screen = pygame.display.set_mode((w, h))
    clock = pygame.time.Clock()
    tanks = pygame.sprite.Group()

    finished = False
    mouse_pressed = False
    updating_tank_list = False
    rubber_mod = False
    player_flag = False

    pl_flags = []
    fa, fw, fs, fd, fo, f_ctrl = 0, 0, 0, 0, 0, 0
    scale = 1
    time = 0
    bots_number = 0
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
    change_menu_button = Change_menu_mode_button(screen, w - a * tiles_menu.k - a * 2, h - a * 2, a * 2, a * 2, 'cycle')
    hp_minus_button = HP_button(screen, w - a * tiles_menu.k + a, h-2*a, a, a, 'minus', False)
    hp_plus_button = HP_button(screen, w - 2*a, h-2*a, a, a, 'plus', True)
    tiles_menu.draw_tanks_type()
    player_flag_button = Button(screen, w - a * tiles_menu.k, h-10*a, 2*a,2*a, 'flag')
    rubber_button = Button(screen, w-2*a, h-10*a,2*a,2*a,'rubber')
    # fast_save_button = SaveLoad_Button(screen, 0, 0, a*2,a*2, 'save')
    to_main_menu_button = button_class.Button(screen, 10, 10, 150, 50, 'to_main_menu')

    while not finished:
        screen.fill((0, 0, 0))
        map.draw_level_constructor(chosen_tile.center, scale)
        for tank in tanks:
            tank.draw_tank_for_constructor(chosen_tile.center, scale)
        for flag in pl_flags:
            draw_flag(screen, flag, map, chosen_tile.center, scale)
        draw_dots_from_list_tile(screen, tanks, map, chosen_tile.center, scale)
        draw_chosen_tile(chosen_tile, scale, time)
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
        if tiles_menu.mode == 'tanks':
            player_flag_button.draw(2)
            rubber_button.draw(2)
            if player_flag:
                screen.blit(draw_chosen(2, time, (0,0,0)), (player_flag_button.pos.x, player_flag_button.pos.y))
            if rubber_mod:
                screen.blit(draw_chosen(2, time, (0,0,0)), (rubber_button.pos.x, rubber_button.pos.y))
            hp_minus_button.draw(1)
            hp_plus_button.draw(1)
        to_main_menu_button.check_pressed()
        to_main_menu_button.draw()

        
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
                    fo = 0
                elif event.key == pygame.K_LCTRL:
                    f_ctrl = 0
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if to_main_menu_button.pressed:
                            return 'menu_main()'
                    if tiles_menu.check_pressed() != '':
                        tiles_menu.chosen_type = tiles_menu.check_pressed()
                    elif rotate_clockwise_button.check_pressed():
                        map = rotate_clockwise_button.rotate_map(map)
                    elif rotate_counterclockwise_button.check_pressed():
                        map = rotate_counterclockwise_button.rotate_map(map)
                    elif save_button.check_pressed():
                        save_button.save_map(map, tanks, pl_flags)
                    elif load_button.check_pressed():
                        new_map, tanks_bots_list, tanks_player = load_button.load_level()
                        if new_map != '':
                            map = new_map
                            tanks = tanks_bots_list
                            pl_flags = tanks_player
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
                    elif hp_minus_button.check_pressed() and tiles_menu.mode == 'tanks':
                        hp_minus_button.change_tank_hp(tiles_menu)
                    elif hp_plus_button.check_pressed() and tiles_menu.mode == 'tanks':
                        hp_plus_button.change_tank_hp(tiles_menu)
                    elif player_flag_button.check_pressed() and tiles_menu.mode == 'tanks' and not(updating_tank_list):
                        player_flag = not(player_flag)
                        rubber_mod = False
                    elif rubber_button.check_pressed() and tiles_menu.mode == 'tanks' and not(updating_tank_list):
                        player_flag = False
                        rubber_mod = not(rubber_mod)
                    #                elif fast_save_button.check_pressed():
                    #                    fast_save_button.fast_save(n, map)
                    #                    n += 1
                    else:
                        if player_flag:
                            ma, mb = calculate_map_pressed(map, chosen_tile, scale)
                            if ma != -1 and mb != -1:
                                pl_flags.append([ma,mb])
                        elif rubber_mod:
                            ma, mb = calculate_map_pressed(map, chosen_tile, scale)
                            if ma != -1 and mb != -1:
                                del_all_in_tile(ma,mb,tanks,pl_flags)
                        elif updating_tank_list:
                            ma, mb = calculate_map_pressed(map, chosen_tile, scale)
                            if ma != -1 and mb != -1:
                                if ma == editing_tank.list_tile[0][0] and mb == editing_tank.list_tile[0][1]:
                                    updating_tank_list = False
                                editing_tank.list_tile.append([ma, mb])
                        elif tiles_menu.mode == 'tiles':
                            ma_start, mb_start = calculate_map_pressed(map, chosen_tile, scale)
                            if ma_start != -1 and mb_start != -1:
                                mouse_pressed = True
                        elif tiles_menu.mode == 'tanks':
                            ma, mb = calculate_map_pressed(map, chosen_tile, scale)
                            if ma != -1 and mb != -1:
                                editing_tank = put_tank_on_map(tanks, ma, mb, tiles_menu, bots_number)
                                bots_number += 1
                                updating_tank_list = True
                                player_flag = False
                                rubber_flag = False
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
            save_button.save_map(map, tanks, pl_flags)
        if f_ctrl == 1 and fo == 1:
            new_map, tanks_bots_list, tanks_player = load_button.load_level()
            if new_map != '':
                map = new_map
                tanks = tanks_bots_list
                pl_flags = tanks_player
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
