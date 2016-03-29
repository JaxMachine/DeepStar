import pygame
from pygame import Rect
from pygame.time import get_ticks

from camera.camera_manager import CAMERA


class LayeredDirty_Manager():
    class __LayeredDirty_Manager(pygame.sprite.LayeredDirty):
        def __init__(self):
            pygame.sprite.LayeredDirty.__init__(self)

    instance = None

    def __init__(self):
        if not LayeredDirty_Manager.instance:
            LayeredDirty_Manager.instance = LayeredDirty_Manager.__LayeredDirty_Manager()


class PlayerManager():
    class __PlayerManager(pygame.sprite.LayeredDirty):
        def __init__(self):
            pygame.sprite.LayeredDirty.__init__(self)

    instance = None

    def __init__(self):
        if not PlayerManager.instance:
            PlayerManager.instance = PlayerManager.__PlayerManager()


class PlanetGroup():
    class __PlanetGroup(pygame.sprite.Group):
        def __init__(self):
            pygame.sprite.Group.__init__(self)

        def get_closest(self, other):
            closest, planet = None, None
            # print(self.sprites())
            for p in self.sprites():
                # calculate distance between planet and other
                dist = (p.pos - other.pos).length()
                # print("printing dist")
                # print(dist)
                if closest is None:
                    closest = dist
                    planet = p
                else:
                    if dist < closest:
                        closest = dist
                        planet = p
                return planet

    instance = None

    def __init__(self):
        if not PlanetGroup.instance:
            PlanetGroup.instance = PlanetGroup.__PlanetGroup()


class BulletGroup():
    class __BulletGroup(pygame.sprite.Group):
        def __init__(self):
            pygame.sprite.Group.__init__(self)

    instance = None

    def __init__(self):
        if not BulletGroup.instance:
            BulletGroup.instance = BulletGroup.__BulletGroup()


class GroupWithOwner(pygame.sprite.Group):

        def __init__(self, owner, group_manager=None):
            pygame.sprite.Group.__init__(self)
            self.owner = owner
            if group_manager is not None:
                group_manager.append(self)


class BulletGroupManager():
    class __BulletGroupManager():
        def __init__(self):
            self.b_list = []

        def list(self):
            return self.b_list

        def add(self, bullet_group):
            self.b_list.append(bullet_group)

        def remove(self, bullet_group):
            self.b_list.remove(bullet_group)

    instance = None

    def __init__(self):
        if not BulletGroupManager.instance:
            BulletGroupManager.instance = BulletGroupManager.__BulletGroupManager()
