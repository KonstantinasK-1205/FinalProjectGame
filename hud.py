import pygame as pg

from settings import *


class Hud:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.font = pg.font.Font("resources/fonts/Font.ttf", 32)
        self.sky_offset = 0

        # GUI
        # Health bar
        self.armor_icon = self.get_texture('resources/icons/gui_armor.png', (RES[0] / 35, RES[1] / 25))
        self.health_icon = self.get_texture('resources/icons/gui_health.png', (RES[0] / 35, RES[1] / 25))

    def draw_health_bar(self):
        health_bar_width = RES[0] / 8
        health_bar_height = RES[1] / 25
        health_pixel_size = (health_bar_width / 100)
        health_bar_hp = health_pixel_size * self.game.player.health

        health_bar_bg = pg.Surface((health_bar_width, health_bar_height), pg.SRCALPHA)
        health_bar_bg.fill((128, 128, 128))
        health_bar_bg.set_alpha(20)

        health_bar_fg = pg.Surface((health_bar_hp, health_bar_height), pg.SRCALPHA)
        health_bar_fg.fill((6, 100, 32))
        health_bar_fg.set_alpha(200)

        self.screen.blit(self.health_icon, (0, RES[1] - self.health_icon.get_height()))
        self.screen.blit(health_bar_bg, (self.health_icon.get_width() + 5, RES[1] - self.health_icon.get_height()))
        self.screen.blit(health_bar_fg, (self.health_icon.get_width() + 5, RES[1] - self.health_icon.get_height()))

    def draw_armor_bar(self):
        armor_bar_width = RES[0] / 8
        armor_bar_height = RES[1] / 25
        armor_pixel_size = (armor_bar_width / 100)
        armor_bar_hp = armor_pixel_size * self.game.player.armor

        armor_bar_bg = pg.Surface((armor_bar_width, armor_bar_height), pg.SRCALPHA)
        armor_bar_bg.fill((255, 255, 255))
        armor_bar_bg.set_alpha(20)

        armor_bar_fg = pg.Surface((armor_bar_hp, armor_bar_height), pg.SRCALPHA)
        armor_bar_fg.fill((12, 32, 100))
        armor_bar_fg.set_alpha(200)

        self.screen.blit(self.armor_icon, (0, RES[1] - (self.armor_icon.get_height() * 2)))
        self.screen.blit(armor_bar_bg, (self.armor_icon.get_width() + 5, RES[1] - (self.armor_icon.get_height() * 2)))
        self.screen.blit(armor_bar_fg, (self.armor_icon.get_width() + 5, RES[1] - (self.armor_icon.get_height() * 2)))

    def draw_enemy_left(self):
        killed_text = self.font.render("Enemy left: " + str(self.game.map.enemy_amount - self.game.object_handler.killed),
                                       True, (255, 255, 255))
        self.screen.blit(killed_text, (RES[0] - killed_text.get_size()[0], RES[1] - (self.armor_icon.get_height() * 2)))

    def draw_in_game_gui(self):
        self.draw_armor_bar()
        self.draw_health_bar()

        # Draw Bullet amount
        total_bullet = self.font.render("Bullet: " + str(self.game.weapon.get_cartridge_bullet_left()) +
                                        " / " + str(self.game.weapon.get_total_bullet_left()), True, (255, 255, 255))
        self.screen.blit(total_bullet, (0, RES[1] - (self.armor_icon.get_height() * 3)))

    @staticmethod
    def get_texture(path, res=(TEXTURE_SIZE, TEXTURE_SIZE)):
        texture = pg.image.load(path).convert_alpha()
        return pg.transform.scale(texture, res)

    # In Game Texts
    def draw_old_in_game_gui(self):
        # Draw Killed Amount
        killed_text = self.font.render(
            "Enemy left: " + str(self.game.map.enemy_amount - self.game.object_handler.killed), True, (255, 255, 255))
        self.screen.blit(killed_text, (RES[0] - killed_text.get_size()[0], RES[1] - self.font.get_linesize()))

        # Draw Killed Amount
        killed_text = self.font.render("Killed: " + str(self.game.object_handler.killed), True, (255, 255, 255))
        self.screen.blit(killed_text, (MARGIN, RES[1] - self.font.get_linesize()))

        # Draw Bullet amount
        total_bullet = self.font.render("Bullet: " + str(self.game.weapon.get_cartridge_bullet_left()) +
                                        " / " + str(self.game.weapon.get_total_bullet_left()), True, (255, 255, 255))
        self.screen.blit(total_bullet, (MARGIN, RES[1] - self.font.get_linesize() * 2.1))

        # Draw Armor left amount
        armor_text = self.font.render("Armor: " + str(self.game.player.armor), True, (255, 255, 255))
        self.screen.blit(armor_text, (MARGIN, RES[1] - self.font.get_linesize() * 3.2))

        # Draw HP
        health_text = self.font.render("HP: " + str(self.game.player.health) + " %", True, (255, 255, 255))
        self.screen.blit(health_text, (MARGIN, RES[1] - self.font.get_linesize() * 4.3))

        pos_text = self.font.render(
            "X: " + str(int(self.game.player.pos_x)) + " Y: " + str(int(self.game.player.pos_y)), True, (255, 255, 255))
        self.screen.blit(pos_text, (MARGIN, 0))
