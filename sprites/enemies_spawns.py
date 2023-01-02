from npc.zombie import *
from sprites.sprite import Sprite
import pygame as pg
import random


class ZombieSpawn(Sprite):
    def __init__(self, game, pos):
        super().__init__(game, pos, [0.0001])
        game.sprite_manager.load_single_image("Empty", "resources/sprites/empty.png")
        self.texture_path = game.sprite_manager.get_sprite("Empty")
        self.pos = pos
        self.last_spawned = 0
        self.next_spawn = random.randrange(10000, 30000)

    def update(self):
        super().update()

        current_time = pg.time.get_ticks()
        if current_time - self.last_spawned > self.next_spawn:
            self.game.object_handler.add_npc(Zombie(self.game, self.pos))
            self.next_spawn = random.randrange(10000, 30000)
            self.last_spawned = pg.time.get_ticks()
