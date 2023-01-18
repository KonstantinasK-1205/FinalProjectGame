import gui


class TextPopup(gui.VBox):
    def __init__(self, game, title_str, text_str):
        super().__init__(game)

        self.flexible = (False, False)
        self.size = (400, 120)
        self.position = (
            (self.game.width - self.size[0]) / 2,
            (self.game.height - self.size[1]) / 2
        )

        title_text = gui.Text(self.game)
        title_text.flexible = (True, False)
        title_text.size = (0, 40)
        title_text.font = game.unscaled_fonts[1]
        title_text.string = title_str

        text_text = gui.Text(self.game)
        text_text.flexible = (True, True)
        text_text.size = (0, 0)
        text_text.font = game.unscaled_fonts[1]
        text_text.string = text_str

        cancel_button = gui.Button(self.game)
        cancel_button.flexible = (True, False)
        cancel_button.size = (0, 40)
        cancel_button.font = game.unscaled_fonts[1]
        cancel_button.string = "OK"
        cancel_button.function = self.handle_close

        self.add(title_text)
        self.add(text_text)
        self.add(cancel_button)

    def handle_close(self, component):
        self.game.current_state_obj.popup = None
