import pygame

from maths.vector import Vector
from assets.asset_loader import load_image
from constants import OBJECT_MANAGER, SPRITE_MANAGER, BULLET_MANAGER


class Bullet(pygame.sprite.DirtySprite):

    def __init__(self, trajectory, pos=None):
        # call DirtySprite initializer, add to sprite manager
        pygame.sprite.DirtySprite.__init__(self, SPRITE_MANAGER.instance)
        self.image, self.rect = load_image("Bullet.png", -1)
        self.trajectory = trajectory

        # if pass a position, move it and mark it dirty..
        if pos is not None:
            self.rect.center = pos
            self.dirty = 1
            self.pos = Vector(self.rect.x, self.rect.y)

        self.delete = False
        self.name = "Bullet"
        self.radius = self.rect.centerx - self.rect.x
        OBJECT_MANAGER.instance.add(self)
        BULLET_MANAGER.instance.add(self)
        self.dirty = 1
        self.speed = 5
        self.collided = False

    def get_rect(self):
        return self.rect

    def _get_new_pos(self, trajectory):
        new = self.pos - Vector(-trajectory[0], -trajectory[1])
        self.pos += (new - self.pos).normal() * self.speed
        return self.pos

    def move(self):
        new_pos = self._get_new_pos(self.trajectory)
        self.rect.x = new_pos.x
        self.rect.y = new_pos.y

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
            OBJECT_MANAGER.instance.remove(self)
            self.kill()


        self.move()
