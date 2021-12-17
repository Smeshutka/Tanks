from helper import*
from tank_class import*
from map_maker.tiles import*
from map_maker.map_input import*
from AI import*
import pickle
import socket

def prepared_keys(tank):
    flpk = tank.flpk
    tank.flpk = 0
    return [tank.fw, tank.fa, tank.fs, tank.fd, tank.mouse, flpk, tank.center_visible, tank.corner_visible]

def update_tanks_pos(data_all):

    for tank in tanks:
        flag = False
        for ID in data_all:
            if tank.ID == ID:
                flag = True
                data = data_all[ID]
                tank.center = data[0]
                tank.corner = data[1]
                tank.body_ang = data[2]
                tank.turret_ang = data[3]
                tank.cooldawn = data[4]
                tank.time_cooldawn = data[5]
                tank.hp = data[6]
        if flag == False:
            tank.kill()
    
def update_tank_player_pos(data, tank_player):
    tank_player.center = data[0]
    tank_player.corner = data[1]
    tank_player.body_ang = data[2]
    tank_player.turret_ang = data[3]
    tank_player.cooldawn = data[4]
    tank_player.time_cooldawn = data[5]
    tank_player.hp = data[6]

class all:
    pass

class all_start:
    pass        

def client_main(to_connect_with):

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(to_connect_with)

    pygame.init()

    clock = pygame.time.Clock()
    finished = False
    screen = pygame.display.set_mode((w, h))

    data_all_start = pickle.loads(client.recv(10240))
    client.send(pickle.dumps(""))



    #Декодирование стартовой информации
    map = Map(map_maker(data_all_start.map), screen)

    data_all_start.tank_player.append(screen)
    tank_player = Tank(*data_all_start.tank_player)


    for tank_init in data_all_start.tanks_init:
        tank = data_all_start.tanks_init[tank_init]
        tank.append(screen)
        new_tank = Tank(*tank)
        new_tank.add(tanks)

    observating_point = tank_player.center


    while not finished:

        data_all = pickle.loads(client.recv(10240))

        for update in data_all.list_update:
            map.tiles_array[update[0].y][update[0].x].update_tile(update[1])

        update_tank_player_pos(data_all.tank_player, tank_player)
        update_tanks_pos(data_all.tanks)

        observating_point = tank_player.center

        bullets = pygame.sprite.Group()
        for t in data_all.bullets:
            bul = Bullets(screen, "bullet", t[0].x, t[0].y, t[2], tank_player)
            bul.add(bullets)

        screen.fill((255,255,255))
        map.draw(observating_point)

        update_image_for_tank(tank_player)
        tank_player.before_draw(observating_point)
        for tank in tanks:
            if tank.hp == 0:
                tank.dead()
            update_image_for_tank(tank)
            tank.before_draw(observating_point)
            tank.draw(observating_point)
        update_image_for_tank(tank_player)
        tank_player.update_pos_mouse_for_player()

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
