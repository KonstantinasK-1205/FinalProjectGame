from npc.npc import NPC
from settings import *
import random
import pygame as pg


class Reaper(NPC):
    def __init__(self, game, pos, scale=0.6):
        super().__init__(game, pos, scale)

        self.z = 0.3
        self.width = 0.6
        self.height = 0.6

        # NPC base stats
        self.health = 240
        self.speed = 0.002
        self.damage = random.randint(7, 11)
        self.attack_dist = 1
        self.shoot_delay = 80
        self.bullet_lifetime = 150
        self.damage_reduction = 180

        # NPC animation variables
        self.spritesheet = pg.image.load("resources/sprites/npc/Reaper_Spritesheet.png").convert_alpha()
        self.current_animation = "Idle"
        self.animations = {
            "Idle": {
                "Frames": self.images_at("Reaper_Idle",
                                         [(0, 0, 128, 128)]),
                "Counter": 0,
                "Animation Speed": 180,
                "Animation Completed": False,
            },
            "Walk": {
                "Frames": self.images_at("Reaper_Walk",
                                         [(0, 128, 128, 128),
                                         (128, 128, 128, 128),
                                         (256, 128, 128, 128)]),
                "Counter": 0,
                "Animation Speed": 180,
                "Animation Completed": False,
            },
            "Attack": {
                "Frames": self.images_at("Reaper_Attack",
                                         [(0, 256, 128, 128),
                                         (128, 256, 128, 128),
                                         (256, 256, 128, 128),
                                         (384, 256, 128, 128)]),
                "Counter": 0,
                "Animation Speed": 200,
                "Attack Speed": 800,
                "Animation Completed": False,
            },
            "Pain": {
                "Frames": self.images_at("Reaper_Pain",
                                         [(0, 384, 128, 128)]),
                "Counter": 0,
                "Animation Speed": 300,
                "Animation Completed": False,
            },
            "Death": {
                "Frames": self.images_at("Reaper_Death",
                                         [(0, 512, 128, 128),
                                          (128, 512, 128, 128),
                                          (256, 512, 128, 128),
                                          (384, 512, 128, 128),
                                          (512, 512, 128, 128),
                                          (640, 512, 128, 128),
                                          (768, 512, 128, 128),
                                          (896, 512, 128, 128)]),
                "Counter": 0,
                "Animation Speed": 120,
                "Animation Completed": False,
            },
            "Teleportation": {
                "Frames": self.images_at("Reaper_Teleportation",
                                         [(0, 640, 128, 128),
                                          (128, 640, 128, 128),
                                          (256, 640, 128, 128),
                                          (384, 640, 128, 128),
                                          (512, 640, 128, 128),
                                          (640, 640, 128, 128),
                                          (768, 640, 128, 128)]),
                "Counter": 0,
                "Animation Speed": 150,
                "Animation Completed": False,
            }
        }

        # NPC sound variables
        self.npc_pain = self.game.sound.npc_reaper_pain
        self.npc_death = self.game.sound.npc_reaper_death
        self.npc_attack = self.game.sound.npc_reaper_attack
        self.npc_teleportation = self.game.sound.npc_reaper_teleportation

        # Teleportation variables
        self.teleported = False
        self.teleportation_begin = False
        self.ready_for_teleportation = False
        self.last_teleportation_time = 0
        self.teleportation_cooldown = 2000

    def movement(self, dt):
        # If teleported or player is further than 3 blocks
        if self.distance_from(self.player) > 3 or self.teleportation_begin:
            self.teleport()
        super().movement(dt)

    def update(self, dt):
        super().update(dt)
        if self.current_time - self.last_teleportation_time > self.teleportation_cooldown:
            self.teleported = False

    def teleport(self):
        self.animate_teleportation()
        if self.ready_for_teleportation:
            next_x = self.player.x - random.randint(-1, 1)
            next_y = self.player.y - random.randint(-1, 1)
            self.game.sound.play_sound(self.npc_teleportation, self.exact_pos, self.player.exact_pos)
            if not self.game.map.is_wall(next_x, next_y):
                self.x = next_x
                self.y = next_y
            self.angle = math.atan2(self.player.y - self.y, self.player.x - self.x)
            self.last_teleportation_time = pg.time.get_ticks()
            self.current_animation = "Idle"
            self.teleported = True
            self.teleportation_begin = False
            self.ready_for_teleportation = False
            self.animations["Teleportation"]["Counter"] = 0

    def animate_teleportation(self):
        if not self.teleported:
            self.teleportation_begin = True
            self.current_animation = "Teleportation"
            animation = self.animations[self.current_animation]
            if animation["Animation Completed"] and animation["Counter"] < len(animation["Frames"]) - 1:
                animation["Frames"].rotate(-1)
                self.texture_path = animation["Frames"][0]
                animation["Counter"] += 1

            if animation["Counter"] == len(animation["Frames"]) - 1:
                self.ready_for_teleportation = True
