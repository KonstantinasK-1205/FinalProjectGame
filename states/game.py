from states.state import *


class GameState(State):
    def __init__(self, game):
        super().__init__(game)

    def on_set(self):
        pg.mouse.set_visible(False)
        pg.event.set_grab(True)
        pg.mixer.stop()

    def handle_events(self, event):
        self.game.player.handle_events(event)
        if event.type == pg.KEYUP:
            if event.key == pg.K_ESCAPE:
                self.game.current_state = "Pause"

    def update(self, dt):
        self.game.raycasting.update()
        self.game.object_handler.update(dt)
        self.game.player.update(dt)
        self.game.sound.update()

    def draw(self):
        self.game.object_renderer.draw_background()
        self.game.object_renderer.render_game_objects()
        self.game.weapon.draw()
        self.game.object_renderer.draw_in_game_gui()
