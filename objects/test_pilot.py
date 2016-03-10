import pygame

from objects.game_object import BaseObject

from maths.vector import Vector

from constants import SPRITE_MANAGER, SCREEN, BACKGROUND

from math import atan2, pi, cos, sin, radians

ANGULAR_VELOCITY = 7
SPEED_GROWTH = .2
SPEED_CHANGE = 3
MAX_SPEED = 3
BASE_SPEED = 1


class TestPilot(BaseObject):

    def __init__(self, sprite_name, controller, pos):
        BaseObject.__init__(self, sprite_name, pos, SPRITE_MANAGER.instance)

        self.old_image = self.image
        self.joystick = controller
        self.create_point = 1
        # in degrees, 0 is top, 90 is left, 180 is down, 270 is right
        self.facing_direction = 0
        self.moving_direction = 0
        self._rotate(self.facing_direction)
        self.trajectory = Vector(0, 0)
        self.prev_trajectory = Vector(0, 0)

        self.radius = self.rect.centerx - self.rect.x
        self.old_hspeed, self.old_vspeed = 0, 0
        self.hspeed, self.vspeed = 1, 1
        self.speed = BASE_SPEED
        self.prev_y = 0
        self.prev_x = 0
        self.begun_movement = False
        self.point_list = []
        self.changed_dir = False

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

    def _adjust_speed(self):
        # these number might be wrong...
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
            self._update_speeds(1, -1)
        elif self.facing_direction == 360 or self.facing_direction == 0:
            self._update_speeds(0, -1)

    def _update_speeds(self, x, y):
        self._update_vspeed(y)
        self._update_hspeed(x)

    # need to redo all this shit...
    def _update_vspeed(self, y):
        # take an iterative apporach...
        if y == 0:
            return
        if y > 0:
            if self.prev_y >= 0:
                self.vspeed += SPEED_GROWTH
                if self.vspeed > MAX_SPEED:
                    self.vspeed = MAX_SPEED
                self.prev_y = y
            elif self.prev_y < 0:
                # self.vspeed = BASE_SPEED
                self.vspeed *= -1
                self.prev_y = y
        elif y < 0:
            if self.prev_y <= 0:
                self.vspeed += SPEED_GROWTH
                if self.vspeed > MAX_SPEED:
                    self.vspeed = MAX_SPEED
                self.prev_y = y
            elif self.prev_y > 0:
                # self.vspeed = BASE_SPEED
                self.vspeed *= -1  # what if I divide by 2, and negate?...
                self.prev_y = y

    # need to redo all this shit...
    def _update_hspeed(self, x):
        if x == 0:
            return
        if x > 0:
            if self.prev_x >= 0:
                self.hspeed += SPEED_GROWTH
                if self.hspeed > MAX_SPEED:
                    self.hspeed = MAX_SPEED
                self.prev_x = x
            elif self.prev_x < 0:
                # self.hspeed = BASE_SPEED
                self.hspeed *= -1
                self.prev_x = x
        elif x < 0:
            if self.prev_x <= 0:
                self.hspeed += SPEED_GROWTH
                if self.hspeed > MAX_SPEED:
                    self.hspeed = MAX_SPEED
                self.prev_x = x
            elif self.prev_x > 0:
                # self.hspeed = BASE_SPEED
                self.hspeed *= -1
                self.prev_x = x

    def _get_new_pos(self):
        self.create_points()
        rads = radians(self.moving_direction)

        if self.changed_dir:
            self.trajectory.x, self.trajector.y = sin(rads) * (BASE_SPEED), cos(rads) * (BASE_SPEED)
            test = self.prev_trajectory + self.trajectory  # get new trajectory based on new new shit
            dx, dy = test.x, test.y

        # This gets me the current movement vector
        # this gets things working but I need to calculate change in speed when "reversing direction"
        dx, dy = sin(rads) * (BASE_SPEED * self.hspeed), cos(rads) * (BASE_SPEED * self.vspeed)
        self.pos.x -= dx
        self.pos.y -= dy



    # lets see what it looks like when we are drawing points arl
    def create_points(self):
        print("creating points")
        self.create_point -= 1
        print("self.create_point = ", self.create_point)
        if self.create_point == 0:
            self.create_point = 5
            if len(self.point_list) == 10:
                self.point_list.pop()  # pops last item in the list
            self.point_list.insert(0, self.rect.center)
            print("length of list: ", len(self.point_list))

    def draw_lines(self):
        print("reachign code?")
        if len(self.point_list) > 1:
            print("drawing lines, here is the pointlist ", self.point_list)
            pygame.draw.aalines(SCREEN, (0, 255, 0), False, self.point_list, 1)

    def _check_inputs(self):
        self.left, self.right = self.joystick.get_axes()

        if self.left.x == 0 and self.left.y == 0:
            if self.right.x != 0 or self.right.y != 0:
                self._update_rotation()
                self.changed_dir = True
            else:
                self.changed_dir = False

        if self.left.x != 0 or self.left.y != 0:
            self.moving_direction = self.facing_direction
            self._adjust_speed()
            self.begun_movement = True

    def update(self):
        self._check_inputs()
        if self.begun_movement:
            self._get_new_pos()
            # self.draw_lines()
        self.move()
