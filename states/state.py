import pygame as pg

from settings import *

class State:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen

        self.title_text = ""
        self.text = []
        self.text_surfaces = []
        self.text_height = 0

    def update_text(self):
        self.text_surfaces = []
        self.text_height = 0

        if not self.title_text == "":
            surface = self.game.font.render(self.title_text, True, (255, 255, 255))
            self.text_surfaces.append((self.text_height, surface))
            self.text_height += surface.get_height()

        for text in self.text:
            surface = self.game.font_small.render(text, True, (255, 255, 255))
            self.text_surfaces.append((self.text_height, surface))
            self.text_height += surface.get_height()

    def on_set(self):
        pass

    def handle_events(self, events):
        pass

    def update(self, dt):
        pass

    def draw(self):
        pass

    def draw_text(self):
        for ts in self.text_surfaces:
            self.screen.blit(ts[1], (WIDTH / 2 - ts[1].get_width() / 2, HEIGHT / 2 - self.text_height / 2 + ts[0]))
