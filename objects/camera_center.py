import pygame


from objects.game_object import BaseObject

from constants import SPRITE_MANAGER


class CameraCenter(BaseObject):

    def __init__(self, sprite_name, target):
        BaseObject.__init__(self, sprite_name, (target.pos.x, target.pos.y), SPRITE_MANAGER.instance)
        self.target = target
        self.pos = self.target.pos
        self._update_pos()
        # self.dirty = 0

    def _update_pos(self):
        direction = self.target.get_Player_Direction()
        spawn_distance = -100
        self.pos = self.target.pos + (direction * spawn_distance)

    def update(self):
        self._update_pos()
        self.move()
