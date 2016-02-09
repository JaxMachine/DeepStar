import pygame

from objects.game_object import BaseObject

from maths.vector import Vector
from assets.asset_loader import load_sound
from objects.bullet import Bullet

from sprites.sprite_managers import GroupWithOwner

from constants import PLANET_MANAGER, BULLET_GROUP_MANAGER, SND_PLAYER_GOT_HIT, SND_DEATH

HEALTH = 100
BULLET_DMG = 10  # extract this out to bullet class?


class TestPlayer(BaseObject):

    def __init__(self, sprite_name, controller, pos=None):
        BaseObject.__init__(self, sprite_name, pos)

        # assumes an already initialized controller
        self.joystick = controller

        self.new_x = 0
        self.new_y = 0
        self.can_shoot = 1
        self.can_move = 1

        self.trajectory = Vector(0, 0)
        self.updated_trajectory = False

        self.radius = self.rect.x - self.rect.centerx

        self.old_hspeed, self.old_vspeed = 0, 0

        self.fire_sound = load_sound("321102__nsstudios__laser1.wav")

        self.health = HEALTH
        self.bullet_group = GroupWithOwner(owner=self.name)
        BULLET_GROUP_MANAGER.append(self.bullet_group)

    def shoot(self):
        self.can_shoot -= 1
        if self.can_shoot == 0:
            self.can_shoot = 5
            if self.right_axis[0] != 0 or self.right_axis[1] != 0:
                bullet = Bullet(self.right_axis, self.rect.center)
                self.bullet_group.add(bullet)
                self.fire_sound.play()

    def _colide_with_bullet(self, rect):
        pass

    def _collide_with_planet(self, rect):
        collide = collide = pygame.sprite.spritecollideany(
            self, PLANET_MANAGER.instance, pygame.sprite.collide_circle
        )

    def _collide(self, new_pos):
        self.rect_x = new_pos.x
        self._collide_with_planet(new_pos)

    def _get_new_pos(self):
        trajectory_vector = self.pos - self.trajectory
        new_pos = self.pos
        new_pos += (trajectory_vector - new_pos).normal().mult(self.hspeed, self.vspeed)
        self._collide(new_pos)
