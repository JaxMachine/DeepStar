import pygame
import usb
import os
import sys

os.environ['SDL_VIDEO_CENTERED'] = '1'

if not pygame.joystick.get_init():
    pygame.joystick.init()


class PS3_Controller:

    def __init__(self, joystick):
        self.joystick = joystick
        self.joystick.init()
        self.buttons = self.joystick.get_numbuttons()
        print("HERE AGAINNNNNNNNNNNNN")
        self.right_axis = [self.joystick.get_axis(2), self.joystick.get_axis(3)]

    def update_axis(self):
        print("shouldn't see me")
        if self.joystick is not None:
            try:
                self.right_axis = [self.joystick.get_axis(2), self.joystick.get_axis(3)]
            except pygame.error:
                print("Axis Error")

    def get_init(self):
        if self.joystick.get_init():
            return True
        return False

    def get_right_axis(self):

        sys.stdout = open('log.text', 'w')
        self.update_axis()
        sys.stdout.close()
        sys.stdout = sys.__stdout__
        if self.right_axis is not None:
            return self.right_axis
        else:
            print("right axis is fucking garbage.")

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
