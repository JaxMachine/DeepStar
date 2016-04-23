import pygame

from maths.vector import Vector
from math import cos, sin, radians

from objects.game_object import BaseObject

from constants import SPRITE_MANAGER, BULLET_MANAGER


class PinkBullet(BaseObject):

    def __init__(self, angle, pos):
        BaseObject.__init__(self, "pink_bullet.png", pos, SPRITE_MANAGER.instance)
        rads = radians(angle)
        self.direction = Vector(sin(rads), cos(rads)).normal()
        self.delete = False

        BULLET_MANAGER.instance.add(self)
        self.speed = 30
        self.collided = False
        self._rotate(angle)

    def _rotate(self, angle):
        self.image = pygame.transform.rotate(self.image, angle)
        self.rect = self.image.get_rect()  # move rect to current pos?
        self.rect.centerx = self.pos.x
        self.rect.centery = self.pos.y

    def _get_new_pos(self, direction):
        new = self.pos - self.direction
        self.pos += (new - self.pos).normal() * self.speed
        return self.pos

    def move(self):
        self._get_new_pos(self.direction)
        super(PinkBullet, self).move()

        # delete if we are beyond the bounds of the room...
        if self.rect.right > 1280:
            self.delete = True
        if self.rect.left < -20:
            self.delete = True
        if self.rect.top < -20:
            self.delete = True
        if self.rect.bottom > 720:
            self.delete = True

        self.dirty = 1

    def update(self):
        if self.delete:
            BULLET_MANAGER.instance.remove(self)
            super(PinkBullet, self).delete()
        self.move()


class Bullet(BaseObject):

    def __init__(self, trajectory, pos):
        BaseObject.__init__(self, "Bullet.png", pos, SPRITE_MANAGER.instance)
        self.trajectory = trajectory

        self.delete = False
        self.redius = self.rect.centerx - self.rect.centery

        BULLET_MANAGER.instance.add(self)
        self.speed = 5
        self.collided = False

    def _get_new_pos(self, trajectory):
        new = self.pos - Vector(-trajectory[0], -trajectory[1])
        self.pos += (new - self.pos).normal() * self.speed
        return self.pos

    def move(self):
        self._get_new_pos(self.trajectory)
        super(Bullet, self).move()

        # delete if we are beyond the bounds of the room...
        if self.rect.right > 1280:
            self.delete = True
        if self.rect.left < -20:
            self.delete = True
        if self.rect.top < -20:
            self.delete = True
        if self.rect.bottom > 720:
            self.delete = True

        self.dirty = 1

    def update(self):
        if self.delete:
            BULLET_MANAGER.instance.remove(self)
            super(Bullet, self).delete()
        self.move()
