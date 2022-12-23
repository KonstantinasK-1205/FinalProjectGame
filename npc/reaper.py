from npc.npc import NPC
from settings import *
import random
import pygame as pg


class Reaper(NPC):
    def __init__(self, game, pos, scale=[0.6]):
        super().__init__(game, pos, scale)

        # Position and scale
        self.z = random.uniform(0.3, 0.6)
        self.width = 0.6
        self.height = 0.6

        # Primary stats
        self.health = 150
        self.speed = 0.002

        # Attack stats
        self.damage = random.randint(7, 11)
        self.attack_distance = 1
        self.bullet_lifetime = 150

        # Sounds
        self.sfx_attack = "Reaper attack"
        self.sfx_pain = "Reaper pain"
        self.sfx_death = "Reaper death"
        self.sfx_teleportation = "Reaper teleportation"

        # Animation variables
        self.spritesheet = self.load_image("resources/sprites/npc/Reaper_Spritesheet.png")
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

        # Teleportation variables
        self.teleported = False
        self.teleportation_begin = False
        self.ready_for_teleportation = False
        self.last_teleportation_time = 0
        self.teleportation_cooldown = 2000

    def movement(self):
        # If teleported or player is further than 3 blocks
        if self.distance_from(self.player) > 3 or self.teleportation_begin:
            self.teleport()
        super().movement()

    def update(self):
        super().update()
        if self.current_time - self.last_teleportation_time > self.teleportation_cooldown:
            self.teleported = False

    def teleport(self):
        self.animate_teleportation()
        if self.ready_for_teleportation:
            next_x = self.player.x - random.randint(-1, 1)
            next_y = self.player.y - random.randint(-1, 1)
            self.game.sound.play_sfx(self.sfx_teleportation, [self.exact_pos, self.player.exact_pos])
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
