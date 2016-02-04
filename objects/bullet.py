import pygame

from assets.asset_loader import load_image
from sprites.sprite_managers import LayeredDirty_Manager

sprite_manager = LayeredDirty_Manager()  # returns instance of sprite manager...


class Bullet(pygame.sprite.DirtySprite):

    def __init__(self, trajectory, pos=None):
        # call DirtySprite initializer
        pygame.sprite.DirtySprite.__init__(self, sprite_manager)
        self.image, self.rect = load_image("bullet.png", -1)
        self.trajectory

        # if pass a position, move it and mark it dirty..
        if pos is not None:
            self.rect.center = pos
            self.dirty = 1
        self.delete = False
        # Game_Object_Manager.instance.add(self)
        pygame.sprite.LayeredDirty(self)

        def get_rect(self):
            return self.rect

        def move(self):
            self.rect.left += (self.trajectory[0] * 6)
            self.rect.top += (self.trajectory[1] * 6)
            if self.rect.right > 540:
                self.kill()
            if self.rect.left < 100:
                self.kill()
            if self.rect.top < 100:
                self.kill()
            if self.rect.bottom > 380:
                self.kill()
            self.dirty = 1

        def update(self):
            self.move()
