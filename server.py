from helper import *
from tank_class import *
from constans import *
from map_maker.tiles import *
from map_maker.map_input import *
from AI import *
import socket
import pickle


def convert_map(map):
    ar = []
    for i in range(len(map.tiles_array)):
        ar.append([])
        for j in range(len(map.tiles_array[0])):
            if map.tiles_array[i][j].type == 'stone':
                ttype = 'S'
            else:
                ttype = map.tiles_array[i][j].type[0]
            ar[i].append(ttype)
    return ar


def prepared_tank(tank):
    return [tank.center, tank.corner, tank.body_ang, tank.turret_ang, tank.cooldawn,
            tank.time_cooldawn, tank.hp]


def prepared_bullet(bul):
    return [bul.center, bul.corner, bul.ang]


def update_tank_keys(tank, data):
    tank.fw = data[0]
    tank.fa = data[1]
    tank.fs = data[2]
    tank.fd = data[3]
    tank.mouse = data[4]
    tank.flpk = data[5]
    tank.center_visible = data[6]
    tank.corner_visible = data[7]


class all:
    def __init__(self, tanks, bullets, tank_player, map):
        self.tanks = {}
        for tank in tanks:
            self.tanks[tank.ID] = prepared_tank(tank)
        self.list_update = map.list_update
        self.tank_player = prepared_tank(tank_player)
        self.bullets = []
        for bul in bullets:
            self.bullets.append(prepared_bullet(bul))


class all_start:
    def __init__(self, tanks, map, tank_player):
        self.map = convert_map(map)
        self.tank_player = [tank_player.center.x, tank_player.center.y, tank_player.body_ang, tank_player.type,
                            tank_player.ID]
        self.tanks_init = {}
        for tank in tanks:
            self.tanks_init[tank.ID] = [tank.center.x, tank.center.y, tank.body_ang, tank.type, tank.ID]


def server_main(ip, port):
    try:
        to_connect_with = (ip, int(port))

        pygame.init()

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(to_connect_with)

        number_of_players = 2

        server.listen(number_of_players)
        player1, adress = server.accept()
        if number_of_players == 2:
            player2, adress = server.accept()
        print('connected!')

        clock = pygame.time.Clock()
        finished = False

        screen = pygame.display.set_mode((w, h))

        map = Map(map_maker(file_reader("map_maker/maps/1.txt")), screen)

        tank_player1 = create_tank_player(12, 5, 0, "light", "0", screen)
        if number_of_players == 2:
            tank_player2 = create_tank_player(14, 14, 0, "middle", "1", screen)

        list_tile = [pos(5, 5), pos(5, 20), pos(20, 20), pos(20, 5)]
        bot = create_tank_bot(20, 20, 0, "heavy", "2", screen, list_tile, 2)

        observating_point = tank_player1.center

        start_data = all_start(tanks, map, tank_player1)
        player1.send(pickle.dumps(start_data))
        player1.recv(100)
        if number_of_players == 2:
            start_data = all_start(tanks, map, tank_player2)
            player2.send(pickle.dumps(start_data))
            player2.recv(100)

        for tank in tanks:
            tank.before_draw(observating_point)

        while not finished:
            screen.fill((255, 255, 255))
            map.draw(observating_point)

            for tank in tanks:
                flag = True
                if tank is tank_player1:
                    flag = False
                if number_of_players == 2:
                    if tank is tank_player2:
                        flag = False

                if flag:
                    tank.before_draw(observating_point)
                tank.draw(observating_point)

            for tank in tanks_bots:
                meet_with_tank(tank, tank_player1)
                if number_of_players == 2:
                    meet_with_tank(tank, tank_player2)

            for tank in tanks:
                tank.draw_turret()

            for bul in bullets:
                bul.draw(observating_point)

            pygame.display.update()
            clock.tick(FPS)

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

            # отправка игроку данных
            send_all = all(tanks, bullets, tank_player1, map)
            player1.send(pickle.dumps(send_all))
            if number_of_players == 2:
                send_all = all(tanks, bullets, tank_player2, map)
                player2.send(pickle.dumps(send_all))
            map.list_update = []

            data = pickle.loads(player1.recv(1024))
            update_tank_keys(tank_player1, data)
            if number_of_players == 2:
                data = pickle.loads(player2.recv(1024))
                update_tank_keys(tank_player2, data)

    except ValueError:
        print('ошибка в формате данных')

    except socket.gaierror:
        print('невозможно создать сервер по заданным данным')
