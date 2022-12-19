from states.state import *


class IntroState(State):
    def __init__(self, game):
        super().__init__(game)

        self.title_text = "Welcome to Final Project!"
        self.text.append("")
        self.text.append("In this game you must kill all enemies to proceed to the next level.")
        self.text.append("Press Space or Left Mouse Button to proceed to menu!")
        self.update_state_text()

    def on_set(self):
        pass

    def handle_events(self, event):
        if event.type == pg.KEYUP:
            if event.key == pg.K_RETURN or event.key == pg.K_SPACE:
                self.game.current_state = "Menu"
        if event.type == pg.MOUSEBUTTONUP and event.button == 1:
            self.game.current_state = "Menu"

    def update(self, dt):
        pass

    def draw(self):
        self.game.renderer.draw_fullscreen_rect(color=(44, 44, 44))
        self.draw_state_text()
