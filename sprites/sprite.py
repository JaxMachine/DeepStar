import pygame

from assets.asset_loader import load_image, load_sprite_sheet


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


class BaseAnimatedSprite(pygame.sprite.DirtySprite):

    def __init__(self, name, rows, cols, colorkey=-1, sprite_group=None):
        pygame.sprite.DirtySprite.__init__(self)
        self.images = load_sprite_sheet(name=name, rows=rows, cols=cols, colorkey=colorkey)
        self.index = -1
        self.image, self.rect = self.images[0], self.images[0].get_rect()
        self.dity = 1
        self.name = name
        self.delete = False
        if sprite_group is not None:
            sprite_group.add(self)

    def delete(self):
        self.kill()

    def cycle(self):
        self.index += 1
        # self.image, self.rect = self.images[self.index], self.images[self.index].get_rect()
        self.old_image = self.images[self.index]
        if self.index + 1 == len(self.images):
            self.index = -1
        # self.dirty = 1
