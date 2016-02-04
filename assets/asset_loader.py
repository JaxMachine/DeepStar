import os
import pygame
from pygame.compat import geterror

# game object imports
# from objects.player import Player
#
# from testmain import WIDTH, HEIGHT

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, 'images/')


def load_image(name, colorkey=None):
    filename = os.path.join(data_dir, name)
    try:
        image = pygame.image.load(filename)
    except pygame.error:
        raise SystemExit(str(geterror()))
    image = image.convert()
    
    if colorkey is not None:
        if colorkey is -1:
            # sets color key to color found at 0,0  in the image. that's actually pretty clever.
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, pygame.RLEACCEL)
    return image, image.get_rect()


# def load_level():
#     object_list = []
#
#     # create player object at the center of the level...
#     player = Player((WIDTH/2, HEIGHT/2))
#     object_list.append(player)
#
#     return object_list
