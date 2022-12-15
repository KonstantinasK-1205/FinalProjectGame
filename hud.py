import pygame as pg

from settings import *


class Hud:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.font = pg.font.Font("resources/fonts/Font.ttf", 48)
        self.sky_offset = 0

    # In Game Texts
    def draw_in_game_gui(self):
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
