from npc.npc import NPC
from settings import *
import random
import pygame as pg


class Zombie(NPC):
    def __init__(self, game, pos, scale=0.6):
        super().__init__(game, pos, scale)

        # Base stats
        self.health = random.randint(60, 110)
        self.speed = 0.0008

        # Attack stats
        self.damage = random.randint(15, 20)
        self.attack_distance = 1
        self.bullet_lifetime = 45

        # Sounds
        self.sfx_attack = "Zombie attack"
        self.sfx_pain = "Zombie pain"
        self.sfx_death = "Zombie death"

        # Animations
        self.spritesheet = self.load_image("resources/sprites/npc/Zombie_Spritesheet.png")
        self.current_animation = "Idle"
        self.animations = {
            "Idle": {
                "Frames": self.images_at("Zombie_Idle",
                                         [(0, 0, 64, 64)]),
                "Counter": 0,
                "Animation Speed": 180,
                "Animation Completed": False,
            },
            "Walk": {
                "Frames": self.images_at("Zombie_Walk",
                                         [(0, 64, 64, 64),
                                          (64, 64, 64, 64),
                                          (128, 64, 64, 64),
                                          (192, 64, 64, 64)]),
                "Counter": 0,
                "Animation Speed": 180,
                "Animation Completed": False,
            },
            "Attack": {
                "Frames": self.images_at("Zombie_Attack",
                                         [(0, 128, 64, 64),
                                          (64, 128, 64, 64),
                                          (128, 128, 64, 64)]),
                "Counter": 0,
                "Animation Speed": 100,
                "Attack Speed": 300,
                "Animation Completed": False,
            },
            "Pain": {
                "Frames": self.images_at("Zombie_Pain",
                                         [(0, 192, 64, 64)]),
                "Counter": 0,
                "Animation Speed": 300,
                "Animation Completed": False,
            },
            "Death": {
                "Frames": self.images_at("Zombie_Death",
                                         [(0, 256, 64, 64),
                                          (64, 256, 64, 64),
                                          (128, 256, 64, 64),
                                          (192, 256, 64, 64),
                                          (256, 256, 64, 64)]),
                "Counter": 0,
                "Animation Speed": 120,
                "Animation Completed": False,
            }
        }
