from bullet import *
from npc.npc import NPC
from settings import *
import pygame as pg
import random


class Battlelord(NPC):
    def __init__(self, game, pos, scale=[0.6]):
        super().__init__(game, pos, scale)

        # Position and scale
        self.width = 0.8
        self.height = 0.9

        # Primary stats
        self.health = 2200
        self.speed = 0.003

        # Attack stats
        self.damage = 10
        self.attack_distance = 8
        self.bullet_lifetime = 850

        self.sensing_range = 60  # 0.5   = 1 grid block
        self.reaction_time = 200

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
                "Animation Speed": 100,
                "Attack Speed": 200,
                "Animation Completed": False,
            },
            "Pain": {
                "Frames": self.images_at("Battlelord_Pain",
                                         [(0, 384, 128, 128)]),
                "Counter": 0,
                "Animation Speed": 450,
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

        # Reload functionality, so enemy wouldn't non-stop fire at player
        self.is_reloading = False
        self.bullet_amount = 120
        self.reload_time = 2500
        self.reload_starts = 0

    def update(self):
        super().update()

        if self.bullet_amount < 0 and not self.is_reloading:
            self.is_reloading = True
            self.reload_starts = pg.time.get_ticks()

        if self.current_time - self.reload_starts > self.reload_time and self.is_reloading:
            self.is_reloading = False
            self.bullet_amount = 120

    def attack(self):
        if not self.is_reloading:
            if self.animations[self.current_animation]["Animation Completed"]:
                if self.current_time - self.reaction_time_passed > self.reaction_time:
                    if self.current_time - self.previous_shot > self.animations["Attack"]["Attack Speed"]:
                        for i in range(5):
                            self.create_bullet()
                            self.bullet_amount -= 1
                        self.game.sound.play_sfx(self.sfx_attack, [self.exact_pos, self.player.exact_pos])
                        self.previous_shot = pg.time.get_ticks()
                        self.reaction_time_passed = pg.time.get_ticks()

        else:
            self.current_animation = 'Idle'
            self.animate()

    def create_bullet(self):
        # Add damage reduction based on how far Player from npc
        distance = self.distance_from(self.player)
        if self.damage > distance:
            damage = int(self.damage - distance)
        else:
            damage = 1

        # Calculate enemy angle, so bullet flies where NPC is looking
        angle = math.atan2((self.player.y - random.uniform(-1, 1)) - self.y,
                           (self.player.x - random.uniform(-1, 1)) - self.x)
        self.game.object_handler.add_bullet(Bullet(self.game, self.exact_pos,
                                                   damage, angle, 0, "enemy", self.bullet_lifetime))
