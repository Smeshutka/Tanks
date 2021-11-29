from helper import*
from tank_class import*
from constans import*
from  map_maker.tiles import*
from map_maker.map_input import*
from AI import*

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
tank_player = Tank(250,250,"heavy",screen)
tank_enemy = Tank(400, 400,"heavy",screen) # Пробный вариант танка противника
clock = pygame.time.Clock()
finished = False

w, h, tiles_list = file_reader("map_maker/maps/1.txt")
screen = pygame.display.set_mode((w, h))
map = Map(tiles_list, screen)

while not finished:
    screen.fill((255,255,255))
    map.draw()
    tank_player.draw()
    tank_enemy.draw()
    v = vision(tank_enemy, screen)
    v.meet_with_tank(tank_player)
        
    for bul in bullets:
        bul.draw()
    
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
                
    tank_player.move(0.01,1)
    tank_player.fire_gun()
    tank_player.update_cooldawn()
    tank_enemy.update_cooldawn()
        
    for bul in bullets:
        bul.move()
        for tile in tiles:
            tile.meet_with_bullet(bul)
            
    
pygame.quit()
