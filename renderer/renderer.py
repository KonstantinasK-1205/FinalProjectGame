import pygame as pg
from renderer.opengl import *
from renderer.texture_manager import *
from renderer.vbo_manager import *
from renderer.map_renderer import *
from renderer.minimap_renderer import *
from renderer.skybox_renderer import *
from renderer.hud_renderer import *
from renderer.sprite_renderer import *


class Renderer:
    def __init__(self, game):
        self.game = game

        glEnable(GL_TEXTURE_2D)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_CULL_FACE)

        glEnableClientState(GL_TEXTURE_COORD_ARRAY)
        glEnableClientState(GL_VERTEX_ARRAY)

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        glEnable(GL_FOG)
        glFogfv(GL_FOG_COLOR, (0, 0, 0))
        glFogi(GL_FOG_MODE, GL_LINEAR)
        glFogf(GL_FOG_START, 5)
        glFogf(GL_FOG_END, 15)

        self.texture_manager = TextureManager(game, self)
        self.vbo_manager = VboManager(game, self)
        self.map_renderer = MapRenderer(game, self)
        self.minimap_renderer = MinimapRenderer(game, self)
        self.skybox_renderer = SkyboxRenderer(game, self)
        self.hud_renderer = HudRenderer(game, self)
        self.sprite_renderer = SpriteRenderer(game, self)

        self.camera_pos = [0, 0, 0]
        self.camera_angle = [0, 0]

        self.drawing_minimap = False

    def update_map_vbos(self):
        self.map_renderer.update_vbos()
        self.minimap_renderer.update_vbos()

    def load_texture_from_file(self, path, repeat=False, mipmapped=False):
        try:
            surface = pg.image.load(path)
        except FileNotFoundError:
            print("renderer.py: Failed to load texture - " + path)
            # Load a checkerboard error texture
            surface = pg.Surface((2, 2))
            surface.set_at((0, 1), (255, 0, 255))
            surface.set_at((1, 0), (255, 0, 255))
            surface = pg.transform.scale(surface, (128, 128))

        self.load_texture_from_surface(path, surface, repeat, mipmapped)

    def load_texture_from_surface(self, path, surface, repeat=False, mipmapped=False):
        self.texture_manager.load_texture_from_surface(path, surface, repeat, mipmapped)

    def delete_texture(self, texture):
        self.texture_manager.delete_texture(texture)

    def get_texture_width(self, texture):
        return self.texture_manager.texture_sizes[texture][0]

    def get_texture_height(self, texture):
        return self.texture_manager.texture_sizes[texture][1]

    def get_texture_size(self, texture):
        return self.texture_manager.texture_sizes[texture]

    def load_vbo(self, name, data):
        self.vbo_manager.load_vbo(name, data)

    def draw_rect(self, x, y, width, height, texture=None, color=(255, 255, 255), angle=None):
        self.hud_renderer.rects_to_render.append(
            self.Renderable(x, y, None, width, height, texture, color, False, angle))

    def draw_fullscreen_rect(self, texture=None, color=(255, 255, 255)):
        self.draw_rect(0, 0, self.game.width, self.game.height, texture, color)

    def draw_sprite(self, pos, size, texture=None, color=(255, 255, 255), angle=None):
        self.sprite_renderer.sprites_to_render.append(self.Renderable(pos[0], pos[1], pos[2],
                                                                      size[0], size[1],
                                                                      texture,
                                                                      color,
                                                                      False,
                                                                      angle))

    def draw_sphere(self, pos, size, texture=None, color=(255, 255, 255)):
        self.sprite_renderer.sprites_to_render.append(self.Renderable(pos[0], pos[1], pos[2],
                                                                      size[0], size[1],
                                                                      texture,
                                                                      color,
                                                                      True,
                                                                      None))

    def draw_minimap(self, x, y, tile_size):
        self.minimap_renderer.pos[0] = x
        self.minimap_renderer.pos[1] = y
        self.minimap_renderer.tile_size = tile_size
        self.drawing_minimap = True

    def draw_queued(self):
        glViewport(0, 0, self.game.width, self.game.height)

        self.draw_3d()
        self.draw_2d()

    def draw_3d(self):
        glClear(GL_DEPTH_BUFFER_BIT)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(
            self.game.settings_manager.settings["fov"],
            self.game.width / self.game.height,
            0.1, 50
        )

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        glRotatef(math.degrees(self.camera_angle[1]), 1, 0, 0)
        glRotatef(math.degrees(self.camera_angle[0]) + 90, 0, 1, 0)

        self.skybox_renderer.draw()

        glTranslatef(-self.camera_pos[0], -self.camera_pos[2], -self.camera_pos[1])

        self.map_renderer.draw()
        self.sprite_renderer.draw()

    def draw_2d(self):
        if self.drawing_minimap:
            self.minimap_renderer.draw()
            # Do not draw the minimap next frame unless asked again
            self.drawing_minimap = False

        self.hud_renderer.draw()

    class Renderable:
        def __init__(self, x, y, z, width, height, texture, color, sphere, angle):
            self.x = x
            self.y = y
            self.z = z
            self.width = width
            self.height = height
            self.texture = texture
            self.color = color
            self.sphere = sphere
            self.angle = angle
