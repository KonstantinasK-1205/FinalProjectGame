import gui
import pygame as pg
import editor


class LevelMenu(gui.VBox):
    def __init__(self, game):
        super().__init__(game)

        self.flexible = (False, False)
        self.size = (100, 80)

        resize_button = gui.Button(self.game)
        resize_button.flexible = (True, False)
        resize_button.size = (0, 40)
        resize_button.font = game.unscaled_fonts[2]
        resize_button.string = "Resize"
        resize_button.function = self.handle_resize

        properties_button = gui.Button(self.game)
        properties_button.flexible = (True, False)
        properties_button.size = (0, 40)
        properties_button.font = game.unscaled_fonts[2]
        properties_button.string = "Properties"
        properties_button.function = self.handle_properties

        self.add(resize_button)
        self.add(properties_button)

    def handle_event(self, event):
        super().handle_event(event)

        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            if event.pos[0] < self.position[0] or event.pos[0] > (self.position[0] + self.size[0]) or \
               event.pos[1] < self.position[1] or event.pos[1] > (self.position[1] + self.size[1]):
                self.game.current_state_obj.popup = None

    def handle_resize(self, component):
        self.game.current_state_obj.popup = editor.ResizePopup(self.game)
        self.game.current_state_obj.popup.layout()

    def handle_properties(self, component):
        self.game.current_state_obj.popup = editor.PropertiesPopup(self.game)
        self.game.current_state_obj.popup.layout()
