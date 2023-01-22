from renderer.opengl import *
import math


class MinimapRenderer:
    def __init__(self, game, renderer):
        self.game = game
        self.renderer = renderer
        self.pos = [0, 0, 0]
        self.tile_size = 0
        self.wall_vbo_size = None
        self.unvisited_chunks = []
        self.vbos_initialized = False

        renderer.load_vbo("minimap_tile", [
            1, 1,
            1, 0,
            0, 0,
            0, 1
        ])

        renderer.load_vbo("minimap_dot", [
            1, 0,  0.5,  0.5,
            1, 1,  0.5, -0.5,
            0, 1, -0.5, -0.5,
            0, 0, -0.5,  0.5
        ])

        renderer.load_texture_from_file("resources/icons/minimap_player.png")

    def update_vbos(self):
        self.update_wall_vbo()
        self.update_unvisited_chunks()
        self.vbos_initialized = True

    def update_wall_vbo(self):
        self.wall_vbo_size = 0

        data = []
        for y in range(self.game.map.height):
            for x in range(self.game.map.width):
                if not self.game.map.is_wall(x, y):
                    continue

                data.extend([
                    x + 1, y + 1,
                    x + 1, y + 0,
                    x + 0, y + 0,
                    x + 0, y + 1
                ])
                self.wall_vbo_size += 4

        self.renderer.load_vbo("minimap_wall", data)

    def update_unvisited_chunks(self):
        self.unvisited_chunks = []
        for cy in range(self.game.map.height // MinimapRenderer.Chunk.HEIGHT + 1):
            for cx in range(self.game.map.width // MinimapRenderer.Chunk.WIDTH + 1):
                data = []
                vbo = "minimap_chunk_" + str(cx) + "_" + str(cy)
                vbo_size = 0

                for i in range(cy * MinimapRenderer.Chunk.HEIGHT, (cy + 1) * MinimapRenderer.Chunk.HEIGHT):
                    for j in range(cx * MinimapRenderer.Chunk.WIDTH, (cx + 1) * MinimapRenderer.Chunk.WIDTH):
                        if self.game.map.is_wall(j, i):
                            continue

                        data.extend([
                            j + 1, i + 1,
                            j + 1, i + 0,
                            j + 0, i + 0,
                            j + 0, i + 1
                        ])
                        vbo_size += 4

                self.renderer.load_vbo(vbo, data)
                self.unvisited_chunks.append(MinimapRenderer.Chunk(
                    self.game,
                    [cx * MinimapRenderer.Chunk.WIDTH, cy * MinimapRenderer.Chunk.HEIGHT, 0],
                    vbo,
                    vbo_size
                ))

    def draw(self):
        if not self.vbos_initialized:
            return

        glDisable(GL_DEPTH_TEST)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, self.game.width, self.game.height, 0, 0, 100)

        glMatrixMode(GL_MODELVIEW)

        glBindTexture(GL_TEXTURE_2D, 0)

        self.draw_walls()
        self.draw_unvisited()
        self.draw_dots()

    def draw_walls(self):
        glBindBuffer(GL_ARRAY_BUFFER, self.renderer.vbo_manager.vbos["minimap_wall"])
        glVertexPointer(2, GL_FLOAT, 0, ctypes.c_void_p(0))

        glColor4f(0, 0, 0, 0.9)

        glLoadIdentity()
        glTranslatef(self.pos[0], self.pos[1], self.pos[2])
        glScalef(self.tile_size, self.tile_size, 1)

        glDrawArrays(GL_QUADS, 0, self.wall_vbo_size)

    def draw_unvisited(self):
        glColor4f(0, 0, 0, 0.9)

        for c in self.unvisited_chunks:
            if c.is_valid():
                glBindBuffer(GL_ARRAY_BUFFER, self.renderer.vbo_manager.vbos[c.vbo])
                glVertexPointer(2, GL_FLOAT, 0, ctypes.c_void_p(0))

                glLoadIdentity()
                glTranslatef(self.pos[0], self.pos[1], self.pos[2])
                glScalef(self.tile_size, self.tile_size, 1)

                glDrawArrays(GL_QUADS, 0, c.vbo_size)
            else:
                glBindBuffer(GL_ARRAY_BUFFER, self.renderer.vbo_manager.vbos["minimap_tile"])
                glVertexPointer(2, GL_FLOAT, 0, ctypes.c_void_p(0))

                c.draw_tiles(self.pos, self.tile_size)

    def draw_dots(self):
        glBindBuffer(GL_ARRAY_BUFFER, self.renderer.vbo_manager.vbos["minimap_dot"])
        glTexCoordPointer(2, GL_FLOAT, 4 * 4, ctypes.c_void_p(0))
        glVertexPointer(2, GL_FLOAT, 4 * 4, ctypes.c_void_p(2 * 4))

        self.draw_enemies()
        self.draw_pickups()
        self.draw_player()

    def draw_enemies(self):
        size = self.tile_size / 3

        glColor3f(1, 0, 0)
        for enemy in self.game.object_handler.alive_npc_list:
            if not self.game.map.is_visited(enemy.pos[0], enemy.pos[1]):
                continue

            glLoadIdentity()
            glTranslatef(
                self.pos[0] + enemy.pos[0] * self.tile_size,
                self.pos[1] + enemy.pos[1] * self.tile_size,
                0
            )
            glScalef(size, size, 1)
            glDrawArrays(GL_QUADS, 0, 4)

    def draw_pickups(self):
        size = self.tile_size / 3

        for pickup in self.game.object_handler.pickup_list:
            if not self.game.map.is_visited(pickup.pos[0], pickup.pos[1]):
                continue

            if pickup.type == "Ammo":
                glColor3f(1, 1, 0.8)
            elif pickup.type == "Weapon":
                glColor3f(0, 0.8, 0.8)
            else:
                glColor3f(0, 0, 1)

            glLoadIdentity()
            glTranslatef(
                self.pos[0] + pickup.pos[0] * self.tile_size,
                self.pos[1] + pickup.pos[1] * self.tile_size,
                0
            )
            glScalef(size, size, 1)
            glDrawArrays(GL_QUADS, 0, 4)

    def draw_player(self):
        size = self.tile_size * 4

        glBindTexture(GL_TEXTURE_2D, self.renderer.texture_manager.textures["resources/icons/minimap_player.png"])

        glColor3f(1, 1, 1)

        glLoadIdentity()
        glTranslatef(
            self.pos[0] + self.game.player.pos[0] * self.tile_size,
            self.pos[1] + self.game.player.pos[1] * self.tile_size,
            0
        )
        glRotatef(math.degrees(self.game.player.angle[0]), 0, 0, 1)
        glScalef(size, size, 1)
        glDrawArrays(GL_QUADS, 0, 4)

    class Chunk:
        WIDTH = 8
        HEIGHT = 8

        def __init__(self, game, pos, vbo, vbo_size):
            self.game = game
            self.pos = pos
            self.vbo = vbo
            self.vbo_size = vbo_size
            self.valid = True

        def is_valid(self):
            # Do not recheck if this chunk was already invalidated, as an
            # already visited chunk will not be unvisited
            if not self.valid:
                return False

            for y in range(self.pos[1], self.pos[1] + MinimapRenderer.Chunk.HEIGHT):
                for x in range(self.pos[0], self.pos[0] + MinimapRenderer.Chunk.WIDTH):
                    if self.game.map.is_visited(x, y):
                        self.valid = False
                        return False
            return True

        def draw_tiles(self, pos, tile_size):
            for y in range(self.pos[1], self.pos[1] + MinimapRenderer.Chunk.HEIGHT):
                for x in range(self.pos[0], self.pos[0] + MinimapRenderer.Chunk.WIDTH):
                    if self.game.map.is_wall(x, y) or self.game.map.is_visited(x, y):
                        continue

                    glLoadIdentity()
                    glTranslatef(pos[0] + x * tile_size, pos[1] + y * tile_size, 0)
                    glScalef(tile_size, tile_size, 1)
                    glDrawArrays(GL_QUADS, 0, self.vbo_size)
