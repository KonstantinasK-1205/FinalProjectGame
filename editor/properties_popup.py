import gui
import editor


class PropertiesPopup(gui.VBox):
    def __init__(self, game):
        super().__init__(game)

        self.flexible = (False, False)
        self.size = (600, 520)
        self.position = (
            (self.game.width - self.size[0]) / 2,
            (self.game.height - self.size[1]) / 2
        )

        title_text = gui.Text(self.game)
        title_text.flexible = (True, False)
        title_text.size = (0, 40)
        title_text.font = game.unscaled_fonts[1]
        title_text.string = "Level Properties"

        key_text = gui.Text(self.game)
        key_text.flexible = (True, True)
        key_text.size = (0, 0)
        key_text.font = game.unscaled_fonts[1]
        key_text.string = "Key"

        value_text = gui.Text(self.game)
        value_text.flexible = (True, True)
        value_text.size = (0, 0)
        value_text.font = game.unscaled_fonts[1]
        value_text.string = "Value"

        header_hbox = gui.HBox(self.game)
        header_hbox.size = (0, 40)
        header_hbox.flexible = (True, False)
        header_hbox.add(key_text)
        header_hbox.add(value_text)

        self.add(title_text)
        self.add(header_hbox)

        self.key_fields = [None] * 10
        self.value_fields = [None] * 10
        for i in range(10):
            self.key_fields[i] = gui.InputField(self.game)
            self.key_fields[i].flexible = (True, True)
            self.key_fields[i].size = (0, 0)
            self.key_fields[i].font = game.unscaled_fonts[2]
            self.key_fields[i].string = ""

            self.value_fields[i] = gui.InputField(self.game)
            self.value_fields[i].flexible = (True, True)
            self.value_fields[i].size = (0, 0)
            self.value_fields[i].font = game.unscaled_fonts[2]
            self.value_fields[i].string = ""

            if len(self.game.map.properties) > i:
                prop = self.game.map.properties[i].split(": ")
                self.key_fields[i].string = prop[0]
                self.value_fields[i].string = prop[1]

            hbox = gui.HBox(self.game)
            hbox.size = (0, 40)
            hbox.flexible = (True, False)
            hbox.add(self.key_fields[i])
            hbox.add(self.value_fields[i])

            self.add(hbox)

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

        button_hbox = gui.HBox(self.game)
        button_hbox.size = (0, 40)
        button_hbox.flexible = (True, False)
        button_hbox.add(save_button)
        button_hbox.add(cancel_button)

        self.add(button_hbox)

    def handle_save(self, component):
        for i in range(10):
            self.key_fields[i].string = self.key_fields[i].string.strip()
            self.value_fields[i].string = self.value_fields[i].string.strip()

            if ":" in self.key_fields[i].string or ":" in self.value_fields[i].string:
                self.game.current_state_obj.popup = editor.TextPopup(
                    self.game,
                    "Level Properties",
                    "Invalid character in properties"
                )
                self.game.current_state_obj.popup.layout()
                return
            elif self.key_fields[i].string and not self.value_fields[i].string:
                self.game.current_state_obj.popup = editor.TextPopup(
                    self.game,
                    "Level Properties",
                    "Key specified without value"
                )
                self.game.current_state_obj.popup.layout()
                return
            elif not self.key_fields[i].string and self.value_fields[i].string:
                self.game.current_state_obj.popup = editor.TextPopup(
                    self.game,
                    "Level Properties",
                    "Value specified without key"
                )
                self.game.current_state_obj.popup.layout()
                return

        self.game.map.properties = []
        
        for i in range(10):
            if not (self.key_fields[i].string and self.value_fields[i].string):
                continue

            self.game.map.properties.append(self.key_fields[i].string + ": " + self.value_fields[i].string)

        self.game.current_state_obj.popup = None

    def handle_close(self, component):
        self.game.current_state_obj.popup = None
