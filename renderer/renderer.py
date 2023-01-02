import pygame as pg
from renderer.opengl import *
from renderer.texture_manager import *
from renderer.vbo_manager import *
from renderer.map_renderer import *
from renderer.minimap_renderer import *
from renderer.skybox_renderer import *
from settings import *


class Renderer:
    def __init__(self, game):
        self.game = game
        self.rects_to_render = []
        self.sprites_to_render = []
        self.draw_world = False
        self.drawing_minimap = False

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

        self.load_vbo("object", [
            1, 0, -0.5, 0, 0,
            0, 0,  0.5, 0, 0,
            0, 1,  0.5, 1, 0,
            1, 1, -0.5, 1, 0
        ])

        self.load_vbo("hud", [
            1, 0, 1, 1,
            1, 1, 1, 0,
            0, 1, 0, 0,
            0, 0, 0, 1
        ])

        self.vbo_manager.load_sphere_vbo()

    def update_map(self):
        self.map_renderer.update_vbos()
        self.minimap_renderer.update_vbos()

    def load_texture_from_file(self, path, repeat = False, mipmapped = False):
        try:
            surface = pg.image.load(path)
        except FileNotFoundError:
            print("Failed to load texture " + path)
            # Load a checkerboard error texture
            surface = pg.Surface((2, 2))
            surface.set_at((0, 1), (255, 0, 255))
            surface.set_at((1, 0), (255, 0, 255))
            surface = pg.transform.scale(surface, (128, 128))

        self.load_texture_from_surface(path, surface, repeat, mipmapped)

    def load_texture_from_surface(self, path, surface, repeat = False, mipmapped = False):
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
        self.rects_to_render.append(self.Renderable(x, y, None, width, height, texture, color, False, angle))

    def draw_fullscreen_rect(self, texture=None, color=(255, 255, 255)):
        self.draw_rect(0, 0, self.game.width, self.game.height, texture, color)

    def draw_sprite(self, x, y, z, width, height, texture=None, color=(255, 255, 255), angle=None):
        self.sprites_to_render.append(self.Renderable(x, y, z, width, height, texture, color, False, angle))

    def draw_sphere(self, x, y, z, width, height, texture=None, color=(255, 255, 255)):
        self.sprites_to_render.append(self.Renderable(x, y, z, width, height, texture, color, True, None))

    def draw_minimap(self, x, y, tile_size):
        self.minimap_renderer.x = x
        self.minimap_renderer.y = y
        self.minimap_renderer.tile_size = tile_size
        self.drawing_minimap = True

    def draw_queued(self):
        glViewport(0, 0, self.game.width, self.game.height)

        if self.draw_world:
            self.draw_3d()
        self.draw_2d_fg()

    def draw_2d_fg(self):
        glDisable(GL_DEPTH_TEST)

        glBindBuffer(GL_ARRAY_BUFFER, self.vbo_manager.vbos["hud"])
        glTexCoordPointer(2, GL_FLOAT, 4 * 4, ctypes.c_void_p(0))
        glVertexPointer(2, GL_FLOAT, 4 * 4, ctypes.c_void_p(2 * 4))

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, self.game.width, self.game.height, 0, 0, 100)

        glMatrixMode(GL_MODELVIEW)

        for rect in self.rects_to_render:
            # Position and size should be rounded to avoid blurry text, etc.
            rect.x = round(rect.x)
            rect.y = round(rect.y)
            rect.width = round(rect.width)
            rect.height = round(rect.height)

            if rect.texture == None:
                glBindTexture(GL_TEXTURE_2D, 0)
            else:
                glBindTexture(GL_TEXTURE_2D, self.texture_manager.textures[rect.texture])

            glColor4f(1, 1, 1, 1)
            if not rect.color == None:
                if len(rect.color) == 3:
                    glColor3f(rect.color[0] / 255, rect.color[1] / 255, rect.color[2] / 255)
                elif len(rect.color) == 4:
                    glColor4f(rect.color[0] / 255, rect.color[1] / 255, rect.color[2] / 255, rect.color[3] / 255)

            glLoadIdentity()
            glTranslatef(rect.x, rect.y, 0)
            if not rect.angle == None:
                # Don't ask. Just believe.
                glTranslatef(rect.width / 2, rect.height / 2, 0)
                glRotatef(math.degrees(rect.angle), 0, 0, 1)
                glTranslatef(-rect.width / 2, -rect.height / 2, 0)
            glScalef(rect.width, rect.height, 1)
            glDrawArrays(GL_QUADS, 0, 4)

        self.rects_to_render = []

        if self.drawing_minimap:
            self.minimap_renderer.draw()
            # Do not draw the minimap next frame unless asked again
            self.drawing_minimap = False

        glEnable(GL_DEPTH_TEST)
        glColor4f(1, 1, 1, 1)

    def draw_3d(self):
        glClear(GL_DEPTH_BUFFER_BIT)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(FOV, self.game.width / self.game.height, 0.1, 50)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        glRotatef(math.degrees(self.game.player.angle_ver), 1, 0, 0)
        glRotatef(math.degrees(self.game.player.angle) + 90, 0, 1, 0)

        self.skybox_renderer.draw()

        glTranslatef(-self.game.player.x, -self.game.player.z - self.game.player.height, -self.game.player.y)

        self.map_renderer.draw()
        self.draw_3d_objects()

    def draw_3d_objects(self):
        glDisable(GL_CULL_FACE)

        # Objects must be sorted from farthest to closest for transparency to
        # work properly
        for o in self.sprites_to_render:
            o.__distance_from_player = math.hypot(
                o.x - self.game.player.x,
                o.y - self.game.player.y,
                o.z - self.game.player.z
            )
        self.sprites_to_render = sorted(self.sprites_to_render, key=lambda t: t.__distance_from_player, reverse=True)

        for o in self.sprites_to_render:
            if o.texture == None:
                glBindTexture(GL_TEXTURE_2D, 0)
            else:
                glBindTexture(GL_TEXTURE_2D, self.texture_manager.textures[o.texture])

            if len(o.color) == 3:
                glColor3f(o.color[0] / 255, o.color[1] / 255, o.color[2] / 255)
            elif len(o.color) == 4:
                glColor4f(o.color[0] / 255, o.color[1] / 255, o.color[2] / 255, o.color[3] / 255)

            glPushMatrix()

            glTranslatef(o.x, o.z, o.y)
            if o.angle == None:
                # TODO: Why does the player angle need an offset?
                glRotatef(-math.degrees(self.game.player.angle) + 90, 0, 1, 0)
            else:
                glRotatef(math.degrees(o.angle), 0, 1, 0)
            glScalef(o.width, o.height, 1)

            if o.sphere:
                glBindBuffer(GL_ARRAY_BUFFER, self.vbo_manager.vbos["sphere"])
                glTexCoordPointer(2, GL_FLOAT, 5 * 4, ctypes.c_void_p(0 * 4))
                glVertexPointer(3, GL_FLOAT, 5 * 4, ctypes.c_void_p(2 * 4))
                glDrawArrays(GL_QUADS, 0, self.vbo_manager.sphere_vbo_verts)
            else:
                glBindBuffer(GL_ARRAY_BUFFER, self.vbo_manager.vbos["object"])
                glTexCoordPointer(2, GL_FLOAT, 5 * 4, ctypes.c_void_p(0))
                glVertexPointer(3, GL_FLOAT, 5 * 4, ctypes.c_void_p(2 * 4))
                glDrawArrays(GL_QUADS, 0, 4)

            glPopMatrix()

        self.sprites_to_render = []

        glEnable(GL_CULL_FACE)

        glColor4f(1, 1, 1, 1)


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
