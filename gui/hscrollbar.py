import pygame as pg
from gui.text import *
from gui.hbox import *
from gui.button import *
from gui.component import *


class HScrollbar(HBox):
    def __init__(self, game):
        super().__init__(game)

        self.min_value = 0
        self.max_value = 100
        self.value = 50

        self.step = 10

        self.button_width = 20
        self.slider_width = 100

        self.button_hold_delay = 100
        self.button_hold_delay_timer = 0

        self.left_button = Button(self.game)
        self.left_button.size = (20, 0)
        self.left_button.flexible = (False, True)
        self.left_button.font = self.game.unscaled_fonts[2]
        self.left_button.string = "<"
        self.left_button.function = self.handle_left_button
        self.add(self.left_button)

        self.spacer = Component(self.game)
        self.spacer.background_color = (0, 0, 0)
        self.add(self.spacer)

        self.right_button = Button(self.game)
        self.right_button.size = (20, 0)
        self.right_button.flexible = (False, True)
        self.right_button.font = self.game.unscaled_fonts[2]
        self.right_button.string = ">"
        self.right_button.function = self.handle_right_button
        self.add(self.right_button)

        self.slider_position = (
            self.spacer.position[0] + ((self.value - self.min_value) / (self.max_value - self.min_value)) * (self.size[0] - self.slider_width - self.button_width * 2),
            self.position[1]
        )
        self.slider_pressed = False

    def update(self):
        super().update()

    def handle_event(self, event):
        super().handle_event(event)

        if event.type == pg.MOUSEMOTION:
            if self.slider_pressed:
                self.value = ((event.pos[0] - self.spacer.position[0]) / (self.spacer.size[0])) * (self.max_value - self.min_value) + self.min_value
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
            self.spacer.position[0] + ((self.value - self.min_value) / (self.max_value - self.min_value)) * (self.size[0] - self.slider_width - self.button_width * 2),
            self.position[1]
        )
        self.game.renderer.draw_rect(
            self.slider_position[0],
            self.slider_position[1],
            self.slider_width,
            self.size[1],
            color = (64, 64, 64)
        )

    def handle_left_button(self, component):
        self.value = max(self.min_value, self.value - self.step)
        self.button_hold_delay_timer = 0

    def handle_right_button(self, component):
        self.value = min(self.max_value, self.value + self.step)
        self.button_hold_delay_timer = 0
