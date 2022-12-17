from states.state import *


class GameState(State):
    def __init__(self, game):
        super().__init__(game)
        self.map_state = 0

    def on_set(self):
        pg.mouse.set_visible(False)
        pg.event.set_grab(True)
        pg.mixer.stop()

    def handle_events(self, event):
        self.game.player.handle_events(event)
        if event.type == pg.KEYUP:
            if event.key == pg.K_ESCAPE:
                self.game.current_state = "Pause"
            elif event.key == pg.K_TAB:
                self.map_state = (self.map_state + 1) % 3

    def update(self, dt):
        self.game.object_handler.update(dt)
        self.game.player.update(dt)
        self.game.sound.update()

    def draw(self):
        self.game.object_handler.draw()
        self.game.weapon.draw()
        self.game.hud.draw(self.map_state)
