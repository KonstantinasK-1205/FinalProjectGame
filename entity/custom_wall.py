import math

from sprites.sprite import Sprite
import random


class BreakableWall(Sprite):
    def __init__(self, game, pos):
        super().__init__(game, pos, [1, 1.5])
        self.game = game
        self.load_texture("resources/sprites/default.png")
        self.health = 150
        self.angle = 0
        self.angle_updated = False

    def draw(self):
        self.game.renderer.draw_sprite(self.x, self.y, self.z, 1, 1.5, self.texture_path, angle=self.angle)

    def update(self):
        super().update()

        # Breakable wall should be between 2 walls, try to find angle for it
        if not self.angle_updated:
            if self.game.map.is_wall(self.x, self.y - 1) and self.game.map.is_wall(self.x, self.y + 1):
                self.x = self.x
                self.y = self.y + 0.5
                self.angle = math.pi / 2
                texture = str(self.game.map.get_tile(self.x, self.y - 1))
            else:
                self.x = self.x + 0.5
                self.y = self.y
                self.angle = 0
                texture = str(self.game.map.get_tile(self.x + 1, self.y))
            self.load_texture("resources/textures/cracked_wall" + texture + ".png")
            self.angle_updated = True

        if self.health <= 0:
            self.delete = True

