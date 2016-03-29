from constants import OBJECT_MANAGER
from maths.vector import Vector

from sprites.sprite import BaseSprite
from camera.camera_manager import CAMERA


class BaseObject(BaseSprite):

    def __init__(self, sprite_name, pos=None, sprite_group=None):
        BaseSprite.__init__(self, sprite_name, sprite_group)
        OBJECT_MANAGER.instance.add(self)
        print("printing initial pos")

        if pos is not None:
            # print("setting center")
            self.rect.center = pos

        self.pos = Vector(pos[0], pos[1])
        self.speed = self.hspeed, self.vspeed = 0, 0

    def move(self):
        self.rect.centerx = self.pos.x
        self.rect.centery = self.pos.y
        if self.name == "Bullet.png":
        # if self.name == "ShipSprite.png":
            CAMERA.update(self)
        offset = CAMERA.apply(self.rect)
        self.rect.centerx = offset.x
        self.rect.centery = offset.y
        # if self.name != "Bullet.png":
        self.dirty = 1

    def delete(self, remove=True):
        super(BaseObject, self).delete()
        if remove:
            OBJECT_MANAGER.instance.remove(self)
