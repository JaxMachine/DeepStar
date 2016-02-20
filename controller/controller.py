# interface for virtual controller
class Controller:

    # assumes an initialized controller
    def __init__(self, controller):
        self.controller = controller

    def get_axes(self):
        return self.controller.get_axes()

    def get_right_axis(self):
        return self.controller.get_right_axis()

    def get_left_axis(self):
        return self.controller.get_left_axis()

    def get_action_button(self):
        return self.controller.get_action_button()

    def update_buttons(self):
        return self.controller.update_buttons()

    def done_with_input(self):
        self.controller.done_with_input()
