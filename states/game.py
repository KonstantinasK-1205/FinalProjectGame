from states.state import *


class GameState(State):
    def __init__(self, game):
        super().__init__(game)
        self.map_state = 0
        self.hit_flash_ms = HIT_FLASH_MS

    def on_set(self):
        pg.mouse.set_visible(False)
        pg.event.set_grab(True)
        pg.mixer.stop()
        self.game.hud.on_resize()

    def handle_events(self, event):
        self.game.player.handle_events(event)
        if event.type == pg.KEYUP:
            if event.key == pg.K_ESCAPE:
                self.game.player.on_level_change()
                self.game.current_state = "Menu"
            elif event.key == pg.K_TAB:
                self.game.hud.minimap.update_map_size((self.map_state + 1) % 3)
                self.map_state = (self.map_state + 1) % 3

    def update(self):
        self.game.player.update()
        self.game.object_handler.update()
        self.game.sound.update()

        if self.hit_flash_ms < HIT_FLASH_MS:
            self.hit_flash_ms = self.hit_flash_ms + self.game.dt

    def draw(self):
        self.game.object_handler.draw()
        self.game.weapon.draw()
        self.game.hud.draw(self.map_state)

        if self.hit_flash_ms < HIT_FLASH_MS:
            self.game.renderer.draw_fullscreen_rect(color=HIT_FLASH_COLOR)

        if self.game.show_fps:
            self.game.hud.draw_fps_counter()
