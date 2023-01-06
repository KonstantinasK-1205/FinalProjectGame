import pygame as pg


STATE_WAIT_MS = 500


class State:
    def __init__(self, game):
        self.game = game

        self.title_text = ""
        self.text = []
        self.text_surfaces = []
        self.text_height = 0

    def on_set(self):
        pass

    def handle_event(self, event):
        pass

    def update(self):
        pass

    def draw(self):
        self.game.renderer.draw_fullscreen_rect(color=(44, 44, 44))

    def update_state_text(self):
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

    def draw_state_text(self):
        self.update_state_text()
        for i in range(len(self.text_surfaces)):
            surface = self.text_surfaces[i]
            self.game.renderer.load_texture_from_surface("state_text_" + str(i), surface[1])
            self.game.renderer.draw_rect(
                self.game.width / 2 - surface[1].get_width() / 2,
                self.game.height / 2 - self.text_height / 2 + surface[0],
                surface[1].get_width(),
                surface[1].get_height(),
                "state_text_" + str(i)
            )
