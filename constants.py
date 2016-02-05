from sprites.sprite_managers import LayeredDirty_Manager, BulletGroup, PlanetGroup
from objects.object_managers import G_Object_Manager
from assets.asset_loader import load_sound

SCREEN_SIZE = WIDTH, HEIGHT = 1280, 720

SPRITE_MANAGER = LayeredDirty_Manager()
OBJECT_MANAGER = G_Object_Manager()

PLANET_MANAGER = PlanetGroup()
BULLET_MANAGER = BulletGroup()


# SOUNDS
SND_IMPACT = load_sound("impact.wav")
