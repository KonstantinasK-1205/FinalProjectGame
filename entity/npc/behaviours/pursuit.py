from collision import *
from entity.npc.behaviours.behaviour import Behaviour


class Pursuit(Behaviour):
    def __init__(self, game, enemy):
        super().__init__(game, enemy)

    def movement(self, destination):
        # If Enemy see player or enemy saw player before disappearing, move toward last know position
        if self.enemy.seeing_player or self.enemy.in_pursuit:
            if int(self.enemy.pos[0]) == self.enemy.last_known_pos[0] and int(self.enemy.pos[1]) == \
                    self.enemy.last_known_pos[1]:
                self.enemy.in_pursuit = False
                return

            next_pos = self.game.pathfinding.get_path(self.enemy.exact_pos, destination)
            next_x = next_pos[0] + 0.5
            next_y = next_pos[1] + 0.5

            # Update velocity only if pathfinding gave correct result
            if math.hypot(next_x - self.enemy.pos[0], next_y - self.enemy.pos[1]) < 2:
                self.enemy.angle = math.atan2(next_y - self.enemy.pos[1], next_x - self.enemy.pos[0])

            # Calculate the NPC moving direction based on upper conditions
            self.enemy.dx = math.cos(self.enemy.angle) * self.enemy.speed * self.game.dt
            self.enemy.dy = math.sin(self.enemy.angle) * self.enemy.speed * self.game.dt

            # Handle collision and move NPC
            res = resolve_collision(self.enemy.pos, self.enemy.dx, self.enemy.dy, self.game.map, 0.15)
            self.enemy.pos = res.pos[:3]

    def update(self):
        pass
