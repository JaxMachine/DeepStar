import pygame
# from pygame.locals import *
import sys
from objects.bullet import Bullet
from assets.asset_loader import load_image

from maths.vector import Vector

from constants import SPRITE_MANAGER


class Player(pygame.sprite.DirtySprite):

    def __init__(self, controller, pos=None):
        # call DirtySprite initializer
        pygame.sprite.DirtySprite.__init__(self, SPRITE_MANAGER.instance)
        self.image, self.rect = load_image("DeepStar_Player.png", -1)
        if pos is not None:
            self.rect.center = pos
            self.dirty = 1
        self.name = "player"
        # make sure controller is initialized
        self.joystick = controller
        if not self.joystick.get_init():
            self.joystick.init()
        self.new_x = 0
        self.new_y = 0
        self.can_shoot = 1

        self.pos = Vector(self.rect.x, self.rect.y)
        self.trajectory = Vector(0, 0)
        self.updated_trajectory = False

        # new code
        self.vspeed = 0
        self.hspeed = 0
        self.old_hspeed = 0
        self.old_vspeed = 0

    def get_rect(self):
        return self.rect

    def shoot(self):
        self.can_shoot -= 1
        if self.can_shoot == 0:
            self.can_shoot = 5
            if self.new_x != 0 or self.new_y != 0:
                Bullet((self.new_x, self.new_y), (self.rect.x, self.rect.y))

                self.old_hspeed = self.hspeed
                self.old_vspeed = self.vspeed
                if self.new_x > 0:
                    self.hspeed += .2
                else:
                    self.hspeed -= .2
                if self.new_y > 0:
                    self.vspeed += .2
                else:
                    self.vspeed -= .2

    def pn(self, name, vector):
        out = "{0}: ({1}, {2})".format(name, vector.x, vector.y)
        print(out)

    def move(self, left=None, right=None, top=None, bottom=None):
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

        self.rect.x = self.pos.x
        self.rect.y = self.pos.y
        self.dirty = 1

    def _get_new_pos(self):
        new = self.pos - self.trajectory
        self.pos += (new - self.pos).normal().mult(self.hspeed, self.vspeed)
        return self.pos

    def update_trajectory(self):
        self.new_x, self.new_y = self.joystick.get_right_axis()

        if self.new_x != 0 or self.new_y != 0:
            if self.trajectory.x == 0:
                self.trajectory.x = self.new_x
            if self.trajectory.y == 0:
                self.trajectory.y = self.new_y

            if self.old_hspeed > 0 and self.hspeed < 0:  # that means we have switched directions, get a new trajecorty
                self.trajectory.x = self.new_x
            elif self.old_hspeed < 0 and self.hspeed > 0:  # that means we have switched directios, get a new trajectory
                self.trajectory.x = self.new_x

            if self.old_vspeed > 0 and self.vspeed < 0:  # that means we have switched directions, get a new trajecorty
                self.trajectory.y = self.new_y
            elif self.old_vspeed < 0 and self.vspeed > 0:  # that means we have switched directios, get a new trajectory
                self.trajectory.y = self.new_y

            if self.trajectory.x < 0:
                self.trajectory.x *= -1
            if self.trajectory.y < 0:
                self.trajectory.y *= -1
            self.updated_trajectory = True

    def update(self):
        self.update_trajectory()
        if self.updated_trajectory:
            self._get_new_pos()

        self.move()
        self.shoot()
