from entity.npc.enemies.pinky import Pinky
from entity.npc.enemies.reaper import Reaper
from entity.npc.enemies.soldier import Soldier
from entity.npc.enemies.zombie import *
from sprites.sprite import Sprite
import pygame as pg
import random


class ZombieSpawn(Sprite):
    def __init__(self, game, pos):
        super().__init__(game, pos, [0.0001])
        game.sprite_manager.load_single_image("Empty", "resources/sprites/empty.png")
        self.sprite = game.sprite_manager.get_sprite("Empty")
        self.pos = pos
        self.last_spawned = 0
        self.next_spawn = random.randrange(15000, 30000)

    def update(self):
        current_time = pg.time.get_ticks()
        if current_time - self.last_spawned > self.next_spawn:
            self.game.object_handler.add_npc(Zombie(self.game, self.pos))
            self.next_spawn = random.randrange(15000, 30000)
            self.last_spawned = pg.time.get_ticks()


class Corpse:
    def __init__(self, game, pos):
        handler = game.object_handler
        r = random.randint(0, 3)
        if r == 0:
            handler.add_npc(Zombie(game, pos, False))
        elif r == 1:
            handler.add_npc(Soldier(game, pos, False))
        elif r == 2:
            handler.add_npc(Pinky(game, pos, False))
        elif r == 3:
            handler.add_npc(Reaper(game, pos, False))
