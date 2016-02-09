import pygame
# from pygame.locals import *
import sys
from assets.asset_loader import load_sound
from objects.bullet import Bullet
from assets.asset_loader import load_image

from maths.vector import Vector

from constants import SPRITE_MANAGER, PLANET_MANAGER, OBJECT_MANAGER, BULLET_GROUP_MANAGER, SND_PLAYER_GOT_HIT, SND_DEATH, PLAYERS
from sprites.sprite_managers import GroupWithOwner


HEALTH = 100
BULLET_DMG = 10


class Player(pygame.sprite.DirtySprite):

    def __init__(self, sprite_name, controller, pos=None):
        # call DirtySprite initializer
        pygame.sprite.DirtySprite.__init__(self, SPRITE_MANAGER.instance)
        self.image, self.rect = load_image(sprite_name, -1)
        OBJECT_MANAGER.instance.add(self)
        self.name = sprite_name
        self.delete = False

        if pos is not None:
            self.old_position = pos
            self.rect.center = pos
            self.dirty = 1
        self.name = sprite_name

        # make sure controller is initialized
        self.joystick = controller
        if not self.joystick.get_init():
            self.joystick.init()

        self.new_x = 0
        self.new_y = 0
        self.can_shoot = 1
        self.can_move = 1

        self.pos = Vector(self.rect.x, self.rect.y)
        # self.old_position = self.pos
        self.trajectory = Vector(0, 0)
        self.updated_trajectory = False

        self.radius = self.rect.x - self.rect.centerx

        self.vspeed = 0
        self.hspeed = 0
        self.old_hspeed = 0
        self.old_vspeed = 0

        self.fire_sound = load_sound("321102__nsstudios__laser1.wav")

        self.health = HEALTH
        self.bullet_group = GroupWithOwner(owner=self.name)
        BULLET_GROUP_MANAGER.append(self.bullet_group)
        # f.close()
        # sys.stdout = sys.__stdout__

    def reset(self):
        self.rect.center = self.old_position
        self.pos = Vector(self.rect.x, self.rect.y)
        self.trajectory = Vector(0, 0)
        self.updated_trajectory = False
        self.delete = False

        self.vspeed = 0
        self.hspeed = 0
        self.old_hspeed = 0
        self.old_vspeed = 0

        self.can_shoot = 1
        self.can_move = 1
        self.health = HEALTH
        self.dirty = 1
        SPRITE_MANAGER.instance.add(self)

    def get_rect(self):
        return self.rect

    def shoot(self):
        self.can_shoot -= 1
        if self.can_shoot == 0:
            self.can_shoot = 5
            if self.new_b_x != 0 or self.new_b_y != 0:
                b = Bullet((self.new_b_x, self.new_b_y), (self.rect.centerx, self.rect.centery))
                self.bullet_group.add(b)
                self.fire_sound.play()

    def pn(self, name, vector):
        out = "{0}: ({1}, {2})".format(name, vector.x, vector.y)
        print(out)

    def move(self):
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y

        self.dirty = 1

    def _get_new_pos(self):
        new = self.pos - self.trajectory
        new_pos = self.pos
        new_pos += (new - new_pos).normal().mult(self.hspeed, self.vspeed)

        # check to see if that new position collides....
        self.rect.x = new_pos.x
        self.rect.y = new_pos.y
        collide = pygame.sprite.spritecollideany(
            self, PLANET_MANAGER.instance, pygame.sprite.collide_circle
        )
        if collide is not None:
            self.hspeed = (self.hspeed * -1)/1.25
            self.vspeed = (self.vspeed * -1)/1.25
            # set rect back to old position
            self.rect.x = self.pos.x
            self.rect.y = self.pos.y
        elif new_pos.x > 1280 or new_pos.x < 0:
            # print("we are colliding with wallLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL")
            self.rect.x = self.pos.x
            self.rect.y = self.pos.y
            self.hspeed = (self.hspeed * -1)/1.25
        elif new_pos.y > 720 or new_pos.y < 0:
            # print("we are colliding with cielingGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGg")
            self.rect.x = self.pos.x
            self.rect.y = self.pos.y
            self.vspeed = (self.vspeed * -1)/1.25
        else:
            self.pos = new_pos
        return self.pos

    def update_trajectory(self):
        self.can_move -= 1

        left, right = self.joystick.get_axes()
        self.new_b_x, self.new_b_y = right

        self.new_x, self.new_y = left

        if self.can_move == 0:
            self.can_move = 5
            if self.new_x != 0 or self.new_y != 0:

                self.old_hspeed = self.hspeed
                self.old_vspeed = self.vspeed
                if self.new_x > 0:
                    self.hspeed += .2
                else:
                    self.hspeed -= .2
                if self.new_y > 0:
                    self.vspeed += .2
                else:
                    self.vspeed -= .2

                if self.trajectory.x == 0:
                    self.trajectory.x = self.new_x
                if self.trajectory.y == 0:
                    self.trajectory.y = self.new_y

                if self.old_hspeed > 0 and self.hspeed < 0:  # that means we have switched directions, get a new trajecorty
                    self.trajectory.x = self.new_x
                elif self.old_hspeed < 0 and self.hspeed > 0:  # that means we have switched directios, get a new trajectory
                    self.trajectory.x = self.new_x

                if self.old_vspeed > 0 and self.vspeed < 0:  # that means we have switched directions, get a new trajecorty
                    self.trajectory.y = self.new_y
                elif self.old_vspeed < 0 and self.vspeed > 0:  # that means we have switched directios, get a new trajectory
                    self.trajectory.y = self.new_y

                if self.trajectory.x < 0:
                    self.trajectory.x *= -1
                if self.trajectory.y < 0:
                    self.trajectory.y *= -1
                self.updated_trajectory = True

    def collide_with_bullet(self):
        for group in BULLET_GROUP_MANAGER:
            if group != self.bullet_group:
                bullets = pygame.sprite.spritecollide(
                    self, group, False, pygame.sprite.collide_circle)
                for bullet in bullets:
                    self.health -= BULLET_DMG
                    if self.health < 0:
                        self.delete = True
                    bullet.delete = True
                    SND_PLAYER_GOT_HIT.play()

    def update(self):
        if self.delete:
            self.kill()
            SND_DEATH.play()
            self.reset()
        self.update_trajectory()
        if self.updated_trajectory:
            self._get_new_pos()

        self.collide_with_bullet()
        self.move()
        self.shoot()
