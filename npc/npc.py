from bullet import Bullet
from settings import *
from sprites.sprite import Sprite
import pygame as pg
import random
from collision import *


class NPC(Sprite):
    def __init__(self, game, pos, scale=0.6):
        super().__init__(game, pos, scale)

        self.z = 0
        self.width = 0.3
        self.height = 0.6

        # NPC base stats
        self.pain = False
        self.alive = True
        self.health = 100
        self.speed = 0.002
        self.damage = 0
        self.damage_reduction = 0
        self.attack_dist = 0
        self.bullet_lifetime = 0
        self.reaction_time = random.randrange(600, 1200, 100)
        self.reaction_time_passed = 0

        # NPC animation variables
        self.current_animation = "Idle"
        self.animations = {}

        # Sounds
        self.sfx_attack = "Soldier attack"
        self.sfx_pain = "Soldier pain"
        self.sfx_death = "Soldier death"

        self.size = 50
        self.approaching_player = False
        self.angle = 0
        self.current_time = 0
        self.previous_shot = 0

    def update(self):
        self.current_time = pg.time.get_ticks()
        self.check_animation_time()
        self.run_logic()

    def run_logic(self):
        if self.alive:
            # NPC angle is always opposing player - used for movement and sight
            # calculation
            self.angle = math.atan2(self.player.y - self.y, self.player.x - self.x)

            # May be computationally intensive, so calculate only once per tick
            can_see_player = self.can_see_player()

            if self.pain:
                self.animate_pain()
            elif can_see_player:
                self.approaching_player = True

                if self.distance_from(self.player) < self.attack_dist:
                    self.current_animation = "Attack"
                    self.animate()
                    self.attack()
                else:
                    self.current_animation = "Walk"
                    self.animate()
                    self.movement()
            elif self.approaching_player:
                self.current_animation = "Walk"
                self.animate()
                self.movement()
            else:
                self.current_animation = "Idle"
                self.animate()
        else:
            self.animate_death()

    # Attack
    def attack(self):
        if self.animations[self.current_animation]["Animation Completed"]:
            if self.current_time - self.reaction_time_passed > self.reaction_time:
                if self.current_time - self.previous_shot > self.animations["Attack"]["Attack Speed"]:
                    self.create_bullet()
                    self.game.sound.play_sfx(self.sfx_attack, [self.exact_pos, self.player.exact_pos])
                    self.previous_shot = pg.time.get_ticks()
                    self.reaction_time_passed = pg.time.get_ticks()

    def create_bullet(self):
        # Add damage reduction based on how far Player from npc
        distance = self.distance_from(self.player)
        if self.damage > distance:
            damage = int(self.damage - distance)
        else:
            damage = 0
        # Calculate enemy angle, so bullet flies exactly where NPC is looking
        angle = math.atan2(self.player.y - random.random() - self.y, self.player.x - random.random() - self.x)
        self.game.object_handler.add_bullet(Bullet(self.game, self.exact_pos,
                                                   damage, angle, 0, "enemy", self.bullet_lifetime))

    def apply_damage(self, damage, weapon):
        self.pain = True
        if weapon == ["Shotgun", "Melee"] and self.damage_reduction < damage:
            damage -= self.damage_reduction
        self.health -= damage
        if self.health > 1:
            self.game.sound.play_sfx(self.sfx_pain, [self.exact_pos, self.player.exact_pos])
        else:
            self.alive = False
            self.current_animation = "Death"
            self.game.sound.play_sfx(self.sfx_death, [self.exact_pos, self.player.exact_pos])

    # Movement
    def movement(self):
        next_pos = self.game.pathfinding.get_path(self.grid_pos, self.player.grid_pos)
        if next_pos not in self.game.object_handler.npc_positions:
            dx = math.cos(self.angle) * self.speed * self.game.dt
            dy = math.sin(self.angle) * self.speed * self.game.dt

            res = resolve_collision(self.x, self.y, dx, dy, self.game.map, 0.15)
            self.x = res.x
            self.y = res.y

    # Animations
    def animate_pain(self):
        self.current_animation = "Pain"
        self.animate()
        if self.animations[self.current_animation]["Animation Completed"]:
            self.pain = False

    def animate_death(self):
        animation = self.animations[self.current_animation]
        if self.dead:
            if animation["Animation Completed"] and animation["Counter"] < len(animation["Frames"]) - 1:
                animation["Counter"] += 1
                animation["Frames"].rotate(-1)
                self.texture_path = animation["Frames"][0]

    def can_see_player(self):
        # Larger step sizes are more efficient, but may cause NPC to see through
        # the player
        STEP = 0.5
        # Limiting the max number of steps makes NPC near-sighted, but prevents
        # the check from taking too long
        MAX_STEPS = 25

        # If it is possible to walk straight line to the player, it means that
        # NPC can see them
        x, y, z = self.exact_pos
        for i in range(MAX_STEPS):
            x += math.cos(self.angle) * STEP
            y += math.sin(self.angle) * STEP
            if self.game.map.is_wall(x, y):
                break
            elif self.player.grid_pos == (int(x), int(y)):
                return True

        return False

    # Getters
    @property
    def exact_pos(self):
        return self.x, self.y, self.z

    @property
    def grid_pos(self):
        return int(self.x), int(self.y)

    @property
    def dead(self):
        return not self.alive
