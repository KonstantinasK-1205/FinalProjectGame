from npc.npc import NPC
from settings import *
import random
import pygame as pg


class Pinky(NPC):
    def __init__(self, game, pos, scale=0.6):
        super().__init__(game, pos, scale)

        self.z = 0
        self.width = 0.6
        self.height = 0.6
        self.size = 5

        # NPC base stats
        self.health = 350
        self.speed = 0.003
        self.damage = random.randint(7, 11)
        self.attack_dist = 1
        self.shoot_delay = 80
        self.bullet_lifetime = 150
        self.damage_reduction = 180

        # NPC animation variables
        self.spritesheet = pg.image.load("resources/sprites/npc/Pinky_Spritesheet.png").convert_alpha()
        self.current_animation = "Idle"
        self.animations = {
            "Idle": {
                "Frames": self.images_at("Pinky_Idle",
                                         [(0, 0, 64, 64)]),
                "Counter": 0,
                "Animation Speed": 180,
                "Animation Completed": False,
            },
            "Walk": {
                "Frames": self.images_at("Pinky_Walk",
                                         [(0, 64, 64, 64),
                                         (64, 64, 64, 64),
                                         (128, 64, 64, 64)]),
                "Counter": 0,
                "Animation Speed": 120,
                "Animation Completed": False,
            },
            "Attack": {
                "Frames": self.images_at("Pinky_Attack",
                                         [(0, 256, 64, 64),
                                         (64, 256, 64, 64),
                                         (128, 256, 64, 64)]),
                "Counter": 0,
                "Animation Speed": 300,
                "Attack Speed": 900,
                "Animation Completed": False,
            },
            "Pain": {
                "Frames": self.images_at("Pinky_Pain",
                                         [(0, 320, 64, 64)]),
                "Counter": 0,
                "Animation Speed": 300,
                "Animation Completed": False,
            },
            "Death": {
                "Frames": self.images_at("Pinky_Death",
                                         [(0, 320, 64, 64),
                                          (64, 320, 64, 64),
                                          (128, 320, 64, 64),
                                          (192, 320, 64, 64),
                                          (256, 320, 64, 64)]),
                "Counter": 0,
                "Animation Speed": 120,
                "Animation Completed": False,
            },
            "Stomp": {
                "Frames": self.images_at("Pinky_Stomp",
                                         [(0, 384, 64, 64),
                                          (64, 384, 64, 64),
                                          (128, 384, 64, 64),
                                          (192, 384, 64, 64)]),
                "Counter": 0,
                "Animation Speed": 400,
                "Animation Completed": False,
            }
        }

        # NPC sound variables
        self.npc_pain = self.game.sound.npc_reaper_pain
        self.npc_death = self.game.sound.npc_reaper_death
        self.npc_attack = self.game.sound.npc_reaper_attack
        self.npc_teleportation = self.game.sound.npc_reaper_teleportation

    def update(self, dt):
        super().update(dt)

    def animate_stomp(self):
        animation = self.animations[self.current_animation]
        if animation["Animation Completed"] and animation["Counter"] < len(animation["Frames"]) - 1:
            animation["Counter"] += 1
            animation["Frames"].rotate(-1)
            self.texture_path = animation["Frames"][0]
