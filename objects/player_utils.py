import objects.player
import objects.player_on_planet
import objects.test_pilot


def create_player(sprite_name, controller, pos):
    print("creating player again!!")
    objects.player.Player(sprite_name, controller, pos)


def create_player_on_planet(sprite_name, controller, pos, planet):
    objects.player_on_planet.PlayerOnPlanet(sprite_name, controller, pos, planet)


def create_test_pilot(sprite_name, controller, pos):
    objects.test_pilot.TestPilot(sprite_name, controller, pos)
