from projectile import *
from npc.npc import NPC
import pygame as pg
import random


class Battlelord(NPC):
    def __init__(self, game, pos):
        super().__init__(game, pos, [0.6])

        # Position and scale
        self.width = 0.8
        self.height = 0.9

        # Primary stats
        self.health = 2200
        self.speed = 0.003

        # Attack stats
        self.damage = 10
        self.bullet_speed = 0.007
        self.bullet_lifetime = 2000
        self.bullet_width = 0.01
        self.bullet_height = 0.01
        self.bullet_sprite = "resources/sprites/projectile/bullet.png"
        self.attack_distance = 10

        self.sensing_range = 60  # 0.5   = 1 grid block
        self.reaction_time = 200

        # Sound variables
        self.sfx_attack = "Battlelord attack"
        self.sfx_pain = "Battlelord pain"
        self.sfx_death = "Battlelord death"

        # Animations
        path = "resources/sprites/npc/Battlelord/"
        self.states = {
            "Idle": {
                "Frames": self.sprite_manager.load_single_image("Battlelord Idle", path + "idle.png"),
                "Speed": 0
            },
            "Walk": {
                "Frames": self.sprite_manager.load_multiple_images("Battlelord Walk", path + "Walk/"),
                "Speed": 180
            },
            "Attack": {
                "Frames": self.sprite_manager.load_multiple_images("Battlelord Attack", path + "Attack/"),
                "Speed": 100,
                "Attack Speed": 200
            },
            "Pain": {
                "Frames": self.sprite_manager.load_multiple_images("Battlelord Pain", path + "Pain/"),
                "Speed": 450
            },
            "Death": {
                "Frames": self.sprite_manager.load_multiple_images("Battlelord Death", path + "Death/"),
                "Speed": 200
            }
        }
        self.animation.load_sprite_animations(self.states)
        self.animation.change_animation("Idle")

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
            if self.animation.completed:
                for i in range(5):
                    self.create_bullet()
                    self.bullet_amount -= 1
                self.game.sound.play_sfx(self.sfx_attack, [self.exact_pos, self.player.exact_pos])
                self.previous_shot = pg.time.get_ticks()
        else:
            self.change_state("Idle")

    def create_bullet(self):
        # Calculate enemy angle, so bullet flies where NPC is looking
        angle = math.atan2((self.player.y - random.uniform(-1, 1)) - self.y,
                           (self.player.x - random.uniform(-1, 1)) - self.x)
        angle = [angle, 0]

        handler = self.game.object_handler
        position = [self.x, self.y, self.z + (self.height / 2)]
        bullet_data = [self.damage,
                       self.bullet_speed,
                       self.bullet_lifetime,
                       "Enemy",
                       self.bullet_width,
                       self.bullet_height]
        handler.add_bullet(Projectile(self.game,
                                      position,
                                      angle,
                                      bullet_data,
                                      self.bullet_sprite))
