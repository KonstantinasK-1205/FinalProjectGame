from npc.npc import NPC
import random
import pygame as pg
from collision import *


class LostSoul(NPC):
    def __init__(self, game, pos):
        super().__init__(game, pos, [0.6])

        self.z = random.uniform(0.5, 0.8)
        self.width = 0.6
        self.height = 0.6

        # Primary stats
        self.health = 20
        self.speed = 0.006

        # Attack stats
        self.damage = 35

        # Sounds variables
        self.sfx_attack = "Soldier attack"
        self.sfx_pain = "Soldier pain"
        self.sfx_death = "Soldier death"

        # Animations
        path = "resources/sprites/npc/LostSoul/"
        self.states = {
            "Idle": {
                "Frames": self.sprite_manager.load_single_image("LostSoul Idle", path + "idle.png"),
                "Speed": 0
            },
            "Walk": {
                "Frames": self.sprite_manager.load_multiple_images("LostSoul Walk", path + "Walk/"),
                "Speed": 180
            },
            "Attack": {
                "Frames": self.sprite_manager.load_multiple_images("LostSoul Attack", path + "Attack/"),
                "Speed": 20,
                "Attack Speed": 100
            },
            "Pain": {
                "Frames": self.sprite_manager.load_multiple_images("LostSoul Pain", path + "Pain/"),
                "Speed": 300
            },
            "Death": {
                "Frames": self.sprite_manager.load_multiple_images("LostSoul Death", path + "Death/"),
                "Speed": 120
            }
        }
        self.animation.load_sprite_animations(self.states)
        self.animation.change_animation("Idle")

        # Dash ability ( dash towards player )
        self.is_dashing = False
        self.dash_distance = 4
        self.dash_start_time = 0
        self.wait_time = 1500  # Wait for 2 seconds before dashing again
        self.wait_start_time = 0

    def movement(self):
        if self.is_dashing:
            res = resolve_collision(self.x, self.y, self.dx, self.dy, self.game.map, 0.15)
            self.x = res.x
            self.y = res.y

    def update(self):
        super().update()
        elapsed_time = pg.time.get_ticks()
        if self.is_dashing:
            # Calculate how far the enemy has traveled during the dash
            distance_traveled = (elapsed_time - self.dash_start_time) * self.speed * self.game.dt
            if distance_traveled >= self.dash_distance:
                # Stop the dash if the enemy has traveled the maximum distance
                self.is_dashing = False
                self.wait_start_time = elapsed_time
        elif elapsed_time - self.wait_start_time >= self.wait_time:
            # Start dashing again if the wait time has elapsed
            self.start_dash()

    def attack(self):
        if self.animation.completed:
            self.create_bullet()
            self.game.sound.play_sfx(self.sfx_attack, [self.exact_pos, self.player.exact_pos])
            self.previous_shot = pg.time.get_ticks()
            self.apply_damage(100)

    def start_dash(self):
        self.is_dashing = True
        self.dash_start_time = pg.time.get_ticks()
        # Calculate the dash velocity based on the target position
        self.dx = math.cos(self.angle) * self.speed * self.game.dt
        self.dy = math.sin(self.angle) * self.speed * self.game.dt

        # Multiply by thirteen or more to convert it to real position
        # and let fly behind player ( else, it will travel by few pixels )
        self.dash_distance = self.distance_from_player * random.randint(2, 4)
