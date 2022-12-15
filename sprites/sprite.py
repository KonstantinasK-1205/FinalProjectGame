from collections import deque
from settings import *
import os
import pygame as pg


class Sprite:
    def __init__(self, game, pos, scale):
        self.game = game
        self.player = game.player

        # Init position and dimension
        self.x = pos[0]
        self.y = pos[1]
        self.z = 0
        self.width = scale
        self.height = scale

        # Init texture and animation variables
        self.texture_path = None
        self.current_animation = None
        self.animations = {}
        self.animation_time_prev = pg.time.get_ticks()
        self.delete = False

    def update(self):
        if self.current_animation:
            self.check_animation_time()
            self.animate()

    def draw(self):
        self.game.renderer.objects_to_render.append(self)

    def load_texture(self, path):
        self.texture_path = path
        self.game.renderer.load_texture_from_file(self.texture_path)

    def load_animation_textures(self, path):
        images = deque()
        for file_name in sorted(os.listdir(path)):
            if os.path.isfile(os.path.join(path, file_name)):
                texture_path = path + '/' + file_name
                self.game.renderer.load_texture_from_file(texture_path)
                images.append(texture_path)
        return images

    def animate(self):
        animation_set = self.animations[self.current_animation]
        if animation_set["Animation Completed"]:
            self.animations[self.current_animation]["Frames"].rotate(-1)
            self.texture_path = animation_set["Frames"][0]

    def check_animation_time(self):
        animation_set = self.animations[self.current_animation]
        animation_set["Animation Completed"] = False
        time_now = pg.time.get_ticks()
        if time_now - self.animation_time_prev > animation_set["Animation Speed"]:
            self.animation_time_prev = time_now
            animation_set["Animation Completed"] = True

    def set_position(self, x, y, z=0):
        self.x = x
        self.y = y
        self.z = z

    def set_height(self, height):
        self.height = height

    def set_width(self, width):
        self.width = width

