from renderer.opengl import *


class MapRenderer:
    def __init__(self, game, renderer):
        self.game = game
        self.renderer = renderer
        self.layers = []
        self.vbos_initialized = False

        renderer.load_texture_from_file("resources/textures/desert/floor_1.jpg", True, True)
        self.wall_textures = 4
        for i in range(1, self.wall_textures + 1):
            renderer.load_texture_from_file("resources/textures/desert/wall_" + str(i) + ".jpg", True, True)

    def update_vbos(self):
        # Separate layers are used to draw surfaces with different textures
        # Create a layer for the floor and each wall texture
        layer_data = []
        self.layers = []
        for i in range(self.wall_textures + 1):
            layer_data.append([])
            if i == 0:
                self.layers.append(MapRenderer.Layer("resources/textures/desert/floor_1.jpg", "map_layer_0", 0))
            else:
                self.layers.append(MapRenderer.Layer("resources/textures/desert/wall_" + str(i) + ".jpg", "map_layer_" + str(i), 0))

        for i in range(self.game.map.height):
            for j in range(self.game.map.width):
                # Skip wall tiles, instead add visible wall surfaces from an
                # empty tile
                if self.game.map.is_wall(j, i):
                    continue

                # Add floor vertices
                layer_data[0].extend([
                    0, 0, j + 0, 0, i + 1,
                    1, 0, j + 1, 0, i + 1,
                    1, 1, j + 1, 0, i + 0,
                    0, 1, j + 0, 0, i + 0
                ])
                self.layers[0].vbo_size += 4

                # Add visible wall vertices
                self.add_visible_wall(j - 1, i    , 0, layer_data)
                self.add_visible_wall(j + 1, i    , 1, layer_data)
                self.add_visible_wall(j    , i - 1, 2, layer_data)
                self.add_visible_wall(j    , i + 1, 3, layer_data)

        for i in range(self.wall_textures + 1):
            self.renderer.load_vbo(self.layers[i].vbo, layer_data[i])

        self.vbos_initialized = True

    def add_visible_wall(self, x, y, direction, layer_data):
        WALL_HEIGHT = 1.5

        tile = self.game.map.get_tile(x, y)
        if tile == 0:
            return

        if direction == 0:
            layer_data[tile].extend([
                1, 0          , x + 1, 0          , y + 0,
                1, WALL_HEIGHT, x + 1, WALL_HEIGHT, y + 0,
                0, WALL_HEIGHT, x + 1, WALL_HEIGHT, y + 1,
                0, 0          , x + 1, 0          , y + 1
            ])
        elif direction == 1:
            layer_data[tile].extend([
                0, 0          , x + 0, 0          , y + 0,
                1, 0          , x + 0, 0          , y + 1,
                1, WALL_HEIGHT, x + 0, WALL_HEIGHT, y + 1,
                0, WALL_HEIGHT, x + 0, WALL_HEIGHT, y + 0
            ])
        elif direction == 2:
            layer_data[tile].extend([
                0, 0          , x + 0, 0          , y + 1,
                1, 0          , x + 1, 0          , y + 1,
                1, WALL_HEIGHT, x + 1, WALL_HEIGHT, y + 1,
                0, WALL_HEIGHT, x + 0, WALL_HEIGHT, y + 1
            ])
        else:
            layer_data[tile].extend([
                1, 0          , x + 0, 0          , y + 0,
                1, WALL_HEIGHT, x + 0, WALL_HEIGHT, y + 0,
                0, WALL_HEIGHT, x + 1, WALL_HEIGHT, y + 0,
                0, 0          , x + 1, 0          , y + 0
            ])
        self.layers[tile].vbo_size += 4

    def draw(self):
        for l in self.layers:
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
