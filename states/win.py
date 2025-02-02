from states.state import *


class WinState(State):
    def __init__(self, game):
        super().__init__(game)

        self.on_set_ms = 0
        self.elapsed_ms = 0

        self.title_text = "Winner!"
        self.text.append("")
        self.text.append("Congratulations! You have cleared all levels!")
        self.text.append("Press Space or Left Mouse Button to quit.")
        self.update_state_text()

    def on_set(self):
        self.on_set_ms = pg.time.get_ticks()
        self.elapsed_ms = 0
        pg.mixer.stop()
        self.game.sound.play_sfx("Win")

    def handle_event(self, event):
        if self.elapsed_ms > STATE_WAIT_MS:
            if event.type == pg.KEYUP:
                if event.key == pg.K_RETURN or event.key == pg.K_SPACE:
                    self.game.running = False
            if event.type == pg.MOUSEBUTTONUP and event.button == 1:
                self.game.running = False

    def update(self):
        self.elapsed_ms = pg.time.get_ticks() - self.on_set_ms

    def draw(self):
        super().draw()
        self.draw_state_text()
