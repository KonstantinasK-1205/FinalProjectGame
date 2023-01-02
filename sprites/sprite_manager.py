import os
import pygame as pg


class SpriteManager:
    def __init__(self, game):
        self.game = game
        self.sprites = {}

    def get_sprite(self, name):
        if name in self.sprites:
            return self.sprites[name][0]
        else:
            print("sprite_manager.py: Sprite doesn't exist - " + name)
        return None

    def load_single_image(self, name, path, scale=2.5):
        # Check if image exist in dict, and return if its does
        if name in self.sprites:
            return self.sprites[name]

        # If image doesn't exist, load it and save it into dict
        if os.path.exists(path):
            img = pg.image.load(path).convert_alpha()
            img = pg.transform.smoothscale(img, (img.get_width() * scale, img.get_height() * scale))
        else:
            img = pg.image.load("resources/sprites/default.png").convert_alpha()
            print("sprite_manager.py: Path doesn't exist - " + path)
        self.game.renderer.load_texture_from_surface(path, img)
        self.sprites[name] = [path]
        return self.sprites[name]

    def load_multiple_images(self, name, path, scale=2.5):
        # Check if images exist in dict, and return if it does
        if name in self.sprites:
            return self.sprites[name]

        # If images doesn't exist, load it and save it into dict
        list_of_images = []
        if os.path.exists(path):
            files = os.listdir(path)
            for file in files:
                file = path + file
                img = pg.image.load(file).convert_alpha()
                img = pg.transform.smoothscale(img, (img.get_width() * scale, img.get_height() * scale))
                list_of_images.append(file)
                self.game.renderer.load_texture_from_surface(file, img)
        else:
            print("sprite_manager.py: Path doesn't exist - " + path)
            return []
        list_of_images.sort()
        self.sprites[name] = list_of_images
        return self.sprites[name]
