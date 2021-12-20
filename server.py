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
            elif map.tiles_array[i][j].type == 'finish':
                ttype = 'F'
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
        self.tank_player = [tank_player.center.x, tank_player.center.y, tank_player.body_ang,
                            tank_player.type, tank_player.ID]
        self.tanks_init = {}
        for tank in tanks:
            self.tanks_init[tank.ID] = [tank.center.x, tank.center.y, tank.body_ang,
                                        tank.type, tank.ID]


def server_main(ip, port, game_input, num_of_pl):
    try:
        to_connect_with = (ip, int(port))

        pygame.init()

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(to_connect_with)

        number_of_players = int(num_of_pl)
        server.listen(number_of_players)
        players = {}
        for i in range(number_of_players):
            player, adress = server.accept()
            players['pl'+str(i)] = player
        print('connected!')
        
        players_start_tank_types = {}
        for ID in players:
            players_start_tank_types[ID] = pickle.loads(players[ID].recv(1024))
        
        clock = pygame.time.Clock()
        finished = False

        screen = pygame.display.set_mode((w, h))

        map, tanks_bots_list, tanks_players = file_reader_level(game_input)
        map = Map(map, screen)
        dict_tanks_players = {}
        for i in range(number_of_players):
            tank_player = create_tank_player(tanks_players[i][0], tanks_players[i][1], tanks_players[i][2],
                                             players_start_tank_types['pl'+str(i)],
                                             tanks_players[i][3], screen)
            dict_tanks_players['pl'+str(i)] = tank_player
        
        #dict_tanks_bots = {}
        for i in range(len(tanks_bots_list)):
            tank_bot = create_tank_bot(tanks_bots_list[i][0], tanks_bots_list[i][1], tanks_bots_list[i][2],
                                       tanks_bots_list[i][3], tanks_bots_list[i][4], screen,
                                       tanks_bots_list[i][5], tanks_bots_list[i][6])
            #dict_tanks_bots[str(i)] = tank_bot
        
        observating_point = dict_tanks_players['pl0'].center

        for ID in players:
            start_data = all_start(tanks, map, dict_tanks_players[ID])
            players[ID].send(pickle.dumps(start_data))
            players[ID].recv(100)

        for tank in tanks:
            tank.before_draw(observating_point)

        while not finished:
            screen.fill((255, 255, 255))
            map.draw(observating_point)

            for tank in tanks:
                #tank.before_draw(observating_point)
                tank.draw(observating_point)

            for tank in tanks_bots:
                for ID in players:
                    meet_with_tank(tank, dict_tanks_players[ID])

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
            for ID in players:
                send_all = all(tanks, bullets, dict_tanks_players[ID], map)
                players[ID].send(pickle.dumps(send_all))
            
            map.list_update = []

            for ID in players:
                data = pickle.loads(players[ID].recv(1024))
                update_tank_keys(dict_tanks_players[ID], data)
                
    except ValueError:
        print('ошибка в формате данных')

    except socket.gaierror:
        print('невозможно создать сервер по заданным данным')
