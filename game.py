from helper import *
from tank_class import *
from map_maker.tiles import *
from map_maker.map_input import *
from AI import *
from button_class import *


def game_main(game_input, tank_type):
    pygame.init()

    all_dead()

    clock = pygame.time.Clock()
    finished = False
    paused = False

    screen = pygame.display.set_mode((w, h))
    
    """
    if game_input == "map_maker/maps/1.txt":
        map = Map(map_maker(file_reader(game_input)), screen)
        tank_player = create_tank_player(12, 12, 0, tank_type, "0", screen)

        list_tile = [pos(5, 5), pos(5, 20), pos(20, 20), pos(20, 5)]
        create_tank_bot(20, 20, 0, "heavy", "1", screen, list_tile, 1)  # Пробный вариант танка противника
    elif game_input == "map_maker/maps/great_level.txt":
        map = Map(map_maker(file_reader(game_input)), screen)
        tank_player = create_tank_player(41, 139, 3.14, tank_type, "0", screen)
        tank_player.hp = 7
        list_tile = [pos(3, 145), pos(3, 129), pos(12, 129), pos(12, 145)]
        create_tank_bot(7, 140, 0, "heavy", "1", screen, list_tile, 2)  # Пробный вариант танка противника

        list_tile = [pos(5, 100), pos(46, 100)]
        create_tank_bot(5, 100, 0, "light", "2", screen, list_tile, 1)  # Пробный вариант танка противника

        list_tile = [pos(27, 109), pos(45, 109)]
        create_tank_bot(27, 113, 0, "middle", "3", screen, list_tile, 1)  # Пробный вариант танка противника

        # list_tile = [pos(25, 75), pos(38, 45)]
        # create_tank_bot(25, 75, 0, "heavy", "4", screen, list_tile, 2)  # Пробный вариант танка противника

        list_tile = [pos(7, 82), pos(6, 89), pos(17, 82), pos(26, 82)]
        create_tank_bot(7, 82, 0, "heavy", "5", screen, list_tile, 2)  # Пробный вариант танка противника

        list_tile = [pos(23, 87), pos(39, 87)]
        create_tank_bot(23, 87, 0, "middle", "6", screen, list_tile, 1)  # Пробный вариант танка противника

        list_tile = [pos(45, 36), pos(32, 36)]
        create_tank_bot(45, 37, 0, "middle", "7", screen, list_tile, 2)  # Пробный вариант танка противника

        list_tile = [pos(6, 11), pos(44, 16), pos(5, 19)]
        create_tank_bot(6, 11, 0, "light", "8", screen, list_tile, 3)  # Пробный вариант танка противника"""


    input = file_reader_level(game_input)
    map, tanks_bots_list, tanks_player = input[0], input[1], input[2]
    map = Map(map, screen)
    for i in range(len(tanks_bots_list)):
        list = tanks_bots_list[i]
        list.insert(5, screen)
        create_tank_bot(*tanks_bots_list[i])
    tank_player = tanks_player[0]
    tank_player.insert(3, tank_type)
    tank_player.insert(5, screen)
    tank_player = create_tank_player(*tank_player)
        
        
        
    observating_point = tank_player.center
    pause_text = Entry(screen, 300, 225, 200, 50, 'pause', None)
    button1 = Button(screen, 325, 300, 150, 50, 'resume')
    button2 = Button(screen, 325, 360, 150, 50, 'to_main_menu')

    while not finished:
        if not paused:
            screen.fill((255, 255, 255))
            map.draw(observating_point)

            for tank in tanks:
                tank.before_draw(observating_point)
                tank.draw(observating_point)

            tank_player.update_pos_mouse_for_player()

            for tank in tanks_bots:
                meet_with_tank(tank, tank_player)

            for tank in tanks:
                tank.draw_turret()

            for bul in bullets:
                bul.draw(observating_point)

        pygame.display.update()
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if paused:
                        paused = False
                    else:
                        paused = True
            if not paused:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        tank_player.fw = 1
                    if event.key == pygame.K_a:
                        tank_player.fa = 1
                    if event.key == pygame.K_s:
                        tank_player.fs = 1
                    if event.key == pygame.K_d:
                        tank_player.fd = 1
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_w:
                        tank_player.fw = 0
                    if event.key == pygame.K_a:
                        tank_player.fa = 0
                    if event.key == pygame.K_s:
                        tank_player.fs = 0
                    if event.key == pygame.K_d:
                        tank_player.fd = 0
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        tank_player.reload_left()
                    if event.button == 3:
                        tank_player.reload_right()
            else:
                pause_text.draw()
                button1.check_pressed()
                button1.draw()
                button2.check_pressed()
                button2.draw()
                if event.type == pygame.MOUSEBUTTONUP:
                    if button1.pressed:
                        paused = False
                    if button2.pressed:
                        return 'menu_main()'

        if not paused:
            for tank in tanks_bots:
                move_AI(tank)

            for tank in tanks:
                tank.move(map)
                tank.fire_gun()
                tank.update_cooldawn()

            for bul in bullets:
                bul.move()
                for tile in bul.tiles_near(map):
                    tile.meet_with_bullet(bul, map)

                for tank in tanks:
                    tank.meet_with_bullet(bul)

            if tank_player.game_over():
                return 'death()'
            if tank_player.game_win():
                return 'win()'
