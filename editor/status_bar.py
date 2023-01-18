import gui

class StatusBar(gui.Text):
    def __init__(self, game):
        super().__init__(game)

        self.font = game.unscaled_fonts[1]
        self.flexible = (False, False)
        self.size = (400, 40)
        self.centered = (False, True)

    def update(self):
        self.string = "  "
        self.string += "Cursor: " + str(self.game.current_state_obj.center_panel.cursor_pos)
        self.string += "    "
        self.string += "Tool: " + self.game.current_state_obj.left_panel.selected_tool
        self.string += "    "
        self.string += "Brush: " + self.game.current_state_obj.left_panel.selected_brush
