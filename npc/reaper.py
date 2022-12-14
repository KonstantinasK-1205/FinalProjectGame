from npc.npc import NPC
from settings import *
import random


class Reaper(NPC):
    def __init__(self, game, path='resources/sprites/npc/reaper/0.png', pos=(3, 3),
                 scale=0.6, shift=0.38, animation_time=180):
        super().__init__(game, path, pos, scale, shift, animation_time)

        # NPC base stats
        self.pain = False
        self.alive = True
        self.health = 240
        self.speed = 0.05
        self.damage = random.randint(21, 25)
        self.attack_dist = 1
        self.shoot_delay = 80
        self.bullet_lifetime = 150

        # NPC animation variables
        self.frame_counter = 0
        self.attack_images = self.get_images(self.path + '/attack')
        self.death_images = self.get_images(self.path + '/death')
        self.idle_images = self.get_images(self.path + '/idle')
        self.pain_images = self.get_images(self.path + '/pain')
        self.walk_images = self.get_images(self.path + '/walk')

        self.size = 20
        self.ray_cast_value = False
        self.player_search_trigger = False
        self.angle = 0
        self.current_time = 0
        self.previous_shot = 0
