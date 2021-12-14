from helper import*
from tank_class import*
from constans import*
from map_maker.tiles import*
from map_maker.map_input import*
from AI import*
import pickle
import socket

def prepared_keys(tank):
    return [tank.fw, tank.fa, tank.fs, tank.fd]

def update_tank_pos(data, tank):
    tank.center = data[0]
    tank.corner = data[1]
    tank.body_ang = data[2]
    tank.turret_ang = data[3]

def 

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("192.168.31.118", 12345))

pygame.init()

clock = pygame.time.Clock()
finished = False
tank_player = Tank(250, 250, 0, "light", screen)
tank_enemy = Tank(400, 400, 0, "heavy", screen)
screen = pygame.display.set_mode((w, h))

observating_point = tank_player.center

while not finished:
    map = Map(map_maker(pickle.loads(client.recv(1024)),screen))
    player_new_pos = pickle.loads(client.recv(1024))
    enemy_new_pos = pickle.loads(client.recv(1024))
    update_tank_pos(player_new_pos, tank_player)
    update_tank_pos(enemy_new_pos, tank_enemy)
    n = pickle.loads(client.recv(1024))
    for i in range(n):
        bul_data = pickle.loads(client.recv(1024))
        bullets 
    
    screen.fill((255,255,255))
    map.draw(observating_point)
'''
    for tank in tanks:
        tank.draw(observating_point)

    tank_player.update_pos_mouse_for_player()

    for tank in tanks_bots:
        meet_with_tank(tank, tank_player)

    for tank in tanks:
        tank.draw_turret()
        
    for bul in bullets:
        bul.draw(observating_point)
'''
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
    
    client.send(pickle.dumps(prepared_keys(tank_player)))

