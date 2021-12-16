from button_class import *
import game
import level_constructor
import map_maker.map_input
import tkinter

game_input = "map_maker/maps/1.txt"

def menu_main():
    pygame.init()

    screen = pygame.display.set_mode((w, h))
    clock = pygame.time.Clock()

    finished = False

    menu = Static(screen, 0, 0, w, h, 'metall')
    button1 = Button(screen, 250, 10, 300, 100, 'singleplayer')
    button2 = Button(screen, 250, 130, 300, 100, 'multiplayer')
    button3 = Button(screen, 250, 250, 300, 100, 'level_constructor')
    button4 = Button(screen, 250, 370, 300, 100, 'settings')
    button5 = Button(screen, 250, 490, 300, 100, 'exit_game')
    buttons = [button1, button2, button3, button4, button5]

    while not finished:
        screen.fill((0, 0, 0))

        menu.draw()
        for button in buttons:
            button.check_pressed()
            button.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    for button in buttons:
                        if button.pressed:
                            eval(button.trigger())


        pygame.display.update()

        clock.tick(FPS)


def menu_singleplayer():
    pygame.init()

    screen = pygame.display.set_mode((w, h))
    clock = pygame.time.Clock()

    finished = False

    menu = Static(screen, 0, 0, w, h, 'metall')
    button1 = Button(screen, 10, 10, 150, 50, 'go_back')
    button2 = Button(screen, 250, 490, 300, 100, 'start_game')
    button3 = Button(screen, 550, 350, 200, 66, 'choose_level')
    buttons = [button1, button2, button3]

    while not finished:
        screen.fill((0, 0, 0))

        menu.draw()
        for button in buttons:
            button.check_pressed()
            button.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    for button in buttons:
                        if button.pressed:
                            eval(button.trigger())

        pygame.display.update()

        clock.tick(FPS)

def menu_multiplayer():
    pygame.init()

    screen = pygame.display.set_mode((w, h))
    clock = pygame.time.Clock()

    finished = False

    menu = Static(screen, 0, 0, w, h, 'metall')
    button1 = Button(screen, 10, 10, 150, 50, 'go_back')
    button2 = Button(screen, 250, 100, 300, 100, 'host_game')
    button3 = Button(screen, 250, 220, 300, 100, 'join_game')
    buttons = [button1, button2, button3]

    while not finished:
        screen.fill((0, 0, 0))

        menu.draw()
        for button in buttons:
            button.check_pressed()
            button.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    for button in buttons:
                        if button.pressed:
                            eval(button.trigger())

        pygame.display.update()

        clock.tick(FPS)

def menu_settings():
    pygame.init()

    screen = pygame.display.set_mode((w, h))
    clock = pygame.time.Clock()

    finished = False

    menu = Static(screen, 0, 0, w, h, 'metall')
    button1 = Button(screen, 10, 10, 150, 50, 'go_back')
    buttons = [button1]

    while not finished:
        screen.fill((0, 0, 0))

        menu.draw()
        for button in buttons:
            button.check_pressed()
            button.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    for button in buttons:
                        if button.pressed:
                            finished = button.trigger()

        pygame.display.update()

        clock.tick(FPS)

def choose_level():
    root = tkinter.Tk()
    new_map = tkinter.filedialog.askopenfilename(filetypes=(("Text file", ".txt"),))
    root.destroy()
    global game_input
    if new_map != '':
        game_input = new_map

menu_main()