from states.state import *


class ControlsState(State):
    def __init__(self, game):
        super().__init__(game)

        self.title_text = "Controls"
        self.text.append("")
        self.text.append("Movement: WASD")
        self.text.append("")
        self.text.append("Fire Weapon: Left Mouse Button")
        self.text.append("Reload Weapon: R")
        self.text.append("Change Weapon: Number Keys")
        self.text.append("")
        self.text.append("Toggle Map: Tab")
        self.text.append("Pause to Menu: Esc")
        self.text.append("")
        self.text.append("Press Space or Left Mouse Button to return to menu...")
        self.update_state_text()

    def handle_event(self, event):
        if event.type == pg.KEYUP:
            if event.key == pg.K_RETURN or event.key == pg.K_SPACE:
                self.game.current_state = "Menu"
        if event.type == pg.MOUSEBUTTONUP and event.button == 1:
            self.game.current_state = "Menu"

    def draw(self):
        super().draw()
        self.draw_state_text()
