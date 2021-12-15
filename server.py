from helper import*
from tank_class import*
from constans import*
from map_maker.tiles import*
from map_maker.map_input import*
from AI import*
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
            tank.time_cooldawn]

def prepared_bullet(bul):
    return [bul.center, bul.corner, bul.ang]

def update_tank_keys(tank, data):
    tank.fw = data[0]
    tank.fa = data[1]
    tank.fs = data[2]
    tank.fd = data[3]
    tank.mouse = data[4]
    tank.flpk = data[5]

class all:
    def __init__(self, tank_player, bullets, map):  
        self.tank_player = prepared_tank(tank_player)
        self.list_update = map.list_update
        
        self.bullets = []
        for bul in bullets:
            self.bullets.append(prepared_bullet(bul))

class all_start:
    def __init__(self, tanks, tanks_bots, map, tank_player):
        self.map = convert_map(map)
        '''
        self.tank_player = [tank_player.center.x, tank_player.center.y, tank_player.body_ang, tank_player.type]
        self.tanks_init = []
        self.tanks_bots_init = []
        for tank in tanks:
            self.tanks_init.append([tank.center.x, tank.center.y, tank.body_ang, tank.type])
        for tank in tanks_bots:
            self.tanks_bots_init.append([tank.center.x, tank.center.y, tank.body_ang, tank.type])
    '''
pygame.init()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("192.168.31.130",12345))

server.listen(1)
player, adress = server.accept()
print('connected!')

clock = pygame.time.Clock()
finished = False

screen = pygame.display.set_mode((w, h))

map = Map(map_maker(file_reader("map_maker/maps/1.txt")), screen)

tank_player = Tank(250, 250, 0, "light", screen)
#tank_enemy = Tank(400, 400, 0, "heavy", screen) # Пробный вариант танка противника
#tank_enemy.add(tanks_bots)

list_tile = [pos(5, 5), pos(5, 20), pos(20, 20), pos(20, 5)] #Список точек, по которым будет двигаться бот
#tank_enemy.update_list_tile(list_tile)

observating_point = tank_player.center

start_data = all_start(tanks, tanks_bots, map, tank_player)
player.send(pickle.dumps(convert_map(map)))
player.recv(100)

while not finished:
    screen.fill((255,255,255))
    map.draw(observating_point)

    for tank in tanks:
        tank.draw(observating_point)

    #tank_player.update_pos_mouse_for_player()

    for tank in tanks_bots:
        meet_with_tank(tank, tank_player)

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
    
    #отправка игроку данных
    #player.send(pickle.dumps(convert_map(map)))
    #player.recv(100)
    send_all = all(tank_player, bullets, map)
    player.send(pickle.dumps(send_all))
    map.list_update = []
    #player.recv(100)
    #player.send(pickle.dumps(prepared_tank(tank_enemy)))
    #player.recv(100)
    #player.send(pickle.dumps(len(bullets)))
    #player.recv(100)
    #for bul in bullets:
    #    player.send(pickle.dumps(prepared_bullet(bul)))
    #    player.recv(100)
    
    data = pickle.loads(player.recv(1024))
    update_tank_keys(tank_player, data)
    #player.send(pickle.dumps(''))
