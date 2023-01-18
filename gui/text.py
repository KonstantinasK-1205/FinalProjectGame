import pygame as pg
from gui.component import *


class Text(Component):
    texture_id = 0

    def __init__(self, game):
        super().__init__(game)

        self.font = None
        self.string = ""
        self.color = (255, 255, 255)
        self.centered = (True, True)

        self.texture_out_of_date = True
        self.texture_name = "gui_text_" + str(Text.texture_id)
        self.texture_size = (0, 0)
        Text.texture_id += 1

    def draw(self):
        super().draw()

        if not self.visible or self.font == None:
            return
        
        if self.texture_out_of_date:
            surface = self.font.render(self.string, True, self.color)
            self.texture_size = surface.get_size()
            self.game.renderer.load_texture_from_surface(self.texture_name, surface)
            self.texture_out_of_date = False

        rect_size = (
            max(self.size[0], self.texture_size[0]),
            max(self.size[1], self.texture_size[1])            
        )

        self.game.renderer.draw_rect(self.position[0], self.position[1], rect_size[0], rect_size[1], color=self.background_color)

        if self.centered[0]:
            position_x = self.position[0] + (self.size[0] - self.texture_size[0]) / 2
        else:
            position_x = self.position[0]
        if self.centered[1]:
            position_y = self.position[1] + (self.size[1] - self.texture_size[1]) / 2
        else:
            position_y = self.position[1]

        self.game.renderer.draw_rect(position_x, position_y, self.texture_size[0], self.texture_size[1], self.texture_name)

    @property
    def font(self):
        return self._font

    @font.setter
    def font(self, font):
        self._font = font
        self.texture_out_of_date = True

    @property
    def string(self):
        return self._string

    @string.setter
    def string(self, string):
        self._string = string
        self.texture_out_of_date = True

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, color):
        self._color = color
        self.texture_out_of_date = True
