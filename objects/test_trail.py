import pygame


class Trail(pygame.sprite.DirtySprite):

    def __init__(self, sprite_group=None):
        pygame.sprite.DirtySprite.__init__(self)
        if sprite_group is not None:
            sprite_group.add(self)
        self.rect = None
