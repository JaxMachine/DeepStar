import os
import pygame
from pygame.compat import geterror

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, 'images/')
sound_dir = os.path.join(main_dir, 'sounds/')

pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.init()


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


def load_sound(name):
    filename = os.path.join(sound_dir, name)
    try:
        sound = pygame.mixer.Sound(os.path.join(filename))
    except pygame.error:
        raise "could not load or play sound file found in /sounds folder"
    sound.set_volume(.25)
    return sound


def load_music(name):
    filename = os.path.join(sound_dir, name)
    try:
        pygame.mixer.music.load(filename)
        pygame.mixer.music.set_volume(1)
        pygame.mixer.music.play(-1)
    except:
        raise "could not load or play music file found in /sounds folder"
