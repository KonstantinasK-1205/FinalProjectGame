from npc.npc import NPC
from settings import *
import random


class Soldier(NPC):
    def __init__(self, game, path='resources/sprites/npc/soldier/0.png', pos=(3, 3),
                 scale=0.6, shift=0.38, animation_time=180):
        super().__init__(game, path, pos, scale, shift, animation_time)

        # NPC base stats
        self.pain = False
        self.alive = True
        self.health = 100
        self.speed = 0.03
        self.damage = random.randint(15, 20)
        self.attack_dist = random.randint(3, 5)
        self.shoot_delay = 250
        self.bullet_lifetime = 3000

        self.size = 50
        self.ray_cast_value = False
        self.player_search_trigger = False
        self.angle = 0
        self.current_time = 0
        self.previous_shot = 0
