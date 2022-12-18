from npc.npc import NPC
from settings import *
import random
import pygame as pg


class Soldier(NPC):
    def __init__(self, game, pos, scale=0.6):
        super().__init__(game, pos, scale)

        self.width = 0.6
        self.height = 0.6

        # NPC base stats
        self.health = 100
        self.speed = 0.002
        self.damage = random.randint(15, 20)
        self.attack_dist = random.randint(3, 5)
        self.shoot_delay = 250
        self.bullet_lifetime = 600

        # NPC animation variables
        self.spritesheet = pg.image.load("resources/sprites/npc/Soldier_Spritesheet.png").convert_alpha()
        self.current_animation = "Idle"
        self.animations = {
            "Idle": {
                "Frames": self.images_at("Soldier_Idle",
                                         [(0, 0, 64, 64)]),
                "Counter": 0,
                "Animation Speed": 180,
                "Animation Completed": False,
            },
            "Walk": {
                "Frames": self.images_at("Soldier_Walk",
                                         [(0, 64, 64, 64),
                                          (64, 64, 64, 64),
                                          (128, 64, 64, 64),
                                          (192, 64, 64, 64)]),
                "Counter": 0,
                "Animation Speed": 180,
                "Animation Completed": False,
            },
            "Attack": {
                "Frames": self.images_at("Soldier_Attack",
                                         [(0, 256, 64, 64),
                                          (64, 256, 64, 64)]),
                "Counter": 0,
                "Animation Speed": 400,
                "Attack Speed": 800,
                "Animation Completed": False,
            },
            "Pain": {
                "Frames": self.images_at("Soldier_Pain",
                                         [(0, 320, 64, 64)]),
                "Counter": 0,
                "Animation Speed": 300,
                "Animation Completed": False,
            },
            "Death": {
                "Frames": self.images_at("Soldier_Death",
                                         [(0, 384, 64, 64),
                                          (64, 384, 64, 64),
                                          (128, 384, 64, 64),
                                          (192, 384, 64, 64),
                                          (256, 384, 64, 64),
                                          (320, 384, 64, 64)]),
                "Counter": 0,
                "Animation Speed": 120,
                "Animation Completed": False,
            }
        }
