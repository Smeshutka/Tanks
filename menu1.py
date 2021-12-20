import sys
from button_class import *
import game
import level_constructor
import map_maker.map_input
import tkinter
import server
import client
from tank_class import *

'''Функции окон меню'''


def menu_main():
    pygame.init()

    screen = pygame.display.set_mode((w, h))
    clock = pygame.time.Clock()

    finished = False

    menu = Static(screen, 0, 0, w, h, 'metal')
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
                exit()
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    for button in buttons:
                        if button.pressed:
                            eval(button.trigger())

        pygame.display.update()

        clock.tick(FPS)


def menu_singleplayer():


    def back_stage():
        menu_main()

    pygame.init()

    global game_input
    global tank_type
    game_input = "map_maker/maps/1.txt"
    tank_type = 'light'

    screen = pygame.display.set_mode((w, h))
    clock = pygame.time.Clock()

    finished = False

    menu = Static(screen, 0, 0, w, h, 'metal')
    button1 = Button(screen, 10, 10, 150, 50, 'go_back')
    button2 = Button(screen, 250, 490, 300, 100, 'start_game')
    button3 = Button(screen, 550, 350, 200, 66, 'choose_level')
    tank1 = Button(screen, 20, 200, 100, 200, 'tank_light')
    tank2 = Button(screen, 170, 200, 100, 200, 'tank_middle')
    tank3 = Button(screen, 320, 200, 119, 200, 'tank_heavy')
    level_text = Entry(screen, 525, 250, 250, 66, game_input)
    buttons = [button1, button2, button3, tank1, tank2, tank3]

    while not finished:
        screen.fill((0, 0, 0))

        menu.draw()
        for button in buttons:
            button.check_pressed()
            button.draw()

        level_text.change_text(game_input)
        level_text.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    for button in buttons:
                        if button.pressed:
                            button.set_bg_color((255, 255, 0))
                            eval(button.trigger())
                        else:
                            button.set_bg_color(None)

        pygame.display.update()

        clock.tick(FPS)


def menu_multiplayer():

    def back_stage():
        menu_main()

    time_meazure = 0
    pygame.init()

    screen = pygame.display.set_mode((w, h))
    clock = pygame.time.Clock()

    finished = False

    menu = Static(screen, 0, 0, w, h, 'metal')
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


