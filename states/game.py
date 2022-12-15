from states.state import *


class GameState(State):
    def __init__(self, game):
        super().__init__(game)
        self.in_map = False
        self.mini_map = []
        self.margin = 0
        self.size = 0

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
        self.game.object_handler.update(dt)
        self.game.player.update(dt)
        self.game.sound.update()

    def draw(self):
        self.game.object_handler.draw()
        self.game.weapon.draw()
        self.game.hud.draw_in_game_gui()
        if self.in_map:
            self.game.state["Game"].draw_mini_map()

    def init_mini_map(self):
        world_size = self.game.map.get_size()
        world_map = self.game.map.world_map
        self.mini_map = []

        self.size = [(RES[0] - (0.05 * RES[0])) / world_size[0],
                    (RES[1] - (0.05 * RES[1])) / world_size[1]]
        self.size = min(self.size[0], self.size[1])
        self.margin = (RES[0] - (world_size[0] * self.size) / 2)

        for position, wall in world_map.items():
            wall_column = pg.Surface((self.size, self.size))
            wall_column.fill((0, 0, 0))
            self.mini_map.append((wall_column, (position[0] * self.size, position[1] * self.size)))

    def draw_mini_map(self):
        surface = pg.Surface((RES[0], RES[1]), pg.SRCALPHA)
        surface.fill(HIT_FLASH_COLOR)
        self.screen.blit(surface, (0, 0))
        for image, pos in self.mini_map:
            self.screen.blit(image, pos)
        for enemy in self.game.object_handler.alive_npc_list:
            pg.draw.circle(self.screen, (255, 0, 0),
                           (enemy.exact_pos[0] * self.size, enemy.exact_pos[1] * self.size), 4)
        pg.draw.circle(self.screen, (0, 255, 0),
                       (self.game.player.exact_pos[0] * self.size, self.game.player.exact_pos[1] * self.size), 4)
        self.game.hud.draw_enemy_left()