class Minimap:
    def __init__(self, game, hud):
        self.game = game
        self.hud = hud

        # Minimap variables
        self.x = 0
        self.y = 0
        self.tile_size = 0
        self.last_map_state = 0

        # Enemy (left / killed ) stats variables
        self.enemy_killed_text = None
        self.enemy_left_text = None
        self.text_width = 0
        self.text_height = 0

    def draw(self, map_state):
        if map_state > 0:
            if map_state > 1:
                self.game.renderer.draw_rect(
                    self.game.width - self.text_width - self.hud.margin,
                    self.game.height - self.text_height - self.hud.margin,
                    self.enemy_killed_text.get_width(),
                    self.enemy_killed_text.get_height(),
                    "killed_text"
                )
                self.game.renderer.draw_rect(
                    self.game.width - self.text_width - self.hud.margin,
                    self.game.height - self.text_height + self.enemy_killed_text.get_size()[1] - self.hud.margin,
                    self.enemy_left_text.get_width(),
                    self.enemy_left_text.get_height(),
                    "left_text"
                )
            self.game.renderer.draw_minimap(self.x, self.y, self.tile_size)

    def on_change(self):
        self.update_map_size(self.last_map_state)
        self.update_enemy_stats()

    def update_map_size(self, map_state):
        self.last_map_state = map_state
        if map_state == 1:
            # Maximum minimap size
            minimap_width = self.game.width / 5
            minimap_height = self.game.height / 4

            # Maximum tile size
            self.tile_size = min(int(minimap_width / self.game.map.width),
                                 int(minimap_height / self.game.map.height))

            # Reduce minimap size to fit tiles
            minimap_width = self.tile_size * self.game.map.width

            # Offset minimap from top right
            self.x = self.game.width - minimap_width - self.hud.margin
            self.y = self.hud.margin

        # Display a large minimap
        elif map_state == 2:
            # Maximum minimap size
            minimap_width = self.game.width - self.hud.margin * 2
            minimap_height = self.game.height - self.hud.margin * 2 - self.game.height / 8

            # Maximum tile size
            self.tile_size = min(int(minimap_width / self.game.map.width),
                                 int(minimap_height / self.game.map.height))

            # Reduce minimap size to fit tiles
            minimap_width = self.tile_size * self.game.map.width

            # Center minimap and offset from top
            self.x = self.game.width / 2 - minimap_width / 2
            self.y = self.hud.margin

    def update_enemy_stats(self):
        enemy_left = self.game.map.enemy_amount - self.game.object_handler.killed
        self.enemy_killed_text = self.game.font_small.render("Enemies killed: " +
                                                             str(self.game.object_handler.killed),
                                                             True,
                                                             (255, 255, 255))
        self.enemy_left_text = self.game.font_small.render("Enemies left: " +
                                                           str(enemy_left),
                                                           True,
                                                           (255, 255, 255))

        self.text_width = max(self.enemy_killed_text.get_size()[0], self.enemy_left_text.get_size()[0])
        self.text_height = self.enemy_killed_text.get_size()[1] + self.enemy_left_text.get_size()[1]

        self.game.renderer.load_texture_from_surface("killed_text", self.enemy_killed_text)
        self.game.renderer.load_texture_from_surface("left_text", self.enemy_left_text)
