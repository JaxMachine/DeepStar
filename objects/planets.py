import pygame

from objects.game_object import BaseObject

from constants import PLANET_MANAGER, BULLET_MANAGER, SND_IMPACT


class Planet(BaseObject):

    def __init__(self, sprite_name, pos):
        BaseObject.__init__(self, sprite_name, pos)

        self.radius = self.rect.x - self.rect.centerx
        PLANET_MANAGER.instance.add(self)
        self.dirty = 0

    def update(self):
        bullets = pygame.sprite.spritecollide(
            self, BULLET_MANAGER.instance, False, pygame.sprite.collide_circle)
        for bullet in bullets:
            SND_IMPACT.play()
            bullet.delete = True
        self.dirty = 1
