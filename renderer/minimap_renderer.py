from renderer.opengl import *
import math


class MinimapRenderer:
    def __init__(self, game, renderer):
        self.game = game
        self.renderer = renderer
        self.x = 0
        self.y = 0
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
        for i in range(self.game.map.height):
            for j in range(self.game.map.width):
                if not self.game.map.is_wall(j, i):
                    continue

                data.extend([
                    j + 1, i + 1,
                    j + 1, i + 0,
                    j + 0, i + 0,
                    j + 0, i + 1
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
                    cx * MinimapRenderer.Chunk.WIDTH,
                    cy * MinimapRenderer.Chunk.HEIGHT,
                    vbo,
                    vbo_size
                ))

    def draw(self):
        if not self.vbos_initialized:
            return

        glBindTexture(GL_TEXTURE_2D, 0)

        self.draw_walls()
        self.draw_unvisited()
        self.draw_dots()

    def draw_walls(self):
        glBindBuffer(GL_ARRAY_BUFFER, self.renderer.vbos["minimap_wall"])
        glVertexPointer(2, GL_FLOAT, 0, ctypes.c_void_p(0))

        glColor4f(0, 0, 0, 0.9)

        glLoadIdentity()
        glTranslatef(self.x, self.y, 0)
        glScalef(self.tile_size, self.tile_size, 1)

        glDrawArrays(GL_QUADS, 0, self.wall_vbo_size)

    def draw_unvisited(self):
        glColor4f(0, 0, 0, 0.4)

        for c in self.unvisited_chunks:
            if c.is_valid():
                glBindBuffer(GL_ARRAY_BUFFER, self.renderer.vbos[c.vbo])
                glVertexPointer(2, GL_FLOAT, 0, ctypes.c_void_p(0))

                glLoadIdentity()
                glTranslatef(self.x, self.y, 0)
                glScalef(self.tile_size, self.tile_size, 1)

                glDrawArrays(GL_QUADS, 0, c.vbo_size)
            else:
                glBindBuffer(GL_ARRAY_BUFFER, self.renderer.vbos["minimap_tile"])
                glVertexPointer(2, GL_FLOAT, 0, ctypes.c_void_p(0))

                c.draw_tiles(self.x, self.y, self.tile_size)

    def draw_dots(self):
        glBindBuffer(GL_ARRAY_BUFFER, self.renderer.vbos["minimap_dot"])
        glTexCoordPointer(2, GL_FLOAT, 4 * 4, ctypes.c_void_p(0))
        glVertexPointer(2, GL_FLOAT, 4 * 4, ctypes.c_void_p(2 * 4))

        self.draw_enemies()
        self.draw_pickups()
        self.draw_player()

    def draw_enemies(self):
        size = self.tile_size / 3

        glColor3f(1, 0, 0)
        for enemy in self.game.object_handler.alive_npc_list:
            if not self.game.map.is_visited(enemy.x, enemy.y):
                continue

            glLoadIdentity()
            glTranslatef(
                self.x + enemy.x * self.tile_size,
                self.y + enemy.y * self.tile_size,
                0
            )
            glScalef(size, size, 1)
            glDrawArrays(GL_QUADS, 0, 4)

    def draw_pickups(self):
        size = self.tile_size / 3

        for pickup in self.game.object_handler.pickup_list:
            if not self.game.map.is_visited(pickup.x, pickup.y):
                continue
            if pickup.type == "Ammo":
                glColor3f(1, 1, 0.8)
            elif pickup.type == "Weapon":
                glColor3f(0, 0.8, 0.8)
            else:
                glColor3f(0, 0, 1)

            glLoadIdentity()
            glTranslatef(
                self.x + pickup.x * self.tile_size,
                self.y + pickup.y * self.tile_size,
                0
            )
            glScalef(size, size, 1)
            glDrawArrays(GL_QUADS, 0, 4)

    def draw_player(self):
        size = self.tile_size * 4

        glBindTexture(GL_TEXTURE_2D, self.renderer.textures["resources/icons/minimap_player.png"])

        glColor3f(1, 1, 1)

        glLoadIdentity()
        glTranslatef(
            self.x + self.game.player.x * self.tile_size,
            self.y + self.game.player.y * self.tile_size,
            0
        )
        glRotatef(math.degrees(self.game.player.angle), 0, 0, 1)
        glScalef(size, size, 1)
        glDrawArrays(GL_QUADS, 0, 4)


    class Chunk:
        WIDTH = 8
        HEIGHT = 8

        def __init__(self, game, x, y, vbo, vbo_size):
            self.game = game
            self.x = x
            self.y = y
            self.vbo = vbo
            self.vbo_size = vbo_size
            self.valid = True

        def is_valid(self):
            # Do not recheck if this chunk was already invalidated, as an
            # already visitd chunk will not be unvisited
            if not self.valid:
                return False

            for i in range(self.y, self.y + MinimapRenderer.Chunk.HEIGHT):
                for j in range(self.x, self.x + MinimapRenderer.Chunk.WIDTH):
                    if self.game.map.is_visited(j, i):
                        self.valid = False
                        return False
            return True

        def draw_tiles(self, x, y, tile_size):
            for i in range(self.y, self.y + MinimapRenderer.Chunk.HEIGHT):
                for j in range(self.x, self.x + MinimapRenderer.Chunk.WIDTH):
                    if self.game.map.is_wall(j, i) or self.game.map.is_visited(j, i):
                        continue

                    glLoadIdentity()
                    glTranslatef(x + j * tile_size, y + i * tile_size, 0)
                    glScalef(tile_size, tile_size, 1)
                    glDrawArrays(GL_QUADS, 0, self.vbo_size)
