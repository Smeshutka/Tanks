from Tanks.helper import*

class vision(pygame.sprite.Sprite):
    def __init__(self, owner, screen):
        """
        """

        pygame.sprite.Sprite.__init__(self)
        self.owner = owner
        self.screen = screen
        self.image = pygame.image.load('textures/visibility.png').convert_alpha()
        a, b = self.image.get_size()
        self.corner = pos(self.owner.center.x - a/2, self.owner.center.y - b/2)
        self.rect = self.image.get_rect()

    def draw(self):
        self.screen.blit(self.image, (self.corner.x, self.corner.y))

    def meet_with_tank(self, tank):
        """Обработка пересечения с игроком"""
        if meet(tank, self):
            self.owner.turn_turret(tank.center.x, tank.center.y)
            self.owner.reload_left()
            self.owner.fire_gun()
