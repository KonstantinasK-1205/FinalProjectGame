from npc.npc import NPC
from settings import *
import random
import pygame as pg


class Battlelord(NPC):
    def __init__(self, game, pos, scale=[0.6]):
        super().__init__(game, pos, scale)

        # Position and scale
        self.width = 0.8
        self.height = 0.9

        # Primary stats
        self.health = 1800
        self.speed = 0.003

        # Attack stats
        self.damage = random.randint(10, 25)
        self.attack_distance = 8
        self.bullet_lifetime = 1500

        self.sensing_range = 60  # 0.5   = 1 grid block
        self.reaction_time = 250

        # Sound variables
        self.sfx_attack = "Battlelord attack"
        self.sfx_pain = "Battlelord pain"
        self.sfx_death = "Battlelord death"

        # Animation variables
        self.spritesheet = self.load_image("resources/sprites/npc/Battlelord_Spritesheet.png")
        self.current_animation = "Idle"
        self.animations = {
            "Idle": {
                "Frames": self.images_at("Battlelord_Idle",
                                         [(0, 0, 128, 128)]),
                "Counter": 0,
                "Animation Speed": 180,
                "Animation Completed": False,
            },
            "Walk": {
                "Frames": self.images_at("Battlelord_Walk",
                                         [(0, 128, 128, 128),
                                         (128, 128, 128, 128)]),
                "Counter": 0,
                "Animation Speed": 180,
                "Animation Completed": False,
            },
            "Attack": {
                "Frames": self.images_at("Battlelord_Attack",
                                         [(0, 256, 128, 128),
                                         (128, 256, 128, 128)]),
                "Counter": 0,
                "Animation Speed": 200,
                "Attack Speed": 400,
                "Animation Completed": False,
            },
            "Pain": {
                "Frames": self.images_at("Battlelord_Pain",
                                         [(0, 384, 128, 128)]),
                "Counter": 0,
                "Animation Speed": 300,
                "Animation Completed": False,
            },
            "Death": {
                "Frames": self.images_at("Battlelord_Death",
                                         [(0, 512, 128, 128),
                                          (128, 512, 128, 128),
                                          (256, 512, 128, 128),
                                          (384, 512, 128, 128),
                                          (512, 512, 128, 128),
                                          (640, 512, 128, 128)]),
                "Counter": 0,
                "Animation Speed": 200,
                "Animation Completed": False,
            }
        }
