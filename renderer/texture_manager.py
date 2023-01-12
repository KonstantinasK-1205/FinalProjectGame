from renderer.opengl import *
import math
import pygame as pg


class TextureManager:
    def __init__(self, game, renderer):
        self.game = game
        self.renderer = renderer
        self.textures = {}
        self.texture_sizes = {}

    def load_texture_from_file(self, path, repeat = False, mipmapped = False):
        try:
            surface = pg.image.load(path)
        except FileNotFoundError:
            print("texture_manager.py: Failed to load texture - " + path)
            # Load a checkerboard error texture
            surface = pg.Surface((2, 2))
            surface.set_at((0, 1), (255, 0, 255))
            surface.set_at((1, 0), (255, 0, 255))
            surface = pg.transform.scale(surface, (128, 128))

        self.load_texture_from_surface(path, surface, repeat, mipmapped)

    def load_texture_from_surface(self, path, surface, repeat = False, mipmapped = False):
        self.texture_sizes[path] = (surface.get_width(), surface.get_height())

        # Downscale texture if greater than maximum size
        # Enabled only for resources/ textures to avoid rescaling text
        max_size = self.game.settings_manager.settings["texture_size"]
        if max_size > 0 and "resources/" in path:
            if surface.get_width() > max_size or surface.get_height() > max_size:
                new_width = min(max_size, surface.get_width())
                new_height = min(max_size, surface.get_height())
                surface = pg.transform.scale(surface, (new_width, new_height))

        # Pygame text can produce a 0 width surface, so in such cases replace
        # it with a 1x1 transparent surface
        if surface.get_width() == 0 or surface.get_height() == 0:
            surface = pg.Surface((1, 1)).convert_alpha()
            surface.fill((0, 0, 0, 0))
        else:
            surface = surface.convert_alpha()

        # Is the GL texture already created?
        if not path in self.textures:
            gl_texture = glGenTextures(1)
            self.textures[path] = gl_texture

        glBindTexture(GL_TEXTURE_2D, self.textures[path])
        if repeat:
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        else:
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)

        if mipmapped:
            # Define mipmap levels
            # Levels must be same width and height, and powers of two
            levels = [math.pow(2, math.ceil(math.log2(max(surface.get_width(), surface.get_height()))))]
            while levels[-1] != 1:
                levels.append(levels[-1] / 2)

            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            # GL_TEXTURE_MAX_LEVEL refers to the largest mipmap level index, so
            # minus the mipmap level count by one
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAX_LEVEL, len(levels) - 1)
            # Use anisotropic filtering to reduce blur
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAX_ANISOTROPY, GL_MAX_TEXTURE_MAX_ANISOTROPY)

            for i in range(len(levels)):
                mipmap_surface = pg.transform.smoothscale(surface, (levels[i], levels[i])).convert_alpha()
                bitmap = pg.image.tostring(mipmap_surface, "RGBA", 1)

                glTexImage2D(GL_TEXTURE_2D, i, GL_RGBA, levels[i], levels[i], 0, GL_RGBA, GL_UNSIGNED_BYTE, bitmap)
        else:
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

            bitmap = pg.image.tostring(surface, "RGBA", 1)

            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, surface.get_width(), surface.get_height(), 0, GL_RGBA, GL_UNSIGNED_BYTE, bitmap)

    def delete_texture(self, texture):
        glDeleteTextures(1, self.textures[texture])
        del self.textures[texture]
        del self.texture_sizes[texture]

    def get_texture_width(self, texture):
        return self.texture_sizes[texture][0]

    def get_texture_height(self, texture):
        return self.texture_sizes[texture][1]

    def get_texture_size(self, texture):
        return self.texture_sizes[texture]

