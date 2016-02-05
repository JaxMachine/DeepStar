import pygame
from pygame.locals import *

from assets.asset_loader import load_image
from constants import SPRITE_MANAGER, OBJECT_MANAGER, PLANET_MANAGER, BULLET_MANAGER


class Planet(pygame.sprite.DirtySprite):

    def __init__(self, image, pos=None):
        pygame.sprite.DirtySprite.__init__(self, SPRITE_MANAGER.instance)
        self.image, self.rect = load_image(image, -1)

        if pos is not None:
            self.rect.center = pos
            self.dirty = 1

        self.radius = self.rect.centerx - self.rect.x

        OBJECT_MANAGER.instance.add(self)
        PLANET_MANAGER.instance.add(self)

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rect.left += -1
            if self.rect.left < 0:
                self.rect.left = 0
        if keys[pygame.K_d]:
            self.rect.right += 1
            if self.rect.right > 1280:
                self.rect.right = 1280
        if keys[pygame.K_w]:
            self.rect.top += -1
            if self.rect.top < 0:
                self.rect.top = 0
        if keys[pygame.K_s]:
            self.rect.bottom += 1
            if self.rect.bottom > 720:
                self.rect.bottom = 270
        self.dirty = 1
        print(self.rect.center)

    def update(self):
        self.move()
        bullets = pygame.sprite.spritecollide(
            self, BULLET_MANAGER.instance, False, pygame.sprite.collide_circle)
        if len(bullets) != 0:
            print("WE HAVE COLLIDED")
        for bullet in bullets:
            bullet.delete = True
