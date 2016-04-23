
from objects.game_object import BaseObject

from camera.camera_manager import CAMERA

from constants import SPRITE_MANAGER, SCREEN


class CameraCenter(BaseObject):

    def __init__(self, sprite_name, target):
        BaseObject.__init__(self, sprite_name, (target.pos.x, target.pos.y), SPRITE_MANAGER.instance)
        self.target = target
        self.pos = self.target.pos
        self._update_pos()
        # self.dirty = 0

    # how should I do this?...

    def _update_pos(self):
        direction = self.target.getPlayerDirection()
        spawn_distance = -150
        # radi = self.target.radius
        self.pos = self.target.pos + (direction * spawn_distance)
        # p = self.target.pos + (direction * radi)
        # p = CAMERA.apply_point(p)
        # pygame.draw.circle(SCREEN, (0, p )

    def update(self):
        self._update_pos()
        self.move()

    def move(self):
        self.rect.centerx = self.pos.x
        self.rect.centery = self.pos.y
        CAMERA.update(self)
        offset = CAMERA.apply(self.rect)
        self.rect.x = offset.x
        self.rect.y = offset.y
        self.dirty = 1
