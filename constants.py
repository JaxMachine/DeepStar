import pygame
pygame.init()

from sprites.sprite_managers import LayeredDirty_Manager, BulletGroup, PlanetGroup, PlayerManager
from objects.object_managers import SingletonList
from assets.asset_loader import load_sound, load_music, load_image
from misc.clock import Clock

# this is my viewport!
SCREEN_SIZE = WIDTH, HEIGHT = 1280, 720
TOTAL_LEVEL_SIZE = LEVEL_WIDTH, LEVEL_HEIGHT = 1280*2, 720*2
HALF_WIDTH = int(WIDTH/2)
HALF_HEIGHT = int(HEIGHT/2)

SPRITE_MANAGER = LayeredDirty_Manager()
PLAYER_MANAGER = PlayerManager()
OBJECT_MANAGER = SingletonList()

PLANET_MANAGER = PlanetGroup()
BULLET_MANAGER = BulletGroup()

BULLET_GROUP_MANAGER = []

# SOUNDS
SND_IMPACT = load_sound("impact.wav")
SND_PLAYER_GOT_HIT = load_sound("3049__starpause__k9dhhpulsekick.wav")
SND_DEATH = load_sound("death.wav")

SND_THRUST = load_sound("thrust.wav")
SND_SHOOT = load_sound("shoot.wav")

# SND_BACKGROUND = load_music("com-truise-mind[mp3freex].mp3")
# SND_BACKGROUND = load_music("HOME - Odyssey - 03 Decay.mp3")
BLACK = pygame.Color('black')
GREEN = pygame.Color('green')
BLUE = pygame.Color('blue')
RED = pygame.Color('red')

SCREEN = pygame.display.set_mode(SCREEN_SIZE)

BACKGROUND, BACKGROUND_POS = load_image("big_background.jpg")

PLAYERS = [True, True]
CLOCK = Clock()
