from helper import*
from tank_class import*
from constans import*
from map_maker.tiles import*
from map_maker.map_input import*
from AI import*
import socket
import pickle

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
    send_map = pickle.dumps(map)
    player.send(send_map)
    send_tanks = pickle.dumps(tanks)
    player.send(send_tanks)
    send_tanks_bots = pickle.dumps(tanks_bots)
    player.send(send_tanks_bots)
    send_bullets = pickle.dumps(bullets)
    player.send(send_bullets)
    
    player_data = player.recv(1024)
    tank_player = pickle.loads(player_data)