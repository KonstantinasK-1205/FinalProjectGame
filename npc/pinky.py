from npc.npc import NPC
from settings import *
import random
import pygame as pg
from collision import *


class Pinky(NPC):
    def __init__(self, game, pos, scale=[0.6]):
        super().__init__(game, pos, scale)

        # Primary stats
        self.health = 250
        self.speed = 0.0025

        # Attack stats
        self.damage = random.randint(10, 14)
        self.attack_distance = 1
        self.bullet_lifetime = 35

        # Sounds
        self.sfx_attack = "Soldier attack"
        self.sfx_pain = "Soldier pain"
        self.sfx_death = "Soldier death"

        # Animation variables
        self.spritesheet = self.load_image("resources/sprites/npc/Pinky_Spritesheet.png")
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
                "Animation Speed": 150,
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

        # Dash ability ( dash away from bullet )
        self.is_dashing = False
        self.dodge_chance = 6
        self.dash_distance = 18
        self.dash_start_time = 0

    def movement(self):
        if self.is_dashing:
            res = resolve_collision(self.x, self.y, self.dx, self.dy, self.game.map, 0.15)
            self.x = res.x
            self.y = res.y
        else:
            super().movement()

    def update(self):
        super().update()
        elapsed_time = pg.time.get_ticks()
        distance_traveled = (elapsed_time - self.dash_start_time) * self.speed * self.game.dt
        if distance_traveled >= self.dash_distance:
            self.is_dashing = False

    def avoid_bullet(self):
        if random.randint(1, 10) > self.dodge_chance:
            self.dx = math.sin(self.angle) * self.speed * self.game.dt
            self.dy = math.cos(self.angle) * self.speed * self.game.dt
            self.is_dashing = True
            self.dash_start_time = pg.time.get_ticks()
            return True
        return False
