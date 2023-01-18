import pygame as pg
from gui.text import *


class Button(Text):
    def __init__(self, game):
        super().__init__(game)

        self.hover_color = (64, 8, 8)
        self.pressed_color = (32, 8, 8)
        self.hovering = False
        self.pressed = False
        self.function = None

    def handle_event(self, event):
        super().handle_event(event)

        if not self.visible or not self.active:
            return

        if event.type == pg.MOUSEMOTION:
            if event.pos[0] >= self.position[0] and event.pos[0] < (self.position[0] + self.size[0]) and \
               event.pos[1] >= self.position[1] and event.pos[1] < (self.position[1] + self.size[1]):
                self.hovering = True
            else:
                self.hovering = False
                self.pressed = False
        elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            if self.hovering == True:
                self.pressed = True
        elif event.type == pg.MOUSEBUTTONUP and event.button == 1:
            self.hovering = False
            self.pressed = False
            if event.pos[0] >= self.position[0] and event.pos[0] < (self.position[0] + self.size[0]) and \
               event.pos[1] >= self.position[1] and event.pos[1] < (self.position[1] + self.size[1]):
                self.function(self)
        elif event.type == pg.WINDOWFOCUSLOST:
            self.hovering = False
            self.pressed = False

    def draw(self):
        if not self.visible:
            return

        if self.pressed:
            self.game.renderer.draw_rect(
                self.position[0],
                self.position[1],
                self.size[0],
                self.size[1],
                color=self.pressed_color
            )
        elif self.hovering:
            self.game.renderer.draw_rect(
                self.position[0],
                self.position[1],
                self.size[0],
                self.size[1],
                color=self.hover_color
            )
        else:
            self.game.renderer.draw_rect(
                self.position[0],
                self.position[1],
                self.size[0],
                self.size[1],
                color=self.background_color
            )

        if not self.background_texture == None:
            self.game.renderer.draw_rect(
                self.position[0],
                self.position[1],
                self.size[0],
                self.size[1],
                self.background_texture
            )

        if self.font == None:
            return

        if self.texture_out_of_date:
            surface = self.font.render(self.string, True, self.color)
            self.texture_size = surface.get_size()
            self.game.renderer.load_texture_from_surface(self.texture_name, surface)
            self.texture_out_of_date = False

        position = (
            self.position[0] + (self.size[0] - self.texture_size[0]) / 2,
            self.position[1] + (self.size[1] - self.texture_size[1]) / 2
        )
        self.game.renderer.draw_rect(
            position[0],
            position[1],
            self.texture_size[0],
            self.texture_size[1],
            self.texture_name
        )
