from npc.npc import NPC
from settings import *
import random
import pygame as pg


class Reaper(NPC):
    def __init__(self, game, pos, scale=0.6):
        super().__init__(game, pos, scale)

        # NPC base stats
        self.pain = False
        self.alive = True
        self.health = 240
        self.speed = 0.03
        self.damage = random.randint(7, 11)
        self.attack_dist = 1
        self.shoot_delay = 80
        self.bullet_lifetime = 150
        self.damage_reduction = 180
        self.width = 0.6
        self.height = 0.6

        # NPC animation variables
        animation_path = "resources/sprites/npc/reaper/"
        self.current_animation = "Idle"
        self.animations = {
            "Idle": {
                "Frames": self.load_animation_textures(animation_path + "/idle"),
                "Counter": 0,
                "Animation Speed": 180,
                "Animation Completed": False,
            },
            "Walk": {
                "Frames": self.load_animation_textures(animation_path + "/walk"),
                "Counter": 0,
                "Animation Speed": 180,
                "Animation Completed": False,
            },
            "Attack": {
                "Frames": self.load_animation_textures(animation_path + "/attack"),
                "Counter": 0,
                "Animation Speed": 250,
                "Attack Speed": 250,
                "Animation Completed": False,
            },
            "Teleportation": {
                "Frames": self.load_animation_textures(animation_path + "/teleportation"),
                "Counter": 0,
                "Animation Speed": 150,
                "Animation Completed": False,
            },
            "Pain": {
                "Frames": self.load_animation_textures(animation_path + "/pain"),
                "Counter": 0,
                "Animation Speed": 300,
                "Animation Completed": False,
            },
            "Death": {
                "Frames": self.load_animation_textures(animation_path + "/death"),
                "Counter": 0,
                "Animation Speed": 120,
                "Animation Completed": False,
            }
        }

        # NPC sound variables
        self.npc_pain = self.game.sound.npc_reaper_pain
        self.npc_death = self.game.sound.npc_reaper_death
        self.npc_attack = self.game.sound.npc_reaper_attack
        self.npc_teleportation = self.game.sound.npc_reaper_teleportation

        self.size = 35
        self.ray_cast_value = False
        self.player_search_trigger = False
        self.angle = 0
        self.current_time = 0

        # Teleportation variables
        self.teleported = False
        self.ready_for_teleportation = False
        self.last_teleportation_time = 0
        self.teleportation_cooldown = 2000

    def movement(self):
        # If teleported or player is further than 3 blocks
        distance_to_player = int(abs(self.player.exact_pos[0] - self.x) + abs(self.player.exact_pos[1] - self.y))
        if distance_to_player > 3:
            self.teleport()
        super().movement()

    def update(self):
        super().update()
        if self.current_time - self.last_teleportation_time > self.teleportation_cooldown:
            self.teleported = False

    def teleport(self):
        self.animate_teleportation()
        if self.ready_for_teleportation:
            next_pos_x = self.player.exact_pos[0] - random.randint(-1, 1)
            next_pos_y = self.player.exact_pos[1] - random.randint(-1, 1)
            self.game.sound.play_sound(self.npc_teleportation, self.grid_pos, self.player.exact_pos)
            if not self.game.map.is_wall(next_pos_x, next_pos_y):
                self.x = next_pos_x
                self.y = next_pos_y
            self.angle = math.atan2(self.player.exact_pos[1] - self.exact_pos[1],
                                    self.player.exact_pos[0] - self.exact_pos[0])
            self.last_teleportation_time = pg.time.get_ticks()
            self.teleported = True
            self.animations[self.current_animation]["Counter"] = 0
            self.ready_for_teleportation = False
            self.current_animation = "Idle"

    def animate_teleportation(self):
        if not self.teleported:
            self.current_animation = "Teleportation"
            animation = self.animations[self.current_animation]
            if animation["Animation Completed"] and animation["Counter"] < len(animation["Frames"]) - 1:
                animation["Frames"].rotate(-1)
                self.texture_path = animation["Frames"][0]
                animation["Counter"] += 1

            if animation["Counter"] == len(animation["Frames"]) - 1:
                self.ready_for_teleportation = True
