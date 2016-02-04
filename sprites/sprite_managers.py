import pygame


class LayeredDirty_Manager():
    class __LayeredDirty_Manager(pygame.sprite.LayeredDirty):
        def __init__(self):
            pygame.sprite.LayeredDirty.__init__(self)

    instance = None

    def __init__(self):
        if not LayeredDirty_Manager.instance:
            LayeredDirty_Manager.instance = LayeredDirty_Manager.__LayeredDirty_Manager()
