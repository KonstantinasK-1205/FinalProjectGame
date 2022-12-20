import pygame as pg

from settings import *


class Hud:
    def __init__(self, game):
        self.game = game

        self.game.renderer.load_texture_from_file("resources/icons/gui_armor.png")
        self.game.renderer.load_texture_from_file("resources/icons/gui_health.png")

    def draw_health_bar(self):
        health_icon_width = self.game.width / 40
        health_icon_height = self.game.height / 25

        health_bar_width = self.game.width / 8
        health_bar_height = self.game.height / 25
        health_pixel_size = (health_bar_width / 100)
        health_bar_hp = health_pixel_size * self.game.player.health

        self.game.renderer.draw_rect(
            self.margin,
            self.game.height - health_icon_height - self.margin,
            health_icon_width,
            health_icon_height,
            "resources/icons/gui_health.png"
        )
        self.game.renderer.draw_rect(
            self.margin + health_icon_width + 5,
            self.game.height - health_icon_height - self.margin,
            health_bar_width,
            health_bar_height,
            color=(128, 128, 128, 20)
        )
        self.game.renderer.draw_rect(
            self.margin + health_icon_width + 5,
            self.game.height - health_icon_height - self.margin,
            health_bar_hp,
            health_bar_height,
            color=(6, 100, 32, 200)
        )

        health_text = self.game.font_small.render(str(self.game.player.health), True, (0, 64, 0))
        self.game.renderer.load_texture_from_surface("health_text", health_text)
        self.game.renderer.draw_rect(
            self.margin + health_icon_width + 5 + health_bar_width / 2 - health_text.get_width() / 2,
            self.game.height - health_icon_height - self.margin,
            health_text.get_width(),
            health_text.get_height(),
            "health_text"
        )

    def draw_armor_bar(self):
        armor_icon_width = self.game.width / 40
        armor_icon_height = self.game.height / 25

        armor_bar_width = self.game.width / 8
        armor_bar_height = self.game.height / 25
        armor_pixel_size = (armor_bar_width / 100)
        armor_bar_hp = armor_pixel_size * self.game.player.armor

        self.game.renderer.draw_rect(
            self.margin,
            self.game.height - armor_icon_height * 2 - self.margin,
            armor_icon_width,
            armor_icon_height,
            "resources/icons/gui_armor.png"
        )
        self.game.renderer.draw_rect(
            self.margin + armor_icon_width + 5,
            self.game.height - armor_icon_height * 2 - self.margin,
            armor_bar_width,
            armor_bar_height,
            color=(255, 255, 255, 20)
        )
        self.game.renderer.draw_rect(
            self.margin + armor_icon_width + 5,
            self.game.height - armor_icon_height * 2 - self.margin,
            armor_bar_hp,
            armor_bar_height,
            color=(12, 32, 100, 200)
        )

        armor_text = self.game.font_small.render(str(self.game.player.armor), True, (0, 0, 64))
        self.game.renderer.load_texture_from_surface("armor_text", armor_text)
        self.game.renderer.draw_rect(
            self.margin + armor_icon_width + 5 + armor_bar_width / 2 - armor_text.get_width() / 2,
            self.game.height - armor_icon_height * 2 - self.margin,
            armor_text.get_width(),
            armor_text.get_height(),
            "armor_text"
        )

    def draw_enemy_stats(self):
        killed_text = self.game.font_small.render("Enemies killed: " + str(self.game.object_handler.killed), True, (255, 255, 255))
        left_text = self.game.font_small.render("Enemies left: " + str(self.game.map.enemy_amount - self.game.object_handler.killed), True, (255, 255, 255))
        
        text_width = max(killed_text.get_size()[0], left_text.get_size()[0])
        text_height = killed_text.get_size()[1] + left_text.get_size()[1]

        self.game.renderer.load_texture_from_surface("killed_text", killed_text)
        self.game.renderer.load_texture_from_surface("left_text", left_text)
        self.game.renderer.draw_rect(
            self.game.width - text_width - self.margin,
            self.game.height - text_height - self.margin,
            killed_text.get_width(),
            killed_text.get_height(),
            "killed_text"
        )
        self.game.renderer.draw_rect(
            self.game.width - text_width - self.margin,
            self.game.height - text_height + killed_text.get_size()[1] - self.margin,
            left_text.get_width(),
            left_text.get_height(),
            "left_text"
        )

    def draw_in_game_gui(self):
        self.draw_armor_bar()
        self.draw_health_bar()

        # Draw Bullet amount
        total_bullet = self.game.font_small.render("Ammo: " + str(self.game.weapon.get_cartridge_bullet_left()) +
                                        " / " + str(self.game.weapon.get_total_bullet_left()), True, (255, 255, 255))
        self.game.renderer.load_texture_from_surface("total_bullet", total_bullet)
        self.game.renderer.draw_rect(
            self.margin,
            self.game.height - self.margin - self.game.height / 25 * 3,
            total_bullet.get_width(),
            total_bullet.get_height(),
            "total_bullet"
        )

    def draw_minimap(self, small):
        # Display a small minimap
        if small:
            # Maximum minimap size
            minimap_width = self.game.width / 5
            minimap_height = self.game.height / 4

            # Maximum tile size
            tile_size = min(int(minimap_width / self.game.map.width), int(minimap_height / self.game.map.height))

            # Reduce minimap size to fit tiles
            minimap_width = tile_size * self.game.map.width
            minimap_height = tile_size * self.game.map.height

            # Offset minimap from top right
            minimap_x = self.game.width - minimap_width - self.margin
            minimap_y = self.margin

        # Display a large minimap
        else:
            # Maximum minimap size
            minimap_width = self.game.width - self.margin * 2
            minimap_height = self.game.height - self.margin * 2 - self.game.height / 8

            # Maximum tile size
            tile_size = min(int(minimap_width / self.game.map.width), int(minimap_height / self.game.map.height))

            # Reduce minimap size to fit tiles
            minimap_width = tile_size * self.game.map.width
            minimap_height = tile_size * self.game.map.height

            # Center minimap and offset from top
            minimap_x = self.game.width / 2 - minimap_width / 2
            minimap_y = self.margin

        # Draw walls
        for i in range(self.game.map.height):
            for j in range(self.game.map.width):
                color = (0, 0, 0, 224)

                if not self.game.map.is_wall(j, i):
                    if not self.game.map.is_visited(j, i):
                        color = (0, 0, 0, 96)
                    else:
                        continue

                self.game.renderer.draw_rect(
                    minimap_x + j * tile_size,
                    minimap_y + i * tile_size,
                    tile_size,
                    tile_size,
                    color=color
                )

        # Draw enemies
        dot_size = tile_size / 4
        
        for enemy in self.game.object_handler.alive_npc_list:
            if self.game.map.is_visited(enemy.x, enemy.y):
                self.game.renderer.draw_rect(
                    minimap_x + enemy.x * tile_size - dot_size / 2,
                    minimap_y + enemy.y * tile_size - dot_size / 2,
                    dot_size,
                    dot_size,
                    color=(255, 0, 0)
                )

        # Draw pickups
        for pickup in self.game.object_handler.pickup_list:
            if self.game.map.is_visited(pickup.x, pickup.y):
                self.game.renderer.draw_rect(
                    minimap_x + pickup.x * tile_size - dot_size / 2,
                    minimap_y + pickup.y * tile_size - dot_size / 2,
                    dot_size,
                    dot_size,
                    color=(0, 0, 255)
                )

        # Draw player
        self.game.renderer.draw_rect(
            minimap_x + self.game.player.x * tile_size - dot_size / 2,
            minimap_y + self.game.player.y * tile_size - dot_size / 2,
            dot_size,
            dot_size,
            color=(0, 255, 0)
        )

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
            self.draw_minimap(True)
        # Draw large minimap
        elif map_state == 2:
            self.draw_minimap(False)
            self.draw_enemy_stats()
        self.draw_in_game_gui()
