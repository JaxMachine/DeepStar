from objects.player import Player
from objects.planets import Planet
from controller.PS3 import PS3_Controller

# from constants import WIDTH, HEIGHT


def load_level(joysticks):
    object_list = []

    # create player object at the center of the level...

    controller = PS3_Controller(joysticks[0])

    player = Player(controller, (0, 0))
    object_list.append(player)

    seed_p = Planet("SeedPlanet_Solid.png", (1038, 144))
    object_list.append(seed_p)

    meat_p = Planet("MeatPlanet_Solid.png", (637, 339))
    object_list.append(meat_p)

    quilt_p = Planet("QuiltPlanet_Solid.png", (229, 550))
    object_list.append(quilt_p)

    earth_p = Planet("EarthTwo_Solid.png", (245, 152))
    object_list.append(earth_p)

    ice_p = Planet("IcePlanet_Solid.png", (1038, 542))
    object_list.append(ice_p)

    return object_list
