from renderer.opengl import *


class SkyboxRenderer:
    def __init__(self, game, renderer):
        self.game = game
        self.renderer = renderer

        renderer.load_vbo("skybox", [
            1, 0, -10, 10,  10,
            1, 1, -10, 10, -10,
            0, 1,  10, 10, -10,
            0, 0,  10, 10,  10
        ])

        renderer.load_texture_from_file("resources/textures/skybox/up.jpg")
        renderer.load_texture_from_file("resources/textures/skybox/down.jpg")
        renderer.load_texture_from_file("resources/textures/skybox/north.jpg")
        renderer.load_texture_from_file("resources/textures/skybox/west.jpg")
        renderer.load_texture_from_file("resources/textures/skybox/south.jpg")
        renderer.load_texture_from_file("resources/textures/skybox/east.jpg")

    def draw(self):
        glDisable(GL_FOG)
        glDisable(GL_DEPTH_TEST)

        glBindBuffer(GL_ARRAY_BUFFER, self.renderer.vbo_manager.vbos["skybox"])
        glTexCoordPointer(2, GL_FLOAT, 5 * 4, ctypes.c_void_p(0))
        glVertexPointer(3, GL_FLOAT, 5 * 4, ctypes.c_void_p(2 * 4))

        self.draw_side("up", (0, 0))

        self.draw_side("north", (0, 90))
        self.draw_side("west", (90, 90))
        self.draw_side("south", (180, 90))
        self.draw_side("east", (270, 90))

        self.draw_side("down", (0, 180))

        glEnable(GL_FOG)
        glEnable(GL_DEPTH_TEST)

    def draw_side(self, texture_name, angle):
        glBindTexture(GL_TEXTURE_2D, self.renderer.texture_manager.textures["resources/textures/skybox/" + texture_name + ".jpg"])

        glPushMatrix()

        glRotatef(angle[0], 0, 1, 0)
        glRotatef(angle[1], 1, 0, 0)

        glDrawArrays(GL_QUADS, 0, 6 * 4)

        glPopMatrix()
