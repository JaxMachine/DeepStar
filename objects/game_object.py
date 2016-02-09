import pygame

from constants import OBJECT_MANAGER
from maths.vector import Vector

from sprites.sprite import BaseSprite


class BaseObject(BaseSprite):

    def __init__(self, sprite_name, pos=None):
        BaseSprite.__init__(self, sprite_name)
        OBJECT_MANAGER.add(self)

        if pos is not None:
            self.rect.center = pos

        self.pos = Vector(self.rect.centerx, self.rect.centery)
        self.speed = self.hspeed, self.vspeed = 0, 0

    def move(self):
        self.rect.centerx = self.pos.x
        self.rect.centery = self.pos.y
        self.dirty = 1

    def delete(self, remove=True):
        super(BaseSprite, self).delete()
        if remove:
            OBJECT_MANAGER.remove(self)
