from renderer.opengl import *
import os


class MapRenderer:
    def __init__(self, game, renderer):
        self.game = game
        self.renderer = renderer

        # Separate layers are used to draw surfaces with different textures
        self.layers = {}

        for folder, subdirs, files in os.walk("resources/textures"):
            for filename in files:
                if "floor_" in filename or "wall_" in filename:
                    renderer.load_texture_from_file(folder + "/" + filename, True, True)

    def update_vbos(self):
        self.layers = {}

        # VBO data is accumulated here until it's stored in the VBO
        layer_data = {}

        for i in range(self.game.map.height):
            for j in range(self.game.map.width):
                # Skip wall tiles, instead add visible wall surfaces from an
                # empty tile
                if self.game.map.is_wall(j, i):
                    continue

                # Add visible wall vertices
                self.add_visible_wall(j - 1, i    , 0, layer_data)
                self.add_visible_wall(j + 1, i    , 1, layer_data)
                self.add_visible_wall(j    , i - 1, 2, layer_data)
                self.add_visible_wall(j    , i + 1, 3, layer_data)

                # Add floor vertices
                floor = self.game.map.get_floor(j, i)
                if floor:
                    name = "desert/floor_" + str(floor) + ".jpg"
                    if not name in layer_data:
                        self.layers[name] = MapRenderer.Layer(
                            "resources/textures/" + name,
                            "map_layer_" + name,
                            0
                        )
                        layer_data[name] = []

                    layer_data[name].extend([
                        0, 0, j + 0, 0, i + 1,
                        1, 0, j + 1, 0, i + 1,
                        1, 1, j + 1, 0, i + 0,
                        0, 1, j + 0, 0, i + 0
                    ])
                    self.layers[name].vbo_size += 4

        for k in self.layers:
            self.renderer.load_vbo(self.layers[k].vbo, layer_data[k])

    def add_visible_wall(self, x, y, direction, layer_data):
        wall_height = 1.5

        wall = self.game.map.get_wall(x, y)
        if not wall:
            return

        name = "desert/wall_" + str(wall) + ".jpg"
        if not name in layer_data:
            self.layers[name] = MapRenderer.Layer(
                "resources/textures/" + name,
                "map_layer_" + name,
                0
            )
            layer_data[name] = []

        if direction == 0:
            layer_data[name].extend([
                1, 0, x + 1, 0          , y + 0,
                1, 1, x + 1, wall_height, y + 0,
                0, 1, x + 1, wall_height, y + 1,
                0, 0, x + 1, 0          , y + 1
            ])
        elif direction == 1:
            layer_data[name].extend([
                0, 0, x + 0, 0          , y + 0,
                1, 0, x + 0, 0          , y + 1,
                1, 1, x + 0, wall_height, y + 1,
                0, 1, x + 0, wall_height, y + 0
            ])
        elif direction == 2:
            layer_data[name].extend([
                0, 0, x + 0, 0          , y + 1,
                1, 0, x + 1, 0          , y + 1,
                1, 1, x + 1, wall_height, y + 1,
                0, 1, x + 0, wall_height, y + 1
            ])
        else:
            layer_data[name].extend([
                1, 0, x + 0, 0          , y + 0,
                1, 1, x + 0, wall_height, y + 0,
                0, 1, x + 1, wall_height, y + 0,
                0, 0, x + 1, 0          , y + 0
            ])
        self.layers[name].vbo_size += 4

    def draw(self):
        tm = self.renderer.texture_manager
        vm = self.renderer.vbo_manager

        for k in self.layers:
            l = self.layers[k]

            glBindTexture(GL_TEXTURE_2D, tm.textures[l.texture])

            glBindBuffer(GL_ARRAY_BUFFER, vm.vbos[l.vbo])
            glTexCoordPointer(2, GL_FLOAT, 5 * 4, ctypes.c_void_p(0))
            glVertexPointer(3, GL_FLOAT, 5 * 4, ctypes.c_void_p(2 * 4))

            glDrawArrays(GL_QUADS, 0, l.vbo_size)

    class Layer:
        def __init__(self, texture, vbo, vbo_size):
            self.texture = texture
            self.vbo = vbo
            self.vbo_size = vbo_size
