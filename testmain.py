import pygame
import usb

from controller.PS3 import PS3_Controller

from assets.asset_loader import load_image
from assets.level_loader import load_level

from sprites.sprite_managers import LayeredDirty_Manager

SCREEN_SIZE = WIDTH, HEIGHT = 640, 480


class DeepStar:

    def __init__(self):
        pygame.init()
        pygame.joystick.init()
        self.joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
        # self.joystick = eslf.joysticks[0]
        # self.joystick.init()

        # print(joysticks[0].get_name())
        # print(pygame.joystick.get_count())

        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption('DeepStar')

        self.clock = pygame.time.Clock()

        if pygame.font:
            self.font = pygame.font.Font(None, 30)
        else:
            self.font = None

        self.init_game()

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

    # initialize game objects, etc..
    def init_game(self):
        # set game constants
        self.prev_mouse_pos = (0, 0)
        # self.controller = PS3_Controller(self.screen)
        if self.check_if_connected():
            print("conntected")
        else:
            print("not connected")

        # create the background, blit it to the screen...
        self.background, self.background_pos = load_image("background.jpg")
        self.screen.blit(self.background, (0, 0))

        # init all game objects... // only one list
        # self.game_objects = Game_Object_Manager()

        self.game_objects = []
        self.game_objects = load_level(self.joysticks)

        self.sprites = LayeredDirty_Manager()

        # add all GOs to spriteList - at this point, all GOs are just dirty sprite objects
        allSprites = ()
        for game_object in self.game_objects:
            allSprites = allSprites + (game_object,)

        self.allSprites = pygame.sprite.LayeredDirty(allSprites)
        self.allSprites.clear(self.screen, self.background)

        self.exit = False

    def check_inputs(self):
        self.cur_mouse_pos = pygame.mouse.get_pos()
        ball = self.game_objects[0]

        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            ball.move(left=-5)
        if keys[pygame.K_d]:
            ball.move(right=5)
        if keys[pygame.K_w]:
            ball.move(top=-5)
        if keys[pygame.K_s]:
            ball.move(bottom=5)

        # cycle through game objects controllers, if you have a controller, update
        ball.update()

    def update(self):
        for game_object in self.game_objects:
            game_object.update()

    def draw(self):
        # this will redraw all sprites with dirty=1
        rects = self.allSprites.draw(self.screen)
        pygame.display.update(rects)

        # other dirty sprites..



    def run(self):
        # self.controller.check_status()
        # if self.check_if_connected():
        #     print("connected")
        # else:
        #     print("not connected")
        #
        # if self.joystick.get_init():
        #     print("we are init")
        # else:
        #     print("we are not init")
        # print(self.joystick.get_numbuttons())
        # buttons = self.joystick.get_numbuttons()
        # num_axes = self.joystick.get_numaxes()
        # print("num axes")
        # print(num_axes)
        # self.left_axis = [self.joystick.get_axis(0), self.joystick.get_axis(1)]
        # self.right_axis = [self.joystick.get_axis(2), self.joystick.get_axis(3)]

        # for i in range(buttons):
        #     button = self.joystick.get_button(i)
        #     if button:
        #
        #         print(button)

        while not self.exit:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit = True
            # test joystick axes
            # outstr = ""
            # for i in range(0, 4):
            #     axis = self.joystick.get_axis(i)
            #     outstr = outstr + str(i) + ":" + str(axis) + "|"
            #     print(outstr)

            self.clock.tick(50)

            # get player inputs..
            self.check_inputs()
            self.update()
            self.draw()

        pygame.quit()

if __name__ == "__main__":
    game = DeepStar()
    game.run()
