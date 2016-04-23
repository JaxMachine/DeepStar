import pygame

SCREEN_SIZE = WIDTH, HEIGHT = 1280, 720
HALF_WIDTH = int(WIDTH/2)
HALF_HEIGHT = int(HEIGHT/2)

# from constants import SCREEN


class Camera(object):

    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = pygame.Rect(0, 0, width, height)
        self.inner_rect = pygame.Rect(HALF_WIDTH/1.5, HALF_HEIGHT/1.5, HALF_WIDTH/2, HALF_HEIGHT/2)

    def apply(self, rect):
        new_rect = rect.copy()
        new_rect.centerx = new_rect.centerx + self.state.x
        new_rect.centery = new_rect.centery - self.state.y
        return new_rect

    def apply_points(self, point_list):
        new = []
        for point in point_list:
            new_point = (point[0] + self.state.x,  point[1] - self.state.y)
            new.append(new_point)
        return new

    def apply_point(self, point):
        new = (point[0] + self.state.x, point[1] - self.state.y)
        return new

    def update(self, target):
        temp = self.camera_func(self, target.rect, self.inner_rect)
        if temp is not None:
            self.state = temp
        # self.state = self.camera_func(self.state, target.rect)
        # self.state = self.camera_func(self.state, target)
