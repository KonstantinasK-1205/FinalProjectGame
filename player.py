import pygame as pg

from settings import *
from collections import deque
from collision import *
import copy
import math


class Player:
    def __init__(self, game):
        self.game = game

        self.x = 0
        self.y = 0
        self.z = 0
        self.width = 0.6
        self.height = 0.6

        self.angle = PLAYER_ANGLE
        self.angle_ver = 0

        self.armor = 0
        self.health = 100
        self.saved_armor = 0
        self.saved_health = 0

        self.moving_forw = False
        self.moving_back = False
        self.moving_left = False
        self.moving_right = False

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
        self.angle = (self.angle + rel[0] * MOUSE_SENSITIVITY) % math.tau
        self.angle_ver = (self.angle_ver + rel[1] * MOUSE_SENSITIVITY) % math.tau
        if math.radians(90) < self.angle_ver < math.radians(180):
            self.angle_ver = math.radians(90)
        elif math.radians(180) < self.angle_ver < math.radians(270):
            self.angle_ver = math.radians(270)

        self.movement()
        self.game.weapon.update()
        self.fill_map_visited()

        self.game.renderer.camera_x = self.x
        self.game.renderer.camera_y = self.y
        self.game.renderer.camera_z = self.z + self.height
        self.game.renderer.camera_angle = self.angle
        self.game.renderer.camera_angle_ver = self.angle_ver

    def movement(self):
        speed = PLAYER_SPEED * self.game.dt
        speed_sin = speed * math.sin(self.angle)
        speed_cos = speed * math.cos(self.angle)

        dx = 0
        dy = 0
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

        # Collision handling
        # Player radius prevents the camera from getting too close to a wall
        # Should not be greater than 0.5 (half wall size), as there is no
        # support for collisions with 3 walls at the same time
        res = resolve_collision(self.x, self.y, dx, dy, self.game.map, 0.2)
        self.x = res.x
        self.y = res.y

    def on_level_change(self):
        self.save_player_stats()
        self.moving_forw = False
        self.moving_back = False
        self.moving_left = False
        self.moving_right = False

    def fill_map_visited(self):
        RADIUS = 25

        done = set()
        visit = deque()

        visit.append(self.grid_pos)
        for i in range(RADIUS):
            if len(visit) == 0:
                break

            pos = visit.popleft()
            self.game.map.set_visited(pos[0], pos[1])
            done.add(pos)

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

    # Getters
    @property
    def exact_pos(self):
        return self.x, self.y, self.z

    @property
    def grid_pos(self):
        return int(self.x), int(self.y)

    # Setters
    def set_spawn(self, x, y):
        self.x = x
        self.y = y

    def add_health(self, hp):
        # Increase player health value without exceeding max value
        new_health = self.health + hp
        if new_health > 100:
            new_health = 100
        self.health = new_health
        self.game.hud.healthbar.update_healthbar_info(self.health)

    def add_armor(self, armor):
        # Increase player armor value without exceeding max value
        new_armor = self.armor + armor
        if new_armor > 100:
            new_armor = 100
        self.armor = new_armor
        self.game.hud.armorbar.update_armorbar_info(self.armor)

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

        self.game.hud.healthbar.update_healthbar_info(self.health)
        self.game.hud.armorbar.update_armorbar_info(self.armor)
        # Give audible & visual feedback to player, if he is still alive
        if self.health > 1:
            self.game.current_state_obj.hit_flash_ms = 0
            self.game.sound.play_sfx("Player pain")

    def distance_from(self, other):
        return math.hypot(other.x - self.x, other.y - self.y, other.z - self.z)

    def save_player_stats(self):
        self.saved_health = copy.deepcopy(self.health)
        self.saved_armor = copy.deepcopy(self.armor)

    def load_player_stats(self):
        self.moving_forw = False
        self.moving_back = False
        self.moving_left = False
        self.moving_right = False

        self.health = copy.deepcopy(self.saved_health)
        self.armor = copy.deepcopy(self.saved_armor)
