class Hud:
    def __init__(self, game):
        self.game = game
        self.margin = 0

        self.health_icon_width = 0
        self.health_icon_height = 0
        self.health_bar_width = 0
        self.health_bar_height = 0
        self.health_bar_hp = 0
        self.health_text = None

        self.armor_icon_width = 0
        self.armor_icon_height = 0
        self.armor_bar_width = 0
        self.armor_bar_height = 0
        self.armor_bar_hp = 0
        self.armor_text = None

        self.bullet_left_text = None
        self.killed_text = None
        self.left_text = None
        self.text_width = 0
        self.text_height = 0

        self.minimap_pos = [0, 0]
        self.minimap_tile = 0

        self.game.renderer.load_texture_from_file("resources/icons/gui_armor.png")
        self.game.renderer.load_texture_from_file("resources/icons/gui_health.png")

    def on_resize(self):
        # Recalculate health icon size
        self.health_icon_width = self.game.width / 40
        self.health_icon_height = self.game.height / 25

        # Recalculate health bar size
        self.health_bar_width = self.game.width / 8
        self.health_bar_height = self.game.height / 25

        # Recalculate armor icon size
        self.armor_icon_width = self.game.width / 40
        self.armor_icon_height = self.game.height / 25

        # Recalculate armor bar size
        self.armor_bar_width = self.game.width / 8
        self.armor_bar_height = self.game.height / 25

        # Also update health and armor text
        self.update_player_info()
        self.on_enemy_down()
        self.update_bullets()

    def update_player_info(self):
        self.health_text = self.game.font_small.render(str(self.game.player.health), True, (0, 64, 0))
        self.game.renderer.load_texture_from_surface("health_text", self.health_text)
        self.health_bar_hp = (self.health_bar_width / 100) * self.game.player.health

        self.armor_text = self.game.font_small.render(str(self.game.player.armor), True, (0, 0, 64))
        self.game.renderer.load_texture_from_surface("armor_text", self.armor_text)
        self.armor_bar_hp = (self.armor_bar_width / 100) * self.game.player.armor

    def on_enemy_down(self):
        self.killed_text = self.game.font_small.render("Enemies killed: " +
                                                       str(self.game.object_handler.killed),
                                                       True,
                                                       (255, 255, 255))
        self.left_text = self.game.font_small.render("Enemies left: " +
                                                     str(self.game.map.enemy_amount - self.game.object_handler.killed),
                                                     True,
                                                     (255, 255, 255))

        self.text_width = max(self.killed_text.get_size()[0], self.left_text.get_size()[0])
        self.text_height = self.killed_text.get_size()[1] + self.left_text.get_size()[1]

    def update_bullets(self):
        self.bullet_left_text = self.game.font_small.render("Ammo: " + str(self.game.weapon.bullet_left_in_weapon()) +
                                                            " / " + str(self.game.weapon.total_bullet_left()),
                                                            True, (255, 255, 255))
        self.game.renderer.load_texture_from_surface("total_bullet", self.bullet_left_text)

    def update_minimap(self, size):
        if size == 1:
            # Maximum minimap size
            minimap_width = self.game.width / 5
            minimap_height = self.game.height / 4

            # Maximum tile size
            self.minimap_tile = min(int(minimap_width / self.game.map.width),
                                    int(minimap_height / self.game.map.height))
            # Reduce minimap size to fit tiles
            minimap_width = self.minimap_tile * self.game.map.width
            minimap_height = self.minimap_tile * self.game.map.height

            # Offset minimap from top right
            self.minimap_pos[0] = self.game.width - minimap_width - self.margin
            self.minimap_pos[1] = self.margin

        # Display a large minimap
        elif size == 2:
            # Maximum minimap size
            minimap_width = self.game.width - self.margin * 2
            minimap_height = self.game.height - self.margin * 2 - self.game.height / 8

            # Maximum tile size
            self.minimap_tile = min(int(minimap_width / self.game.map.width),
                                    int(minimap_height / self.game.map.height))
            # Reduce minimap size to fit tiles
            minimap_width = self.minimap_tile * self.game.map.width
            minimap_height = self.minimap_tile * self.game.map.height

            # Center minimap and offset from top
            self.minimap_pos[0] = self.game.width / 2 - minimap_width / 2
            self.minimap_pos[1] = self.margin

    def draw_health_bar(self):
        self.game.renderer.draw_rect(
            self.margin,
            self.game.height - self.health_icon_height - self.margin,
            self.health_icon_width,
            self.health_icon_height,
            "resources/icons/gui_health.png"
        )
        self.game.renderer.draw_rect(
            self.margin + self.health_icon_width + 5,
            self.game.height - self.health_icon_height - self.margin,
            self.health_bar_width,
            self.health_bar_height,
            color=(128, 128, 128, 20)
        )
        self.game.renderer.draw_rect(
            self.margin + self.health_icon_width + 5,
            self.game.height - self.health_icon_height - self.margin,
            self.health_bar_hp,
            self.health_bar_height,
            color=(6, 100, 32, 200)
        )

        self.game.renderer.draw_rect(
            self.margin + self.health_icon_width + 5 + self.health_bar_width / 2 - self.health_text.get_width() / 2,
            self.game.height - self.health_icon_height - self.margin,
            self.health_text.get_width(),
            self.health_text.get_height(),
            "health_text"
        )

    def draw_armor_bar(self):
        self.game.renderer.draw_rect(
            self.margin,
            self.game.height - self.armor_icon_height * 2 - self.margin,
            self.armor_icon_width,
            self.armor_icon_height,
            "resources/icons/gui_armor.png"
        )
        self.game.renderer.draw_rect(
            self.margin + self.armor_icon_width + 5,
            self.game.height - self.armor_icon_height * 2 - self.margin,
            self.armor_bar_width,
            self.armor_bar_height,
            color=(255, 255, 255, 20)
        )
        self.game.renderer.draw_rect(
            self.margin + self.armor_icon_width + 5,
            self.game.height - self.armor_icon_height * 2 - self.margin,
            self.armor_bar_hp,
            self.armor_bar_height,
            color=(12, 32, 100, 200)
        )

        self.game.renderer.draw_rect(
            self.margin + self.armor_icon_width + 5 + self.armor_bar_width / 2 - self.armor_text.get_width() / 2,
            self.game.height - self.armor_icon_height * 2 - self.margin,
            self.armor_text.get_width(),
            self.armor_text.get_height(),
            "armor_text"
        )

    def draw_enemy_stats(self):
        self.game.renderer.load_texture_from_surface("killed_text", self.killed_text)
        self.game.renderer.load_texture_from_surface("left_text", self.left_text)
        self.game.renderer.draw_rect(
            self.game.width - self.text_width - self.margin,
            self.game.height - self.text_height - self.margin,
            self.killed_text.get_width(),
            self.killed_text.get_height(),
            "killed_text"
        )
        self.game.renderer.draw_rect(
            self.game.width - self.text_width - self.margin,
            self.game.height - self.text_height + self.killed_text.get_size()[1] - self.margin,
            self.left_text.get_width(),
            self.left_text.get_height(),
            "left_text"
        )

    def draw_bullet_stats(self):
        self.game.renderer.draw_rect(
            self.margin,
            self.game.height - self.margin - self.game.height / 25 * 3,
            self.bullet_left_text.get_width(),
            self.bullet_left_text.get_height(),
            "total_bullet"
        )

    def draw_minimap(self):
        self.game.renderer.draw_minimap(self.minimap_pos[0], self.minimap_pos[1], self.minimap_tile)

    def draw_fps_counter(self):
        fps_counter = self.game.font_small.render("FPS: " + str(int(self.game.clock.get_fps())), True, (255, 255, 255))
        self.game.renderer.load_texture_from_surface("fps_counter", fps_counter)
        self.game.renderer.draw_rect(
            self.margin,
            self.margin,
            fps_counter.get_width(),
            fps_counter.get_height(),
            "fps_counter"
        )

    def draw(self, map_state):
        self.margin = self.game.width / 100

        # Draw small minimap
        if map_state == 1:
            self.draw_minimap()
        # Draw large minimap
        elif map_state == 2:
            self.draw_minimap()
            self.draw_enemy_stats()
        self.draw_armor_bar()
        self.draw_health_bar()
        if not self.game.weapon.current_weapon_type() == "Melee":
            self.draw_bullet_stats()
