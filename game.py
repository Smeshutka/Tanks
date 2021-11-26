from helper import*
from tank_class import*
from constans import*
from  map_maker.tiles import*
from map_maker.map_input import*

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
tank_player = Tank(250,250,"heavy",screen)
fw, fa, fs, fd, flpk, frpk = 0, 0, 0, 0, 0, 0
clock = pygame.time.Clock()
finished = False

w, h, tiles_list = file_reader("map_maker/maps/1.txt")
screen = pygame.display.set_mode((w, h))
map = Map(tiles_list, screen)

while not finished:
    screen.fill((255,255,255))
    map.draw()
    tank_player.draw()
        
    for bul in bullets:
        bul.draw()
    
    pygame.display.update()
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                fw = 1
            if event.key == pygame.K_a:
                fa = 1
            if event.key == pygame.K_s:
                fs = 1
            if event.key == pygame.K_d:
                fd = 1
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                fw = 0
            if event.key == pygame.K_a:
                fa = 0
            if event.key == pygame.K_s:
                fs = 0
            if event.key == pygame.K_d:
                fd = 0
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                flpk = 1
            if event.button == 3:
                frpk = 1     
                
    tank_player.move(fw,fa,fs,fd,0.01,1)
    flpk, frpk = tank_player.fire_gun(flpk, frpk)
    tank_player.update_cooldawn()
        
    for bul in bullets:
        bul.move()

    
pygame.quit()
