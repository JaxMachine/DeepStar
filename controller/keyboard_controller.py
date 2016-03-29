import pygame

from maths.vector import Vector


class KeyboardController:

    def __init__(self):
        self.updated_buttons = False
        self.left_axis = Vector(0, 0)
        self.right_axis = Vector(0, 0)

    def update_buttons(self):
        keys = pygame.key.get_pressed()
        self.buttons = {
            'space': keys[pygame.K_SPACE],
            'a': keys[pygame.K_a],
            'd': keys[pygame.K_d],
            'w': keys[pygame.K_w],
            's': keys[pygame.K_s],
            'e': keys[pygame.K_e],
            'up': keys[pygame.K_UP],
            'down': keys[pygame.K_DOWN],
            'right': keys[pygame.K_RIGHT],
            'left': keys[pygame.K_LEFT]
        }
        self.updated_buttons = True

    def get_left_axis(self):
        if not self.updated_buttons:
            self.update_buttons()
        if (self.buttons['a'] and self.buttons['d']) or (not self.buttons['a'] and not self.buttons['d']):
            self.left_axis.x = 0
        else:
            self.left_axis.x = -1 if self.buttons['a'] else 1  # inverted axis
        if (self.buttons['w'] and self.buttons['s']) or (not self.buttons['w'] and not self.buttons['s']):
            self.left_axis.y = 0
        else:
            self.left_axis.y = -1 if self.buttons['w'] else 1  # inverted axis
        return self.left_axis

    def get_right_axis(self):
        if not self.updated_buttons:
            self.update_buttons()
        if (self.buttons['left'] and self.buttons['right']) or (not self.buttons['left'] and not self.buttons['right']):
            self.right_axis.x = 0
        else:
            self.right_axis.x = -1 if self.buttons['left'] else 1
        if (self.buttons['up'] and self.buttons['down']) or (not self.buttons['up'] and not self.buttons['down']):
            self.right_axis.y = 0
        else:
            self.right_axis.y = -1 if self.buttons['w'] else 1
        return self.right_axis

    def get_axes(self):
        return self.get_left_axis(), self.get_right_axis()

    def get_action_button(self):
        if not self.updated_buttons:
            self.update_buttons()
        return self.buttons['space']

    def get_brake_button(self):
        if not self.updated_buttons:
            self.update_buttons()
        return self.buttons['e']

    def done_with_input(self):
        self.updated_buttons = False

    def get_init(self):
        return True
