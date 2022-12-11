import pygame as pg

from settings import *


class ObjectRenderer:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.wall_textures = self.load_wall_textures()
        self.font = pg.font.Font("resources/fonts/Font.ttf", 48)
        self.sky_image = self.get_texture('resources/textures/sky.jpg', (WIDTH, HALF_HEIGHT))
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

    def player_is_hit(self):
        pg.draw.rect(self.screen, (102, 0, 0), pg.Rect(0, 0, RES[0], RES[1]))

    def draw_background(self):
        self.sky_offset = (self.sky_offset + 4.5 * self.game.player.rel) % WIDTH
        # Angle between 0 and 360
        angle = math.fmod(self.game.player.angle * 180 / math.pi, 360)
        if angle < 0:
            angle = angle + 360

        self.sky_offset = math.fmod(angle * WIDTH / 360, WIDTH)

        self.screen.blit(self.sky_image, (-self.sky_offset, 0))
        self.screen.blit(self.sky_image, (-self.sky_offset + WIDTH, 0))
        pg.draw.rect(self.screen, FLOOR_COLOR, (0, HALF_HEIGHT, WIDTH, HEIGHT))

    def render_game_objects(self):
        list_objects = sorted(self.game.raycasting.objects_to_render, key=lambda t: t[0], reverse=True)
        for depth, image, pos in list_objects:
            self.screen.blit(image, pos)

    @staticmethod
    def get_texture(path, res=(TEXTURE_SIZE, TEXTURE_SIZE)):
        texture = pg.image.load(path).convert_alpha()
        return pg.transform.scale(texture, res)

    def load_wall_textures(self):
        return {
            1: self.get_texture('resources/textures/wall1.png'),
            2: self.get_texture('resources/textures/wall2.jpg'),
            3: self.get_texture('resources/textures/wall3.png')
        }
