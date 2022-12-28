from collections import deque
import math
import os
import pygame as pg


class Sprite:
    def __init__(self, game, pos=None, scale=None):
        self.game = game
        self.player = game.player

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
        self.spritesheet = None
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
        self.game.renderer.draw_sprite(self.x, self.y, self.z, self.width, self.height, self.texture_path)

    def load_weapon_images(self, weapon, images, scale=2.5):
        loaded_images = deque()
        for image in images:
            full_path = "resources/sprites/weapon/" + weapon + "/" + str(image) + ".png"
            if os.path.exists(full_path):
                img = pg.image.load(full_path).convert_alpha()
            else:
                break
            img = pg.transform.smoothscale(img, (img.get_width() * scale, img.get_height() * scale))

            self.game.renderer.load_texture_from_surface(full_path, img)
            loaded_images.append(full_path)
        return loaded_images

    def load_image(self, path):
        try:
            image = pg.image.load(path).convert_alpha()
        except pg.error:
            print("Image wasn't found: " + path)
            image = pg.image.load("resources/sprites/default.png").convert_alpha()
        return image

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

    def images_at(self, texture_name, rects):
        frame = 0
        images = deque()
        for rect in rects:
            texture = texture_name + str(frame)
            image = self.spritesheet.subsurface(rect)
            self.game.renderer.load_texture_from_surface(texture, image)
            images.append(texture)
            frame += 1
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

    def distance_from(self, other):
        return math.hypot(other.x - self.x, other.y - self.y, other.z - self.z)
