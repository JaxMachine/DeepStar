import pygame
import usb
import os

from maths.vector import Vector

os.environ['SDL_VIDEO_CENTERED'] = '1'

if not pygame.joystick.get_init():
    pygame.joystick.init()


class PS3_Controller:

    def __init__(self, joystick):
        self.joystick = joystick
        self.joystick.init()
        self.buttons = self.joystick.get_numbuttons()
        self.left_axis = [self.joystick.get_axis(0), self.joystick.get_axis(1)]
        self.right_axis = [self.joystick.get_axis(2), self.joystick.get_axis(3)]
        self.updated_buttons = False

    def update_axis(self):
        if self.joystick is not None:
            try:
                self.left_axis = [self.joystick.get_axis(0), self.joystick.get_axis(1)]
                self.right_axis = [self.joystick.get_axis(2), self.joystick.get_axis(3)]
            except pygame.error:
                print("Axis Error")

    def update_buttons(self):
        if self.joystick is not None:
            try:
                self.buttons = {
                    'x': self.joystick.get_button(14)
                }
                self.updated_buttons = True
                return self.buttons
            except pygame.error:
                print("could not get joystick buttons")
        else:
            self.buttons = None

    def get_action_button(self):
        if not self.updated_buttons:
            self.update_buttons()
            self.updated_buttons = True
        return self.buttons['x']

    def done_with_input(self):
        self.updated_buttons = False

    def get_init(self):
        if self.joystick.get_init():
            return True
        return False

    def get_right_axis(self):
        self.update_axis()
        if self.right_axis is not None:
            right = Vector(self.right_axis[0], self.right_axis[1])
            return right
        else:
            print("right axis is fucking garbage.")

    def get_left_axis(self):
        self.update_axis()
        if self.left_axis is not None:
            left = Vector(self.left_axis[0], self.left_axis[1])
            return left
        else:
            print("left axis is fucking garbage.")

    # returns axes input as vectors
    def get_axes(self):
        self.update_axis()
        if self.left_axis is not None and self.right_axis is not None:
            left = Vector(self.left_axis[0], self.left_axis[1])
            right = Vector(self.right_axis[0], self.right_axis[1])
            return left, right

    def check_if_connected(self):
        try:
            busses = usb.busses()
            for bus in busses:
                devices = bus.devices
                for dev in devices:
                    if dev.idVendor == 1356:
                        return True
            return False
        except usb.core.USBError:
            print("USB Disconnected")
            return False
