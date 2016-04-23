import pygame

SCREEN_SIZE = WIDTH, HEIGHT = 1280, 720
HALF_WIDTH = int(WIDTH/2)
HALF_HEIGHT = int(HEIGHT/2)

from .camera import Camera

from constants import SCREEN


def simple_camera(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    new_rect = pygame.Rect(-l+HALF_WIDTH, t+-HALF_HEIGHT, w, h)
    return new_rect


def projected_focus_camera(camera, target):
    cur_target_pos = target.getPosition()
    future_target_pos = target.getPosition()
    target_rect = target.rect.copy()
    # target_velocity = target.getVelocity()
    # calc position 3 time steps from now...
    for i in range(0, 5, 1):
        future_target_pos.x, future_target_pos.y = target.calc_new_position(future_target_pos)

    # to_lerp = cur_target_pos + ((future_target_pos - cur_target_pos) * target.get_elasped())
    # so now we have the position 10 time steps from now...
    # we need to lerp that shit...
    p = CAMERA.apply_point((future_target_pos.x, future_target_pos.y))
    # pygame.draw.circle(SCREEN, (0, 255, 0), (int(p[0]),  int(p[1])), 10)

    target_rect.centerx, target_rect.centery = future_target_pos.x, future_target_pos.y

    l, t, _, _ = target_rect
    _, _, w, h = camera
    # new_rect = pygame.Rect(-l+HALF_WIDTH, t+-HALF_HEIGHT, w, h)
    # return new_rect
    return camera


def complex_camera(camera, target_rect, inner_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera.state

    rect = camera.apply(inner_rect)
    target_copy = target_rect.copy()

    # why the fuck am I applying twice???
    target_copy = camera.apply(target_copy)
    target_copy = camera.apply(target_copy)

    if not rect.contains(target_copy):
        if target_copy.top < rect.top:  # then the target rect is ABOVE the camera box...
            diff = rect.top - target_copy.top
            top = camera.state.top - diff
        elif target_copy.bottom > rect.bottom:  # then the target rect is below the camera box
            diff = target_copy.bottom - rect.bottom
            top = camera.state.top + diff
        else:
            top = camera.state.top

        if target_copy.left < rect.left:  # then the target rect is to the left of camera box..
            diff = rect.left - target_copy.left
            left = camera.state.left + diff
        elif target_copy.right > rect.right:
            diff = target_copy.right - rect.right
            left = camera.state.left - diff
        else:
            left = camera.state.left

        new_rect = pygame.Rect(left, top, w, h)
        return new_rect
    else:
        return None

CAMERA = Camera(complex_camera, WIDTH*2, HEIGHT*2)
# CAMERA = Camera(simple_camera, WIDTH*2, HEIGHT*2)
# CAMERA = Camera(projected_focus_camera, WIDTH*2, HEIGHT*2)
