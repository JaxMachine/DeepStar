from constants import OBJECT_MANAGER
from maths.vector import Vector

from sprites.sprite import BaseSprite, BaseAnimatedSprite
from camera.camera_manager import CAMERA


class BaseAnimatedObject(BaseAnimatedSprite):

    def __init__(self, name, rows, cols, pos, sprite_group):
        BaseAnimatedSprite.__init__(
            self, name=name, rows=rows, cols=cols, colorkey=-1, sprite_group=sprite_group)
        OBJECT_MANAGER.instance.add(self)
        self.pos = Vector(pos[0], pos[1])
        self.rect.center = pos

    def move(self):
        self.rect.centerx, self.rect.centery = self.pos.x, self.pos.y
        offset = CAMERA.apply(self.rect)
        self.dirty = 1
        self.rect.x, self.rect.y = offset.x, offset.y


class BaseObject(BaseSprite):

    def __init__(self, sprite_name, pos=None, sprite_group=None):
        BaseSprite.__init__(self, sprite_name, sprite_group)
        OBJECT_MANAGER.instance.add(self)
        if pos is not None:
            self.rect.centerx = pos[0]
            self.rect.centery = pos[1]
        self.pos = Vector(pos[0], pos[1])

    def move(self):
        self.rect.centerx = self.pos.x
        self.rect.centery = self.pos.y
        # if self.name == "Bullet.png":
        #     CAMERA.update(self)
        offset = CAMERA.apply(self.rect)
        self.rect.x = offset.x
        self.rect.y = offset.y
        # if self.name != "Bullet.png":
            # self.dirty = 1
        self.dirty = 1

    def delete(self, remove=True):
        super(BaseObject, self).delete()
        if remove:
            OBJECT_MANAGER.instance.remove(self)
