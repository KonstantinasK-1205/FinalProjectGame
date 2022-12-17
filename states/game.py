from states.state import *


class GameState(State):
    def __init__(self, game):
        super().__init__(game)
        self.in_map = False
        self.surface = pg.Surface(RES, pg.SRCALPHA)

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

        if self.in_map:
            self.game.state["Game"].draw_minimap()
            self.game.hud.draw_enemy_stats()
        else:
            self.game.hud.draw_in_game_gui()

    def draw_minimap(self):
        # Define maximum minimap size
        # A margin is used so that the minimap does not take up all screen
        minimap_width = WIDTH - WIDTH / 10
        minimap_height = HEIGHT - HEIGHT / 5

        # Calculate maximum tile size that can fit and reduce minimap size to
        # fit all tiles (necessary for centering)
        tile_size = min(int(minimap_width / self.game.map.width), int(minimap_height / self.game.map.height))
        minimap_width = tile_size * self.game.map.width
        minimap_height = tile_size * self.game.map.height

        # Center minimap
        minimap_x = WIDTH / 2 - minimap_width / 2
        # Offset Y by margin
        minimap_y = HEIGHT / 20

        self.surface.fill((0, 0, 0, 0))

        # Draw walls
        for i in range(self.game.map.height):
            for j in range(self.game.map.width):
                color = (0, 0, 0, 224)

                if not self.game.map.is_wall(j, i):
                    if not self.game.map.is_visited(j, i):
                        color = (0, 0, 0, 96)
                    else:
                        continue

                pg.draw.rect(self.surface, color, (minimap_x + j * tile_size, minimap_y + i * tile_size, tile_size, tile_size))

        # Draw enemies
        for enemy in self.game.object_handler.alive_npc_list:
            if self.game.map.is_visited(enemy.x, enemy.y):
                pg.draw.circle(self.surface, (255, 0, 0), (minimap_x + enemy.x * tile_size, minimap_y + enemy.y * tile_size), 4)

        # Draw pickups
        for pickup in self.game.object_handler.pickup_list:
            if self.game.map.is_visited(pickup.x, pickup.y):
                pg.draw.circle(self.surface, (0, 0, 255), (minimap_x + pickup.x * tile_size, minimap_y + pickup.y * tile_size), 4)

        # Draw player
        pg.draw.circle(self.surface, (0, 255, 0), (minimap_x + self.game.player.x * tile_size, minimap_y + self.game.player.y * tile_size), 4)

        # Minimap is drawn to a separate surface and then blitted to avoid
        # issues with transparency
        self.game.screen.blit(self.surface, (0, 0))
