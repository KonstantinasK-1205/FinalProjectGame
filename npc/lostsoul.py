from npc.npc import NPC
from settings import *
import random
import pygame as pg


class LostSoul(NPC):
    def __init__(self, game, pos, scale=0.6):
        super().__init__(game, pos, scale)

        self.z = 0.7
        self.width = 0.6
        self.height = 0.6
        self.size = 10

        # NPC base stats
        self.health = 20
        self.speed = 0.006
        self.damage = random.randint(30, 40)
        self.attack_dist = 1
        self.shoot_delay = 80
        self.bullet_lifetime = 150
        self.damage_reduction = 180

        # NPC animation variables
        self.spritesheet = pg.image.load("resources/sprites/npc/LostSoul_Spritesheet.png").convert_alpha()
        self.current_animation = "Idle"
        self.animations = {
            "Idle": {
                "Frames": self.images_at("LostSoul_Idle",
                                         [(0, 0, 64, 64)]),
                "Counter": 0,
                "Animation Speed": 180,
                "Animation Completed": False,
            },
            "Walk": {
                "Frames": self.images_at("LostSoul_Walk",
                                         [(0, 64, 64, 64),
                                         (64, 64, 64, 64),
                                         (128, 64, 64, 64),
                                         (192, 64, 64, 64)]),
                "Counter": 0,
                "Animation Speed": 180,
                "Animation Completed": False,
            },
            "Attack": {
                "Frames": self.images_at("LostSoul_Attack",
                                         [(0, 64, 64, 64),
                                         (64, 64, 64, 64),
                                         (128, 64, 64, 64),
                                         (192, 64, 64, 64)]),
                "Counter": 0,
                "Animation Speed": 20,
                "Attack Speed": 100,
                "Animation Completed": False,
            },
            "Pain": {
                "Frames": self.images_at("LostSoul_Pain",
                                         [(0, 128, 64, 64)]),
                "Counter": 0,
                "Animation Speed": 300,
                "Animation Completed": False,
            },
            "Death": {
                "Frames": self.images_at("LostSoul_Death",
                                         [(0, 192, 64, 64),
                                          (64, 192, 64, 64),
                                          (128, 192, 64, 64),
                                          (192, 192, 64, 64),
                                          (256, 192, 64, 64),
                                          (320, 192, 64, 64),
                                          (384, 192, 64, 64),
                                          (448, 192, 64, 64)]),
                "Counter": 0,
                "Animation Speed": 120,
                "Animation Completed": False,
            }
        }

        # NPC sound variables
        self.sfx_attack = "Soldier attack"
        self.sfx_pain = "Soldier pain"
        self.sfx_death = "Soldier death"

        # New variables
        self.dx = 0
        self.dy = 0
        # Set lost soul barrel toward player time
        self.barrel_towards = False
        self.barrel_cooldown = 500
        self.last_barrel_time = 0
        # Set how much lost soul need time to rest
        self.is_rested = True
        self.resting_cooldown = 2500
        self.last_rested_time = 0

    def movement(self):
        next_pos = self.game.pathfinding.get_path(self.grid_pos, self.player.grid_pos)
        if self.barrel_towards:
            self.barrel_towards = False
            self.last_barrel_time = pg.time.get_ticks()

            if next_pos not in self.game.object_handler.npc_positions:
                self.dx = math.cos(self.angle) * self.speed * self.game.dt
                self.dy = math.sin(self.angle) * self.speed * self.game.dt

        if self.is_rested:
            if not self.game.map.is_wall(int(self.x + self.dx * self.size), int(self.y)):
                self.x += self.dx

            if not self.game.map.is_wall(int(self.x), int(self.y + self.dy * self.size)):
                self.y += self.dy

    def update(self):
        super().update()
        print("Current - Rush: " + str(self.current_time - self.last_barrel_time) + " | Bool: " + str(self.barrel_cooldown))
        print("Current - Attk: " + str(self.current_time - self.last_rested_time) + " | Bool: " + str(self.resting_cooldown))
        print(" ")

        if self.current_time - self.last_barrel_time > self.barrel_cooldown:
            self.barrel_towards = True

        if self.current_time - self.last_rested_time > self.resting_cooldown:
            self.is_rested = not self.is_rested
            self.last_rested_time = pg.time.get_ticks()


    def attack(self):
        if self.animations[self.current_animation]["Animation Completed"]:
            self.create_bullet()
            self.game.sound.play_sfx(self.sfx_attack, [self.exact_pos, self.player.exact_pos])
            self.previous_shot = pg.time.get_ticks()
            self.apply_damage(50, None)
