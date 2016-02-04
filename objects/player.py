import pygame
# from pygame.locals import *
from objects.bullet import Bullet
from assets.asset_loader import load_image


class Player(pygame.sprite.DirtySprite):

    def __init__(self, controller, pos=None):
        # call DirtySprite initializer
        pygame.sprite.DirtySprite.__init__(self)
        self.image, self.rect = load_image("DeepStar_Player.png", -1)
        # if passed a position, move it and mark it dirty..
        if pos is not None:
            self.rect.center = pos
            self.dirty = 1

        # make sure controller is initialized
        self.joystick = controller
        if not self.joystick.get_init():
            self.joystick.init()
        self.new_x = 0
        self.new_y = 0
        self.can_shoot = 1

    def get_rect(self):
        return self.rect

    def shoot(self):
        # have to figure out how to spread them out...
        self.can_shoot -= 1
        if self.can_shoot == 0:
            # shoot
            Bullet((self.new_x, self.new_y), self.rect)

            self.can_shoot = 10

    def move(self, left=None, right=None, top=None, bottom=None):
        # if left is None and right is None and top is None and bottom is None:
        #     pos = pygame.mouse.get_pos()
        #     self.rect.center = pos
        if left:
            self.rect.left += left
            if self.rect.left < 0:
                self.rect.left = 0
        if right:
            self.rect.right += right
            if self.rect.right > 640:
                self.rect.right = 640
        if top:
            self.rect.top += top
            if self.rect.top < 0:
                self.rect.top = 0
        if bottom:
            self.rect.bottom += bottom
            if self.rect.bottom > 480:
                self.rect.bottom = 480

        self.rect.left += (self.new_x * -5)
        self.rect.top += (self.new_y * -5)
        self.dirty = 1

    def update(self):
        self.new_x, self.new_y = self.joystick.get_right_axis()
        self.move()
