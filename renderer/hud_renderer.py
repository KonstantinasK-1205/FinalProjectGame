from renderer.opengl import *


class HudRenderer:
    def __init__(self, game, renderer):
        self.game = game
        self.renderer = renderer

        self.rects_to_render = []

        renderer.load_vbo("hud", [
            1, 0, 1, 1,
            1, 1, 1, 0,
            0, 1, 0, 0,
            0, 0, 0, 1
        ])

    def draw(self):
        glDisable(GL_DEPTH_TEST)

        glBindBuffer(GL_ARRAY_BUFFER, self.renderer.vbo_manager.vbos["hud"])
        glTexCoordPointer(2, GL_FLOAT, 4 * 4, ctypes.c_void_p(0))
        glVertexPointer(2, GL_FLOAT, 4 * 4, ctypes.c_void_p(2 * 4))

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, self.game.width, self.game.height, 0, 0, 100)

        glMatrixMode(GL_MODELVIEW)

        for rect in self.rects_to_render:
            # Position and size should be integer to avoid blurry text
            rect.x = int(rect.x)
            rect.y = int(rect.y)
            rect.width = int(rect.width)
            rect.height = int(rect.height)

            if rect.texture:
                glBindTexture(GL_TEXTURE_2D, self.renderer.texture_manager.textures[rect.texture])
            else:
                glBindTexture(GL_TEXTURE_2D, 0)

            if len(rect.color) == 3:
                glColor3ub(rect.color[0], rect.color[1], rect.color[2])
            elif len(rect.color) == 4:
                glColor4ub(rect.color[0], rect.color[1], rect.color[2], rect.color[3])

            glLoadIdentity()
            glTranslatef(rect.x, rect.y, 0)
            glScalef(rect.width, rect.height, 1)
            glDrawArrays(GL_QUADS, 0, 4)

        self.rects_to_render = []
