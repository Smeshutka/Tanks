from helper import*
from constans import*

screen = pygame.display.set_mode((WIDTH, HEIGHT))

bullets_type = ["bullet"]
name_images = {}
images = {}
masks = {}
for bul in bullets_type:
    name_images[bul] = "textures/" + bul + ".png"
    
    images[bul] = pygame.image.load(name_images[bul]).convert_alpha()
    masks[bul] = pygame.mask.from_surface(images[bul])


class Bullets(pygame.sprite.Sprite):
    def __init__(self, screen, bullet_type, x, y, ang):
        """ 
        x,y:  положение центра снаряда
        bullet_type: тип снаряда, возможные: "bullet", "shell"
        sreen: экран на котором будет отображаться танк
        ang: Угол между направлением вектора скорости снаряда и горизонтом
        """
        
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.center = pos(x,y)
        self.ang = ang
        self.image_start = pygame.image.load(name_images[bullet_type]).convert_alpha() 
        self.image = self.image_start
        update_corner(self)
        self.mask = masks[bul]
        
        if bullet_type == "bullet":
            self.v = 10
        elif bullet_type == "shell":
            self.v = 15

        vx = self.v * math.cos(self.ang)
        vy = self.v * math.sin(-self.ang)
        self.velocity = pos(vx,vy)
        
    def check_board(self, WIDTH, HEIGHT):
        if self.x > WIDTH or self.x < 0 or self.y > HEIGHT or self.y < 0:
            return True
        else:
            return False
      
    def move(self):
        self.center.x += self.velocity.x
        self.center.y += self.velocity.y

    def draw(self):
        self.image = pygame.transform.rotate(self.image_start, self.ang*180/math.pi)
        update_corner(self)
        self.screen.blit(self.image, (self.corner.x, self.corner.y))
        

#class Shell:
#class Bullet:
