from collections import deque
import math
import os
import pygame as pg


class Sprite:
    def __init__(self, game, pos=None, scale=None):
        self.game = game
        self.player = game.player
        self.sprite_manager = game.sprite_manager

        # Init position and dimension
        if pos is None:
            self.x = self.y = self.z = 0
        else:
            self.x = pos[0]
            self.y = pos[1]
            if len(pos) == 3:
                self.z = pos[2]
            else:
                self.z = 0

        if scale is None:
            self.width = self.height = 0
        elif len(scale) > 1:
            self.width = scale[0]
            self.height = scale[1]
        else:
            self.width = self.height = scale[0]

        # Init texture and animation variables
        self.texture_path = None
        self.current_state = None
        self.delete = False

    def update(self):
        pass

    def draw(self):
        self.game.renderer.draw_sprite(self.x, self.y, self.z, self.width, self.height, self.texture_path)

    def set_position(self, x, y, z=0):
        self.x = x
        self.y = y
        self.z = z

    def distance_from(self, other):
        return math.hypot(other.x - self.x, other.y - self.y, other.z - self.z)
