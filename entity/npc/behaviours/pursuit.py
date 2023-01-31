from collision import *
from entity.npc.behaviours.behaviour import Behaviour
from pathfinding import *
import random


class Pursuit(Behaviour):
    def __init__(self, game, enemy):
        super().__init__(game, enemy)

    def movement(self, destination):
        if not self.enemy.in_pursuit:
            return

        # If the player cannot be seen, find the path to the last known player
        # position and set the angle towards it
        if not self.enemy.seeing_player:
            self.next_pos = find_path(self.enemy.exact_pos, self.enemy.last_known_pos, self.game.map)
            next_x = self.next_pos[0] + 0.5
            next_y = self.next_pos[1] + 0.5

            self.enemy.angle = math.atan2(next_y - self.enemy.pos[1], next_x - self.enemy.pos[0])

        # Calculate the velocity for motion
        self.enemy.dx = math.cos(self.enemy.angle) * self.enemy.speed * self.game.dt
        self.enemy.dy = math.sin(self.enemy.angle) * self.enemy.speed * self.game.dt

        # Handle collision and move the NPC
        self.enemy.pos = resolve_collision(self.enemy.pos, self.enemy.dx, self.enemy.dy, self.game.map, 0.15)[0]

    def update(self):
        pass
