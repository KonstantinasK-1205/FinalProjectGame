from collision import *
from projectile import Projectile
from sprites.animation_manager import *
from sprites.sprite import Sprite
import pygame as pg
import random


class NPC(Sprite):
    def __init__(self, game, pos, scale):
        super().__init__(game, pos, scale)
        self.animation = Animation()
        self.current_time = 0

        # Base position and scale
        self.z = 0
        self.width = 0.7
        self.height = 0.7

        # Base primary stats
        self.alive = True
        self.pain = False
        self.health = 100
        self.speed = 0.002
        self.angle = 0
        self.dx = 0
        self.dy = 0

        # Base attack stats
        self.bullet_sprite = "resources/sprites/projectile/empty.png"
        self.bullet_width = 0.1
        self.bullet_height = 0.1
        self.bullet_speed = 0.025
        self.bullet_lifetime = 80

        self.damage = 0
        self.previous_shot = 0
        self.attack_distance = 1

        self.sensing_range = 35  # 0.5   = 1 grid block
        self.distance_from_player = 0
        self.seeing_player = False
        self.seeing_player_counter = 0
        self.seeing_player_interval = 30  # Ticks

        # Base Sounds
        self.sfx_attack = "Soldier attack"
        self.sfx_pain = "Soldier pain"
        self.sfx_death = "Soldier death"

        # Base Animation variables
        self.sprite = self.texture_path
        self.current_state = "Idle"
        self.states = {}

    def update(self):
        self.current_time = pg.time.get_ticks()

        self.animation.animate(self.game.dt)

        self.current_state = self.animation.get_state()
        self.sprite = self.animation.get_sprite()

        self.run_logic()

    def draw(self):
        self.game.renderer.draw_sprite(self.x, self.y, self.z, self.width, self.height, self.sprite)

    def run_logic(self):
        if not self.alive:
            self.change_state("Death")
            return

        # If NPC hurt, he can't do anything else
        if self.pain:
            if self.animation.completed:
                self.pain = False
            self.change_state("Pain")
            return

        # Calculate distance from player once per tick and reuse it
        self.distance_from_player = self.distance_from(self.player)

        # Check if seeing_player_interval (default 30 ticks), has passed and set bool to false
        # This will limit can_see_player(), as we don't need to check that each tick
        if self.seeing_player_counter >= self.seeing_player_interval:
            self.seeing_player = False

        # If player too far from NPC, quit logic
        if self.distance_from_player < self.sensing_range:

            # Calculate NPC angle which is always opposing player - used for movement and sight
            self.angle = math.atan2(self.player.y - self.y, self.player.x - self.x)

            # If enemy isn't seeing player, allow it to check if he sees player
            if not self.seeing_player:
                self.seeing_player = self.can_see_player()
                self.seeing_player_counter = 0
            else:
                self.seeing_player_counter += 1

            if self.seeing_player:
                if self.distance_from_player < self.attack_distance:
                    self.change_state("Attack")
                    self.attack()
                else:
                    self.change_state("Walk")
                    self.movement()
            else:
                self.change_state("Idle")

    # Attack
    def attack(self):
        if self.animation.completed:
            self.create_bullet()
            self.game.sound.play_sfx(self.sfx_attack, [self.exact_pos, self.player.exact_pos])
            self.previous_shot = pg.time.get_ticks()

    def create_bullet(self):
        position = [self.x, self.y, self.z + (self.height / 2)]

        angle = [math.atan2(self.player.y - self.y, self.player.x - self.x),
                 math.atan(self.player.z - self.z)]

        bullet_data = [self.damage,
                       self.bullet_speed,
                       self.bullet_lifetime,
                       "Enemy",
                       self.bullet_width,
                       self.bullet_height]
        self.game.object_handler.add_bullet(Projectile(self.game, position, angle, bullet_data, self.bullet_sprite))

    def apply_damage(self, damage):
        if damage > 0:
            self.pain = True
            self.health -= damage
            if self.health > 1:
                self.game.sound.play_sfx(self.sfx_pain, [self.exact_pos, self.player.exact_pos])
            else:
                self.alive = False
                self.game.sound.play_sfx(self.sfx_death, [self.exact_pos, self.player.exact_pos])

    # Movement
    def movement(self):
        if self.seeing_player:
            self.dx = math.cos(self.angle) * self.speed * self.game.dt
            self.dy = math.sin(self.angle) * self.speed * self.game.dt
        else:
            next_pos = self.game.pathfinding.get_path(self.grid_pos, self.player.grid_pos)
            next_x = next_pos[0] + 0.5
            next_y = next_pos[1] + 0.5

            # Update velocity only if pathfinding gave correct result
            if math.hypot(next_x - self.x, next_y - self.y) < 2:
                self.angle = math.atan2(next_y - self.y, next_x - self.x)

                self.dx = math.cos(self.angle) * self.speed * self.game.dt
                self.dy = math.sin(self.angle) * self.speed * self.game.dt

        if True:
            res = resolve_collision(self.x, self.y, self.dx, self.dy, self.game.map, 0.15)
            self.x = res.x
            self.y = res.y

    def can_see_player(self):
        # Init variables
        step = 0.5
        x, y, z = self.exact_pos

        # Get player grid pos once, and reuse it
        player_grid_pos = self.player.grid_pos

        # Calculate NPC sin and cos of angle once
        cos_angle = math.cos(self.angle)
        sin_angle = math.sin(self.angle)

        # If it is possible to walk straight line to the player, it means that
        # NPC can see them
        for i in range(self.sensing_range):
            x += cos_angle * step
            y += sin_angle * step
            if self.game.map.is_wall(x, y):
                break
            elif player_grid_pos == (int(x), int(y)):
                return True
        return False

    def change_state(self, state):
        if self.animation.completed or state == "Death":
            if not self.current_state == state:
                self.current_state = state
                self.animation.change_animation(state)

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

    def get_frames(self):
        return self.states[self.current_state]
