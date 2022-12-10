import pygame as pg

from settings import *


class Player:
    def __init__(self, game):
        self.game = game
        self.rel = 0
        self.pos_x = 0
        self.pos_y = 0
        self.angle = PLAYER_ANGLE
        self.health = PLAYER_MAX_HEALTH
        self.health_recovery_delay = 10000
        self.time_prev = pg.time.get_ticks()

        self.health = 100
        self.armor = 0

        self.movingForward = False
        self.movingBackward = False
        self.movingLeft = False
        self.movingRight = False

    def handle_events(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_w:
                self.movingForward = True
            if event.key == pg.K_s:
                self.movingBackward = True
            if event.key == pg.K_a:
                self.movingLeft = True
            if event.key == pg.K_d:
                self.movingRight = True

        elif event.type == pg.KEYUP:
            if event.key == pg.K_w:
                self.movingForward = False
            if event.key == pg.K_s:
                self.movingBackward = False
            if event.key == pg.K_a:
                self.movingLeft = False
            if event.key == pg.K_d:
                self.movingRight = False

        if event.type == pg.MOUSEMOTION:
            self.rel = max(-MOUSE_MAX_REL, min(MOUSE_MAX_REL, pg.mouse.get_rel()[0]))
            self.angle += self.rel * MOUSE_SENSITIVITY * self.game.delta_time

        self.game.weapon.handle_events(event)

    def update(self):
        self.movement()
        self.game.weapon.update()

    def movement(self):
        dx, dy = 0, 0
        speed = PLAYER_SPEED * self.game.delta_time
        speed_sin = speed * math.sin(self.angle)
        speed_cos = speed * math.cos(self.angle)

        if self.movingForward:
            dx += speed_cos
            dy += speed_sin
        if self.movingBackward:
            dx += -speed_cos
            dy += -speed_sin
        if self.movingLeft:
            dx += speed_sin
            dy += -speed_cos
        if self.movingRight:
            dx += -speed_sin
            dy += speed_cos

        if not (dx == 0 and dy == 0):
            scale = PLAYER_SIZE_SCALE / self.game.delta_time
            if not self.game.map.is_wall(int(self.pos_x + dx * scale), int(self.pos_y)):
                self.pos_x += dx
            if not self.game.map.is_wall(int(self.pos_x), int(self.pos_y + dy * scale)):
                self.pos_y += dy
            # Calculate new angle
            self.angle %= math.tau

    # Getters
    @property
    def get_angle(self):
        return self.angle

    @property
    def get_pos(self):
        return self.pos_x, self.pos_y

    @property
    def get_map_pos(self):
        return int(self.pos_x), int(self.pos_y)

    # Setters
    def set_spawn(self, x, y):
        self.pos_x = x
        self.pos_y = y

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
            self.game.object_renderer.player_is_hit()
            self.game.sound.player_pain.play()
        else:
            self.game.set_state("Game over")

