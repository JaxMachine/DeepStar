import pygame

from objects.game_object import BaseObject

from constants import PLANET_MANAGER, BULLET_MANAGER, SND_IMPACT, SPRITE_MANAGER


class Planet(BaseObject):

    def __init__(self, sprite_name, pos, debug=None):
        BaseObject.__init__(self, sprite_name, pos, SPRITE_MANAGER.instance)

        self.radius = self.rect.centerx - self.rect.x
        PLANET_MANAGER.instance.add(self)

    def update(self):
        self.move()
        bullets = pygame.sprite.spritecollide(
            self, BULLET_MANAGER.instance, False, pygame.sprite.collide_circle)
        for bullet in bullets:
            SND_IMPACT.play()
            bullet.delete = True
        self.dirty = 1
