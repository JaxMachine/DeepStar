import pygame
pygame.init()


class Clock():

    def __init__(self):
        self.clock = pygame.time.Clock()
        self.elasped = 0

    def tick(self, framerate=None):
        self.elasped = self.clock.tick(framerate)

    def get_elasped(self):
        return self.elasped
