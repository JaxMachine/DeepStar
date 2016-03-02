import pygame

from objects.game_object import BaseObject
from maths.vector import Circle
from math import atan2, degrees, pi, cos, sin

from constants import SPRITE_MANAGER

import objects.player_utils

ANGULAR_VELOCITY = 0.05


class PlayerOnPlanet(BaseObject):

    def __init__(self, sprite_name, controller, pos, planet):
        BaseObject.__init__(self, sprite_name, pos, SPRITE_MANAGER.instance)
        self.joystick = controller
        self.speed = 0
        self.planet = planet
        self.landed = False
        self.got_angle = False
        self.radius = self.rect.centerx - self.rect.x
        self.old_image = self.image
        self.taking_off = False

    def deleteMe(self):
        super(PlayerOnPlanet, self).delete()
        objects.player_utils.create_player("DeepStar_Player2.png", self.joystick, self.pos.to_tuple())

    def _take_off(self):
        # get new vector from planet and player
        dist = (self.pos - self.planet.pos).length()

        if dist < self.planet.radius + 50:
            new_pos = self.pos
            new_pos -= (self.planet.pos - new_pos).normal() * 3
            self.pos = new_pos
        else:
            self.delete = True

    def _get_new_pos(self):
        if not self.landed:
            new_pos = self.pos
            new_pos += (self.planet.pos - new_pos).normal() * 3
            if not self._collide(new_pos) and not self.landed:
                self.pos = new_pos
                if self.landed:
                    if not self._collide(new_pos):
                        print("not colliding after landing")
        if self.taking_off:
            self._take_off()

    def _collide_with_planet(self, rect):
        c = Circle(self.planet.rect.centerx, self.planet.rect.centery, self.planet.radius)
        if not c.intersects_rect(rect):
            return False
        self._adjust_angle(-self._get_angle_planet() * (180/pi))
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

    def _adjust_angle(self, angle):
        self.image = pygame.transform.rotate(self.old_image, angle)
        self.rect = self.image.get_rect()

    def _get_angle_planet(self):
        dx = self.rect.centerx - self.planet.rect.centerx
        dy = self.rect.centery - self.planet.rect.centery
        rads = atan2(dy, dx)
        rads %= 2*pi
        return rads

    def _move_on_planet(self):
        if not self.got_angle:
            self.cur_angle = self._get_angle_planet()
            self.got_angle = True
        else:
            if self.left.x < 0:
                self.cur_angle -= ANGULAR_VELOCITY
            else:
                self.cur_angle += ANGULAR_VELOCITY
        self._adjust_angle(-self.cur_angle * (180/pi))
        self.pos.x = self.planet.rect.centerx + (cos(self.cur_angle) * (self.planet.radius + self.radius))
        self.pos.y = self.planet.rect.centery + (sin(self.cur_angle) * (self.planet.radius + self.radius))

    def _check_inputs(self):
        if self.landed and not self.taking_off:
            self.left = self.joystick.get_left_axis()
            if self.left.x != 0 or self.left.y != 0:
                self._move_on_planet()
            if self.joystick.get_action_button():
                self.taking_off = True
            self.joystick.done_with_input()

    def update(self):
        if self.delete:
            self.deleteMe()
        self._check_inputs()
        self._get_new_pos()
        self.move()
