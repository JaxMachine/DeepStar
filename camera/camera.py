import pygame

SCREEN_SIZE = WIDTH, HEIGHT = 1280, 720
HALF_WIDTH = int(WIDTH/2)
HALF_HEIGHT = int(HEIGHT/2)


class Camera(object):

    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = pygame.Rect(0, 0, width, height)
        self.inner_rect = pygame.Rect(HALF_WIDTH/2, HALF_HEIGHT/2, HALF_WIDTH, HALF_HEIGHT)

    def apply(self, rect):
        new_rect = rect.copy()
        new_rect.centerx = new_rect.centerx + self.state.x
        new_rect.centery = new_rect.centery - self.state.y
        return new_rect

    def update(self, target):
        temp = self.camera_func(self, target.rect, self.inner_rect)
        if temp is not None:
            self.state = temp
        # self.state = self.camera_func(self.state, target.rect)
