from maths.vector import Vector

from objects.game_object import BaseObject

from constants import SPRITE_MANAGER, BULLET_MANAGER


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
