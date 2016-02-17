import pygame

from assets.asset_loader import load_image


class BaseSprite(pygame.sprite.DirtySprite):

    def __init__(self, sprite_name, sprite_group=None):
        pygame.sprite.DirtySprite.__init__(self)
        if sprite_group is not None:
            sprite_group.add(self)
        self.image, self.rect = load_image(sprite_name, -1)
        self.name = sprite_name
        self.dirty = 1
        self.delete = False

    def delete(self):
        self.kill()
