from renderer.opengl import *


class MapRenderer:
    def __init__(self, game, renderer):
        self.game = game
        self.renderer = renderer

        self.floor_layers = []
        self.wall_layers = []

        self.vbos_initialized = False

        self.floor_textures = 3
        self.wall_textures = 4
        for i in range(1, self.floor_textures + 1):
            renderer.load_texture_from_file("resources/textures/desert/floor_" + str(i) + ".jpg", True, True)
        for i in range(1, self.wall_textures + 1):
            renderer.load_texture_from_file("resources/textures/desert/wall_" + str(i) + ".jpg", True, True)

    def update_vbos(self):
        # Separate layers are used to draw surfaces with different textures
        # Create a layer for each floor and wall texture
        self.floor_layers = []
        self.wall_layers = []
        floor_layer_data = []
        wall_layer_data = []
        for i in range(1, self.floor_textures + 1):
            floor_layer_data.append([])
            self.floor_layers.append(MapRenderer.Layer("resources/textures/desert/floor_" + str(i) + ".jpg", "map_floor_" + str(i), 0))
        for i in range(1, self.wall_textures + 1):
            wall_layer_data.append([])
            self.wall_layers.append(MapRenderer.Layer("resources/textures/desert/wall_" + str(i) + ".jpg", "map_wall_" + str(i), 0))

        for i in range(self.game.map.height):
            for j in range(self.game.map.width):
                # Skip wall tiles, instead add visible wall surfaces from an
                # empty tile
                if self.game.map.is_wall(j, i):
                    continue

                # Add visible wall vertices
                self.add_visible_wall(j - 1, i    , 0, wall_layer_data)
                self.add_visible_wall(j + 1, i    , 1, wall_layer_data)
                self.add_visible_wall(j    , i - 1, 2, wall_layer_data)
                self.add_visible_wall(j    , i + 1, 3, wall_layer_data)

                # Add floor vertices
                floor = self.game.map.get_floor(j, i)
                if floor > 0:
                    layer = floor - 1

                    floor_layer_data[layer].extend([
                        0, 0, j + 0, 0, i + 1,
                        1, 0, j + 1, 0, i + 1,
                        1, 1, j + 1, 0, i + 0,
                        0, 1, j + 0, 0, i + 0
                    ])
                    self.floor_layers[layer].vbo_size += 4

        for i in range(self.floor_textures):
            self.renderer.load_vbo(self.floor_layers[i].vbo, floor_layer_data[i])
        for i in range(self.wall_textures):
            self.renderer.load_vbo(self.wall_layers[i].vbo, wall_layer_data[i])

        self.vbos_initialized = True

    def add_visible_wall(self, x, y, direction, layer_data):
        WALL_HEIGHT = 1.5

        layer = self.game.map.get_wall(x, y) - 1
        if layer < 0:
            return

        if direction == 0:
            layer_data[layer].extend([
                1, 0, x + 1, 0          , y + 0,
                1, 1, x + 1, WALL_HEIGHT, y + 0,
                0, 1, x + 1, WALL_HEIGHT, y + 1,
                0, 0, x + 1, 0          , y + 1
            ])
        elif direction == 1:
            layer_data[layer].extend([
                0, 0, x + 0, 0          , y + 0,
                1, 0, x + 0, 0          , y + 1,
                1, 1, x + 0, WALL_HEIGHT, y + 1,
                0, 1, x + 0, WALL_HEIGHT, y + 0
            ])
        elif direction == 2:
            layer_data[layer].extend([
                0, 0, x + 0, 0          , y + 1,
                1, 0, x + 1, 0          , y + 1,
                1, 1, x + 1, WALL_HEIGHT, y + 1,
                0, 1, x + 0, WALL_HEIGHT, y + 1
            ])
        else:
            layer_data[layer].extend([
                1, 0, x + 0, 0          , y + 0,
                1, 1, x + 0, WALL_HEIGHT, y + 0,
                0, 1, x + 1, WALL_HEIGHT, y + 0,
                0, 0, x + 1, 0          , y + 0
            ])
        self.wall_layers[layer].vbo_size += 4

    def draw(self):
        for l in self.floor_layers:
            glBindTexture(GL_TEXTURE_2D, self.renderer.texture_manager.textures[l.texture])

            glBindBuffer(GL_ARRAY_BUFFER, self.renderer.vbo_manager.vbos[l.vbo])
            glTexCoordPointer(2, GL_FLOAT, 5 * 4, ctypes.c_void_p(0))
            glVertexPointer(3, GL_FLOAT, 5 * 4, ctypes.c_void_p(2 * 4))

            glDrawArrays(GL_QUADS, 0, l.vbo_size)

        for l in self.wall_layers:
            glBindTexture(GL_TEXTURE_2D, self.renderer.texture_manager.textures[l.texture])

            glBindBuffer(GL_ARRAY_BUFFER, self.renderer.vbo_manager.vbos[l.vbo])
            glTexCoordPointer(2, GL_FLOAT, 5 * 4, ctypes.c_void_p(0))
            glVertexPointer(3, GL_FLOAT, 5 * 4, ctypes.c_void_p(2 * 4))

            glDrawArrays(GL_QUADS, 0, l.vbo_size)

    class Layer:
        def __init__(self, texture, vbo, vbo_size):
            self.texture = texture
            self.vbo = vbo
            self.vbo_size = vbo_size
