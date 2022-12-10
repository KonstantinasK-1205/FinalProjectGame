from States.State import *


class GameState(State):
    def __init__(self, game):
        super().__init__(game)

    @staticmethod
    def on_set():
        pg.mouse.set_visible(False)
        pg.event.set_grab(True)
        pg.mixer.stop()

    def handle_events(self, event):
        self.game.player.handle_events(event)
        if event.type == pg.KEYUP:
            if event.key == pg.K_ESCAPE:
                self.game.set_state("Pause")

    def update(self):
        self.game.raycasting.update()
        self.game.object_handler.update()
        self.game.player.update()
        self.game.delta_time = self.game.clock.tick(FPS)

    def draw(self):
        self.game.object_renderer.draw()
        self.game.weapon.draw()
        pg.display.flip()
