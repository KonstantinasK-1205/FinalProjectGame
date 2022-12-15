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
            if event.key == pg.K_TAB:
                if self.game.state["Game"].in_map:
                    self.game.state["Game"].in_map = False
                else:
                    self.game.state["Game"].init_mini_map()
                    self.game.state["Game"].in_map = True

            if event.key == pg.K_EQUALS:
                self.add_health(1)
            if event.key == pg.K_MINUS:
                self.apply_damage(1)

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
        self.rel = max(-MOUSE_MAX_REL, min(MOUSE_MAX_REL, pg.mouse.get_rel()[0]))
        self.angle = (self.angle + self.rel * MOUSE_SENSITIVITY * dt) % math.tau

        self.movement(dt)
        self.game.weapon.update()

    def movement(self, dt):
        speed = PLAYER_SPEED * dt
        speed_sin = speed * math.sin(self.angle)
        speed_cos = speed * math.cos(self.angle)

        new_x = self.pos_x
        new_y = self.pos_y
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
        if new_x < self.pos_x:
            if self.game.map.is_wall(new_x - playerRadius, self.pos_y - playerRadius) or \
               self.game.map.is_wall(new_x - playerRadius, self.pos_y + playerRadius):
                new_x = math.ceil(new_x - playerRadius) + playerRadius + margin
        elif new_x > self.pos_x:
            if self.game.map.is_wall(new_x + playerRadius, self.pos_y - playerRadius) or \
               self.game.map.is_wall(new_x + playerRadius, self.pos_y + playerRadius):
                new_x = math.floor(new_x + playerRadius) - playerRadius - margin

        # Next handle motion and collision in the Y axis
        if new_y < self.pos_y:
            if self.game.map.is_wall(new_x - playerRadius, new_y - playerRadius) or \
               self.game.map.is_wall(new_x + playerRadius, new_y - playerRadius):
                new_y = math.ceil(new_y - playerRadius) + playerRadius + margin
        elif new_y > self.pos_y:
            if self.game.map.is_wall(new_x - playerRadius, new_y + playerRadius) or \
               self.game.map.is_wall(new_x + playerRadius, new_y + playerRadius):
                new_y = math.floor(new_y + playerRadius) - playerRadius - margin

        self.pos_x = new_x
        self.pos_y = new_y

    # Getters
    @property
    def get_angle(self):
        return self.angle

    @property
    def exact_pos(self):
        return self.pos_x, self.pos_y

    @property
    def grid_pos(self):
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
            self.game.hit_flash_ms = 0
            self.game.sound.player_pain.play()
        else:
            self.game.current_state = "Game over"
