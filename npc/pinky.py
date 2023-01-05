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

        # Animations
        path = "resources/sprites/npc/Pinky/"
        self.states = {
            "Idle": {
                "Frames": self.sprite_manager.load_single_image("Pinky Idle", path + "idle.png"),
                "Speed": 0
            },
            "Walk": {
                "Frames": self.sprite_manager.load_multiple_images("Pinky Walk", path + "Walk/"),
                "Speed": 120
            },
            "Attack": {
                "Frames": self.sprite_manager.load_multiple_images("Pinky Attack", path + "Attack/"),
                "Speed": 300,
                "Attack Speed": 900,
            },
            "Pain": {
                "Frames": self.sprite_manager.load_multiple_images("Pinky Pain", path + "Pain/"),
                "Speed": 150,
            },
            "Death": {
                "Frames": self.sprite_manager.load_multiple_images("Pinky Death", path + "Death/"),
                "Speed": 120,
            },
            "Stomp": {
                "Frames": self.sprite_manager.load_multiple_images("Pinky Stomp", path + "Stomp/"),
                "Speed": 400,
            }
        }
        self.animation.load_sprite_animations(self.states)
        self.animation.change_animation("Idle")

        # Rush ability (increase speed)
        self.is_rushing = False
        self.rush_timer = 0

        # Dash ability ( dash away from bullet )
        self.is_dashing = False
        self.dodge_chance = 6
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

        if self.current_time - self.last_attack > 7000 and self.distance_from_player <= 3 and not self.is_rushing:
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
            self.speed = 0.009
            self.is_rushing = True
            self.rush_timer = pg.time.get_ticks()
