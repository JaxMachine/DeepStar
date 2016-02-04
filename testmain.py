import pygame
import usb

from assets.asset_loader import load_image
from assets.level_loader import load_level

from constants import SCREEN_SIZE, OBJECT_MANAGER, SPRITE_MANAGER


class DeepStar:

    def __init__(self):
        pygame.init()
        pygame.joystick.init()
        self.joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]

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
        self.game_objects = OBJECT_MANAGER.instance.list()
        self.game_objects = load_level(self.joysticks)

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
        for game_object in OBJECT_MANAGER.instance.list():
            game_object.update()

    def draw(self):
        rects = SPRITE_MANAGER.instance.draw(self.screen)
        pygame.display.update(rects)

        # other dirty sprites..

    def run(self):
        SPRITE_MANAGER.instance.clear(self.screen, self.background)
        # allsprites.clear(screen, background)
        while not self.exit:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit = True

            self.clock.tick(50)

            # get player inputs..
            self.check_inputs()
            self.update()
            self.draw()

        pygame.quit()

if __name__ == "__main__":
    game = DeepStar()
    game.run()