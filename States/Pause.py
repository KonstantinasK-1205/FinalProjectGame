from States.State import *


class PauseState(State):
    def __init__(self, game):
        super().__init__(game)
        self.pause_surface = create_text_surface(self.font, "Game Paused!")
        self.continue_surface = create_text_surface(self.font, "Press mouse to continue")

    @staticmethod
    def on_set():
        pg.mouse.set_visible(True)
        pg.event.set_grab(False)
        pg.mixer.stop()

    def handle_events(self, event):
        if event.type == pg.KEYUP:
            if event.key == pg.K_RETURN or event.key == pg.K_SPACE or event.key == pg.K_ESCAPE:
                self.game.set_state("Game")
        if event.type == pg.MOUSEBUTTONUP and event.button == 1:
            self.game.set_state("Game")

    @staticmethod
    def update():
        return None

    def draw(self):
        pg.draw.rect(self.screen, (44, 44, 44), pg.Rect(0, 0, RES[0], RES[1]))
        self.screen.blit(self.pause_surface[0], (self.pause_surface[1][0],
                                                 self.pause_surface[1][1] - self.pause_surface[0].get_height()))
        self.screen.blit(self.continue_surface[0], (self.continue_surface[1][0], self.continue_surface[1][1]))
        pg.display.flip()
