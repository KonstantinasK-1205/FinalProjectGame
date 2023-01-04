from states.state import *


class LoseState(State):
    def __init__(self, game):
        super().__init__(game)

        self.on_set_ms = 0
        self.elapsed_ms = 0

        self.title_text = "Loser!"
        self.text.append("")
        self.text.append("You have died.")
        self.text.append("Press Space or Left Mouse Button to try again.")
        self.update_state_text()

    def on_set(self):
        self.on_set_ms = pg.time.get_ticks()
        self.elapsed_ms = 0
        pg.mixer.stop()
        self.game.sound.play_sfx("Lose")

    def handle_event(self, event):
        if self.elapsed_ms > STATE_WAIT_MS:
            if event.type == pg.KEYUP:
                if event.key == pg.K_RETURN or event.key == pg.K_SPACE:
                    self.game.current_state = "Loading"
                    self.game.restart_level(self.game.current_map)
                if event.key == pg.K_ESCAPE:
                    self.game.running = False

            if event.type == pg.MOUSEBUTTONUP and event.button == 1:
                self.game.current_state = "Loading"
                self.game.restart_level(self.game.current_map)

    def update(self):
        self.elapsed_ms = pg.time.get_ticks() - self.on_set_ms

    def draw(self):
        self.game.renderer.draw_fullscreen_rect(color=(44, 44, 44))
        self.draw_state_text()