def menu_multiplayer_host():

    def back_stage():
        menu_multiplayer()

    def start_function():
        server.server_main(ip_entry.text, port_entry.text, game_input, players_entry.text)

    time_meazure = 0
    pygame.init()

    global game_input
    game_input = "map_maker/maps/1.txt"

    screen = pygame.display.set_mode((w, h))
    clock = pygame.time.Clock()

    finished = False

    menu = Static(screen, 0, 0, w, h, 'metal')
    button1 = Button(screen, 10, 10, 150, 50, 'go_back')
    button2 = Button(screen, 100, 250, 200, 66, 'choose_level')
    button3 = Button(screen, 250, 490, 300, 100, 'start_game')
    ip_entry = Entry(screen, 100, 400, 200, 50)
    port_entry = Entry(screen, 500, 400, 200, 50)
    players_entry = Entry(screen, 500, 250, 200, 50)
    level_text = Entry(screen, 75, 150, 250, 66, game_input)
    ip_text = Entry(screen, 100, 350, 200, 50, 'IP', None)
    port_text = Entry(screen, 500, 350, 200, 50, 'port', None)
    players_text = Entry(screen, 500, 200, 200, 50, 'amount of players', None)

    buttons = [button1, button2, button3]
    entries = [ip_entry, port_entry, players_entry]
    text = [ip_text, port_text, players_text]

    while not finished:
        screen.fill((0, 0, 0))

        menu.draw()
        for button in buttons:
            button.check_pressed()
            button.draw()

        for entry in entries:
            entry.check_pressed()
            if (time_meazure // 1 % 2) == 0:
                entry.draw(True)
            else:
                entry.draw()

        for t in text:
            t.draw()

        level_text.change_text(game_input)
        level_text.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    for button in buttons:
                        if button.pressed:
                            eval(button.trigger())
                    for entry in entries:
                        entry.trigger()
            if event.type == pygame.KEYUP:
                ip_entry.writing(event, True)
                port_entry.writing(event)
                players_entry.writing(event)

        pygame.display.update()

        time_meazure += 2 / FPS
        clock.tick(FPS)


def menu_multiplayer_join():

    def back_stage():
        menu_multiplayer()

    def start_function():
        client.client_main(ip_entry.text, port_entry.text, tank_type)

    time_meazure = 0
    pygame.init()

    global tank_type
    tank_type = 'light'

    screen = pygame.display.set_mode((w, h))
    clock = pygame.time.Clock()

    finished = False

    menu = Static(screen, 0, 0, w, h, 'metal')
    button1 = Button(screen, 10, 10, 150, 50, 'go_back')
    button2 = Button(screen, 250, 490, 300, 100, 'start_game')
    tank1 = Button(screen, 220, 150, 100, 200, 'tank_light')
    tank2 = Button(screen, 370, 150, 100, 200, 'tank_middle')
    tank3 = Button(screen, 520, 150, 119, 200, 'tank_heavy')
    ip_entry = Entry(screen, 100, 400, 200, 50)
    port_entry = Entry(screen, 500, 400, 200, 50)
    ip_text = Entry(screen, 100, 350, 200, 50, 'IP', None)
    port_text = Entry(screen, 500, 350, 200, 50, 'port', None)

    buttons = [button1, button2, tank1, tank2, tank3]
    entries = [ip_entry, port_entry]
    text = [ip_text, port_text]

    while not finished:
        screen.fill((0, 0, 0))

        menu.draw()
        for button in buttons:
            button.check_pressed()
            button.draw()

        for entry in entries:
            entry.check_pressed()
            if (time_meazure // 1 % 2) == 0:
                entry.draw(True)
            else:
                entry.draw()

        for t in text:
            t.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    for button in buttons:
                        if button.pressed:
                            button.set_bg_color((255, 255, 0))
                            eval(button.trigger())
                        else:
                            button.set_bg_color(None)
                    for entry in entries:
                        entry.trigger()
            if event.type == pygame.KEYUP:
                ip_entry.writing(event, True)
                port_entry.writing(event)

        pygame.display.update()

        time_meazure += 2 / FPS
        clock.tick(FPS)


def menu_settings():

    def back_stage():
        menu_main()

    pygame.init()

    screen = pygame.display.set_mode((w, h))
    clock = pygame.time.Clock()

    finished = False

    menu = Static(screen, 0, 0, w, h, 'metal')
    button1 = Button(screen, 300, 100, 250, 100, 'go_back')
    button2 = Button(screen, 300, 220, 250, 100, 'music')
    buttons = [button1, button2]

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


def music():

    def back_stage():
        menu_settings()

    def volume_change():
        x, y = pygame.mouse.get_pos()
        button5.size.x = x - button5.pos.x
        button6.pos.x = x - 10
        pygame.mixer.music.set_volume(1.9 * (button5.size.x / button4.size.x))

    pygame.init()

    screen = pygame.display.set_mode((w, h))
    clock = pygame.time.Clock()

    finished = False

    menu = Static(screen, 0, 0, w, h, 'metal')
    button1 = Button(screen, 270, 100, 250, 100, 'go_back')
    button2 = Button(screen, 140, 250, 250, 100, 'on')
    button3 = Button(screen, 400, 250, 250, 100, 'off')
    button4 = Button(screen, 140, 400, 500, 40, 'volume')
    button5 = Button(screen, 140, 400, 200, 40, 'volumehight')
    button6 = Button(screen, 340, 400, 20, 40, 'slide')

    buttons = [button1, button2, button3, button4, button5, button6]



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


def death():
    pygame.init()

    screen = pygame.display.set_mode((w, h))
    clock = pygame.time.Clock()

    finished = False

    menu = Static(screen, 0, 0, w, h, 'game_over')
    button1 = Button(screen, 325, 400, 150, 50, 'restart')
    button2 = Button(screen, 325, 470, 150, 50, 'to_main_menu')
    buttons = [button1, button2]

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


def win():
    pygame.init()

    screen = pygame.display.set_mode((w, h))
    clock = pygame.time.Clock()

    finished = False

    menu = Static(screen, 0, 0, w, h, 'floppa_win')
    button1 = Button(screen, 325, 400, 150, 50, 'restart')
    button2 = Button(screen, 325, 470, 150, 50, 'to_main_menu')
    buttons = [button1, button2]

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


'''Вспомогательные функции'''


def choose_level():
    root = tkinter.Tk()
    new_map = tkinter.filedialog.askopenfilename(filetypes=(("Text file", ".txt"),))
    root.destroy()
    global game_input
    if new_map != '':
        splited_path = new_map.split('/')
        for i in range(len(splited_path)):
            if splited_path[i] == 'Tanks':
                game_input = splited_path[i + 1]
                for j in range(i + 2, len(splited_path)):
                    game_input += '/' + splited_path[j]


def start_function():
    ending = game.game_main(game_input, tank_type)
    if ending != None:
        eval(ending)


def set_tank_type(type):
    global tank_type
    tank_type = type

def on():
    pygame.mixer.music.load("music/1.mp3")
    pygame.mixer.music.set_volume(0.7)
    pygame.mixer.music.play()
def off():
    pygame.mixer.music.pause()


menu_main()
