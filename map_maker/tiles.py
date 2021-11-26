import os
import sys

#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..\..')))
from Tanks.helper import*
from Tanks.constans import*

tiles = pygame.sprite.Group() 
tiles_type = ["grass", "water", "bricks"]
name_images = {}
images = {}
masks = {}
screen = pygame.display.set_mode((WIDTH, HEIGHT))
for tile in tiles_type:
    name_images[tile] = "map_maker/images/tile_" + tile + "1.png"
    images[tile] = pygame.image.load(name_images[tile]).convert_alpha()
    masks[tile] = pygame.mask.from_surface(images[tile])


class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, tile_type, screen):
        """ 
        x, y:  положение левого верхнего угла тайла
        tile_type: тип тайла, возможные: "grass", "water", "bricks"
        sreen: экран на котором будет отображаться танк
        """
        
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.image = pygame.image.load(name_images[tile_type]).convert_alpha()
        self.corner = pos(x,y)
        self.type = tile_type
        
        if tile_type == "grass":
            self.hp = -1
        elif tile_type == "water":
            self.hp = -1
        elif tile_type == "bricks":
            self.hp = 1
    def update_tile(self, tile_type):
        """Обновляет тип тайла с сохранением всего прочего"""
        
        self.type = tile_type
        self.image = pygame.image.load(name_images[tile_type]).convert_alpha()

    def draw(self):
        self.screen.blit(self.image, (self.corner.x, self.corner.y))

    def meet_with_bullet(tile, bul):
        """Обработка пересечения с пулей"""
        
        if tile.type == "bricks":
                if meet(tile, bul):
                    bul.kill()
                    tile.update_tile("grass")
    
class Map(pygame.sprite.Sprite):
    """По списку tiles_list формата (x, y, name_image) создает группу тайлов"""
    
    def __init__(self, tiles_list, screen):
        for t in tiles_list:
            tile = Tile(t[0], t[1], t[2], screen)
            tile.add(tiles)
    def draw(self):
        for t in tiles:
            t.draw()

   
            
