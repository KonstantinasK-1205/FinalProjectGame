from renderer.opengl import *
import math
from array import array


class VboManager:
    def __init__(self, game, renderer):
        self.game = game
        self.renderer = renderer
        self.vbos = {}

    def load_vbo(self, name, data):
        data_array = array("f", data)
        array_bytes = data_array.tobytes()

        # Is the GL VBO already created?
        if not name in self.vbos:
            vbo = glGenBuffers(1)
            self.vbos[name] = vbo

        glBindBuffer(GL_ARRAY_BUFFER, self.vbos[name])
        glBufferData(GL_ARRAY_BUFFER, len(array_bytes), array_bytes, GL_STATIC_DRAW)

    def load_sphere_vbo(self):
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
