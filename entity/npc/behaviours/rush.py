from collision import *
from entity.npc.behaviours.behaviour import Behaviour


class Rush(Behaviour):
    def __init__(self, game, enemy):
        super().__init__(game, enemy)
        self.need_rest = False
        self.rush_stop_after = None

    def movement(self, destination=None):
        if not self.need_rest:
            # Calculate rush trajectory only once
            if not self.enemy.is_rushing:
                self.enemy.is_rushing = True
                self.enemy.dash_time = 0
                self.enemy.dx = math.cos(self.enemy.angle) * self.enemy.speed * self.game.dt
                self.enemy.dy = math.sin(self.enemy.angle) * self.enemy.speed * self.game.dt

            # Handle collision and move
            self.enemy.pos = resolve_collision(self.enemy.pos,
                                               self.enemy.dx,
                                               self.enemy.dy,
                                               self.game.map,
                                               0.15)[0]

    def update(self):
        # If enemy need rest, let him rest, without moving him
        if self.need_rest and self.enemy.rushing_time <= self.enemy.rushing_cooldown:
            self.enemy.rushing_time += self.game.dt
            return
        elif self.need_rest and self.enemy.rushing_time >= self.enemy.rushing_cooldown:
            self.need_rest = False
            self.enemy.rushing_time = 0
            return

        # Disable rush after N time
        if self.enemy.can_rush and self.enemy.is_rushing and not self.need_rest:
            self.enemy.rushing_time += self.game.dt
            if self.rush_stop_after is None:
                self.rush_stop_after = self.enemy.distance_from_player * 10
            # Set rushing timer based on distance between enemy and player
            if self.enemy.rushing_time > self.rush_stop_after:
                self.enemy.rushing_time = 0
                self.rush_stop_after = None
                self.enemy.is_rushing = False
                self.need_rest = True
