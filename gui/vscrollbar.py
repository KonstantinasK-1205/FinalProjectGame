import pygame as pg
from gui.text import *
from gui.vbox import *
from gui.button import *
from gui.component import *


class VScrollbar(VBox):
    def __init__(self, game):
        super().__init__(game)

        self.min_value = 0
        self.max_value = 100
        self.value = 50

        self.step = 10

        self.button_height = 20
        self.slider_height = 100

        self.button_hold_delay = 100
        self.button_hold_delay_timer = 0

        self.top_button = Button(self.game)
        self.top_button.size = (0, 20)
        self.top_button.flexible = (True, False)
        self.top_button.font = self.game.unscaled_fonts[2]
        self.top_button.string = "^"
        self.top_button.function = self.handle_top_button
        self.add(self.top_button)

        self.spacer = Component(self.game)
        self.spacer.background_color = (0, 0, 0)
        self.add(self.spacer)

        self.bottom_button = Button(self.game)
        self.bottom_button.size = (0, 20)
        self.bottom_button.flexible = (True, False)
        self.bottom_button.font = self.game.unscaled_fonts[2]
        self.bottom_button.string = "v"
        self.bottom_button.function = self.handle_bottom_button
        self.add(self.bottom_button)

        self.slider_position = (
            self.position[0],
            self.spacer.position[1] + ((self.value - self.min_value) / (self.max_value - self.min_value)) * (self.size[1] - self.slider_height - self.button_height * 2)
        )
        self.slider_pressed = False

    def update(self):
        super().update()

    def handle_event(self, event):
        super().handle_event(event)

        if event.type == pg.MOUSEMOTION:
            if self.slider_pressed:
                self.value = ((event.pos[1] - self.spacer.position[1]) / (self.spacer.size[1])) * (self.max_value - self.min_value) + self.min_value
                self.value = min(self.max_value, max(self.min_value, self.value))
        elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            if event.pos[0] > self.spacer.position[0] and event.pos[0] < self.spacer.position[0] + self.spacer.size[0] and event.pos[1] > self.spacer.position[1] and event.pos[1] < self.spacer.position[1] + self.spacer.size[1]:
                self.slider_pressed = True
        elif event.type == pg.MOUSEBUTTONUP and event.button == 1:
            self.slider_pressed = False
        elif event.type == pg.WINDOWFOCUSLOST:
            self.slider_pressed = False

    def draw(self):
        super().draw()

        # Draw box
        self.slider_position = (
            self.position[0],
            self.spacer.position[1] + ((self.value - self.min_value) / (self.max_value - self.min_value)) * (self.size[1] - self.slider_height - self.button_height * 2)
        )
        self.game.renderer.draw_rect(
            self.slider_position[0],
            self.slider_position[1],
            self.size[0],
            self.slider_height,
            color = (64, 64, 64)
        )

    def handle_top_button(self, component):
        self.value = max(self.min_value, self.value - self.step)
        self.button_hold_delay_timer = 0

    def handle_bottom_button(self, component):
        self.value = min(self.max_value, self.value + self.step)
        self.button_hold_delay_timer = 0
