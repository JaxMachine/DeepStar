import pygame

from objects.game_object import BaseObject

from maths.vector import Vector

from constants import SPRITE_MANAGER, CLOCK

from math import atan2, pi, cos, sin, radians

ANGULAR_VELOCITY = 7

DRAG_COEFFICIENT = .5
MASS = 250
THRUST = .5


class TestPilot(BaseObject):

    def __init__(self, sprite_name, controller, pos):
        BaseObject.__init__(self, sprite_name, pos, SPRITE_MANAGER.instance)

        self.old_image = self.image
        self.joystick = controller
        self.create_point = 1
        # in degrees, 0 is top, 90 is left, 180 is down, 270 is right
        self.facing_direction = 0
        self.moving_direction = 0
        self.prev_moving_direction = 0
        self._rotate(self.facing_direction)

        self.radius = self.rect.centerx - self.rect.x
        self.begun_movement = False
        self.point_list = []
        self.changed_dir = False

        self.velocity = Vector(0, 0)
        self.acceleration = Vector(0, 0)
        self.impulse = False

        # ship properties..
        self.mass = MASS
        self.thrust = THRUST
        self.engine_thrust = Vector(0, 0)

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
        if self.right.x < 0:
            self.facing_direction += ANGULAR_VELOCITY
            if self.facing_direction > 360:
                self.facing_direction -= 360
        else:
            self.facing_direction -= ANGULAR_VELOCITY
            if self.facing_direction < 0:
                self.facing_direction += 360
        self._rotate(self.facing_direction)

    def _resolve_direction_vector(self):
        # but we should only add acceleration if we are holding down the left stick..
        rads = radians(self.moving_direction)
        dx, dy = sin(rads) * self.thrust, cos(rads) * self.thrust
        self.engine_thrust.x, self.engine_thrust.y = -dx, -dy  # new directional thrust from engines

    def _get_new_pos(self):
        if self.impulse:
            print("adding thrust from engines")
            self._resolve_direction_vector()
        else:
            self.engine_thrust.x, self.engine_thrust.y = 0, 0

        # calculate acceleration.x
        print("printing engine thrust: ")
        print(self.engine_thrust)
        drag_force = Vector(
            -DRAG_COEFFICIENT * self.velocity.x, -DRAG_COEFFICIENT * self.velocity.y)
        print("printing drag_force: ")
        print(drag_force)

        self.acceleration.x = (self.engine_thrust.x + drag_force.x)/self.mass
        self.acceleration.y = (self.engine_thrust.y + drag_force.y)/self.mass

        self.velocity.x = self.velocity.x + (self.acceleration.x * CLOCK.get_elasped())
        self.velocity.y = self.velocity.y + (self.acceleration.y * CLOCK.get_elasped())  # might have to subtract this value..

        self.pos.x = self.pos.x + (0.5 * self.acceleration.x * CLOCK.get_elasped()**2) + (self.velocity.x * CLOCK.get_elasped())
        self.pos.y = self.pos.y + (0.5 * self.acceleration.y * CLOCK.get_elasped()**2) + (self.velocity.y * CLOCK.get_elasped())

    def _add_point(self, point):
        self.point_list.insert(0, point)

        if len(self.point_list) > 5:
            del self.point_list[-1]


    def _check_inputs(self):
        self.left, self.right = self.joystick.get_axes()

        if self.left.x == 0 and self.left.y == 0:
            if self.right.x != 0 or self.right.y != 0:
                self._update_rotation()

        if self.left.x != 0 or self.left.y != 0:
            # print("begun movement is true")
            self.impulse = True
            self.moving_direction = self.facing_direction
            self.begun_movement = True
        else:
            self.impulse = False

    def update(self):
        self._check_inputs()
        if self.begun_movement:
            self._get_new_pos()
        self.move()
