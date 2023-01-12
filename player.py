import pygame as pg

from collections import deque
from collision import *
import copy
import math


class Player:
    def __init__(self, game):
        self.game = game

        self.pos = [0, 0, 0]
        self.size = [0.6, 0.6]
        self.saved_angle = self.angle = [0, 0]

        self.max_health = 100
        self.saved_health = self.health = 100

        self.max_armor = 100
        self.saved_armor = self.armor = 0

        self.moving_forw = False
        self.moving_back = False
        self.moving_left = False
        self.moving_right = False
        self.moved = False

        # Save values of radians to array, no need to calculate them each tick
        self.radians_angles = [math.radians(90),
                               math.radians(180),
                               math.radians(270)]

    def handle_events(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_w:
                self.moving_forw = True
            if event.key == pg.K_s:
                self.moving_back = True
            if event.key == pg.K_a:
                self.moving_left = True
            if event.key == pg.K_d:
                self.moving_right = True

        elif event.type == pg.KEYUP:
            if event.key == pg.K_w:
                self.moving_forw = False
            if event.key == pg.K_s:
                self.moving_back = False
            if event.key == pg.K_a:
                self.moving_left = False
            if event.key == pg.K_d:
                self.moving_right = False

        self.game.weapon.handle_events(event)

    def update(self):
        rel = pg.mouse.get_rel()
        sensitivity = self.game.settings_manager.settings["sensitivity"]
        self.angle = [(self.angle[0] + rel[0] * sensitivity) % math.tau,
                      (self.angle[1] + rel[1] * sensitivity) % math.tau]
        if self.radians_angles[0] < self.angle[1] < self.radians_angles[1]:
            self.angle[1] = self.radians_angles[0]
        elif self.radians_angles[1] < self.angle[1] < self.radians_angles[2]:
            self.angle[1] = self.radians_angles[2]

        self.movement()
        self.game.weapon.update()
        self.fill_map_visited()

        self.game.renderer.camera_pos = [self.pos[0],
                                         self.pos[1],
                                         self.pos[2] + self.size[1]]
        self.game.renderer.camera_angle = [self.angle[0], self.angle[1]]

    def movement(self):
        speed = 0.003 * self.game.dt
        speed_sin = speed * math.sin(self.angle[0])
        speed_cos = speed * math.cos(self.angle[0])

        dx = dy = 0
        if self.moving_forw:
            dx += speed_cos
            dy += speed_sin
        if self.moving_back:
            dx += -speed_cos
            dy += -speed_sin
        if self.moving_left:
            dx += speed_sin
            dy += -speed_cos
        if self.moving_right:
            dx += -speed_sin
            dy += speed_cos

        # Check if player moved, which will be used for fill_map_visited
        if not dx == 0 or not dy == 0:
            self.moved = True
        else:
            self.moved = False

        # Collision handling
        # Player radius prevents the camera from getting too close to a wall
        # Should not be greater than 0.5 (half wall size), as there is no
        # support for collisions with 3 walls at the same time
        res = resolve_collision(self.pos, dx, dy, self.game.map, 0.2)
        self.pos = res.pos[:3]

    # Remove Fog Of War based on player map movement
    def fill_map_visited(self):
        # Early quit, if player hasn't moved a bit
        if not self.moved:
            return

        RADIUS = 25
        done = set()
        visit = deque()

        visit.append(self.grid_pos)
        for i in range(RADIUS):
            if len(visit) == 0:
                break

            pos = visit.popleft()
            self.game.map.set_visited(pos[0], pos[1])
            done.add(tuple(pos))

            new_pos = (pos[0] - 1, pos[1])
            if new_pos not in done and not self.game.map.is_wall(new_pos[0], new_pos[1]):
                visit.append(new_pos)

            new_pos = (pos[0] + 1, pos[1])
            if new_pos not in done and not self.game.map.is_wall(new_pos[0], new_pos[1]):
                visit.append(new_pos)

            new_pos = (pos[0], pos[1] - 1)
            if new_pos not in done and not self.game.map.is_wall(new_pos[0], new_pos[1]):
                visit.append(new_pos)

            new_pos = (pos[0], pos[1] + 1)
            if new_pos not in done and not self.game.map.is_wall(new_pos[0], new_pos[1]):
                visit.append(new_pos)

    # Increase player health value without exceeding max value
    def add_health(self, health):
        health += self.health
        self.health = self.max_health if health > self.max_health else health
        self.game.hud.healthbar.update_healthbar_info(health)

    # Increase player armor value without exceeding max value
    def add_armor(self, armor):
        armor += self.armor
        self.armor = self.max_armor if armor > self.max_armor else armor
        self.game.hud.armorbar.update_armorbar_info(armor)

    # Calculate damage done to player armor and/or health
    def apply_damage(self, damage):
        # Calculate player health and armor applying damage
        if self.armor > 0 and self.armor >= damage:
            self.armor -= damage
        elif 0 < self.armor < damage:
            self.health -= damage - self.armor
            self.armor = 0
        else:
            self.armor = 0
            self.health -= damage

        # If player didn't die, give audible & visual feedback to player
        if self.health > 1:
            # Update Armor and Health HUD information
            self.game.hud.on_player_update(self.armor, self.health)
            self.game.current_state_obj.hit_flash_ms = 0
            self.game.sound.play_sfx("Player pain")

    # If level has changed save player stats, and disable previous movements
    def on_level_change(self):
        self.save_player_stats()
        self.moving_forw = False
        self.moving_back = False
        self.moving_left = False
        self.moving_right = False

    # Save and load functions
    def save_player_stats(self):
        self.saved_health = copy.copy(self.health)
        self.saved_armor = copy.copy(self.armor)
        self.saved_angle = self.angle

    def load_player_stats(self):
        self.moving_forw = False
        self.moving_back = False
        self.moving_left = False
        self.moving_right = False

        self.health = self.saved_health
        self.armor = self.saved_armor
        self.angle = self.saved_angle

    # Calculate distance between player and passed object position
    def distance_from(self, other):
        return math.hypot(self.pos[0] - other.pos[0],  # X Position
                          self.pos[1] - other.pos[1],  # Y Position
                          self.pos[2] - other.pos[2])  # Z Position

    # Set spawning point of player
    def set_spawn(self, x, y, z=0):
        self.pos = [x, y, z]

    # Positional getters
    # Returns exact (float) position
    @property
    def exact_pos(self):
        return self.pos

    # Returns grid (int) position
    @property
    def grid_pos(self):
        return [int(self.pos[0]),  # X Position
                int(self.pos[1]),  # Y Position
                int(self.pos[2])]  # Z Position

    # Returns exact (float) position on X axis
    @property
    def pos_x(self):
        return self.pos[0]

    # Returns exact (float) position on Y axis
    @property
    def pos_y(self):
        return self.pos[1]

    # Returns exact (float) position on Z axis
    @property
    def pos_z(self):
        return self.pos[2]

    # Size getters
    # Returns player width
    @property
    def width(self):
        return self.size[0]

    # Returns player height
    @property
    def height(self):
        return self.size[1]
