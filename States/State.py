import pygame as pg
from settings import *

rgb_colors = {
    "White": (255, 255, 255),
    "Red": (255, 0, 0),
    "Green": (0, 255, 0),
    "Blue": (0, 0, 255),
    "Black": (0, 0, 0),
}


def center_surface(surface):
    return (RES[0] - surface.get_width()) / 2, (RES[1] - surface.get_height()) / 2


def create_text_surface(font, string, color='White', centered=True):
    position = (0, 0)
    if color not in rgb_colors:
        color = 'White'
    surface = font.render(string, True, rgb_colors[color])

    if centered:
        position = center_surface(surface)
    return [surface, position]


class State:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.font = pg.font.Font("resources/fonts/Font.ttf", 48)

    @staticmethod
    def on_set():
        return None

    @staticmethod
    def update():
        return None

    @staticmethod
    def draw():
        return None
