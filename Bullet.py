from sprites.sprite import Sprite
import pygame as pg
import math


class Bullet:
    def __init__(self, game, pos, damage, angle, owner):
        self.game = game
        self.pos_x = pos[0]
        self.pos_y = pos[1]
        self.damage = damage
        self.angle = angle
        self.owner = owner

        self.image = pg.image.load('resources/sprites/static_sprites/bullet.png').convert_alpha()
        self.speed = 0.1
        self.scale = 0.0005
        self.collided = False

    def update(self):
        dx, dy = 0, 0
        dx += self.speed * math.cos(self.angle)
        dy += self.speed * math.sin(self.angle)

        # Check collision with npc
        if self.owner == 'player':
            for enemy in self.game.object_handler.alive_npc_list:
                if enemy.map_pos == (int(self.pos_x), int(self.pos_y)):
                    self.collided = True
                    enemy.apply_damage(self.damage)
        # Check collision with player
        if self.owner == 'enemy':
            if self.game.player.get_map_pos == (int(self.pos_x), int(self.pos_y)):
                self.collided = True
                self.game.player.apply_damage(self.damage)

        # Check collision with walls
        if not self.collision_with_wall((int(self.pos_x + dx * self.scale), int(self.pos_y))):
            self.pos_x += dx
        if not self.collision_with_wall((int(self.pos_x), int(self.pos_y + dy * self.scale))):
            self.pos_y += dy

    def collision_with_wall(self, pos):
        if not self.game.map.is_wall(pos[0], pos[1]):
            return False
        self.collided = True
        return True
