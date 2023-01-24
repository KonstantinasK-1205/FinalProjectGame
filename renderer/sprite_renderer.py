from renderer.opengl import *
import math


class SpriteRenderer:
    see_tolerance = math.pi / 4

    def __init__(self, game, renderer):
        self.game = game
        self.renderer = renderer

        self.sprites_to_render = []

        self.renderer.load_vbo("sprite", [
            1, 0, -0.5, 0, 0,
            0, 0,  0.5, 0, 0,
            0, 1,  0.5, 1, 0,
            1, 1, -0.5, 1, 0
        ])
        self.load_sphere_vbo()

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

        self.renderer.load_vbo("sphere", data)

    def can_see(self, x, y, camera_pos, camera_angle):
        angle = (camera_angle[0] - math.atan2(y - camera_pos[1], x - camera_pos[0])) % math.tau
        return angle < SpriteRenderer.see_tolerance or angle > math.tau - SpriteRenderer.see_tolerance

    def draw(self):
        glDisable(GL_CULL_FACE)

        # Save camera position for quicker access
        camera_pos = self.renderer.camera_pos
        camera_angle = self.renderer.camera_angle

        # Objects must be sorted from farthest to closest for transparency to
        # work properly
        self.sprites_to_render = [o for o in self.sprites_to_render if self.can_see(o.x, o.y, camera_pos, camera_angle)]
        for o in self.sprites_to_render:
            o.__distance_from_camera = math.hypot(
                o.x - camera_pos[0],
                o.y - camera_pos[1],
                o.z - camera_pos[2]
            )
        self.sprites_to_render.sort(key=lambda o: o.__distance_from_camera, reverse=True)

        # It is faster to only rebind the buffer and reset the pointers if the
        # sprite VBO differs
        sphere_bound = False
        glBindBuffer(GL_ARRAY_BUFFER, self.renderer.vbo_manager.vbos["sprite"])
        glTexCoordPointer(2, GL_FLOAT, 5 * 4, ctypes.c_void_p(0))
        glVertexPointer(3, GL_FLOAT, 5 * 4, ctypes.c_void_p(2 * 4))

        last_texture = None
        glBindTexture(GL_TEXTURE_2D, 0)

        last_color = (255, 255, 255)
        glColor3ub(last_color[0], last_color[1], last_color[2])

        glDepthMask(GL_FALSE)

        for o in self.sprites_to_render:
            if not o.texture == last_texture:
                last_texture = o.texture
                if o.texture == None:
                    glBindTexture(GL_TEXTURE_2D, 0)
                else:
                    glBindTexture(GL_TEXTURE_2D, self.renderer.texture_manager.textures[o.texture])

            if not o.color == last_color:
                last_color = o.color
                if len(o.color) == 3:
                    glColor3ub(o.color[0], o.color[1], o.color[2])
                elif len(o.color) == 4:
                    glColor4ub(o.color[0], o.color[1], o.color[2], o.color[3])

            glPushMatrix()

            glTranslatef(o.x, o.z, o.y)
            if o.angle == None:
                glRotatef(-math.degrees(camera_angle[0]) + 90, 0, 1, 0)
            else:
                glRotatef(math.degrees(o.angle), 0, 1, 0)
            glScalef(o.width, o.height, 1)

            if o.sphere:
                if not sphere_bound:
                    sphere_bound = True
                    glBindBuffer(GL_ARRAY_BUFFER, self.renderer.vbo_manager.vbos["sphere"])
                    glTexCoordPointer(2, GL_FLOAT, 5 * 4, ctypes.c_void_p(0))
                    glVertexPointer(3, GL_FLOAT, 5 * 4, ctypes.c_void_p(2 * 4))
                glDrawArrays(GL_QUADS, 0, self.sphere_vbo_verts)
            else:
                if sphere_bound:
                    sphere_bound = False
                    glBindBuffer(GL_ARRAY_BUFFER, self.renderer.vbo_manager.vbos["sprite"])
                    glTexCoordPointer(2, GL_FLOAT, 5 * 4, ctypes.c_void_p(0))
                    glVertexPointer(3, GL_FLOAT, 5 * 4, ctypes.c_void_p(2 * 4))
                glDrawArrays(GL_QUADS, 0, 4)

            glPopMatrix()

        glDepthMask(GL_TRUE)

        self.sprites_to_render = []

    class Sprite:
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
