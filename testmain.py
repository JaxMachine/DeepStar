import pygame
from pygame.locals import *
import sys


pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.init()

from assets.asset_loader import load_image
from assets.level_loader import load_level

from constants import SCREEN_SIZE, OBJECT_MANAGER, SPRITE_MANAGER


class DeepStar:

    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.init()
        pygame.joystick.init()
        self.joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]

        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption('DeepStar')

        self.clock = pygame.time.Clock()

        if pygame.font:
            self.font = pygame.font.Font(None, 30)
        else:
            self.font = None

        self.init_game()

    # initialize game objects, etc..
    def init_game(self):
        # set game constants

        # create the background, blit it to the screen...
        self.background, self.background_pos = load_image("Map.png")
        self.screen.blit(self.background, (0, 0))

        load_level(self.joysticks)

        self.exit = False

    def update(self):
        for game_object in OBJECT_MANAGER.instance.list():
            game_object.update()

    def draw(self):
        rects = SPRITE_MANAGER.instance.draw(self.screen)
        pygame.display.update(rects)

    def run(self):
        SPRITE_MANAGER.instance.clear(self.screen, self.background)

        # for debug purposes...
        f = open("log3", 'a')
        sys.stdout = f
        while not self.exit:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit = True
            self.clock.tick(50)
            self.update()
            self.draw()
            # should call this once per game loop to ensure pygame talks to sys
            pygame.event.pump()
        f.close()
        sys.stdout = sys.__stdout__
        pygame.quit()

if __name__ == "__main__":
    game = DeepStar()
    game.run()
