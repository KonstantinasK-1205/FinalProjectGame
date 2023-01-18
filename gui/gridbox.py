from gui.component import *


class GridBox(Component):
    def __init__(self, game):
        super().__init__(game)
        self.tile_size = (48, 48)
        self.rows = 10
        self.column_offset = 0
        self.row_offset = 0
        self.wrap = False
        self.draw_grid = True

        self.game.renderer.load_texture_from_file("resources/textures/grid.png")

    def draw(self):
        super().draw()

        if not self.visible or not self.draw_grid:
            return

        rows = int(self.size[0] // self.tile_size[0])
        cols = int(self.size[1] // self.tile_size[1])
        for i in range(cols):
            for j in range(rows):
                self.game.renderer.draw_rect(
                    self.position[0] + j * self.tile_size[0],
                    self.position[1] + i * self.tile_size[0],
                    self.tile_size[0],
                    self.tile_size[1],
                    "resources/textures/grid.png",
                    (255, 255, 255, 64)
                )

    def layout(self):
        if self.wrap:
            rows = self.size[0] // self.tile_size[0]
        else:
            rows = self.rows
        cols = self.size[1] // self.tile_size[1]

        tile_pos = (0, 0)
        for c in self.children:
            c.position = (
                self.position[0] + (tile_pos[0] - int(self.column_offset)) * self.tile_size[0],
                self.position[1] + (tile_pos[1] - int(self.row_offset)) * self.tile_size[1]
            )
            if c.flexible[0]:
                c.size = (self.tile_size[0], c.size[1])
            if c.flexible[1]:
                c.size = (c.size[0], self.tile_size[0])

            # Make sure element children are also updated
            c.layout()

            tile_pos = (tile_pos[0] + 1, tile_pos[1])
            if tile_pos[0] >= rows:
                tile_pos = (0, tile_pos[1] + 1)
            if tile_pos[1] >= cols:
                pass
