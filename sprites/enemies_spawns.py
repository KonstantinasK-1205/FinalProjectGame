from npc.soldier import *
from npc.zombie import *
from sprites.sprite import Sprite
import pygame as pg
import random


class ZombieSpawn(Sprite):
    def __init__(self, game, pos, scale=[0.0001]):
        super().__init__(game, pos, scale)
        self.load_texture("resources/sprites/pickups/ammo/pistol.png")
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
            self.game.map.enemy_amount += 1
