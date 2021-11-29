import sys

import pygame
from constans import*
from game import *

window = pygame.display.set_mode((WIDTH, HEIGHT))
screen1 = pygame.display.set_mode((WIDTH, HEIGHT))
'''
class Button:
    def __init__(self, screen, pos:pos, size:pos, text, command):
        self.screen = screen
        self.text = text
        self.size = size
        self.pos = pos
        self.command = command
    def draw(self):

    def check_pressed(self):

    def call_func(self):
'''
class Menu:
    def __init__(self, punkts):
        self.punkts=punkts
    def render(self, poverhnost, font, num_punkt):
        for i in self.punkts:
            if num_punkt==i[5]:
                poverhnost.blit(font.render(i[2], 1, i[4]), (i[0], i[1]))
            else:
                poverhnost.blit(font.render(i[2], 1, i[3]), (i[0], i[1]))
    def menu(self):
        done=True
        font_menu = pygame.font.SysFont('arial', 25)
        #font_menu = pygame.font.Font("C:\Users\Admin\Tanks\BriosoPro Italic.otf", 50)
        punkt=0
        while done:
            screen1.fill(0, 100, 200)
            mp=pygame.mouse.get.pos()
            for i in self.punkts:
                if mp[0]>i[0] and mp[0]<i[0]+155 and mp[1]>i[1] and mp[1]<i[1]+50:
                    punkt = i[5]
                self.render(screen, font_menu, punkt)

            for e in pygame.event.get():
                if e.type==pygame.QUIT:
                    sys.exit()
                if e.type==pygame.KEYDOWN:
                    if e.type==pygame.K_ESCAPE:
                        sys.exit()
                if e.key == pygame.K_UP:
                    if punkt>0:
                        punkt-=1
                    if e.key == pygame.K_DOWN:
                        if punkt<len(self.punkts)-1:
                            punkt+=1
                if e.type==pygame.MOUSEBUTTON and e.button==1:
                    if punkt==0:
                        done = False
                    elif punkt==1:
                        sys.exit
        window.blit(screen, (0, 0))
        pygame.dislplay.flip()


punkts=[(120, 140, u"singleplayer", (250, 250, 30), (250, 30, 250), 0), \
                (130, 210, u"settings", (250, 250, 30), (250, 30, 250), 1)]
game = Menu(punkts)
game.menu()