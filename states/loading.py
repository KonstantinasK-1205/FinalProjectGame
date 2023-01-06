from states.state import *


class LoadingState(State):
    def __init__(self, game):
        super().__init__(game)
        self.on_set_ms = 0
        self.elapsed_ms = 0
        self.game_ready = None

    def on_set(self):
        self.game_ready = False
        self.on_set_ms = pg.time.get_ticks()
        self.elapsed_ms = 0
        self.text = []

    def handle_event(self, event):
        if self.elapsed_ms > STATE_WAIT_MS:
            if event.type == pg.KEYUP:
                if event.key == pg.K_RETURN or event.key == pg.K_SPACE:
                    self.game.current_state = "Game"
            elif event.type == pg.MOUSEBUTTONUP and event.button == 1:
                self.game.current_state = "Game"

    def update(self):
        self.elapsed_ms = pg.time.get_ticks() - self.on_set_ms

        if self.elapsed_ms < STATE_WAIT_MS:
            dot_count = 1 + self.elapsed_ms // 200 % 3
            self.title_text = "Loading " + self.game.current_map + "." * dot_count
            self.update_state_text()
        else:
            self.title_text = ""
            self.text = [
                self.game.current_map + " loaded!",
                "Press Space or Left Mouse Button to continue..."
            ]
            self.update_state_text()

    def draw(self):
        super().draw()
        self.draw_state_text()
