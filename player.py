import pygame as pg

from settings import *
import math
from collections import deque


class Player:
    def __init__(self, game):
        self.game = game
        self.x = 0
        self.y = 0
        self.z = 0
        self.angle = PLAYER_ANGLE
        self.angle_ver = 0
        self.health = PLAYER_MAX_HEALTH
        self.health_recovery_delay = 10000
        self.time_prev = pg.time.get_ticks()

        self.armor = 0

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

    def update(self, dt):
        rel = pg.mouse.get_rel()
        self.angle = (self.angle + rel[0] * MOUSE_SENSITIVITY) % math.tau
        self.angle_ver = (self.angle_ver + rel[1] * MOUSE_SENSITIVITY) % math.tau
        if math.radians(90) < self.angle_ver < math.radians(180):
            self.angle_ver = math.radians(90)
        elif math.radians(180) < self.angle_ver < math.radians(270):
            self.angle_ver = math.radians(270)

        self.movement(dt)
        self.game.weapon.update()
        self.fill_map_visited()

    def movement(self, dt):
        speed = PLAYER_SPEED * dt
        speed_sin = speed * math.sin(self.angle)
        speed_cos = speed * math.cos(self.angle)

        new_x = self.x
        new_y = self.y
        if self.moving_forw:
            new_x += speed_cos
            new_y += speed_sin
        if self.moving_back:
            new_x += -speed_cos
            new_y += -speed_sin
        if self.moving_left:
            new_x += speed_sin
            new_y += -speed_cos
        if self.moving_right:
            new_x += -speed_sin
            new_y += speed_cos

        # Collision handling
        # Player radius prevents the camera from getting too close to a wall
        # Should not be greater than 0.5 (half wall size), as there is no
        # support for collisions with 3 walls at the same time
        playerRadius = 0.2

        # Margin is used to push the player away from a wall and prevent the
        # collision from persisting due to rounding or floating point error
        margin = 0.001

        # First handle motion and collision in the X axis
        if new_x < self.x:
            if self.game.map.is_wall(new_x - playerRadius, self.y - playerRadius) or \
               self.game.map.is_wall(new_x - playerRadius, self.y + playerRadius):
                new_x = math.ceil(new_x - playerRadius) + playerRadius + margin
        elif new_x > self.x:
            if self.game.map.is_wall(new_x + playerRadius, self.y - playerRadius) or \
               self.game.map.is_wall(new_x + playerRadius, self.y + playerRadius):
                new_x = math.floor(new_x + playerRadius) - playerRadius - margin

        # Next handle motion and collision in the Y axis
        if new_y < self.y:
            if self.game.map.is_wall(new_x - playerRadius, new_y - playerRadius) or \
               self.game.map.is_wall(new_x + playerRadius, new_y - playerRadius):
                new_y = math.ceil(new_y - playerRadius) + playerRadius + margin
        elif new_y > self.y:
            if self.game.map.is_wall(new_x - playerRadius, new_y + playerRadius) or \
               self.game.map.is_wall(new_x + playerRadius, new_y + playerRadius):
                new_y = math.floor(new_y + playerRadius) - playerRadius - margin

        self.x = new_x
        self.y = new_y

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
            if not new_pos in done and not self.game.map.is_wall(new_pos[0], new_pos[1]):
                visit.append(new_pos)
            new_pos = (pos[0] + 1, pos[1])
            if not new_pos in done and not self.game.map.is_wall(new_pos[0], new_pos[1]):
                visit.append(new_pos)
            new_pos = (pos[0], pos[1] - 1)
            if not new_pos in done and not self.game.map.is_wall(new_pos[0], new_pos[1]):
                visit.append(new_pos)
            new_pos = (pos[0], pos[1] + 1)
            if not new_pos in done and not self.game.map.is_wall(new_pos[0], new_pos[1]):
                visit.append(new_pos)

    # Getters
    @property
    def exact_pos(self):
        return self.x, self.y

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

    def add_armor(self, armor):
        # Increase player armor value without exceeding max value
        new_armor = self.armor + armor
        if new_armor > 100:
            new_armor = 100
        self.armor = new_armor

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

        # Give audible & visual feedback to player, if he is still alive
        if self.health > 1:
            self.game.hit_flash_ms = 0
            self.game.sound.play_sfx("Player pain")
        else:
            self.game.current_state = "Game over"

    def distance_from(self, other):
        return math.hypot(other.x - self.x, other.y - self.y, other.z - self.z)
