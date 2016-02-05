import pygame
from pygame.locals import *
import usb
import sys
import os


pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.init()

from assets.asset_loader import load_image
from assets.level_loader import load_level

from constants import SCREEN_SIZE, OBJECT_MANAGER, SPRITE_MANAGER, BULLET_MANAGER, PLANET_MANAGER


class DeepStar:

    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.init()
        pygame.joystick.init()
        self.joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]

        # self.screen = pygame.display.set_mode(SCREEN_SIZE, HWSURFACE | DOUBLEBUF | RESIZABLE)
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption('DeepStar')

        self.clock = pygame.time.Clock()

        if pygame.font:
            self.font = pygame.font.Font(None, 30)
        else:
            self.font = None

        self.init_game()

    def check_if_connected(self):
        try:
            busses = usb.busses()
            for bus in busses:
                devices = bus.devices
                for dev in devices:
                    if dev.idVendor == 1356:
                        return True
            return False
        except usb.core.USBError:
            print("USB Disconnected")
            return False

    # initialize game objects, etc..
    def init_game(self):
        # set game constants
        self.prev_mouse_pos = (0, 0)
        # self.controller = PS3_Controller(self.screen)
        if self.check_if_connected():
            print("conntected")
        else:
            print("not connected")

        # create the background, blit it to the screen...
        self.background, self.background_pos = load_image("Map.png")
        self.screen.blit(self.background, (0, 0))

        # init all game objects... // only one list
        self.game_objects = OBJECT_MANAGER.instance.list()
        self.game_objects = load_level(self.joysticks)

        self.exit = False

    def check_inputs(self):
        player = self.game_objects[0]
        player.update()

    def update(self):
        for game_object in OBJECT_MANAGER.instance.list():
            f = open("log3", 'a')
            sys.stdout = f
            # if game_object.name == "player":
            #     print("updating player")
            # print(game_object.name)
            game_object.update()
            f.close()
            sys.stdout = sys.__stdout__

    def draw(self):
        rects = SPRITE_MANAGER.instance.draw(self.screen)
        pygame.display.update(rects)

        # other dirty sprites..

    def run(self):
        SPRITE_MANAGER.instance.clear(self.screen, self.background)
        # allsprites.clear(screen, background)
        while not self.exit:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit = True
                # elif event.type == VIDEORESIZE:
                #     self.screen = pygame.display.set_mode(event.dict['size'], HWSURFACE | DOUBLEBUF | RESIZABLE)
                #     self.screen.blit(pygame.transform.scale(self.background, event.dict['size']), (0, 0))

            self.clock.tick(50)

            # get player inputs..
            self.check_inputs()
            self.update()
            self.draw()

        pygame.quit()

if __name__ == "__main__":
    game = DeepStar()
    game.run()
