from sprites.particle import *
from collision import *


class Projectile:
    def __init__(self, game, pos, angle, data, projectile=None):
        # Init all object variables and functions, for faster access time in loops
        self.game = game
        self.map = game.map

        self.player = game.player
        self.handler = self.game.object_handler

        # Projectile pos and angle
        self.pos = pos
        self.angle = angle

        # Data
        self.damage = data[0]
        self.speed = data[1]
        self.lifetime = data[2]
        self.owner = data[3]
        self.size = data[4]

        # Texture
        if projectile:
            path = projectile
        else:
            path = "resources/sprites/projectile/bullet.png"
            self.size = [0.02, 0.02]

        self.sprite = self.game.sprite_manager.load_single_image(path, path)[0]
        self.delete = False
        self.alive = 0

    def draw(self):
        self.game.renderer.draw_sprite(self.pos, self.size, self.sprite)

    def update(self):
        self.alive += self.game.dt
        if self.alive < self.lifetime:
            # If fired by player, check collision with npc
            if self.owner == 'Player':
                for enemy in self.handler.alive_npc_list:
                    if self.collided_with(enemy):
                        enemy.apply_damage(self.damage)
                        self.delete = True
                        return

            # If fired by enemy, check collision with player
            if self.owner == 'Enemy' and self.collided_with(self.player):
                self.player.apply_damage(self.damage)
                self.delete = True
                return

            # Check collision with sprite which have health
            for sprite in self.handler.interactive_sprite_list:
                if self.collided_with(sprite):
                    self.handler.add_sprite(Particle(self.game, self.pos, [0.05, 0.05], 1))
                    sprite.health -= self.damage
                    self.delete = True
                    return

            # Calculate cosine of vertical angle once per frame, for reusing
            angle = math.cos(self.angle[1]) * self.game.dt
            # Calculate relative velocity for next frame
            dx = self.speed * math.cos(self.angle[0]) * angle
            dy = self.speed * math.sin(self.angle[0]) * angle
            dz = self.speed * math.sin(self.angle[1]) * self.game.dt

            # Check for collision
            self.pos, collided = resolve_collision(self.pos, dx, dy, self.map, 0.01)
            if collided and self.pos[2] < 1:
                for i in range(5):
                    self.handler.add_sprite(
                        Particle(self.game, [self.pos[0], self.pos[1], self.pos[2] + dz + 0.3], [0.05, 0.05], collided))
                self.game.sound.play_sfx("Bullet in wall")
                self.delete = True
                return

            self.pos[2] += dz
        else:
            self.delete = True

    def collided_with(self, other):
        collision = [False, False, False]
        other_left = other.size[0] / 4
        other_right = other.size[0] / 3

        if other.pos[0] - other_left <= self.pos[0] + self.size[0] and other.pos[0] + other_right >= self.pos[0]:
            collision[0] = True
        if other.pos[1] - other_left <= self.pos[1] + self.size[0] and other.pos[1] + other_right >= self.pos[1]:
            collision[1] = True
        if other.pos[2] <= self.pos[2] <= other.pos[2] + other.size[1]:
            collision[2] = True
        return all(collision)
