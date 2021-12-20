import unittest
import button_class as b
import pygame


class test_Button(unittest.TestCase):
    def setUp(self):

        screen = pygame.display.set_mode((800, 600))
        self.button = b.Button(screen, 300, 220, 250, 100,  'music')

    def test_set_image(self):
        img = 'music'
        self.button.set_image(img)

    def test_draw(self):
        a=1

    def test_check_presed(self):
        a=1

    def test_trigger(self):
        a=1

    def test_set_bg_color(self):
        bg_colour='metall'
        self.button.set_bg_color(bg_colour)

if __name__ == '__main__':
    unittest.main()
