from sprites.particle import *
from collision import *


class Projectile:
    def __init__(self, game, pos, angle, data, projectile=None):
        self.game = game
        self.player = game.player
        self.handler = self.game.object_handler

        self.pos = pos
        self.angle = angle

        # Data
        self.damage = data[0]
        self.speed = data[1]
        self.lifetime = data[2]
        self.owner = data[3]
        self.size = [data[4], data[5]]

        # Texture
        if projectile:
            self.sprite = projectile
        else:
            self.size = [0.02, 0.02]
            self.sprite = "resources/sprites/projectile/bullet.png"
        self.game.renderer.load_texture_from_file(self.sprite)

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

            # If fired by enemy, check collision with player
            if self.owner == 'Enemy':
                if self.collided_with(self.player):
                    self.player.apply_damage(self.damage)
                    self.delete = True

            # Check collision with sprite which have health
            for sprite in self.handler.sprite_list:
                if hasattr(sprite, 'health') and self.collided_with(sprite):
                    self.handler.add_sprite(Particle(self.game, self.pos, [0.05, 0.05], 1))
                    sprite.health -= self.damage
                    self.delete = True

            # Calculate cosine of vertical angle once per frame, for reusing
            angle = math.cos(self.angle[1])
            # Calculate relative velocity for next frame
            dx = self.speed * math.cos(self.angle[0]) * angle * self.game.dt
            dy = self.speed * math.sin(self.angle[0]) * angle * self.game.dt
            dz = self.speed * math.sin(self.angle[1]) * self.game.dt

            # Check for collision
            res = resolve_collision(self.pos, dx, dy, self.game.map, 0.01)
            if res.collided and self.pos[2] < 1:
                for i in range(5):
                    self.handler.add_sprite(
                        Particle(self.game, [res.pos[0], res.pos[1], self.pos[2] + dz + 0.3], [0.05, 0.05],
                                 res.collided))
                self.game.sound.play_sfx("Bullet in wall")
                self.delete = True

            self.pos = res.pos[:3]
            self.pos[2] += dz
        else:
            self.delete = True

    def collided_with(self, other):
        collision = [False, False, False]
        sprite_left = other.size[0] / 4
        sprite_right = other.size[0] / 3
        if other.pos[0] - sprite_left <= self.pos[0] + self.size[0] and other.pos[0] + sprite_right >= self.pos[0]:
            collision[0] = True
        if other.pos[1] - sprite_left <= self.pos[1] + self.size[0] and other.pos[1] + sprite_right >= self.pos[1]:
            collision[1] = True
        if other.pos[2] <= self.pos[2] <= other.pos[2] + other.size[1]:
            collision[2] = True
        return all(collision)
