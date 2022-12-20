import math
import pygame as pg
from sprites.particle import *
from collision import *


class Bullet:
    def __init__(self, game, pos, damage, angle, angle_ver, owner, lifetime=50000):
        self.game = game
        self.player = game.player

        self.x = pos[0]
        self.y = pos[1]
        self.z = pos[2]
        self.width = 0.3
        self.height = 0.3
        self.angle = angle
        self.angle_ver = angle_ver
        self.speed = 0.012
        self.scale = 0.005
        self.owner = owner
        self.damage = damage

        self.delete = False
        self.time_alive = 0
        self.time_to_live = lifetime
        self.creation_time = pg.time.get_ticks()

    def update(self):
        # If bullet is alive for too long, delete it
        if self.time_alive >= self.time_to_live:
            self.delete = True
        else:
            # If fired by player, check collision with npc
            if self.owner == 'player':
                for enemy in self.game.object_handler.alive_npc_list:
                    if self.distance_from(enemy) < 0.3:
                        self.delete = True
                        enemy.apply_damage(self.damage, [self.game.weapon.current_weapon,
                                                         self.game.weapon.current_state])

            # If fired by enemy, check collision with player
            if self.owner == 'enemy':
                if self.distance_from(self.player) < 0.9:
                    self.delete = True
                    self.player.apply_damage(self.damage)

            # Calculate relative velocity for next frame
            dx = self.speed * math.cos(self.angle) * math.cos(self.angle_ver) * self.game.dt
            dy = self.speed * math.sin(self.angle) * math.cos(self.angle_ver) * self.game.dt
            dz = self.speed * math.sin(self.angle_ver) * self.game.dt

            # Check for collision
            res = resolve_collision(self.x, self.y, dx, dy, self.game.map, 0.01)

            if res.collided:
                if self.z < 1:
                    for i in range(5):
                        self.game.object_handler.add_sprite(Particle(self.game, (res.x, res.y, self.z), res.collided))

                    self.game.sound.play_sfx("Bullet in wall")
                self.delete = True

            self.x = res.x
            self.y = res.y

            self.z += dz

        # Update how long bullet is being alive
        self.time_alive = (pg.time.get_ticks() - self.creation_time)

    def distance_from(self, other):
        return math.hypot(other.x - self.x, other.y - self.y, other.z - self.z)
