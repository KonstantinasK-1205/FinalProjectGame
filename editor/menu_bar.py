import gui
import editor


class MenuBar(gui.HBox):
    def __init__(self, game):
        super().__init__(game)

        self.flexible = (True, False)
        self.size = (0, 40)

        self.file_button = gui.Button(self.game)
        self.file_button.flexible = (False, True)
        self.file_button.size = (80, 0)
        self.file_button.font = game.unscaled_fonts[1]
        self.file_button.string = "File"
        self.file_button.function = self.open_file_menu

        self.level_button = gui.Button(self.game)
        self.level_button.flexible = (False, True)
        self.level_button.size = (80, 0)
        self.level_button.font = game.unscaled_fonts[1]
        self.level_button.string = "Level"
        self.level_button.function = self.open_level_menu

        spacer = gui.Component(self.game)

        self.fps_text = gui.Text(self.game)
        self.fps_text.flexible = (False, True)
        self.fps_text.size = (120, 0)
        self.fps_text.font = game.unscaled_fonts[1]

        self.add(self.file_button)
        self.add(self.level_button)
        self.add(spacer)
        self.add(self.fps_text)

    def draw(self):
        super().draw()

        self.fps_text.string = str(int(self.game.clock.get_fps())) + " FPS"

    def open_file_menu(self, component):
        self.game.current_state_obj.popup = editor.FileMenu(self.game)
        self.game.current_state_obj.popup.position = (
            self.file_button.position[0],
            self.position[1] + self.size[1]
        )
        self.game.current_state_obj.popup.layout()

    def open_level_menu(self, component):
        self.game.current_state_obj.popup = editor.LevelMenu(self.game)
        self.game.current_state_obj.popup.position = (
            self.level_button.position[0],
            self.position[1] + self.size[1]
        )
        self.game.current_state_obj.popup.layout()
