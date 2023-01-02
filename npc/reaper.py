from npc.npc import NPC
import math
import random
import pygame as pg


class Reaper(NPC):
    def __init__(self, game, pos):
        super().__init__(game, pos, [0.6])

        # Position and scale
        self.z = random.uniform(0.3, 0.6)
        self.width = 0.6
        self.height = 0.6

        # Primary stats
        self.health = 200
        self.speed = 0.002

        # Attack stats
        self.damage = 10
        self.bullet_lifetime = 110

        # Sounds
        self.sfx_attack = "Reaper attack"
        self.sfx_pain = "Reaper pain"
        self.sfx_death = "Reaper death"
        self.sfx_teleportation = "Reaper teleportation"

        # Animations
        sprite = self.game.sprite_manager
        path = "resources/sprites/npc/Reaper/"
        self.states = {
            "Idle": {
                "Frames": sprite.load_single_image("Reaper Idle", path + "idle.png"),
                "Speed": 0
            },
            "Walk": {
                "Frames": sprite.load_multiple_images("Reaper Walk", path + "Walk/"),
                "Speed": 180
            },
            "Attack": {
                "Frames": sprite.load_multiple_images("Reaper Attack", path + "Attack/"),
                "Speed": 200,
                "Attack Speed": 800,
            },
            "Pain": {
                "Frames": sprite.load_multiple_images("Reaper Pain", path + "Pain/"),
                "Speed": 300,
            },
            "Death": {
                "Frames": sprite.load_multiple_images("Reaper Death", path + "Death/"),
                "Speed": 120,
            },
            "Teleportation": {
                "Frames": sprite.load_multiple_images("Reaper Teleportation", path + "Teleportation/"),
                "Speed": 150,
            }
        }
        self.animation.load_sprite_animations(self.states)
        self.animation.change_animation("Idle")

        # Teleportation variables
        self.teleported = False
        self.teleportation_begin = False
        self.ready_for_teleportation = False
        self.last_teleportation_time = 0
        self.teleportation_cooldown = 2000
        self.last_attack = 0

    def movement(self):
        # If teleported or player is further than 3 blocks
        if self.distance_from(self.player) > 3 or self.teleportation_begin:
            self.change_state("Teleportation")
        super().movement()

    def update(self):
        super().update()
        if self.alive:
            if self.current_state == "Teleportation" and self.animation.completed:
                self.teleport()
                self.last_attack = pg.time.get_ticks()

            if self.current_time - self.last_teleportation_time > self.teleportation_cooldown:
                self.teleported = False

            if self.current_time - self.last_attack > 6000 and 1 < self.distance_from(self.player) < 3:
                self.change_state("Teleportation")

    def attack(self):
        super().attack()
        self.last_attack = pg.time.get_ticks()

    def teleport(self):
        while 1:
            next_x = self.player.x - random.randint(-1, 1)
            next_y = self.player.y - random.randint(-1, 1)
            if not self.game.map.is_wall(next_x, next_y):
                self.x = next_x
                self.y = next_y
                break

        self.last_teleportation_time = pg.time.get_ticks()
        self.game.sound.play_sfx(self.sfx_teleportation, [self.exact_pos, self.player.exact_pos])
        self.angle = math.atan2(self.player.y - self.y, self.player.x - self.x)
        self.teleported = True
        self.teleportation_begin = False
        self.ready_for_teleportation = False
        self.change_state("Idle")
