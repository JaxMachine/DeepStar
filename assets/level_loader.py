from objects.player import Player
from controller.PS3 import PS3_Controller


def load_level(joysticks):
    object_list = []

    # create player object at the center of the level...

    controller = PS3_Controller(joysticks[0])

    player = Player(controller, (640/2, 480/2))
    object_list.append(player)

    # game_objects.add(player)

    return object_list
