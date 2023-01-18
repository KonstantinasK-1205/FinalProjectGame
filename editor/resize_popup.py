import gui
import editor


class ResizePopup(gui.VBox):
    def __init__(self, game):
        super().__init__(game)

        self.flexible = (False, False)
        self.size = (400, 160)
        self.position = (
            (self.game.width - self.size[0]) / 2,
            (self.game.height - self.size[1]) / 2
        )

        title_text = gui.Text(self.game)
        title_text.flexible = (True, False)
        title_text.size = (0, 40)
        title_text.font = game.unscaled_fonts[1]
        title_text.string = "Level Resize"

        x_text = gui.Text(self.game)
        x_text.flexible = (True, True)
        x_text.size = (0, 0)
        x_text.font = game.unscaled_fonts[1]
        x_text.string = "Width:"

        self.x_field = gui.InputField(self.game)
        self.x_field.flexible = (True, True)
        self.x_field.size = (0, 0)
        self.x_field.font = game.unscaled_fonts[1]
        self.x_field.string = str(self.game.map.width)

        y_text = gui.Text(self.game)
        y_text.flexible = (True, True)
        y_text.size = (0, 0)
        y_text.font = game.unscaled_fonts[1]
        y_text.string = "Height:"

        self.y_field = gui.InputField(self.game)
        self.y_field.flexible = (True, True)
        self.y_field.size = (0, 0)
        self.y_field.font = game.unscaled_fonts[1]
        self.y_field.string = str(self.game.map.height)

        x_hbox = gui.HBox(self.game)
        x_hbox.size = (0, 40)
        x_hbox.flexible = (True, False)
        x_hbox.add(x_text)
        x_hbox.add(self.x_field)

        y_hbox = gui.HBox(self.game)
        y_hbox.size = (0, 40)
        y_hbox.flexible = (True, False)
        y_hbox.add(y_text)
        y_hbox.add(self.y_field)

        resize_button = gui.Button(self.game)
        resize_button.flexible = (True, False)
        resize_button.size = (0, 40)
        resize_button.font = game.unscaled_fonts[1]
        resize_button.string = "Resize"
        resize_button.function = self.handle_resize

        cancel_button = gui.Button(self.game)
        cancel_button.flexible = (True, False)
        cancel_button.size = (0, 40)
        cancel_button.font = game.unscaled_fonts[1]
        cancel_button.string = "Cancel"
        cancel_button.function = self.handle_close

        button_hbox = gui.HBox(self.game)
        button_hbox.size = (0, 40)
        button_hbox.flexible = (True, False)
        button_hbox.add(resize_button)
        button_hbox.add(cancel_button)

        self.add(title_text)
        self.add(x_hbox)
        self.add(y_hbox)
        self.add(button_hbox)

    def handle_resize(self, component):
        try:
            x_int = int(self.x_field.string)
            y_int = int(self.y_field.string)
            if x_int < 1 or y_int < 1:
                raise TypeError("Level size must be positive")
        except:
            self.game.current_state_obj.popup = editor.TextPopup(
                self.game,
                "Level Resize",
                "Invalid width or height"                
            )
            self.game.current_state_obj.popup.layout()
            return

        self.game.map.resize((x_int, y_int))
        self.game.current_state_obj.center_panel.update_gridbox()
        self.game.current_state_obj.popup = None

    def handle_close(self, component):
        self.game.current_state_obj.popup = None
