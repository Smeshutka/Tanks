from helper import*
from tank_class import*
from constans import*
from map_maker.tiles import*
from map_maker.map_input import*
from AI import*

pygame.init()

clock = pygame.time.Clock()
finished = False

w, h, = 600, 600
screen_center = pos(w//2, h//2)
screen = pygame.display.set_mode((w, h))

map = Map(file_reader("map_maker/maps/1.txt"), screen)

tank_bots = []
tank_player = Tank(250, 250, 0, "heavy",screen, screen_center)
tank_enemy = Tank(400, 400, 0, "light",screen, screen_center) # Пробный вариант танка противника
tank_enemy.add(tanks_bots)

list_tile = [pos(5, 5), pos(5, 20), pos(20, 20), pos(20, 5)] #Список точек, по которым будет двигаться бот
tank_enemy.update_list_tile(list_tile)

while not finished:
    screen.fill((255,255,255))
    map.draw(screen_center, tank_player)

    for tank in tanks:
        tank.draw(screen_center, tank_player)

    tank_player.update_pos_mouse_for_player()

    for tank in tanks_bots:
        meet_with_tank(tank, tank_player)

    for tank in tanks:
        tank.draw_turret(screen_center, tank_player)

    for tank in tanks_bots:
        tank.draw_turret(screen_center, tank_player)
        
    for bul in bullets:
        bul.draw(screen_center, tank_player)

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
            tile.meet_with_bullet(bul)

        for tank in tanks:
            tank.meet_with_bullet(bul)
            
            

