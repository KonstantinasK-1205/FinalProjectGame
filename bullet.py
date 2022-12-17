import math
import pygame as pg


class Bullet:
    def __init__(self, game, pos, damage, angle, angle_ver, owner, lifetime=50000):
        self.game = game
        self.player = game.player

        self.x = pos[0]
        self.y = pos[1]
        self.z = 0
        self.width = 0.3
        self.height = 0.3
        self.angle = angle
        self.angle_ver = angle_ver
        self.speed = 0.012
        self.scale = 0.005
        self.owner = owner
        self.damage = damage

        self.collided = False
        self.time_alive = 0
        self.time_to_live = lifetime
        self.creation_time = pg.time.get_ticks()

    def update(self, dt):
        # If bullet alive for longer period than it should, count as collided
        if self.time_alive >= self.time_to_live:
            self.collided = True
        else:
            # If fired by player, check collision with npc
            if self.owner == 'player':
                for enemy in self.game.object_handler.alive_npc_list:
                    if self.distance_from(enemy) < 0.3:
                        self.collided = True
                        enemy.apply_damage(self.damage, [self.game.weapon.current_weapon,
                                                         self.game.weapon.current_state])

            # If fired by enemy, check collision with player
            if self.owner == 'enemy':
                if self.distance_from(self.player) < 0.9:
                    self.collided = True
                    self.player.apply_damage(self.damage)

            # Calculate relative velocity for next frame
            dx = self.speed * math.cos(self.angle) * math.cos(self.angle_ver) * dt
            dy = self.speed * math.sin(self.angle) * math.cos(self.angle_ver) * dt
            dz = self.speed * math.sin(self.angle_ver) * dt

            # Check collision with walls on X axis
            if not self.collision_with_wall((int(self.x + dx * self.scale), int(self.y))):
                self.x += dx

            # Check collision with walls on Y axis
            if not self.collision_with_wall((int(self.x), int(self.y + dy * self.scale))):
                self.y += dy

            self.z += dz

        # Update how long bullet is being alive
        self.time_alive = (pg.time.get_ticks() - self.creation_time)

    def collision_with_wall(self, pos):
        if self.game.map.is_wall(pos[0], pos[1]):
            self.game.sound.bullet_wall.play()
            self.collided = True
            return True
        return False

    def distance_from(self, other):
        return math.hypot(other.x - self.x, other.y - self.y, other.z - self.z)
