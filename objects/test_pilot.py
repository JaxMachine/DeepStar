import pygame

from objects.game_object import BaseAnimatedObject
from objects.trail import Trail_Manager, Trail
import objects.player_utils

from objects.bullet import PinkBullet

from random import randint

from maths.vector import Vector

from constants import SPRITE_MANAGER, CLOCK, PLANET_MANAGER, SND_THRUST, SND_SHOOT

from objects.camera_center import CameraCenter
from camera.camera_manager import CAMERA

from math import cos, sin, radians

ANGULAR_VELOCITY = 7

DRAG_COEFFICIENT = .5
MASS = 250
THRUST = .5


class TestPilot(BaseAnimatedObject):

    def __init__(self, sprite_name, controller, pos):
        BaseAnimatedObject.__init__(
            self, name=sprite_name, rows=9, cols=1, pos=pos,
            sprite_group=SPRITE_MANAGER.instance)

        # old image is used for quicker "rotations" of images, also stops the image from
        # being distorted when multiple images are rotated over and over agian.
        self.old_image = self.image
        self.joystick = controller

        # in degrees, 0 is top, 90 is left, 180 is down, 270 is right
        self.facing_direction = 0
        self.moving_direction = 0
        self.bullet_count = 0
        self._rotate(self.facing_direction)

        self.radius = self.rect.centerx - self.rect.x
        self.begun_movement = False
        self.play_thrust = False

        # current trail could also be kicked out to trail manager, I think...
        self.current_trail = Trail(color1=(0, 255, 230), color2=(255, 0, 230), color3=(0, 255, 0))
        self.trails = Trail_Manager()

        self.velocity = Vector(0, 0)
        self.acceleration = Vector(0, 0)
        self.impulse = False
        self.land = False

        # this isn't the proper place for cycle logic. Should kick this out somehow.
        self.can_cycle = -1

        # ship properties..
        self.mass = MASS
        self.thrust = THRUST
        self.engine_thrust = Vector(0, 0)
        self.first_pass = True

        self.camera_center = CameraCenter("Bullet.png", self)

    # "public functions"
    def IsMoving(self):
        return self.impulse

    def getPlayerDirection(self):
        rads = radians(self.facing_direction)
        return Vector(sin(rads), cos(rads)).normal()

    def getVelocity(self):
        return Vector(self.velocity.x, self.velocity.y)

    def getPosition(self):
        return Vector(self.pos.x, self.pos.y)
        # return self.pos

    # "private" functions
    def _rotate(self, angle):
        self.image = pygame.transform.rotate(self.old_image, angle)
        self.rect = self.image.get_rect()  # move rect to current pos?
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
        rads = radians(self.moving_direction)  # this is also the angle where the camera angle object should be

        dx, dy = sin(rads) * self.thrust, cos(rads) * self.thrust
        self.engine_thrust.x, self.engine_thrust.y = -dx, -dy  # new directional thrust from engines

    def _get_new_pos(self):
        dx, dy = self.calc_new_position(self.pos)
        self.pos.x, self.pos.y = dx, dy
        self._update_trails()

    def get_elasped(self):
        return CLOCK.get_elasped()

    def calc_new_position(self, cur_pos):
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

        dx = (0.5 * self.acceleration.x * CLOCK.get_elasped()**2) + (self.velocity.x * CLOCK.get_elasped())
        dy = (0.5 * self.acceleration.y * CLOCK.get_elasped()**2) + (self.velocity.y * CLOCK.get_elasped())
        return cur_pos.x + dx, cur_pos.y + dy

    def _update_trails(self):
        if self.impulse:
            radius_to_use = self.radius + 75
            rads = radians(self.facing_direction)
            dx, dy = (sin(rads) * radius_to_use) + self.pos.x, (cos(rads) * radius_to_use) + self.pos.y
            self.current_trail.add_point((dx, dy), 1)

            rads2 = radians(self.facing_direction + 30)
            dx2, dy2 = (sin(rads2) * radius_to_use) + self.pos.x, (cos(rads2) * radius_to_use) + self.pos.y
            self.current_trail.add_point((dx2, dy2), 2)

            rads3 = radians(self.facing_direction - 30)
            dx3, dy3 = (sin(rads3) * radius_to_use) + self.pos.x, (cos(rads3) * radius_to_use) + self.pos.y
            self.current_trail.add_point((dx3, dy3), 3)
            self.current_trail.draw(False)

        elif not self.impulse and self.current_trail.length(1) > 0:
            self.trails.add_trail(self.current_trail)
            self.current_trail = Trail(color1=(0, 255, 230), color2=(255, 0, 230), color3=(0, 255, 0))
        self.trails.draw()

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
            self.impulse = True
            self.moving_direction = self.facing_direction
            self.begun_movement = True
            if self.play_thrust is False:
                SND_THRUST.play()
                self.play_thrust = True
        else:
            self.impulse = False
            self.play_thrust = False

        if self.joystick.get_action_button():
            self._land()
        if self.joystick.get_shoot_button():
            self.bullet_count -= 1
            if self.bullet_count < 0:
                radius_to_use = self.radius
                rads = radians(self.facing_direction + 180)
                dx, dy = (sin(rads) * radius_to_use) + self.pos.x, (cos(rads) * radius_to_use) + self.pos.y

                PinkBullet(randint(self.facing_direction-13, self.facing_direction+13), (dx, dy))
                SND_SHOOT.play()
                self.bullet_count = 2
        self.joystick.done_with_input()

    def deleteMe(self):
        super(TestPilot, self).delete()

    # def move(self):
    #     self.rect.centerx = self.pos.x
    #     self.rect.centery = self.pos.y
    #     CAMERA.update(self)
    #     offset = CAMERA.apply(self.rect)
    #     self.rect.x = offset.x
    #     self.rect.y = offset.y
    #     self.dirty = 1

    def update(self):
        # this cycle logic should be pushed into a separate function or something...
        self.can_cycle += 1
        if self.can_cycle == 10:
            self.cycle()
            self.can_cycle = -1
        # rotate logic is fucked up also due to cycles happening in animation...
        self._rotate(self.facing_direction)
        if not self.first_pass:
            if self.delete:
                self.deleteMe()
            self._check_inputs()
            if self.begun_movement:
                self._get_new_pos()
        self.first_pass = False
        self.move()
