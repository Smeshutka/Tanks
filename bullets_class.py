from helper import *
from map_maker.tiles import *

screen = pygame.display.set_mode((w, h))

bullets_type = ["bullet"]
name_images = {}
images = {}
masks = {}

for bul in bullets_type:
    name_images[bul] = "textures/" + bul + ".png"
    images[bul] = pygame.image.load(name_images[bul]).convert_alpha()
    masks[bul] = pygame.mask.from_surface(images[bul])


class Bullets(pygame.sprite.Sprite):
    def __init__(self, screen, bullet_type, x, y, ang, owner):
        """ 
        x,y:  положение центра снаряда
        bullet_type: тип снаряда, возможные: "bullet", "shell"
        sreen: экран на котором будет отображаться танк
        ang: Угол между направлением вектора скорости снаряда и горизонтом
        """

        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.center = pos(x, y)
        self.ang = ang
        self.image_start = pygame.image.load(name_images[bullet_type]).convert_alpha()
        self.image = self.image_start
        update_corner(self)
        self.mask = masks[bul]
        self.rect = self.image.get_rect()
        self.damage = 1
        self.owner = owner

        if bullet_type == "bullet":
            self.v = 10
        elif bullet_type == "shell":
            self.v = 15

        vx = self.v * math.cos(self.ang)
        vy = self.v * math.sin(-self.ang)
        self.velocity = pos(vx, vy)

    def check_board(self, WIDTH, HEIGHT):
        if self.x > WIDTH or self.x < 0 or self.y > HEIGHT or self.y < 0:
            return True
        else:
            return False

    def move(self):
        self.center.x += self.velocity.x
        self.center.y += self.velocity.y

    def draw(self, observating_point):
        self.image = pygame.transform.rotate(self.image_start, self.ang * 180 / math.pi)
        update_corner(self)
        self.screen.blit(self.image, (screen_center.x + self.corner.x - observating_point.x,
                                      screen_center.y + self.corner.y - observating_point.y))

    def tiles_near(self, map):
        """
        Возвращает группу тайлов, находящихся поблизости танка
        tiles_array[i][j]: i - номер строчки, j - номер столбца
        """
        tiles_n = pygame.sprite.Group()
        x1, y1, x2, y2 = self.corner.x, self.corner.y, 2 * self.center.x - self.corner.x, 2 * self.center.y - self.corner.y
        x1 = max(int(x1) // a - 2, 0)
        x2 = min(int(x2) // a + 2, len(map.tiles_array[0]))
        y1 = max(int(y1) // a - 2, 0)
        y2 = min(int(y2) // a + 2, len(map.tiles_array))
        for i in range(x1, x2):
            for j in range(y1, y2):
                if j >= 0 and j <= len(map.tiles_array) and i >= 0 and i <= len(map.tiles_array[0]):
                    map.tiles_array[j][i].add(tiles_n)
        return tiles_n

# class Shell:
# class Bullet:
