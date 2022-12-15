import pygame as pg
from OpenGL.GL import *
from OpenGL.GLU import *
from array import array

from settings import *


class Renderer:
    def __init__(self, game):
        self.game = game
        self.objects_to_render = []
        self.textures = {}
        self.draw_world = False

        glEnable(GL_TEXTURE_2D)
        glEnable(GL_BLEND)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_CULL_FACE)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        glEnableClientState(GL_TEXTURE_COORD_ARRAY)
        glEnableClientState(GL_VERTEX_ARRAY)

        glViewport(0, 0, WIDTH, HEIGHT)

        self.load_texture_from_file("resources/textures/sky.jpg")
        self.load_texture_from_file("resources/textures/floor.png")
        self.load_texture_from_file("resources/textures/wall1.png")
        self.load_texture_from_file("resources/textures/wall2.png")
        self.load_texture_from_file("resources/textures/wall3.png")
        self.load_texture_from_file("resources/textures/wall4.png")

        self.wall_vbo = self.load_vbo([
            0, 0, 0, 0, 1,
            1, 0, 1, 0, 1,
            1, 1, 1, 1, 1,
            0, 1, 0, 1, 1,

            1, 0, 0, 0, 0,
            1, 1, 0, 1, 0,
            0, 1, 1, 1, 0,
            0, 0, 1, 0, 0,

            1, 0, 1, 0, 0,
            1, 1, 1, 1, 0,
            0, 1, 1, 1, 1,
            0, 0, 1, 0, 1,

            0, 0, 0, 0, 0,
            1, 0, 0, 0, 1,
            1, 1, 0, 1, 1,
            0, 1, 0, 1, 0
        ])

        self.object_vbo = self.load_vbo([
            1, 0, -0.5, 0, 0,
            0, 0,  0.5, 0, 0,
            0, 1,  0.5, 1, 0,
            1, 1, -0.5, 1, 0
        ])

        self.sky_vbo = self.load_vbo([
            3, 0,  2, 0,
            3, 1,  2, 1,
            0, 1, -1, 1,
            0, 0, -1, 0
        ])

        self.hud_vbo = self.load_vbo([
            1, 0,  1, -1,
            1, 1,  1,  1,
            0, 1, -1,  1,
            0, 0, -1, -1
        ])

    def load_vbo(self, data):
        data_array = array("f", data)
        array_bytes = data_array.tobytes()

        vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, vbo)
        glBufferData(GL_ARRAY_BUFFER, len(array_bytes), array_bytes, GL_STATIC_DRAW)

        return vbo

    def load_texture_from_file(self, path):
        surface = pg.image.load(path)
        self.load_texture_from_surface(path, surface)

    def load_texture_from_surface(self, path, surface):
        bitmap = pg.image.tostring(surface, "RGBA", 1)

        # Is the GL texture already created?
        if not path in self.textures:
            gl_texture = glGenTextures(1)
            self.textures[path] = gl_texture

        glBindTexture(GL_TEXTURE_2D, self.textures[path])
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, surface.get_width(), surface.get_height(), 0, GL_RGBA, GL_UNSIGNED_BYTE, bitmap)

    def render(self):
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
        glBindBuffer(GL_ARRAY_BUFFER, self.sky_vbo)
        glTexCoordPointer(2, GL_FLOAT, 4 * 4, ctypes.c_void_p(0))
        glVertexPointer(2, GL_FLOAT, 4 * 4, ctypes.c_void_p(2 * 4))

        glBindTexture(GL_TEXTURE_2D, self.textures["resources/textures/sky.jpg"])

        offset = (self.game.player.angle % math.tau) / math.tau

        glTranslatef(-offset, 0, 0)
        glDrawArrays(GL_QUADS, 0, 4)

    def draw_2d_fg(self):
        glBindBuffer(GL_ARRAY_BUFFER, self.hud_vbo)
        glTexCoordPointer(2, GL_FLOAT, 4 * 4, ctypes.c_void_p(0))
        glVertexPointer(2, GL_FLOAT, 4 * 4, ctypes.c_void_p(2 * 4))

        glClear(GL_DEPTH_BUFFER_BIT)

        self.load_texture_from_surface("hud", self.game.screen)
        glBindTexture(GL_TEXTURE_2D, self.textures["hud"])

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        glDrawArrays(GL_QUADS, 0, 4)

    def draw_3d(self):
        glClear(GL_DEPTH_BUFFER_BIT)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(FOV, WIDTH / HEIGHT, 0.1, 100)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        glRotatef(math.degrees(self.game.player.get_angle) + 90, 0, 1, 0)
        glTranslatef(-self.game.player.pos_x, -0.5, -self.game.player.pos_y)

        self.draw_3d_floor()
        self.draw_3d_map()
        self.draw_3d_objects()

    def draw_3d_floor(self):
        glBindTexture(GL_TEXTURE_2D, self.textures["resources/textures/floor.png"])

        glPushMatrix()

        glBegin(GL_QUADS)
        glTexCoord2f(0, 0)
        glVertex3f(0, 0, self.game.map.get_size()[1])
        glTexCoord2f(self.game.map.get_size()[0], 0)
        glVertex3f(self.game.map.get_size()[0], 0, self.game.map.get_size()[1])
        glTexCoord2f(self.game.map.get_size()[0], self.game.map.get_size()[1])
        glVertex3f(self.game.map.get_size()[0], 0, 0)
        glTexCoord2f(0, self.game.map.get_size()[1] )
        glVertex3f(0, 0, 0)
        glEnd()

        glPopMatrix()

    def draw_3d_map(self):
        glBindBuffer(GL_ARRAY_BUFFER, self.wall_vbo)
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

        glBindBuffer(GL_ARRAY_BUFFER, self.object_vbo)
        glTexCoordPointer(2, GL_FLOAT, 5 * 4, ctypes.c_void_p(0))
        glVertexPointer(3, GL_FLOAT, 5 * 4, ctypes.c_void_p(2 * 4))

        # Objects must be sorted closest to player first for transparency to
        # work properly
        for o in self.objects_to_render:
            o.distance_from_player = math.hypot(o.x - self.game.player.pos_x, o.y - self.game.player.pos_y)

        self.objects_to_render = sorted(self.objects_to_render, key=lambda t: t.distance_from_player, reverse=True)

        for o in self.objects_to_render:
            glBindTexture(GL_TEXTURE_2D, self.textures[o.texture_path])

            glPushMatrix()

            glTranslatef(o.x, 0, o.y)

            glTranslatef(0, o.z, 0)
            glRotatef(-math.degrees(self.game.player.get_angle) + 90, 0, 1, 0)
            glScalef(o.width, o.height, 1)
            glDrawArrays(GL_QUADS, 0, 4)

            glPopMatrix()

        self.objects_to_render = []

        glEnable(GL_CULL_FACE)
