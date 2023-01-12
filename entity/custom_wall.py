import math
import pygame as pg
import random
from sprites.sprite import Sprite
from sprites.particle import Particle


class BreakableWall(Sprite):
    def __init__(self, game, pos):
        super().__init__(game, pos, [1, 1.5])
        self.game = game
        self.size = [1, 1.5]
        path = "resources/sprites/default.png"
        self.sprite = game.sprite_manager.load_single_image("Breakable Wall 0", path)[0]
        self.health = 150
        self.angle = 0
        self.angle_updated = False

    def draw(self):
        self.game.renderer.draw_sprite(self.pos, self.size, self.sprite, angle=self.angle)

    def update(self):
        super().update()

        # Breakable wall should be between 2 walls, try to find angle for it
        if not self.angle_updated:
            if self.game.map.is_wall(self.pos[0], self.pos[1] - 1) and self.game.map.is_wall(self.pos[0],
                                                                                             self.pos[1] + 1):
                self.pos[0] = self.pos[0]
                self.pos[1] = self.pos[1] + 0.5
                self.angle = math.pi / 2
                texture = str(self.game.map.get_wall(self.pos[0], self.pos[1] - 1))
            else:
                self.pos[0] = self.pos[0] + 0.5
                self.pos[1] = self.pos[1]
                self.angle = 0
                texture = str(self.game.map.get_wall(self.pos[0] + 1, self.pos[1]))
            # Load wall and crack texture and blend them
            wall = pg.image.load("resources/textures/desert/wall_" + texture + ".jpg")
            wall.blit(pg.image.load("resources/textures/crack.png"), (0, 0), special_flags=pg.BLEND_SUB)
            # Save texture and render it
            self.game.renderer.load_texture_from_surface("Crack_" + texture, wall)
            self.sprite = "Crack_" + texture
            self.angle_updated = True

        if self.health <= 0:
            for n in range(25):
                width = random.uniform(0.05, 0.3)
                height = random.uniform(0.05, 0.3)
                self.game.object_handler.add_sprite(Particle(self.game,
                                                             self.pos,
                                                             [width, height]))
            self.delete = True
