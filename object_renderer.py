import pygame as pg
from settings import *

class ObjectRenderer:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.wall_textures = self.load_wall_textures()
        self.sky_image = self.get_texture('resources/textures/sky.jpg', (WIDTH, HALF_HEIGHT))
        self.sky_offset = 0
        self.game_over_image = self.get_texture('resources/textures/game_over.png', RES)
        self.game_victory_image = self.get_texture('resources/textures/win.png', RES)

        # New things
        self.font = pg.font.Font("resources/fonts/Font.ttf", 72)
        self.health_text = self.font.render("0", True, (255, 0, 0))
        self.killed_text = self.font.render("0", True, (0, 0, 0))

    def draw(self):
        self.draw_background()
        self.render_game_objects()
        self.draw_player_health()
        self.draw_killed_amount()

    # In Game Texts
    def draw_player_health(self):
        self.health_text = self.font.render(str(self.game.player.health) + " %", True, (255, 0, 0))
        self.screen.blit(self.health_text, (MARGIN, 0))

    def draw_killed_amount(self):
        self.killed_text = self.font.render(str(self.game.object_handler.killed), True, (255, 255, 255))
        self.screen.blit(self.killed_text, (MARGIN, RES[1] - self.font.get_linesize()))

    # States
    def status_game_over(self):
        self.screen.blit(self.game_over_image, (0, 0))

    def status_game_won(self):
        self.screen.blit(self.game_victory_image, (0, 0))

    def player_hitted(self):
        pg.draw.rect(self.screen, (102, 0, 0), pg.Rect(0, 0, RES[0], RES[1]))

    def draw_background(self):
        self.sky_offset = (self.sky_offset + 4.5 * self.game.player.rel) % WIDTH
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
        }

