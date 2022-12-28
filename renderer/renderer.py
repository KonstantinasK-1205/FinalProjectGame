from array import array
from OpenGL.GLU import *
from renderer.map_renderer import *
from renderer.minimap_renderer import *
from renderer.skybox_renderer import *
from settings import *
import pygame as pg


class Renderer:
    def __init__(self, game):
        self.game = game
        self.rects_to_render = []
        self.sprites_to_render = []
        self.textures = {}
        self.texture_sizes = {}
        self.vbos = {}
        self.draw_world = False
        self.drawing_minimap = False
        self.sphere_vbo_verts = 0

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

        self.load_sphere_vbo()

        self.map_renderer = MapRenderer(game, self)
        self.minimap_renderer = MinimapRenderer(game, self)
        self.skybox_renderer = SkyboxRenderer(game, self)

    def update_map(self):
        self.map_renderer.update_vbos()
        self.minimap_renderer.update_vbos()

    def load_texture_from_file(self, path, repeat=False, mipmapped=False):
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

    def load_texture_from_surface(self, path, surface, repeat=False, mipmapped=False):
        self.texture_sizes[path] = (surface.get_width(), surface.get_height())

        # Pygame text can produce a 0 width surface, so in such cases replace
        # it with a 1x1 transparent surface
        if surface.get_width() == 0 or surface.get_height() == 0:
            surface = pg.Surface((1, 1)).convert_alpha()
            surface.fill((0, 0, 0, 0))
        else:
            surface = surface.convert_alpha()

        # Is the GL texture already created?
        if path not in self.textures:
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
            # Define mipmap levels must be same width and height, and powers of two
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
                bitmap = pg.image.tostring(mipmap_surface, "RGBA", True)

                glTexImage2D(GL_TEXTURE_2D, i, GL_RGBA, levels[i], levels[i], 0, GL_RGBA, GL_UNSIGNED_BYTE, bitmap)
        else:
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

            bitmap = pg.image.tostring(surface, "RGBA", True)

            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, surface.get_width(), surface.get_height(),
                         0, GL_RGBA, GL_UNSIGNED_BYTE, bitmap)

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

    def load_vbo(self, name, data):
        data_array = array("f", data)
        array_bytes = data_array.tobytes()

        # Is the GL VBO already created?
        if name not in self.vbos:
            vbo = glGenBuffers(1)
            self.vbos[name] = vbo

        glBindBuffer(GL_ARRAY_BUFFER, self.vbos[name])
        glBufferData(GL_ARRAY_BUFFER, len(array_bytes), array_bytes, GL_STATIC_DRAW)

    def load_sphere_vbo(self):
        # More steps - less square circle, but more vertices
        steps = 20
        angle_step = math.pi / steps

        self.sphere_vbo_verts = 0

        data = []
        for i in range(steps):
            angle = angle_step * i

            x = math.sin(angle) / 2
            y = (math.sin(angle + math.pi * 1.5) + 1) / 2
            y2 = (math.sin(angle + angle_step + math.pi * 1.5) + 1) / 2
            h = y2 - y

            tx1 = -(x - 0.5)
            ty1 = y
            tx2 = 1 - tx1
            ty2 = ty1 + h

            data.extend([
                tx1, ty1, -x, y + h, 0,
                tx2, ty1,  x, y + h, 0,
                tx2, ty2,  x, y + 0, 0,
                tx1, ty2, -x, y + 0, 0
            ])
            self.sphere_vbo_verts += 4

        self.load_vbo("sphere", data)

    def draw_2d_fg(self):
        glDisable(GL_DEPTH_TEST)

        glBindBuffer(GL_ARRAY_BUFFER, self.vbos["hud"])
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

            if rect.texture:
                glBindTexture(GL_TEXTURE_2D, self.textures[rect.texture])
            else:
                glBindTexture(GL_TEXTURE_2D, 0)

            glColor4f(1, 1, 1, 1)
            if rect.color:
                if len(rect.color) == 3:
                    glColor3f(rect.color[0] / 255, rect.color[1] / 255, rect.color[2] / 255)
                elif len(rect.color) == 4:
                    glColor4f(rect.color[0] / 255, rect.color[1] / 255, rect.color[2] / 255, rect.color[3] / 255)

            glLoadIdentity()
            glTranslatef(rect.x, rect.y, 0)
            if rect.angle:
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

        # Objects must be sorted closest to player first for transparency to
        # work properly
        for o in self.sprites_to_render:
            o.__distance_from_player = math.hypot(o.x - self.game.player.x,
                                                  o.y - self.game.player.y,
                                                  o.z - self.game.player.z)
        self.sprites_to_render = sorted(self.sprites_to_render, key=lambda t: t.__distance_from_player, reverse=True)

        for o in self.sprites_to_render:
            if o.texture:
                glBindTexture(GL_TEXTURE_2D, self.textures[o.texture])
            else:
                glBindTexture(GL_TEXTURE_2D, 0)

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
                glBindBuffer(GL_ARRAY_BUFFER, self.vbos["sphere"])
                glTexCoordPointer(2, GL_FLOAT, 5 * 4, ctypes.c_void_p(0))
                glVertexPointer(3, GL_FLOAT, 5 * 4, ctypes.c_void_p(2 * 4))
                glDrawArrays(GL_QUADS, 0, self.sphere_vbo_verts)
            else:
                glBindBuffer(GL_ARRAY_BUFFER, self.vbos["object"])
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
