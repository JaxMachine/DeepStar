import pygame

from constants import SPRITE_MANAGER

from assets.asset_loader import load_image


class BaseSprite(pygame.sprite.DirtySprite):

    def __init__(self, sprite_name):
        pygame.sprite.DirtySprite.__init__(self, SPRITE_MANAGER.instance)
        self.image, self.rect = load_image(sprite_name, -1)
        self.name = sprite_name
        self.dirty = 1
        self.delete = False

    def delete(self):
        if not self.delete:
            self.kill()
