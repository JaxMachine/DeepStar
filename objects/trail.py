import pygame

from constants import SCREEN, BLACK, BLUE

from camera.camera_manager import CAMERA

ALPHA_RATE = 2


class Trail_Manager(object):

    def __init__(self):
        self.master_list = []

    def add_trail(self, trail):
        self.master_list.append(trail)

    def draw(self):
        for p_list in self.master_list:
            p_list.draw(True)
        self.master_list = [x for x in self.master_list if not x.should_remove()]


class Trail(object):

    def __init__(self, color1=(255, 0, 0), color2=(0, 255, 0), color3=(0, 0, 255)):
        self.surface = SCREEN.copy()
        self.surface.set_colorkey(BLACK)
        self.alpha = 255
        self.p_list1, self.p_list2, self.p_list3 = [], [], []
        self.color1, self.color2, self.color3 = color1, color2, color3

    def add_point(self, point, list_number):
        if list_number == 1:
            self.p_list1.append(point)
        elif list_number == 2:
            self.p_list2.append(point)
        elif list_number == 3:
            self.p_list3.append(point)
        else:
            print("FUCKING ERROR")

        if len(self.p_list1) > 20:
            del self.p_list1[0]
        if len(self.p_list2) > 20:
            del self.p_list2[0]
        if len(self.p_list3) > 20:
            del self.p_list3[0]

    def length(self, list_number):
        if list_number == 1:
            return len(self.p_list1)
        elif list_number == 2:
            return len(self.p_list2)
        elif list_number == 3:
            return len(self.p_list3)

    def should_remove(self):
        if self.alpha < 0:
            return True
        return False

    def draw(self, degrade_alpha):
        if len(self.p_list1) > 1 and len(self.p_list2) > 1 and len(self.p_list3) > 1:
            self.surface.fill(BLACK)

            p_list1 = CAMERA.apply_points(self.p_list1)
            pygame.draw.aalines(self.surface, (self.color1), False, p_list1, 1)

            p_list2 = CAMERA.apply_points(self.p_list2)
            pygame.draw.aalines(self.surface, (self.color2), False, p_list2, 1)

            p_list3 = CAMERA.apply_points(self.p_list3)
            pygame.draw.aalines(self.surface, (self.color3), False, p_list3, 1)

            self.surface.set_alpha(self.alpha)
            if degrade_alpha:
                self.alpha -= ALPHA_RATE
            SCREEN.blit(self.surface, (0, 0))
