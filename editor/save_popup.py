import gui
import editor


class SavePopup(gui.VBox):
    def __init__(self, game):
        super().__init__(game)

        self.flexible = (False, False)
        self.size = (400, 200-80)
        self.position = (
            (self.game.width - self.size[0]) / 2,
            (self.game.height - self.size[1]) / 2
        )

        title_text = gui.Text(self.game)
        title_text.flexible = (True, False)
        title_text.size = (0, 40)
        title_text.font = game.unscaled_fonts[1]
        title_text.string = "Save Level"

        name_text = gui.Text(self.game)
        name_text.flexible = (True, True)
        name_text.size = (0, 0)
        name_text.font = game.unscaled_fonts[1]
        name_text.string = "Level Name:"

        self.name_field = gui.InputField(self.game)
        self.name_field.flexible = (True, True)
        self.name_field.size = (0, 0)
        self.name_field.font = game.unscaled_fonts[1]
        self.name_field.string = ""

        save_button = gui.Button(self.game)
        save_button.flexible = (True, False)
        save_button.size = (0, 40)
        save_button.font = game.unscaled_fonts[1]
        save_button.string = "Save"
        save_button.function = self.handle_save

        cancel_button = gui.Button(self.game)
        cancel_button.flexible = (True, False)
        cancel_button.size = (0, 40)
        cancel_button.font = game.unscaled_fonts[1]
        cancel_button.string = "Cancel"
        cancel_button.function = self.handle_close

        name_hbox = gui.HBox(self.game)
        name_hbox.size = (0, 40)
        name_hbox.flexible = (True, False)
        name_hbox.add(name_text)
        name_hbox.add(self.name_field)

        button_hbox = gui.HBox(self.game)
        button_hbox.size = (0, 40)
        button_hbox.flexible = (True, False)
        button_hbox.add(save_button)
        button_hbox.add(cancel_button)

        self.add(title_text)
        self.add(name_hbox)
        self.add(button_hbox)

    def handle_save(self, component):
        try:
            self.game.map.save(self.name_field.string)
        except:
            self.game.current_state_obj.popup = editor.TextPopup(
                self.game,
                "Save Level",
                "Could not save level"
            )
            self.game.current_state_obj.popup.layout()
            return

        self.game.current_state_obj.center_panel.update_gridbox()
        self.game.current_state_obj.popup = None

    def handle_close(self, component):
        self.game.current_state_obj.popup = None
