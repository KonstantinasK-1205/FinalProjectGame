from npc.npc import NPC
from settings import *
import random


class Soldier(NPC):
    def __init__(self, game, pos, scale=0.6):
        super().__init__(game, pos, scale)

        # NPC base stats
        self.pain = False
        self.alive = True
        self.health = 100
        self.speed = 0.03
        self.damage = random.randint(15, 20)
        self.attack_dist = random.randint(3, 5)
        self.shoot_delay = 250
        self.bullet_lifetime = 600

        self.size = 50
        self.ray_cast_value = False
        self.approaching_player = False
        self.angle = 0
        self.current_time = 0
        self.previous_shot = 0
