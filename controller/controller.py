# interface for virtual controller
from keyboard_controller import KeyboardController
from PS3 import PS3_Controller


def init_controller(joysticks):
    controller_list = []
    if len(joysticks) == 0:
        controller_list.append(KeyboardController())
        return controller_list
    else:
        for controller in joysticks:
            controller_list.append(PS3_Controller(controller))
        return controller_list
