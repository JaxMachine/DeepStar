import pygame
from pygame.locals import *
import sys


pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.init()

from assets.level_loader import load_level

from camera.camera_manager import CAMERA
from objects.test_animation import TestAnimation

from constants import OBJECT_MANAGER, SPRITE_MANAGER, SCREEN, CLOCK

from misc.paralax_background import move_and_draw_stars, init_stars


class DeepStar:

    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.init()

        pygame.joystick.init()
        self.joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]

        pygame.display.set_caption('DeepStar')

        self.clock = CLOCK
        # self.test = TestAnimation(pos=(400, 400))

        if pygame.font:
            self.font = pygame.font.Font(None, 30)
        else:
            self.font = None

        self.init_game()

    # initialize game objects, etc..
    def init_game(self):
        # set game constants
        SCREEN.fill((0, 0, 0))
        init_stars(SCREEN)

        load_level(self.joysticks)

        self.exit = False

    def update(self):
        for game_object in OBJECT_MANAGER.instance.list():
            game_object.update()
        # self.test.update()

    def draw(self):
        rects = SPRITE_MANAGER.instance.draw(SCREEN)
        pygame.display.update(rects)
        pygame.display.flip()

    def run(self):
        # SPRITE_MANAGER.instance.clear(SCREEN, BACKGROUND)

        # for debug purposes...
        f = open("log3", 'a')
        sys.stdout = f

        while not self.exit:
            SCREEN.fill((0, 0, 0))
            move_and_draw_stars(SCREEN, CAMERA)
            # pygame.draw.rect(SCREEN, (255, 0, 0), CAMERA.inner_rect, 2)
            # pygame.display.flip()
            # SCREEN.blit(BACKGROUND, BACKGROUND_POS)

            # SPRITE_MANAGER.instance.clear(SCREEN, BACKGROUND)
            # print("Background pos")
            # print(BACKGROUND_POS)
            pygame.draw.rect(SCREEN, (255, 0, 0), CAMERA.inner_rect, 1)

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
