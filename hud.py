import pygame as pg

from settings import *


class Hud:
    def __init__(self, game):
        self.game = game

        self.armor_icon = pg.image.load("resources/icons/gui_armor.png").convert_alpha()
        self.health_icon = pg.image.load("resources/icons/gui_health.png").convert_alpha()

    def draw_health_bar(self):
        health_icon = pg.transform.scale(self.health_icon, (self.res[0] / 35, self.res[1] / 25))

        health_bar_width = self.res[0] / 8
        health_bar_height = self.res[1] / 25
        health_pixel_size = (health_bar_width / 100)
        health_bar_hp = health_pixel_size * self.game.player.health

        health_bar_bg = pg.Surface((health_bar_width, health_bar_height), pg.SRCALPHA)
        health_bar_bg.fill((128, 128, 128))
        health_bar_bg.set_alpha(20)

        health_bar_fg = pg.Surface((health_bar_hp, health_bar_height), pg.SRCALPHA)
        health_bar_fg.fill((6, 100, 32))
        health_bar_fg.set_alpha(200)

        self.game.screen.blit(health_icon, (self.margin, self.res[1] - health_icon.get_height() - self.margin))
        self.game.screen.blit(health_bar_bg, (self.margin + health_icon.get_width() + 5, self.res[1] - health_icon.get_height() - self.margin))
        self.game.screen.blit(health_bar_fg, (self.margin + health_icon.get_width() + 5, self.res[1] - health_icon.get_height() - self.margin))

        health_text = self.game.font_small.render(str(self.game.player.health), False, (0, 64, 0))
        self.game.screen.blit(health_text, (self.margin + health_icon.get_width() + 5 + health_bar_width / 2 - health_text.get_width() / 2, self.res[1] - health_icon.get_height() - self.margin))

    def draw_armor_bar(self):
        armor_icon = pg.transform.scale(self.armor_icon, (self.res[0] / 35, self.res[1] / 25))

        armor_bar_width = self.res[0] / 8
        armor_bar_height = self.res[1] / 25
        armor_pixel_size = (armor_bar_width / 100)
        armor_bar_hp = armor_pixel_size * self.game.player.armor

        armor_bar_bg = pg.Surface((armor_bar_width, armor_bar_height), pg.SRCALPHA)
        armor_bar_bg.fill((255, 255, 255))
        armor_bar_bg.set_alpha(20)

        armor_bar_fg = pg.Surface((armor_bar_hp, armor_bar_height), pg.SRCALPHA)
        armor_bar_fg.fill((12, 32, 100))
        armor_bar_fg.set_alpha(200)

        self.game.screen.blit(armor_icon, (self.margin, self.res[1] - armor_icon.get_height() * 2 - self.margin))
        self.game.screen.blit(armor_bar_bg, (self.margin + armor_icon.get_width() + 5, self.res[1] - armor_icon.get_height() * 2 - self.margin))
        self.game.screen.blit(armor_bar_fg, (self.margin + armor_icon.get_width() + 5, self.res[1] - armor_icon.get_height() * 2 - self.margin))

        armor_text = self.game.font_small.render(str(self.game.player.armor), False, (0, 0, 64))
        self.game.screen.blit(armor_text, (self.margin + armor_icon.get_width() + 5 + armor_bar_width / 2 - armor_text.get_width() / 2, self.res[1] - armor_icon.get_height() * 2 - self.margin))

    def draw_enemy_stats(self):
        killed_text = self.game.font_small.render("Enemies killed: " + str(self.game.object_handler.killed), True, (255, 255, 255))
        left_text = self.game.font_small.render("Enemies left: " + str(self.game.map.enemy_amount - self.game.object_handler.killed), True, (255, 255, 255))
        
        text_width = max(killed_text.get_size()[0], left_text.get_size()[0])
        text_height = killed_text.get_size()[1] + left_text.get_size()[1]

        self.game.screen.blit(killed_text, (self.res[0] - text_width - self.margin, self.res[1] - text_height - self.margin))
        self.game.screen.blit(left_text, (self.res[0] - text_width - self.margin, self.res[1] - text_height + killed_text.get_size()[1] - self.margin))

    def draw_in_game_gui(self):
        self.draw_armor_bar()
        self.draw_health_bar()

        # Draw Bullet amount
        total_bullet = self.game.font_small.render("Ammo: " + str(self.game.weapon.get_cartridge_bullet_left()) +
                                        " / " + str(self.game.weapon.get_total_bullet_left()), True, (255, 255, 255))
        self.game.screen.blit(total_bullet, (self.margin, self.res[1] - self.margin - self.res[1] / 25 * 3))

    def draw_minimap(self, small):
        # TODO: Draw minimap in OpenGL as PyGame is too slow

        # Draw to separate surface first to avoid transparency issues
        self.surface = pg.Surface(self.res, pg.SRCALPHA)

        # Display a small minimap
        if small:
            # Maximum minimap size
            minimap_width = self.res[0] / 3
            minimap_height = self.res[1] / 2

            # Maximum tile size
            tile_size = min(int(minimap_width / self.game.map.width), int(minimap_height / self.game.map.height))

            # Reduce minimap size to fit tiles
            minimap_width = tile_size * self.game.map.width
            minimap_height = tile_size * self.game.map.height

            # Offset minimap from top right
            minimap_x = self.res[0] - minimap_width - self.margin
            minimap_y = self.margin

        # Display a large minimap
        else:
            # Maximum minimap size
            minimap_width = self.res[0] - self.margin * 2
            minimap_height = self.res[1] - self.margin * 2 - self.res[1] / 8

            # Maximum tile size
            tile_size = min(int(minimap_width / self.game.map.width), int(minimap_height / self.game.map.height))

            # Reduce minimap size to fit tiles
            minimap_width = tile_size * self.game.map.width
            minimap_height = tile_size * self.game.map.height

            # Center minimap and offset from top
            minimap_x = self.res[0] / 2 - minimap_width / 2
            minimap_y = self.margin

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

    def draw(self, map_state):
        self.res = self.game.screen.get_size()
        self.margin = self.res[0] / 100

        # Draw small minimap
        if map_state == 1:
            self.draw_minimap(True)
        # Draw large minimap
        elif map_state == 2:
            self.draw_minimap(False)
        self.draw_enemy_stats()
        self.draw_in_game_gui()
