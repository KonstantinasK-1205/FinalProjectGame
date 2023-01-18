from states.state import *
import gui
import editor
import pygame as pg
import copy


class EditorState(State):
    def __init__(self, game):
        super().__init__(game)

        self.current_level_name = ""

        self.left_panel = editor.LeftPanel(self.game)
        self.center_panel = editor.CenterPanel(self.game)

        main_panel = gui.HBox(self.game)
        main_panel.add(self.left_panel)
        main_panel.add(self.center_panel)
        main_panel.add(editor.RightPanel(self.game))

        self.gui = gui.VBox(self.game)
        self.gui.size = (self.game.width, self.game.height)
        self.gui.add(editor.MenuBar(self.game))
        self.gui.add(main_panel)
        self.gui.add(editor.StatusBar(self.game))

        self.popup = None

    def on_set(self):
        self.game.sound.stop_music()

        self.current_level_name = ""

        self.game.map.create((20, 15))
        self.center_panel.update_gridbox()

        self.gui.size = (self.game.width, self.game.height)
        self.gui.layout()

    def handle_event(self, event):
        if event.type == pg.WINDOWRESIZED:
            self.gui.size = (self.game.width, self.game.height)
            self.gui.layout()

            if self.popup:
                self.popup.position = (
                    (self.game.width - self.popup.size[0]) / 2,
                    (self.game.height - self.popup.size[1]) / 2
                )
                self.popup.layout()

        if self.popup:
            # Only pass events to GUI if they do not overlap the popup
            if event.type == pg.MOUSEMOTION or event.type == pg.MOUSEBUTTONUP or event.type == pg.MOUSEBUTTONDOWN:
                if event.pos[0] < self.popup.position[0] or event.pos[0] > (self.popup.position[0] + self.popup.size[0]) or \
                   event.pos[1] < self.popup.position[1] or event.pos[1] > (self.popup.position[1] + self.popup.size[1]):
                    self.gui.handle_event(event)

            self.popup.handle_event(event)
        else:
            self.gui.handle_event(event)

    def update(self):
        self.gui.update()

        if self.popup:
            self.popup.update()

    def draw(self):
        self.gui.draw()
        self.gui.draw_tooltips()

        if self.popup:
            self.popup.draw()
            self.popup.draw_tooltips()
