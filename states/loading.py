from states.state import *


class LoadingState(State):
    def __init__(self, game):
        super().__init__(game)
        self.on_set_ms = 0
        self.elapsed_ms = 0
        self.game_ready = None
        self.level_surface = None
        self.loading_string = None
        self.loading_surface = None

    def on_set(self):
        self.game_ready = False
        self.on_set_ms = pg.time.get_ticks()
        self.elapsed_ms = 0
        self.level_surface = create_text_surface(self.font, str(self.game.map_lists[0]))

    def handle_events(self, event):
        if self.elapsed_ms > STATE_WAIT_MS:
            if event.type == pg.KEYUP:
                if event.key == pg.K_RETURN or event.key == pg.K_SPACE:
                    self.game.current_state = "Game"
            elif event.type == pg.MOUSEBUTTONUP and event.button == 1:
                self.game.current_state = "Game"

    def update(self, dt):
        self.elapsed_ms = pg.time.get_ticks() - self.on_set_ms

        if self.elapsed_ms < STATE_WAIT_MS:
            dot_count = 1 + self.elapsed_ms // 200 % 3
            self.loading_string = "Loading level" + "." * dot_count
            self.loading_surface = create_text_surface(self.font, self.loading_string)
        else:
            self.loading_string = "Press mouse to continue"
            self.loading_surface = create_text_surface(self.font, self.loading_string)

    def draw(self):
        pg.draw.rect(self.screen, (44, 44, 44), pg.Rect(0, 0, RES[0], RES[1]))
        self.screen.blit(self.level_surface[0], (self.level_surface[1][0],
                                                 self.level_surface[1][1] - self.level_surface[0].get_height()))
        self.screen.blit(self.loading_surface[0], (self.loading_surface[1][0], self.loading_surface[1][1]))
