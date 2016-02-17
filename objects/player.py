import pygame

from objects.game_object import BaseObject

from maths.vector import Vector, Circle
from assets.asset_loader import load_sound
# from objects.bullet import Bullet
from objects.bullet import Bullet

from sprites.sprite_managers import GroupWithOwner

from constants import PLANET_MANAGER, BULLET_GROUP_MANAGER, SND_PLAYER_GOT_HIT, SND_DEATH, SPRITE_MANAGER

HEALTH = 100
BULLET_DMG = 10  # extract this out to bullet class?


class Player(BaseObject):

    def __init__(self, sprite_name, controller, pos):
        BaseObject.__init__(self, sprite_name, pos, SPRITE_MANAGER.instance)

        # assumes an already initialized controller
        # TODO: Create virtual controller - currently we rely on PS3 controller
        self.joystick = controller
        self.can_shoot = 1
        self.can_move = 1

        self.trajectory = Vector(0, 0)
        self.begun_movement = False  # Could eliminate this by having the player already moving at start...

        # TODO: get rid of this line of code, since we will be using a rect mask for collisions...
        self.radius = self.rect.x - self.rect.centerx

        self.old_hspeed, self.old_vspeed = 0, 0
        self.hspeed, self.vspeed = 0, 0

        self.fire_sound = load_sound("321102__nsstudios__laser1.wav")

        self.health = HEALTH
        self.bullet_group = GroupWithOwner(owner=self.name, group_manager=BULLET_GROUP_MANAGER)

    def _shoot(self):
        self.can_shoot -= 1
        if self.can_shoot == 0:
            self.can_shoot = 5
            if self.right.x != 0 or self.right.y != 0:
                bullet = Bullet((self.right.x, self.right.y), self.rect.center)
                self.bullet_group.add(bullet)
                self.fire_sound.play()

    def _hit_with_bullet(self, rect):
        for group in BULLET_GROUP_MANAGER:
            if group != self.bullet_group:
                # TODO: change way bullets check for collision against player to match planet collision check(rect against circle)
                bullets = pygame.sprite.spritecollide(
                    self, group, False, pygame.sprite.collide_circle
                )
                for bullet in bullets:
                    if self.health < 0:
                        self.delete = True
                    bullet.delete = True
                    SND_PLAYER_GOT_HIT.play()

    def _collide_with_planet(self, rect):
        for planet in PLANET_MANAGER.instance.sprites():
            c = Circle(planet.rect.centerx, planet.rect.centery, planet.radius)
            if c.intersects_rect(rect):
                return True

    def _collide_with_walls(self, new_pos):
        collide = False
        if new_pos.x > 1280 or new_pos.x < 0:
            self.hspeed = (self.hspeed * -1)/1.25
            collide = True
        elif new_pos.y > 720 or new_pos.y < 0:
            self.vspeed = (self.vspeed * -1)/1.25
            collide = True
        return collide

    def _collide(self, new_pos):
        copy = self.rect.copy()
        copy.x, copy.y = new_pos.x, new_pos.y
        collide = False
        if self._collide_with_planet(copy):
            self.hspeed = (self.hspeed * -1)/1.25
            self.vspeed = (self.vspeed * -1)/1.25
            collide = True
        elif self._collide_with_walls(new_pos):
            collide = True
        return collide

    def _get_new_pos(self):
        trajectory_vector = self.pos - self.trajectory
        new_pos = self.pos
        new_pos += (trajectory_vector - new_pos).normal().mult(self.hspeed, self.vspeed)
        if not self._collide(new_pos):
            print("we are not colliding ...")
            self.pos = new_pos
        else:
            print("we are colliding")

    # should limit these speeds?
    def _update_hspeed(self, x):
        self.old_hspeed = self.hspeed
        self.hspeed = self.hspeed + .2 if x > 0 else self.hspeed - .2

    # should limit these speeds?
    def _update_vspeed(self, y):
        self.old_vspeed = self.vspeed
        self.vspeed = self.vspeed + .2 if y > 0 else self.vspeed - .2

    def _update_trajectory(self, x, y):
        # code only needed for start of game (whiqle player is not moving...)
        if self.trajectory.x == 0:
            self.trajectory.x = x
        if self.trajectory.y == 0:
            self.trajectory.y = y

        # if we switch directions, change trajectory
        if (self.old_hspeed > 0 and self.hspeed < 0) or (self.old_hspeed < 0 and self.hspeed > 0):
            self.trajectory.x = x

        # if we switch directions, change trajectory
        if (self.old_vspeed > 0 and self.vspeed < 0) or (self.old_vspeed < 0 and self.vspeed > 0):
            self.trajectory.y = y

        # Keeps axes inversion consistent
        if self.trajectory.x < 0:
            self.trajectory.x *= -1
        if self.trajectory.y < 0:
            self.trajectory.y *= -1

        self.begun_movement = True

    def _check_inputs(self):
        self.can_move -= 1

        self.left, self.right = self.joystick.get_axes()

        if self.can_move == 0:
            self.can_move = 5
            if self.left.x != 0 or self.left.y != 0:
                self._update_hspeed(self.left.x)
                self._update_vspeed(self.left.y)
                self._update_trajectory(self.left.x, self.left.y)

    def update(self):
        if self._check_inputs() or self.begun_movement:
            self._get_new_pos()
            self.move()
        self._shoot()
