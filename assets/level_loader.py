from objects.player import Player
from objects.planets import Planet
from objects.test_pilot import TestPilot
from controller.controller import init_controller

from constants import HEIGHT


def load_level(joysticks):
    object_list = []

    controllers = init_controller(joysticks)
    for controller in controllers:
        player = TestPilot("ShipSprite.png", controller, (100, HEIGHT/2))
        object_list.append(player)

    # seed_p = Planet("SeedPlanet_Solid.png", (1038, 144))
    # object_list.append(seed_p)
    # #
    meat_p = Planet("MeatPlanet_Solid.png", (637, 339))
    object_list.append(meat_p)
    #
    # quilt_p = Planet("QuiltPlanet_Solid.png", (229, 550))
    # object_list.append(quilt_p)
    #
    # earth_p = Planet("EarthTwo_Solid.png", (245, 152))
    # object_list.append(earth_p)
    #
    # ice_p = Planet("IcePlanet_Solid.png", (1038, 542))
    # object_list.append(ice_p)

    return object_list
