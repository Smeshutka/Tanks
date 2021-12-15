from helper import*
from tank_class import*
from constans import*
from map_maker.tiles import*
from map_maker.map_input import*
from AI import*
import pickle
import socket

def prepared_keys(tank):
    flpk = tank.flpk
    tank.flpk = 0
    return [tank.fw, tank.fa, tank.fs, tank.fd, tank.mouse, flpk]

def update_tank_pos(data, tank):
    tank.center = data[0]
    tank.corner = data[1]
    tank.body_ang = data[2]
    tank.turret_ang = data[3]
    tank.cooldawn = data[4]
    tank.time_cooldawn = data[5]
    

class all:
    pass

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("192.168.31.130", 12345))

pygame.init()

clock = pygame.time.Clock()
finished = False
screen = pygame.display.set_mode((w, h))

data_all = pickle.loads(client.recv(10240))
print("+")
client.send(pickle.dumps(""))

map = Map(map_maker(data_all.map), screen)
data_all.tank_player.append(screen)
tank_player = Tank(*data_all.tank_player)

#tank_player = Tank(250, 250, 0, "light", screen)
#tank_enemy = Tank(400, 400, 0, "heavy", screen)

observating_point = tank_player.center



while not finished:

    data_all = pickle.loads(client.recv(10240))
    player_new_pos = data_all.tank_player
    
    for update in data_all.list_update:
        map.tiles_array[update[0].y][update[0].x].update_tile(update[1])

    update_tank_pos(player_new_pos, tank_player)
    observating_point = tank_player.center
    #update_tank_pos(enemy_new_pos, tank_enemy)
    
    bullets = pygame.sprite.Group()
    for t in data_all.bullets:
        bul = Bullets(screen, "bullet", t[0].x, t[0].y, t[2], tank_player)
        bul.add(bullets)
    
    screen.fill((255,255,255))
    map.draw(observating_point)

    for tank in tanks:
        update_image_for_tank(tank)
        tank.draw(observating_point)

    tank_player.update_pos_mouse_for_player()

    #for tank in tanks_bots:
      #  meet_with_tank(tank, tank_player)

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
    
    erunda = prepared_keys(tank_player)
    client.send(pickle.dumps(erunda))
