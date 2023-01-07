from states.state import *


class MenuState(State):
    def __init__(self, game):
        super().__init__(game)

        self.menu_surfaces = []
        self.menu_height = 0
        self.menu_list = {}

        self.initialized = False

    def on_set(self):
        if self.game.map.created:
            self.menu_list = {"Final Project": {}, "Resume Game": {}, "Restart Level": {},
                              "New Game": {}, "Options": {}, "Exit": {}}
        else:
            self.menu_list = {"Final Project": {}, "New Game": {}, "Options": {}, "Exit": {}}

        self.initialized = False

        self.create_menu_text()
        pg.mouse.set_visible(True)
        pg.event.set_grab(False)
        pg.mixer.stop()

    def handle_event(self, event):
        if not self.initialized:
            return

        if event.type == pg.MOUSEMOTION:
            for menu in self.menu_list:
                mouse_pos = pg.mouse.get_pos()
                # Menu positions
                pos_x = self.menu_list[menu]["Position"][0]
                pos_y = self.menu_list[menu]["Position"][1]
                # Menu Size
                width = self.menu_list[menu]["Surface"].get_width()
                height = self.menu_list[menu]["Surface"].get_height()

                if pos_y < mouse_pos[1] < pos_y + height:
                    if pos_x < mouse_pos[0] < pos_x + width:
                        self.update_menu_text(True, menu)
                    else:
                        self.update_menu_text(False, menu)
                else:
                    self.update_menu_text(False, menu)
        elif event.type == pg.MOUSEBUTTONUP and event.button == 1:
            for menu in self.menu_list:
                mouse_pos = pg.mouse.get_pos()
                # Menu positions
                pos_x = self.menu_list[menu]["Position"][0]
                pos_y = self.menu_list[menu]["Position"][1]

                width = self.menu_list[menu]["Surface"].get_width()
                height = self.menu_list[menu]["Surface"].get_height()

                if pos_x < mouse_pos[0] < pos_x + width:
                    if pos_y < mouse_pos[1] < pos_y + height:
                        if menu == "New Game":
                            self.game.current_state = "Loading"
                            self.game.new_game(self.game.starting_map)
                        elif menu == "Restart Level":
                            self.game.current_state = "Loading"
                            self.game.restart_level(self.game.current_map)
                        elif menu == "Resume Game":
                            self.game.current_state = "Game"
                        elif menu == "Options":
                            self.game.current_state = "Options"
                        elif menu == "Exit":
                            self.game.running = False
        elif event.type == pg.WINDOWSIZECHANGED:
            self.create_menu_text()

    def update(self):
        pass

    def draw(self):
        super().draw()
        self.draw_menu_text()
        self.initialized = True

    def create_menu_text(self):
        self.menu_surfaces = []
        self.menu_height = 0

        for menu in self.menu_list:
            if "Final Project" in menu:
                surface = self.game.font.render(menu, True, (255, 255, 255))
                self.menu_list[menu]["Clickable"] = False
            else:
                surface = self.game.font_small.render(menu, True, (255, 255, 255))
                self.menu_list[menu]["Clickable"] = True

            self.menu_list[menu]["Original Title"] = menu
            self.menu_list[menu]["Menu Height"] = self.menu_height
            self.menu_list[menu]["Surface"] = surface
            self.menu_height += surface.get_height()

    def draw_menu_text(self):
        for i, menu in enumerate(self.menu_list):
            surface = self.menu_list[menu]["Surface"]
            menu_height = self.menu_list[menu]["Menu Height"]
            pos_x = self.game.width / 2 - surface.get_width() / 2
            if i == 0:
                pos_y = self.game.height / 2 - (self.menu_height + menu_height)
            else:
                pos_y = self.game.height / 2 - self.menu_height / 2 + menu_height * 1.5
            self.menu_list[menu]["Position"] = [pos_x, pos_y]
            self.game.renderer.load_texture_from_surface("menu_text_" + str(i), surface)
            self.game.renderer.draw_rect(
                self.menu_list[menu]["Position"][0],
                self.menu_list[menu]["Position"][1],
                surface.get_width(),
                surface.get_height(),
                "menu_text_" + str(i)
            )

    def update_menu_text(self, hover, menu):
        menu_dict = self.menu_list[menu]
        if not menu_dict["Clickable"]:
            return

        if hover:
            surface = self.game.font_small.render("< " + menu + " >", True, (255, 255, 255))
        else:
            surface = self.game.font_small.render(menu_dict["Original Title"], True, (255, 255, 255))

        self.menu_list[menu]["Surface"] = surface
        self.game.renderer.load_texture_from_surface("menu_text_" + str(menu), surface)
