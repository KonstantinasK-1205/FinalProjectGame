from collision import *
from sprites.sprite import Sprite
import random


class Particle(Sprite):
    def __init__(self, game, pos, size, collided_tile=1):
        super().__init__(game, pos, [0.05])

        self.dir_pos = [random.uniform(-0.0015, 0.0015),
                        random.uniform(-0.0015, 0.0015),
                        random.uniform(-0.002, 0.002)]

        self.size = size
        self.lifetime = 1

        # Try to find collided wall texture
        if collided_tile > 0:
            self.sprite = "resources/textures/desert/wall_" + str(collided_tile) + ".jpg"

    def update(self):
        super().update()

        # Keep collision radius same as bullet to avoid colliding at a position
        # where the bullet was not
        res = resolve_collision(self.pos, self.dir_pos[0] * self.game.dt, self.dir_pos[1] * self.game.dt, self.game.map,
                                0.01)
        self.pos = res.pos
        if res.collided:
            self.dir_pos[0] = -self.dir_pos[0]
            self.dir_pos[1] = -self.dir_pos[1]

        # Gravity
        self.dir_pos[2] -= 0.00001 * self.game.dt
        self.pos[2] += self.dir_pos[2] * self.game.dt

        # If hit ground, apply friction and bounce up
        if self.pos[2] < 0:
            self.dir_pos = [self.dir_pos[0] / 2,
                            self.dir_pos[1] / 2,
                            -self.dir_pos[2] / 2]
            self.pos[2] = 0

        # Lifetime counts seconds, dt is millisecond based, so divide by 1000
        # Only delete once reached -1 seconds to allow for a fade out
        self.lifetime -= self.game.dt / 1000
        if self.lifetime < -1:
            self.delete = True

    def draw(self):
        # Once lifetime reaches 0.-1, it will fade out
        a = max(0, min(255, int(255 + self.lifetime * 255)))
        if self.sprite:
            self.game.renderer.draw_sphere(self.pos, self.size, self.sprite, (255, 255, 255, a))
        else:
            self.game.renderer.draw_sphere(self.pos, self.size, None, (32, 32, 32, a))
