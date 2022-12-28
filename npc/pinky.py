from npc.npc import NPC
import random
import pygame as pg
from collision import *


class Pinky(NPC):
    def __init__(self, game, pos):
        super().__init__(game, pos, [0.6])

        # Primary stats
        self.health = 350
        self.speed = 0.0025

        # Attack stats
        self.damage = 14

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

        # Rush ability (increase speed)
        self.is_rushing = False
        self.rush_timer = 0

        # Dash ability ( dash away from bullet )
        self.is_dashing = False
        self.dodge_chance = 5
        self.dash_distance = 2
        self.dash_start_time = 0
        self.last_attack = 0

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
        if self.is_dashing:
            distance_traveled = (elapsed_time - self.dash_start_time) * self.speed * self.game.dt
            if distance_traveled >= self.dash_distance:
                self.speed = 0.0025
                self.is_dashing = False

        if self.current_time - self.last_attack > 7000 and self.distance_from(self.player) <= 3 and not self.is_rushing:
            self.start_rush()
            self.last_attack = pg.time.get_ticks()

        if self.current_time - self.rush_timer > 2000 and self.is_rushing:
            self.speed = 0.0025
            self.last_attack = pg.time.get_ticks()
            self.attack_distance = 1
            self.bullet_lifetime = 35
            self.is_rushing = False

    def attack(self):
        super().attack()
        self.last_attack = pg.time.get_ticks()

    def avoid_bullet(self):
        if random.randint(1, 10) > self.dodge_chance:
            self.dash_distance = 2
            self.dx = math.sin(self.angle) * self.speed * self.game.dt
            self.dy = math.cos(self.angle) * self.speed * self.game.dt
            self.is_dashing = True
            self.dash_start_time = pg.time.get_ticks()
            return True
        return False

    def start_rush(self):
        if not self.is_rushing:
            self.speed = 0.008
            self.is_rushing = True
            self.attack_distance = 2
            self.bullet_lifetime = 75
            self.rush_timer = pg.time.get_ticks()
