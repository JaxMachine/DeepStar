import pygame

from objects.game_object import BaseObject

from maths.vector import Vector

from constants import SPRITE_MANAGER

from math import atan2, pi, cos, sin, radians

ANGULAR_VELOCITY = 5
SPEED_GROWTH = .1
SPEED_CHANGE = 3
MAX_SPEED = 5
SPEED = 1


class TestPilot(BaseObject):

    def __init__(self, sprite_name, controller, pos):
        BaseObject.__init__(self, sprite_name, pos, SPRITE_MANAGER.instance)

        self.old_image = self.image
        self.joystick = controller
        # in degrees, 0 is top, 90 is left, 180 is down, 270 is right
        self.facing_direction = 0
        self.moving_direction = 0
        self._rotate(self.facing_direction)
        self.trajectory = Vector(0, 0)

        self.radius = self.rect.centerx - self.rect.x
        self.old_hspeed, self.old_vspeed = 0, 0
        self.hspeed, self.vspeed = 1, 1
        self.speed = SPEED
        self.begun_movement = False

    def _adjust_angle(self):
        dx = self.right.x - self.rect.centerx
        dy = self.right.y - self.rect.centery
        rads = atan2(dy, dx)
        rads %= 2*pi
        return rads

    def _rotate(self, angle):
        self.image = pygame.transform.rotate(self.old_image, angle)
        self.rect = self.image.get_rect()

    def _update_rotation(self):
        print("we are calling update_rotation")
        if self.right.x < 0:
            self.facing_direction += ANGULAR_VELOCITY
            if self.facing_direction > 360:
                self.facing_direction -= 360
        else:
            self.facing_direction -= ANGULAR_VELOCITY
            if self.facing_direction < 0:
                self.facing_direction += 360
        self._rotate(self.facing_direction)

    def _adjust_speed(self):
        if self.facing_direction > 0 and self.facing_direction < 90:
            self._update_speeds(-1, -1)
        elif self.facing_direction == 90:
            self._update_speeds(-1, 0)
        elif self.facing_direction > 90 and self.facing_direction < 180:
            self._update_speeds(-1, 1)
        elif self.facing_direction == 180:
            self._update_speeds(0, 1)
        elif self.facing_direction > 180 and self.facing_direction < 270:
            self._update_speeds(1, 1)
        elif self.facing_direction == 270:
            self._update_speeds(1, 0)
        elif self.facing_direction > 270 and self.facing_direction < 360:
            self._update_speeds(1, 1)
        elif self.facing_direction == 360 or self.facing_direction == 0:
            self._update_speeds(0, -1)

    def _update_speeds(self, x, y):
        self._update_vspeed(y)
        self._update_hspeed(x)

    # need to redo all this shit...
    def _update_vspeed(self, y):
        if y > 0 and self.yspeed >= 1

        pass

    # need to redo all this shit...
    def _update_hspeed(self, x):
        pass

    def _get_new_pos(self):

        rads = radians(self.moving_direction)
        # this gets things working but I need to calculate change in speed when "reversing direction"
        dx, dy = sin(rads) * (SPEED * self.hspeed), cos(rads) * (SPEED * self.vspeed)
        self.pos.x -= dx
        self.pos.y -= dy

    def _check_inputs(self):
        self.left, self.right = self.joystick.get_axes()

        # lack of gravity might fuck this up...
        if self.left.x == 0 and self.left.y == 0:
            if self.right.x != 0 or self.right.y != 0:
                print("updating rotation")
                self._update_rotation()

        if self.left.x != 0 or self.left.y != 0:
            self.moving_direction = self.facing_direction
            self._adjust_speed()
            self.begun_movement = True

    def update(self):
        self._check_inputs()
        if self.begun_movement:
            self._get_new_pos()
        self.move()
