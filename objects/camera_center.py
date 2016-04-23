import pygame

from objects.game_object import BaseObject

from camera.camera_manager import CAMERA

from constants import SPRITE_MANAGER, SCREEN


class CameraCenter(BaseObject):

    def __init__(self, sprite_name, target):
        BaseObject.__init__(self, sprite_name, (target.pos.x, target.pos.y), SPRITE_MANAGER.instance)
        self.target = target
        self.pos = self.target.pos
        self.current_dist = self.target.radius
        self._update_pos()

        # self.dirty = 0

    # how should I do this?...

    def _update_pos(self):
        min_dist = self.target.radius - 5
        max_dist = 350
        if self.target.IsMoving():
            if self.current_dist < 200:
                self.current_dist += 5
            else:
                self.current_dist += 1
            if self.current_dist > max_dist:
                self.current_dist = max_dist
        else:
            self.current_dist -= 10
            if self.current_dist < min_dist:
                self.current_dist = min_dist

        direction = self.target.getPlayerDirection()
        # spawn_distance = -300
        # radi = self.target.radius
        self.pos = self.target.pos + (direction * -self.current_dist)
        # p = self.target.pos + (direction * -self.current_dist)
        # p = CAMERA.apply_point((int(p.x), int(p.y)))
        p = self.target.pos + (direction * -min_dist)
        p = CAMERA.apply_point((int(p.x), int(p.y)))
        pygame.draw.circle(SCREEN, (0, 255, 255), p, 5)

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
