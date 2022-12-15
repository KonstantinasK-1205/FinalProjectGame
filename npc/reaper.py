from npc.npc import NPC
from settings import *
import random
import pygame as pg

class Reaper(NPC):
    def __init__(self, game, path='resources/sprites/npc/reaper/0.png', pos=(3, 3),
                 scale=0.6, shift=0.38, animation_time=180):
        super().__init__(game, path, pos, scale, shift, animation_time)

        # NPC base stats
        self.pain = False
        self.alive = True
        self.health = 240
        self.speed = 0.03
        self.damage = random.randint(21, 25)
        self.attack_dist = 1
        self.shoot_delay = 80
        self.bullet_lifetime = 150
        self.damage_reduction = 180

        # NPC sound variables
        self.npc_pain = self.game.sound.npc_reaper_pain
        self.npc_death = self.game.sound.npc_reaper_death
        self.npc_attack = self.game.sound.npc_reaper_attack
        self.npc_teleportation = self.game.sound.npc_reaper_teleportation

        # NPC animation variables
        self.teleportation_images = self.get_images(self.path + '/teleportation')

        self.size = 20
        self.ray_cast_value = False
        self.player_search_trigger = False
        self.angle = 0
        self.current_time = 0

        # Teleportation variables
        self.teleported = False
        self.teleportation_counter = 0
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
            self.teleportation_counter = 0
            self.ready_for_teleportation = False

    def animate_teleportation(self):
        if not self.teleported:
            if self.animation_trigger and self.teleportation_counter < len(self.teleportation_images) - 1:
                self.teleportation_counter += 1
                self.teleportation_images.rotate(-1)
                self.image = self.teleportation_images[0]

            if self.teleportation_counter == len(self.teleportation_images) - 1:
                self.ready_for_teleportation = True
