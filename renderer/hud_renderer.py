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
            # Position and size should be rounded to avoid blurry text, etc.
            rect.x = round(rect.x)
            rect.y = round(rect.y)
            rect.width = round(rect.width)
            rect.height = round(rect.height)

            if rect.texture:
                glBindTexture(GL_TEXTURE_2D, self.renderer.texture_manager.textures[rect.texture])
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
            if not rect.angle == None:
                # Rotate around rect center
                glTranslatef(rect.width / 2, rect.height / 2, 0)
                glRotatef(math.degrees(rect.angle), 0, 0, 1)
                glTranslatef(-rect.width / 2, -rect.height / 2, 0)
            glScalef(rect.width, rect.height, 1)
            glDrawArrays(GL_QUADS, 0, 4)

        self.rects_to_render = []
