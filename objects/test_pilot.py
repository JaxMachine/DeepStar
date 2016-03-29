import pygame

from objects.game_object import BaseObject
import objects.player_utils

from maths.vector import Vector

from constants import SPRITE_MANAGER, CLOCK, PLANET_MANAGER, SCREEN
from camera.camera_manager import CAMERA

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
        self.land = False

        # ship properties..
        self.mass = MASS
        self.thrust = THRUST
        self.engine_thrust = Vector(0, 0)
        self.first_pass = True

    def _adjust_angle(self):
        dx = self.right.x - self.rect.centerx
        dy = self.right.y - self.rect.centery
        rads = atan2(dy, dx)
        rads %= 2*pi
        return rads

    def _rotate(self, angle):
        self.image = pygame.transform.rotate(self.old_image, angle)
        self.rect = self.image.get_rect() ## move rect to current pos?
        self.rect.centerx = self.pos.x
        self.rect.centery = self.pos.y

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
        rads = radians(self.moving_direction)  # this is also the angle where the camera angle object should be

        dx, dy = sin(rads) * self.thrust, cos(rads) * self.thrust
        self.engine_thrust.x, self.engine_thrust.y = -dx, -dy  # new directional thrust from engines

    def _get_new_pos(self):
        if self.impulse:
            self._resolve_direction_vector()
        else:
            self.engine_thrust.x, self.engine_thrust.y = 0, 0

        # calculate acceleration.x
        drag_force = Vector(
            -DRAG_COEFFICIENT * self.velocity.x, -DRAG_COEFFICIENT * self.velocity.y)

        self.acceleration.x = (self.engine_thrust.x + drag_force.x)/self.mass
        self.acceleration.y = (self.engine_thrust.y + drag_force.y)/self.mass

        self.velocity.x = self.velocity.x + (self.acceleration.x * CLOCK.get_elasped())
        self.velocity.y = self.velocity.y + (self.acceleration.y * CLOCK.get_elasped())  # might have to subtract this value..

        self.pos.x = self.pos.x + (0.5 * self.acceleration.x * CLOCK.get_elasped()**2) + (self.velocity.x * CLOCK.get_elasped())
        self.pos.y = self.pos.y + (0.5 * self.acceleration.y * CLOCK.get_elasped()**2) + (self.velocity.y * CLOCK.get_elasped())

        # pygame.draw.rect(SCREEN, (255, 0, 0), self.rect, 2)
        # pygame.draw.circle(SCREEN, (255, 0, 0), (int(self.pos.x), int(self.pos.y)), int(4), int(2))

    def get_Player_Direction(self):
        rads = radians(self.facing_direction)

        return Vector(sin(rads), cos(rads)).normal()

    def _add_point(self, point):
        self.point_list.insert(0, point)

        if len(self.point_list) > 5:
            del self.point_list[-1]

    def _land(self):
        closest_planet = PLANET_MANAGER.instance.get_closest(self)
        if not self.land:
            self.land = True
            self.delete = True
            objects.player_utils.create_player_on_planet(
                "OnPlanetSprite1.png", self.joystick, self.pos.to_tuple(), closest_planet)

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

        if self.joystick.get_action_button():
            # print("action button being pressed")
            self._land()
        self.joystick.done_with_input()

    def deleteMe(self):
        super(TestPilot, self).delete()

    def update(self):
        if not self.first_pass:
            # print("printing rect at the start of update")
            # print(self.rect)
            # print("PLayer POS at start of update")
            # print(self.pos)
            if self.delete:
                self.deleteMe()
            self._check_inputs()
            if self.begun_movement:
                self._get_new_pos()
        self.first_pass = False

        self.move()
