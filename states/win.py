from states.state import *


class WinState(State):
    def __init__(self, game):
        super().__init__(game)
        self.victory_image = pg.image.load('resources/textures/win.png').convert_alpha()
        self.victory_image = pg.transform.scale(self.victory_image, RES)
        self.on_set_ms = 0
        self.elapsed_ms = 0

    def on_set(self):
        self.on_set_ms = pg.time.get_ticks()
        self.elapsed_ms = 0
        pg.mixer.stop()
        self.game.sound.win.play()

    def handle_events(self, event):
        if self.elapsed_ms > STATE_WAIT_MS:
            if event.type == pg.KEYUP:
                if event.key == pg.K_RETURN or event.key == pg.K_SPACE:
                    self.game.is_running = False
            if event.type == pg.MOUSEBUTTONUP and event.button == 1:
                self.game.is_running = False

    def update(self, dt):
        self.elapsed_ms = pg.time.get_ticks() - self.on_set_ms

    def draw(self):
        self.screen.blit(self.victory_image, (0, 0))
