import math

import pygame as pg


class Bullet:
    def __init__(self, game, pos, damage, angle, owner, lifetime=50000):
        self.game = game
        self.player = game.player

        self.image = pg.image.load('resources/sprites/static_sprites/bullet.png').convert_alpha()

        self.pos_x = pos[0]
        self.pos_y = pos[1]
        self.angle = angle
        self.speed = 0.2
        self.scale = 0.005
        self.owner = owner
        self.damage = damage

        self.collided = False
        self.time_alive = 0
        self.time_to_live = lifetime
        self.creation_time = pg.time.get_ticks()

    def update(self):
        # If bullet alive for longer period than it should, count as collided
        if self.time_alive >= self.time_to_live:
            self.collided = True
        else:
            # If fired by player, check collision with npc
            if self.owner == 'player':
                for enemy in self.game.object_handler.alive_npc_list:
                    if abs(enemy.exact_pos[0] - self.pos_x) + abs(enemy.exact_pos[1] - self.pos_y) < 0.3:
                        self.collided = True
                        enemy.apply_damage(self.damage, [self.game.weapon.current_weapon,
                                                         self.game.weapon.current_state])

            # If fired by enemy, check collision with player
            if self.owner == 'enemy':
                # print(abs(self.player.exact_pos[0] - self.pos_x) + abs(self.player.exact_pos[1] - self.pos_y))
                if abs(self.player.exact_pos[0] - self.pos_x) + abs(self.player.exact_pos[1] - self.pos_y) < 0.9:
                    self.collided = True
                    self.player.apply_damage(self.damage)

            # Calculate relative velocity for next frame
            dx = self.speed * math.cos(self.angle)
            dy = self.speed * math.sin(self.angle)

            # Check collision with walls on X axis
            if not self.collision_with_wall((int(self.pos_x + dx * self.scale), int(self.pos_y))):
                self.pos_x += dx

            # Check collision with walls on Y axis
            if not self.collision_with_wall((int(self.pos_x), int(self.pos_y + dy * self.scale))):
                self.pos_y += dy

        # Update how long bullet is being alive
        self.time_alive = (pg.time.get_ticks() - self.creation_time)

    def collision_with_wall(self, pos):
        if self.game.map.is_wall(pos[0], pos[1]):
            self.game.sound.bullet_wall.play()
            self.collided = True
            return True
        return False
