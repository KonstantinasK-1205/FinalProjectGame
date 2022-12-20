import pygame as pg
from OpenGL.GL import *
from OpenGL.GLU import *
from array import array

from settings import *


class Renderer:
    def __init__(self, game):
        self.game = game
        self.rects_to_render = []
        self.sprites_to_render = []
        self.textures = {}
        self.vbos = {}
        self.draw_world = False

        glEnable(GL_TEXTURE_2D)
        glEnable(GL_BLEND)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_CULL_FACE)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        glEnable(GL_FOG)
        glFogfv(GL_FOG_COLOR, (0, 0, 0))
        glFogi(GL_FOG_MODE, GL_LINEAR)
        glFogf(GL_FOG_START, 5)
        glFogf(GL_FOG_END, 15)

        glEnableClientState(GL_TEXTURE_COORD_ARRAY)
        glEnableClientState(GL_VERTEX_ARRAY)

        self.load_texture_from_file("resources/textures/sky.png", True)
        self.load_texture_from_file("resources/textures/floor.png", True)
        self.load_texture_from_file("resources/textures/wall1.png", True)
        self.load_texture_from_file("resources/textures/wall2.png", True)
        self.load_texture_from_file("resources/textures/wall3.png", True)
        self.load_texture_from_file("resources/textures/wall4.png", True)

        self.load_vbo("wall", [
            0, 0  , 0, 0  , 1,
            1, 0  , 1, 0  , 1,
            1, 1.5, 1, 1.5, 1,
            0, 1.5, 0, 1.5, 1,

            1, 0  , 0, 0  , 0,
            1, 1.5, 0, 1.5, 0,
            0, 1.5, 1, 1.5, 0,
            0, 0  , 1, 0  , 0,

            1, 0  , 1, 0  , 0,
            1, 1.5, 1, 1.5, 0,
            0, 1.5, 1, 1.5, 1,
            0, 0  , 1, 0  , 1,

            0, 0  , 0, 0  , 0,
            1, 0  , 0, 0  , 1,
            1, 1.5, 0, 1.5, 1,
            0, 1.5, 0, 1.5, 0
        ])

        self.load_vbo("object", [
            1, 0, -0.5, 0, 0,
            0, 0,  0.5, 0, 0,
            0, 1,  0.5, 1, 0,
            1, 1, -0.5, 1, 0
        ])

        self.load_vbo("sky", [
            3, 0,  2, -1,
            3, 3,  2,  2,
            0, 3, -1,  2,
            0, 0, -1, -1
        ])

        self.load_vbo("hud", [
            1, 0, 1, 1,
            1, 1, 1, 0,
            0, 1, 0, 0,
            0, 0, 0, 1
        ])

        self.update_sphere_vbo()

        self.map_size = (0, 0)

    def update_floor_vbo(self):
        if self.game.map.size == self.map_size:
            return

        self.floor_vbo_verts = 0

        data = []
        for i in range(self.game.map.height):
            for j in range(self.game.map.width):
                if self.game.map.is_wall(j, i):
                    continue

                data.extend([
                    0, 0, j + 0, 0, i + 1,
                    1, 0, j + 1, 0, i + 1,
                    1, 1, j + 1, 0, i + 0,
                    0, 1, j + 0, 0, i + 0
                ])
                self.floor_vbo_verts += 4

        self.load_vbo("floor", data)
        self.map_size = self.game.map.size

    def update_sphere_vbo(self):
        # More steps - less square circle, but more vertices
        STEPS = 20
        ANGLE_STEP = math.pi / STEPS

        self.sphere_vbo_verts = 0

        data = []
        for i in range(STEPS):
            angle = ANGLE_STEP * i

            x = math.sin(angle) / 2
            y = (math.sin(angle + math.pi * 1.5) + 1) / 2
            y2 = (math.sin(angle + ANGLE_STEP + math.pi * 1.5) + 1) / 2
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

    def load_vbo(self, name, data):
        data_array = array("f", data)
        array_bytes = data_array.tobytes()

        # Is the GL VBO already created?
        if not name in self.vbos:
            vbo = glGenBuffers(1)
            self.vbos[name] = vbo

        glBindBuffer(GL_ARRAY_BUFFER, self.vbos[name])
        glBufferData(GL_ARRAY_BUFFER, len(array_bytes), array_bytes, GL_STATIC_DRAW)

    def load_texture_from_file(self, path, repeat = False):
        try:
            surface = pg.image.load(path)
        except pg.error:
            print("Texture wasn't found : " + path)
            surface = pg.image.load("resources/sprite/default.png").convert_alpha()
            return
        self.load_texture_from_surface(path, surface, repeat)

    def load_texture_from_surface(self, path, surface, repeat = False):
        bitmap = pg.image.tostring(surface, "RGBA", 1)

        # Is the GL texture already created?
        if not path in self.textures:
            gl_texture = glGenTextures(1)
            self.textures[path] = gl_texture

        glBindTexture(GL_TEXTURE_2D, self.textures[path])
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        if repeat:
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        else:
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, surface.get_width(), surface.get_height(), 0, GL_RGBA, GL_UNSIGNED_BYTE, bitmap)

    def draw_rect(self, x, y, width, height, texture=None, color=(255, 255, 255, 255)):
        self.rects_to_render.append(self.Renderable(x, y, None, width, height, texture, color, False))

    def draw_fullscreen_rect(self, texture=None, color=(255, 255, 255, 255)):
        self.draw_rect(0, 0, self.game.width, self.game.height, texture, color)

    def draw_sprite(self, x, y, z, width, height, texture=None, color=(255, 255, 255, 255)):
        self.sprites_to_render.append(self.Renderable(x, y, z, width, height, texture, color, False))

    def draw_sphere(self, x, y, z, width, height, texture=None, color=(255, 255, 255, 255)):
        self.sprites_to_render.append(self.Renderable(x, y, z, width, height, texture, color, True))

    def draw_queued(self):
        glViewport(0, 0, self.game.width, self.game.height)

        if self.draw_world:
            self.draw_2d_bg()
            self.draw_3d()
        self.draw_2d_fg()

    def draw_2d_bg(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        self.draw_2d_bg_sky()

    def draw_2d_bg_sky(self):
        glBindBuffer(GL_ARRAY_BUFFER, self.vbos["sky"])
        glTexCoordPointer(2, GL_FLOAT, 4 * 4, ctypes.c_void_p(0))
        glVertexPointer(2, GL_FLOAT, 4 * 4, ctypes.c_void_p(2 * 4))

        glBindTexture(GL_TEXTURE_2D, self.textures["resources/textures/sky.png"])

        offset_x = (self.game.player.angle % math.tau) / math.tau
        offset_y = (-self.game.player.angle_ver % math.tau) / math.tau

        glTranslatef(-offset_x, -offset_y, 0)
        glDrawArrays(GL_QUADS, 0, 4)

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

            if rect.texture == None:
                glBindTexture(GL_TEXTURE_2D, 0)
            else:
                glBindTexture(GL_TEXTURE_2D, self.textures[rect.texture])

            glColor4f(1, 1, 1, 1)
            if not rect.color == None:
                if len(rect.color) == 3:
                    glColor3f(rect.color[0] / 255, rect.color[1] / 255, rect.color[2] / 255)
                elif len(rect.color) == 4:
                    glColor4f(rect.color[0] / 255, rect.color[1] / 255, rect.color[2] / 255, rect.color[3] / 255)

            glLoadIdentity()
            glTranslatef(rect.x, rect.y, 0)
            glScalef(rect.width, rect.height, 1)
            glDrawArrays(GL_QUADS, 0, 4)

        self.rects_to_render = []
        glEnable(GL_DEPTH_TEST)

        glColor4f(1, 1, 1, 1)

    def draw_3d(self):
        glClear(GL_DEPTH_BUFFER_BIT)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(FOV, self.game.width / self.game.height, 0.1, 100)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        glRotatef(math.degrees(self.game.player.angle_ver), 1, 0, 0)
        glRotatef(math.degrees(self.game.player.angle) + 90, 0, 1, 0)
        glTranslatef(-self.game.player.x, -self.game.player.z - 0.6, -self.game.player.y)

        self.draw_3d_floor()
        self.draw_3d_map()
        self.draw_3d_objects()

    def draw_3d_floor(self):
        self.update_floor_vbo()

        glBindTexture(GL_TEXTURE_2D, self.textures["resources/textures/floor.png"])

        glBindBuffer(GL_ARRAY_BUFFER, self.vbos["floor"])
        glTexCoordPointer(2, GL_FLOAT, 5 * 4, ctypes.c_void_p(0))
        glVertexPointer(3, GL_FLOAT, 5 * 4, ctypes.c_void_p(2 * 4))

        glPushMatrix()
        glDrawArrays(GL_QUADS, 0, self.floor_vbo_verts)
        glPopMatrix()

    def draw_3d_map(self):
        glBindBuffer(GL_ARRAY_BUFFER, self.vbos["wall"])
        glTexCoordPointer(2, GL_FLOAT, 5 * 4, ctypes.c_void_p(0))
        glVertexPointer(3, GL_FLOAT, 5 * 4, ctypes.c_void_p(2 * 4))

        for i in range(self.game.map.height):
            for j in range(self.game.map.width):
                if not self.game.map.is_wall(j, i):
                    continue

                texture_index = self.game.map.data[j + i * self.game.map.width]
                glBindTexture(GL_TEXTURE_2D, self.textures["resources/textures/wall" + str(texture_index) + ".png"])

                glPushMatrix()

                glTranslatef(j, 0, i)
                glDrawArrays(GL_QUADS, 0, 4 * 4)

                glPopMatrix()

    def draw_3d_objects(self):
        glDisable(GL_CULL_FACE)

        # Objects must be sorted closest to player first for transparency to
        # work properly
        for o in self.sprites_to_render:
            o.__distance_from_player = math.hypot(o.x - self.game.player.x, o.y - self.game.player.y, o.z - self.game.player.z)
        self.sprites_to_render = sorted(self.sprites_to_render, key=lambda t: t.__distance_from_player, reverse=True)

        for o in self.sprites_to_render:
            if o.texture == None:
                glBindTexture(GL_TEXTURE_2D, 0)
            else:
                glBindTexture(GL_TEXTURE_2D, self.textures[o.texture])

            glColor4f(1, 1, 1, 1)
            if not o.color == None:
                if len(o.color) == 3:
                    glColor3f(o.color[0] / 255, o.color[1] / 255, o.color[2] / 255)
                elif len(o.color) == 4:
                    glColor4f(o.color[0] / 255, o.color[1] / 255, o.color[2] / 255, o.color[3] / 255)

            glPushMatrix()

            glTranslatef(o.x, o.z, o.y)
            glRotatef(-math.degrees(self.game.player.angle) + 90, 0, 1, 0)
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
        def __init__(self, x, y, z, width, height, texture, color, sphere):
            self.x = x
            self.y = y
            self.z = z
            self.width = width
            self.height = height
            self.texture = texture
            self.color = color
            self.sphere = sphere
