from states.state import *


class PauseState(State):
    def __init__(self, game):
        super().__init__(game)

        self.title_text = "Game Paused!"
        self.text.append("Press Space or Left Mouse Button to resume...")
        self.update_state_text()

    def on_set(self):
        pg.mouse.set_visible(True)
        pg.event.set_grab(False)
        pg.mixer.stop()

    def handle_events(self, event):
        if event.type == pg.KEYUP:
            if event.key == pg.K_RETURN or event.key == pg.K_SPACE or event.key == pg.K_ESCAPE:
                self.game.current_state = "Game"
        if event.type == pg.MOUSEBUTTONUP and event.button == 1:
            self.game.current_state = "Game"

    def update(self, dt):
        pass

    def draw(self):
        self.game.renderer.draw_fullscreen_rect(color=(44, 44, 44))
        self.draw_state_text()
