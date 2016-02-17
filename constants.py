
from sprites.sprite_managers import LayeredDirty_Manager, BulletGroup, PlanetGroup
from objects.object_managers import SingletonList
from assets.asset_loader import load_sound, load_music

SCREEN_SIZE = WIDTH, HEIGHT = 1280, 720

SPRITE_MANAGER = LayeredDirty_Manager()
OBJECT_MANAGER = SingletonList()

PLANET_MANAGER = PlanetGroup()
BULLET_MANAGER = BulletGroup()

BULLET_GROUP_MANAGER = []   # BulletGroupManager()

# SOUNDS
SND_IMPACT = load_sound("impact.wav")
SND_PLAYER_GOT_HIT = load_sound("3049__starpause__k9dhhpulsekick.wav")
SND_DEATH = load_sound("death.wav")

SND_BACKGROUND = load_music("com-truise-mind[mp3freex].mp3")


PLAYERS = [True, True]
