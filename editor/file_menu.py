import gui
import pygame as pg
import editor


class FileMenu(gui.VBox):
    def __init__(self, game):
        super().__init__(game)

        self.flexible = (False, False)
        self.size = (100, 200)

        new_button = gui.Button(self.game)
        new_button.flexible = (True, False)
        new_button.size = (0, 40)
        new_button.font = game.unscaled_fonts[2]
        new_button.string = "New"
        new_button.function = self.handle_new

        open_button = gui.Button(self.game)
        open_button.flexible = (True, False)
        open_button.size = (0, 40)
        open_button.font = game.unscaled_fonts[2]
        open_button.string = "Open"
        open_button.function = self.handle_open

        save_button = gui.Button(self.game)
        save_button.flexible = (True, False)
        save_button.size = (0, 40)
        save_button.font = game.unscaled_fonts[2]
        save_button.string = "Save"
        save_button.function = self.handle_save

        save_as_button = gui.Button(self.game)
        save_as_button.flexible = (True, False)
        save_as_button.size = (0, 40)
        save_as_button.font = game.unscaled_fonts[2]
        save_as_button.string = "Save As"
        save_as_button.function = self.handle_save_as

        quit_button = gui.Button(self.game)
        quit_button.flexible = (True, False)
        quit_button.size = (0, 40)
        quit_button.font = game.unscaled_fonts[2]
        quit_button.string = "Quit"
        quit_button.function = self.handle_quit

        self.add(new_button)
        self.add(open_button)
        self.add(save_button)
        self.add(save_as_button)
        self.add(quit_button)

    def handle_event(self, event):
        super().handle_event(event)

        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            if event.pos[0] < self.position[0] or event.pos[0] > (self.position[0] + self.size[0]) or \
               event.pos[1] < self.position[1] or event.pos[1] > (self.position[1] + self.size[1]):
                self.game.current_state_obj.popup = None

    def do_nothing(self, component):
        pass

    def handle_open(self, component):
        self.game.current_state_obj.popup = editor.OpenPopup(self.game)
        self.game.current_state_obj.popup.layout()

    def handle_save(self, component):
        if not self.game.current_state_obj.current_level_name:
            self.game.current_state_obj.popup = editor.SavePopup(self.game)
            self.game.current_state_obj.popup.layout()
        else:
            self.game.map.save(self.game.current_state_obj.current_level_name)
            self.game.current_state_obj.popup = None

    def handle_save_as(self, component):
        self.game.current_state_obj.popup = editor.SavePopup(self.game)
        self.game.current_state_obj.popup.layout()

    def handle_new(self, component):
        self.game.map.create((20, 15))
        self.game.current_state_obj.center_panel.update_gridbox()
        self.game.current_state_obj.current_level_name = ""

        self.game.current_state_obj.popup = None

    def handle_quit(self, component):
        self.game.current_state_obj.popup = None
        self.game.map.reset()
        self.game.sound.play_music()
        self.game.current_state = "Menu"
