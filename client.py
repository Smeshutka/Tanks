from helper import*
from tank_class import*
from constans import*
from map_maker.tiles import*
from map_maker.map_input import*
from AI import*
import pickle
import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("192.168.31.118", 12345))

pygame.init()

clock = pygame.time.Clock()
finished = False

screen = pygame.display.set_mode((w, h))

observating_point = tank_player.center

while not finished:
    map = pickle.loads(client.recv(1024))
    tanks = pickle.loads(client.recv(1024))
    tanks_bots = pickle.loads(client.recv(1024))
    bullets = pickle.loads(client.recv(1024))
    
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
          
    send_player_tank = pickle.dumps(tank_player)
    client.send(send_player_tank)