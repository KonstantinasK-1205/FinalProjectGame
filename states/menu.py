from states.state import *


class MenuState(State):
    def __init__(self, game):
        super().__init__(game)

        self.menu_surfaces = []
        self.menu_height = 0
        self.menu_list = {"Final Project!": {}, "New Game": {}, "Options": {}, "Exit": {}}

    def on_set(self):
        self.create_menu_text()
        pg.mouse.set_visible(True)
        pg.event.set_grab(False)
        pg.mixer.stop()

    def handle_events(self, event):
        if event.type == pg.MOUSEMOTION:
            for menu in self.menu_list:
                mouse_pos = pg.mouse.get_pos()
                # Menu positions
                pos_x = self.menu_list[menu]["Position"][0]
                pos_y = self.menu_list[menu]["Position"][1]
                # Menu Size
                width = self.menu_list[menu]["Surface"].get_width()
                height = self.menu_list[menu]["Surface"].get_height()
                # Menu Size
                clickable = self.menu_list[menu]["Clickable"]

                if pos_y < mouse_pos[1] < pos_y + height:
                    if pos_x < mouse_pos[0] < pos_x + width:
                        self.update_menu_text(True, menu)
                    else:
                        self.update_menu_text(False, menu)
                else:
                    self.update_menu_text(False, menu)

        if event.type == pg.MOUSEBUTTONUP:
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
                            self.game.new_game("resources/levels/" + self.game.map_lists[0] + ".txt")
                        if menu == "Options":
                            self.game.current_state = "Options"
                        if menu == "Exit":
                            self.game.running = False

    def update(self, dt):
        pass

    def draw(self):
        self.game.renderer.draw_fullscreen_rect(color=(44, 44, 44))
        self.draw_menu_text()

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
