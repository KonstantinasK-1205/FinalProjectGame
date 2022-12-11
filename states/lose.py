from states.state import *


class LoseState(State):
    def __init__(self, game):
        super().__init__(game)
        self.lose_image = pg.image.load('resources/textures/game_over.png').convert_alpha()
        self.lose_image = pg.transform.scale(self.lose_image, RES)
        self.on_set_ms = 0
        self.elapsed_ms = 0

    def on_set(self):
        self.on_set_ms = pg.time.get_ticks()
        self.elapsed_ms = 0
        pg.mixer.stop()
        self.game.sound.lose.play()

    def handle_events(self, event):
        if self.elapsed_ms > STATE_WAIT_MS:
            if event.type == pg.KEYUP:
                if event.key == pg.K_RETURN or event.key == pg.K_SPACE:
                    self.game.current_state = "Loading"
                    self.game.new_game("resources/levels/" + self.game.map_lists[0] + ".txt")
                if event.key == pg.K_ESCAPE:
                    self.game.is_running = False

            if event.type == pg.MOUSEBUTTONUP and event.button == 1:
                self.game.current_state = "Loading"
                self.game.new_game("resources/levels/" + self.game.map_lists[0] + ".txt")

    def update(self, dt):
        self.elapsed_ms = pg.time.get_ticks() - self.on_set_ms

    def draw(self):
        self.screen.blit(self.lose_image, (0, 0))
