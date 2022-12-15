import pygame as pg

from settings import *


class Sprite:
    def __init__(self, game, path='resources/sprites/static_sprites/candelabra.png',
                 pos=(2, 2), scale=0.7, shift=0.25, damage=0):
        self.game = game
        self.player = game.player
        self.x = pos[0]
        self.y = pos[1]
        self.z = 0
        self.width = scale / 2
        self.height = scale
        self.texture_path = path
        self.delete = False

        self.game.renderer.load_texture_from_file(self.texture_path)

    def update(self):
        pass

    def draw(self):
        self.game.renderer.objects_to_render.append(self)
