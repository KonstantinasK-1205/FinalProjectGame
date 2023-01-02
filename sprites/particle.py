from collision import *
from sprites.sprite import Sprite
import random


class Particle(Sprite):
    def __init__(self, game, pos, size, collided_tile=1):
        super().__init__(game, pos, [0.05])

        self.dx = 0
        self.dy = 0
        self.dz = 0

        self.dx = random.uniform(-0.0015, 0.0015)
        self.dy = random.uniform(-0.0015, 0.0015)
        self.dz = random.uniform(-0.002, 0.002)

        self.width = size[0]
        self.height = size[1]

        self.lifetime = 1

        # Try to find collided wall texture
        if collided_tile > 0:
            self.texture_path = "resources/textures/wall" + str(collided_tile) + ".png"

    def update(self):
        super().update()

        # Keep collision radius same as bullet to avoid colliding at a position
        # where the bullet was not
        res = resolve_collision(self.x, self.y, self.dx * self.game.dt, self.dy * self.game.dt, self.game.map, 0.01)
        self.x = res.x
        self.y = res.y
        if res.collided:
            self.dx = -self.dx
            self.dy = -self.dy

        # Gravity
        self.dz -= 0.00001 * self.game.dt
        self.z += self.dz * self.game.dt

        # If hit ground, apply friction and bounce up
        if self.z < 0:
            self.dx = self.dx / 2
            self.dy = self.dy / 2
            self.dz = -self.dz / 2
            self.z = 0

        # Lifetime counts seconds, dt is millisecond based, so divide by 1000
        # Only delete once reached -1 seconds to allow for a fade out
        self.lifetime -= self.game.dt / 1000
        if self.lifetime < -1:
            self.delete = True

    def draw(self):
        # Once lifetime reaches 0.-1, it will fade out
        a = min(255, 255 + self.lifetime * 255)
        if self.texture_path:
            self.game.renderer.draw_sphere(self.x, self.y, self.z, self.width,
                                           self.height, self.texture_path, (255, 255, 255, a))
        else:
            self.game.renderer.draw_sphere(self.x, self.y, self.z, self.width, self.height, None, (32, 32, 32, a))
