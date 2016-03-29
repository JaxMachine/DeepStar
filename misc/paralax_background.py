import pygame
from random import randrange, choice

MAX_STARS = 250
STAR_SPEED = 2


def init_stars(screen):

    """ create the starfield """
    global stars
    stars = []
    for i in range(MAX_STARS):
        star = [randrange(0, screen.get_width() - 1),
                randrange(0, screen.get_height() - 1),
                choice([1, 2, 3])]
        stars.append(star)
    # print(stars)
    print("printing screen stats")
    print(screen.get_width(), screen.get_height())


def move_and_draw_stars(screen, camera):
    global stars
    # print(stars)
    for star in stars:
        # does this move the stars? , so can't I take in the current camera pos,
        offset = camera.apply(pygame.Rect(star[0], star[1], star[2], star[2]))

        offset.x += star[2]
        offset.y += star[2]

        # If the star hit the bottom border then we reposition
        # it in the top of the screen with a random X coordinate.
        if star[1] > screen.get_height() + camera.state.y:  # offset will be 0...
            star[1] = camera.state.y + 1
            star[0] = randrange(-camera.state.x, -camera.state.x + screen.get_width() - 1)
            star[2] = choice([1, 2, 3])
        elif star[1] < camera.state.y:
            star[1] = camera.state.y + screen.get_height() - 1
            star[0] = randrange(-camera.state.x, -camera.state.x + screen.get_width() - 1)
            star[2] = choice([1, 2, 3])
        if star[0] > screen.get_width() + (-camera.state.x):
            star[0] = (-camera.state.x)
            star[1] = randrange(camera.state.y, camera.state.y + screen.get_height() - 1)
            star[2] = choice([1, 2, 3])
        elif star[0] < (-camera.state.x):
            star[0] = (-camera.state.x) + screen.get_width() - 1
            star[1] = randrange(camera.state.y, camera.state.y + screen.get_height() - 1)
            star[2] = choice([1, 2, 3])
        # Adjust the star color acording to the speed.
        # The slower the star, the darker should be its color.
        if star[2] == 1:
            color = (100, 100, 100)
        elif star[2] == 2:
            color = (190, 190, 190)
        elif star[2] == 3:
            color = (255, 255, 255)

        # Draw the star as a rectangle.
        screen.fill(color, (offset.x, offset.y, star[2], star[2]))
