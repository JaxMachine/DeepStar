import pygame

from objects.game_object import BaseObject
from maths.vector import Circle
from math import atan2, degrees, pi

from constants import SPRITE_MANAGER


class PlayerOnPlanet(BaseObject):

    def __init__(self, sprite_name, controller, pos, planet):
        BaseObject.__init__(self, sprite_name, pos, SPRITE_MANAGER.instance)
        self.joystick = controller
        self.speed = 0
        self.planet = planet
        self.landed = False

    def deleteMe(self):
        super(PlayerOnPlanet, self).delete()

    def _get_new_landed_position(self):
        # read horizontal input
        return self.pos

    def _get_new_pos(self):
        new_pos = self.pos
        new_pos += (self.planet.pos - new_pos).normal() * 3
        if not self._collide(new_pos) and not self.landed:
            self.pos = new_pos
            if self.landed:
                if not self._collide(new_pos):
                    print("not colliding after landing")
        else:
            print("we are not update pos")
            print(self.rect)
            print(self.pos)
            self.pos = self._get_new_landed_position()

    def _collide_with_planet(self, rect):
        c = Circle(self.planet.rect.centerx, self.planet.rect.centery, self.planet.radius)
        if not c.intersects_rect(rect):
            return False
        self.landed = True
        return True

    def _collide(self, new_pos):
        copy = self.rect.copy()
        copy.x, copy.y = new_pos.x, new_pos.y
        collide = False
        if self._collide_with_planet(copy):
            collide = True
        else:
            collide = False
        return collide

    def _move_on_planet(self):
        # update position and rotation of sprite...
        # start with rotation
        dx = self.rect.centerx - self.planet.rect.centerx
        dy = self.rect.centery - self.planet.rect.centery
        rads = atan2(-dy, dx)
        rads %= 2*pi
        degs = degrees(rads)
        print("printing degrees")
        print(degs)
        self.image = pygame.transform.rotate(self.image, degs)

    def _check_inputs(self):
        if self.landed:
            self.left = self.joystick.get_left_axis()
            if self.left.x != 0:
                self._move_on_planet()

    def update(self):
        self._get_new_pos()
        self._check_inputs()
        self.move()
