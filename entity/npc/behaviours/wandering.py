from collision import *
from entity.npc.behaviours.behaviour import Behaviour
import math
import random


class Wandering(Behaviour):
    def __init__(self, game, enemy):
        super().__init__(game, enemy)
        self.wall_stick_time = 0
        self.wall_stick_stop = 100

    def movement(self, destination=None):
        # Set angle only once per wandering interval
        if self.enemy.is_wandering and self.enemy.wandering_time == 0:
            self.new_trajectory()

        # Handle collision and move
        res = resolve_collision(self.enemy.pos,
                                self.enemy.dx,
                                self.enemy.dy,
                                self.game.map,
                                0.15)
        if res.collided:
            self.wall_stick_time += self.game.dt
            if self.wall_stick_time >= self.wall_stick_stop:
                self.new_trajectory()
                self.wall_stick_time = 0
        self.enemy.pos = res.pos[:3]

    def update(self):
        # Disable wandering after N time
        if self.enemy.is_wandering:
            self.enemy.wandering_time += self.game.dt
            if self.enemy.wandering_time > self.enemy.wandering_cooldown:
                self.enemy.wandering_time = 0
                self.enemy.is_wandering = False

    def new_trajectory(self):
        angle = math.radians(360 * random.random())

        # Calculate moving direction
        self.enemy.dx = math.cos(angle) * self.enemy.speed * self.game.dt
        self.enemy.dy = math.sin(angle) * self.enemy.speed * self.game.dt
