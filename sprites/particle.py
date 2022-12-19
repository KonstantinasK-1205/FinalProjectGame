from sprites.sprite import Sprite
import random
import math
from collision import *


class Particle(Sprite):
    def __init__(self, game, pos, collided_tile):
        super().__init__(game, pos, 0.05)

        # Right now the player shoots bullets out of their legs, so account for
        # player arm height
        self.z += 0.5

        self.dx = 0
        self.dy = 0
        self.dz = 0

        self.dx = random.uniform(-0.01, 0.01)
        self.dy = random.uniform(-0.01, 0.01)
        self.dz = random.uniform(-0.001, 0.001)

        # Try to find collided wall texture
        if collided_tile > 0:
            self.texture_path = "resources/textures/wall" + str(collided_tile) + ".png"

    def update(self):
        super().update()

        # Keep collision radius same as bullet to avoid colliding at a position
        # where the bullet was not
        res = resolve_collision(self.x, self.y, self.dx, self.dy, self.game.map, 0.01)
        self.x = res.x
        self.y = res.y
        if res.collided:
            self.dx = -self.dx
            self.dy = -self.dy

        # Gravity
        self.dz -= 0.00001 * self.game.dt
        self.z += self.dz * self.game.dt

    def draw(self):
        if self.texture_path:
            self.game.renderer.draw_sprite(self.x, self.y, self.z, self.width, self.height, self.texture_path)
        else:
            self.game.renderer.draw_sprite(self.x, self.y, self.z, self.width, self.height, None, (32, 32, 32))
