from helper import *
from tank_class import *
from map_maker.tiles import *
from map_maker.map_input import *
from AI import *


def game_main(game_input, tank_type):
    pygame.init()

    all_dead()

    clock = pygame.time.Clock()
    finished = False

    screen = pygame.display.set_mode((w, h))

    map = Map(map_maker(file_reader(game_input)), screen)
    if game_input == "map_maker/maps/1.txt":
        tank_player = create_tank_player(12, 12, 0, tank_type, "0", screen)

        list_tile = [pos(5, 5), pos(5, 20), pos(20, 20), pos(20, 5)]
        create_tank_bot(20, 20, 0, "heavy", "1", screen, list_tile, 1)  # Пробный вариант танка противника
    elif game_input == "map_maker/maps/great_level.txt":
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
        create_tank_bot(6, 11, 0, "light", "8", screen, list_tile, 3)  # Пробный вариант танка противника

    observating_point = tank_player.center

    while not finished:
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

        tank_player.game_over()
