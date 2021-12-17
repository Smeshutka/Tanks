from helper import *

pygame.init()

ARIAL_32 = pygame.font.SysFont('arial', 32)

class Button:
    '''класс кнопок'''

    def __init__(self, screen, x0, y0, a, b, type):
        '''screen: pygame.display
        x0,y0 - координаты левого верхнего угла относительно экрана
        a,b - размеры окна по x,y соотв.
        image - название файла в папке textures формата png'''
        self.screen = screen
        self.size = pos(a, b)
        self.pos = pos(x0, y0)
        self.type = type
        self.image = pygame.image.load('textures/buttons/' + type + '.png').convert_alpha()
        self.image_selected = pygame.image.load('textures/buttons/' + type + '_selected.png').convert_alpha()
        self.pressed = False

    def set_image(self, image):
        self.image = pygame.image.load('textures/buttons/' + image + '.png').convert_alpha()

    def draw(self, k=1):
        x0, y0 = self.pos.x, self.pos.y
        a0, b0 = self.size.x, self.size.y
        pygame.draw.rect(self.screen, (255, 255, 255), (x0, y0, a0, b0))
        if self.pressed:
            self.screen.blit(update_image(self.image_selected, a0 * k / a, b0 * k / a),
                             (self.pos.x, self.pos.y))
        else:
            self.screen.blit(update_image(self.image, a0 * k / a, b0 * k / a),
                             (self.pos.x, self.pos.y))

    def check_pressed(self):
        mx, my = pygame.mouse.get_pos()
        x0, y0 = self.pos.x, self.pos.y
        a, b = self.size.x, self.size.y
        if mx >= x0 and my >= y0 and mx <= x0 + a and my <= y0 + b:
            self.pressed = True
        else:
            self.pressed = False

    def trigger(self):
        if self.type == 'singleplayer':
            return 'menu_singleplayer()'
        elif self.type == 'multiplayer':
            return 'menu_multiplayer()'
        elif self.type == 'level_constructor':
            return 'level_constructor.level_constructor_main()'
        elif self.type == 'settings':
            return 'menu_settings()'
        elif self.type == 'exit_game':
            return 'exit()'
        elif self.type == 'go_back':
            return 'menu_main()'
        elif self.type == 'start_game':
            return 'game.game_main(game_input)'
        elif self.type == 'choose_level':
            return 'choose_level()'
        elif self.type == 'host_game':
            return 'server.server_main(ip_entry.text, port_entry.text)'
        elif self.type == 'join_game':
            return 'client.client_main(ip_entry.text, port_entry.text)'
        else:
            return 'print("in_progress")'



class Static:
    '''класс кнопок'''

    def __init__(self, screen, x0, y0, a, b, type):
        '''screen: pygame.display
        x0,y0 - координаты левого верхнего угла относительно экрана
        a,b - размеры окна по x,y соотв.
        image - название файла в папке textures формата png'''
        self.screen = screen
        self.size = pos(a, b)
        self.pos = pos(x0, y0)
        self.type = type
        self.image = pygame.image.load('textures/statics/' + type + '.png').convert_alpha()


    def set_image(self, image):
        self.image = pygame.image.load('textures/statics/' + image + '.png').convert_alpha()

    def draw(self, k=1):
        x0, y0 = self.pos.x, self.pos.y
        a0, b0 = self.size.x, self.size.y
        pygame.draw.rect(self.screen, (255, 255, 255), (x0, y0, a0, b0))
        self.screen.blit(update_image(self.image, a0 * k / a, b0 * k / a),
                         (self.pos.x, self.pos.y))

class Entry:
    def __init__(self, screen, x0, y0, a, b, text = '', bg_color = (0, 0, 0)):
        '''screen: pygame.display
        x0,y0 - координаты левого верхнего угла относительно экрана
        a,b - размеры окна по x,y соотв.
        image - название файла в папке textures формата png'''
        self.screen = screen
        self.size = pos(a, b)
        self.pos = pos(x0, y0)
        self.bg_color = bg_color
        self.text = text
        self.is_writing = False

    def draw(self, slash = False, k=1):
        x0, y0 = self.pos.x, self.pos.y
        a0, b0 = self.size.x, self.size.y
        if self.bg_color != None:
            pygame.draw.rect(self.screen, self.bg_color, (x0, y0, a0, b0))
        if self.is_writing and slash:
            text_out = ARIAL_32.render(self.text+'/', True, (255,255,255))
        else:
            text_out = ARIAL_32.render(self.text, True, (255, 255, 255))
        self.screen.blit(text_out, (x0 + (a0 / 2 - text_out.get_width() / 2), y0 + (b0 / 2 -
                                                                                    text_out.get_height() / 2)))

    def check_pressed(self):
        mx, my = pygame.mouse.get_pos()
        x0, y0 = self.pos.x, self.pos.y
        a, b = self.size.x, self.size.y
        if mx >= x0 and my >= y0 and mx <= x0 + a and my <= y0 + b:
            self.pressed = True
        else:
            self.pressed = False



    def trigger(self):
        if self.pressed:
            self.is_writing = True
        else:
            self.is_writing = False

    def writing(self, event):
        text_to_enter = ''
        for i in range(10):
            if event.key == eval('pygame.K_' + str(i)):
                text_to_enter = str(i)

        if self.is_writing:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[0:len(self.text) - 1]
            else:
                self.text += text_to_enter
