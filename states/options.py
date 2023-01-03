from states.state import *


class OptionsState(State):
    def __init__(self, game):
        super().__init__(game)

        self.current_resolution = (WIDTH, HEIGHT)
        self.available_resolutions = pg.display.list_modes()
        self.index_of_resolution = self.available_resolutions.index(self.current_resolution)

        self.menu_surfaces = []
        self.menu_height = 0
        self.menu_list = {
            "Options": {
                "Option": None
            },
            "Resolution": {
                "Option": self.current_resolution
            },
            "Full screen": {
                "Option": False
            },
            "Vsync": {
                "Option": True
            },
            "Show FPS": {
                "Option": self.game.show_fps
            },
            "Sounds": {
                "Option": self.game.sound.sound_enabled
            },
            "Apply": {
                "Option": None
            },
            "Back": {
                "Option": None
            }}

        self.initialized = False

    def on_set(self):
        self.create_menu_text()

    def handle_events(self, event):
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
                        self.on_hover(menu, True)
                    else:
                        self.on_hover(menu, False)
                else:
                    self.on_hover(menu, False)
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
                        self.change_setting(menu)
                        if "Apply" in menu:
                            self.apply_settings()
                        if "Back" in menu:
                            self.game.current_state = "Menu"
        elif event.type == pg.WINDOWSIZECHANGED:
            self.create_menu_text()

    def update(self):
        pass

    def draw(self):
        self.game.renderer.draw_fullscreen_rect(color=(44, 44, 44))
        self.draw_menu_text()
        self.initialized = True

    def apply_settings(self):
        resolution = self.menu_list["Resolution"]["Option"]
        if self.menu_list["Full screen"]["Option"]:
            pg.display.set_mode(resolution, pg.RESIZABLE | pg.FULLSCREEN | pg.OPENGL | pg.DOUBLEBUF, self.menu_list["Vsync"]["Option"])
        else:
            pg.display.set_mode(resolution, pg.RESIZABLE | pg.OPENGL | pg.DOUBLEBUF, self.menu_list["Vsync"]["Option"])

        self.game.sound.sound_enabled = self.menu_list["Sounds"]["Option"]
        self.game.show_fps = self.menu_list["Show FPS"]["Option"]

    def change_setting(self, menu):
        menu_dict = self.menu_list[menu]
        # Change settings only those who have Option
        if type(menu_dict["Option"]) == tuple:
            self.index_of_resolution -= 1
            if self.index_of_resolution < 0:
                self.index_of_resolution = len(self.available_resolutions) - 1
            menu_dict["Option"] = self.available_resolutions[self.index_of_resolution]
            option_text = menu_dict["Option"]
            # Set button text and update it for renderer
            menu_dict["Original Title"] = menu + ": " + str(option_text)
            menu_dict["Surface"] = self.game.font_small.render("< " + menu_dict["Original Title"] + " >",
                                                               True, (255, 255, 255))
            self.game.renderer.load_texture_from_surface("menu_text_" + str(menu), menu_dict["Surface"])

        if type(menu_dict["Option"]) == bool:
            # Reverse boolean and set correct (ON/OFF) option text
            menu_dict["Option"] = not menu_dict["Option"]
            option_text = 'Off' if menu_dict["Option"] is False else 'On'

            # Set button text and update it for renderer
            menu_dict["Original Title"] = menu + ": " + option_text
            menu_dict["Surface"] = self.game.font_small.render("< " + menu_dict["Original Title"] + " >",
                                                               True, (255, 255, 255))
            self.game.renderer.load_texture_from_surface("menu_text_" + str(menu), menu_dict["Surface"])

    def on_hover(self, menu, hover):
        menu_dict = self.menu_list[menu]
        font_small = self.game.font_small
        if hover:
            menu_dict["Surface"] = font_small.render("< " + menu_dict["Original Title"] + " >", True, (255, 255, 255))
        else:
            menu_dict["Surface"] = font_small.render(menu_dict["Original Title"], True, (255, 255, 255))
        self.game.renderer.load_texture_from_surface("menu_text_" + str(menu), menu_dict["Surface"])

    def create_menu_text(self):
        self.menu_surfaces = []
        self.menu_height = 0

        for menu in self.menu_list:
            menu_dict = self.menu_list[menu]
            if type(menu_dict["Option"]) == bool:
                menu_dict["Original Title"] = menu + ": " + self.get_boolean_state(menu_dict["Option"])
            elif type(menu_dict["Option"]) == tuple:
                menu_dict["Original Title"] = menu + ": " + str(menu_dict["Option"])
            else:
                menu_dict["Original Title"] = menu

            menu_dict["Surface"] = self.game.font_small.render(menu_dict["Original Title"], True, (255, 255, 255))
            menu_dict["Menu Height"] = self.menu_height
            self.menu_height += menu_dict["Surface"].get_height()

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

    def get_boolean_state(self, boolean):
        if boolean:
            return "On"
        return "Off"
