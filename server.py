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
            if map.tiles_array[i][j].tile_type = 'stone':
                ttype = 'S'
            else:
                ttype = map.tiles_array[i][j].tile_type[0]
            ar[i].append(ttype)
    return ar

def prepared_tank(tank):
    return ar = [tank.center, tank.corner, tank.body_ang, tank.turret_ang]
def prepared_bullet(bul):
    return ar = [bul.center, bul.corner, bul.ang]

pygame.init()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("192.168.31.118",12345))

server.listen(1)
player, adress = server.accept()

clock = pygame.time.Clock()
finished = False

screen = pygame.display.set_mode((w, h))

map = Map(file_reader("map_maker/maps/1.txt"), screen)

tank_player = Tank(250, 250, 0, "light", screen)
tank_enemy = Tank(400, 400, 0, "heavy", screen) # Пробный вариант танка противника
tank_enemy.add(tanks_bots)

list_tile = [pos(5, 5), pos(5, 20), pos(20, 20), pos(20, 5)] #Список точек, по которым будет двигаться бот
tank_enemy.update_list_tile(list_tile)

observating_point = tank_player.center

while not finished:
    screen.fill((255,255,255))
    map.draw(observating_point)

    for tank in tanks:
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
                
    for tank in tanks_bots:
        move_AI(tank)

    for tank in tanks:
        tank.move(map)
        tank.fire_gun()
        tank.update_cooldawn()
    
    for bul in bullets:
        bul.move()
        for tile in bul.tiles_near(map):
            tile.meet_with_bullet(bul)

        for tank in tanks:
            tank.meet_with_bullet(bul)
    
    #отправка игроку данных
    player.send(pickle.dumps(convert_map(map)))
    
    player.send(pickle.dumps(prepared_tank(tank_player)))
    
    player.send(pickle.dumps(prepared_tank(tank_enemy)))
    
    player.send(pickle.dumps(len(bullets)))
    for bul in bullets:
        player.send(pickle.dumps(prepared_bullet(bul)))
    
    player_data = player.recv(1024)
    tank_player = pickle.loads(player_data)

