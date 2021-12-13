import os
import sys

#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pygame

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..\..')))
from Tanks.helper import*
from Tanks.constans import*

tiles_type = ["grass", "water", "bricks", "ice", "sand", "stone"]
name_images = {}
images = {}
masks = {}
screen = pygame.display.set_mode((w, h))
for tile in tiles_type:
    name_images[tile] = "map_maker/images/" + tile + ".png"
    images[tile] = pygame.image.load(name_images[tile]).convert_alpha()
    masks[tile] = pygame.mask.from_surface(images[tile])

class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, tile_type, screen):
        """ 
        x, y:  положение левого верхнего угла тайла
        tile_type: тип тайла, возможные: "grass", "water", "bricks", "stone",
        "sand", "ice"
        sreen: экран на котором будет отображаться танк
        """
        
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.image = pygame.image.load(name_images[tile_type]).convert_alpha()
        self.corner = pos(x,y)
        self.center = pos(x+a//2, y+a//2)
        self.map_pos = pos(x//a, y//a)
        self.type = tile_type
        self.rect = self.image.get_rect()
            
        if tile_type == "grass":
            self.hp = -1
            self.k1 = 0.01
            self.k2 = 1
        elif tile_type == "water":
            self.hp = -1
            self.k1 = 0.01
            self.k2 = 1
        elif tile_type == "bricks":
            self.hp = 1
            self.k1 = 0.01
            self.k2 = 1
        elif tile_type == "stone":
            self.hp = -1
            self.k1 = 0.01
            self.k2 = 1
        elif tile_type == "sand":
            self.hp = -1
            self.k1 = 0.05
            self.k2 = 5
        elif tile_type == "ice":
            self.hp = -1
            self.k1 = 0.002
            self.k2 = 0.2
            
    def update_tile(self, tile_type):
        """Обновляет тип тайла с сохранением всего прочего"""
        
        self.type = tile_type
        self.image = pygame.image.load(name_images[tile_type]).convert_alpha()

    def draw(self, k=1):
        self.screen.blit(update_image(self.image, k, k), (self.corner_visible.x, self.corner_visible.y))

    def meet_with_bullet(tile, bul):
        """Обработка пересечения с пулей"""
        
        if tile.type == "bricks" or tile.type == "stone":
            if meet(tile, bul):
                bul.kill()
                if tile.type == "bricks":
                    tile_new = "grass"
                    tile.update_tile(tile_new)
    
class Map(pygame.sprite.Sprite):
    """По списку tiles_list формата (x, y, name_image) создает группу тайлов"""
    
    def __init__(self, map, screen):
        tiles = pygame.sprite.Group()
        tiles_array = []
        
        for i in range(len(map)):
            tiles_array.append([])
            for j in range(len(map[i])):
                tiles_array[i].append(Tile(map[i][j][0], map[i][j][1], map[i][j][2], screen))
                tiles_array[i][j].add(tiles)
               
        self.tiles_array = tiles_array
        self.tiles = tiles
            
    def draw(self, observating_point, k=1):
        for t in self.tiles:
            if (t.corner.y - observating_point.y < screen_center.y and observating_point.y - t.corner.y - a < screen_center.y) and \
                    (t.corner.x - observating_point.x < screen_center.x and observating_point.x - t.corner.x - a < screen_center.x):
                t.corner_visible = pos(screen_center.x + t.corner.x - observating_point.x,
                                  screen_center.y + t.corner.y - observating_point.y)
                t.draw(k)
    
def return_tile_ower_pos(x, y, map):
    """Указываются координаты точки, возвращается тайл с данными координатами"""
    i = int(x / a)
    j = int(y / a)
    if j >= 0 and j < len(map.tiles_array) and i >= 0 and i < len(map.tiles_array[0]):
        return map.tiles_array[int(y // a)][int(x // a)]
    return False
    

    
            
