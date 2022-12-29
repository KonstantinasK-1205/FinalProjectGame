from sprites.particle import *
from collision import *


class Projectile:
    def __init__(self, game, pos, angle, data, projectile=None):
        self.game = game
        self.player = game.player
        self.handler = self.game.object_handler

        # Position
        self.x = pos[0]
        self.y = pos[1]
        self.z = pos[2]

        # Angle
        self.angle_hor = angle[0]
        self.angle_ver = angle[1]

        # Data
        self.damage = data[0]
        self.speed = data[1]
        self.lifetime = data[2]
        self.owner = data[3]
        self.width = data[4]
        self.height = data[5]

        # Texture
        if projectile:
            self.texture_path = projectile
        else:
            self.width = 0.02
            self.height = 0.02
            self.texture_path = "resources/sprites/projectile/bullet.png"
        self.game.renderer.load_texture_from_file(self.texture_path)

        self.delete = False
        self.alive = 0

    def draw(self):
        self.game.renderer.draw_sprite(self.x, self.y, self.z, self.width, self.height, self.texture_path)

    def update(self):
        self.alive += self.game.dt
        if self.alive < self.lifetime:
            # If fired by player, check collision with npc
            if self.owner == 'Player':
                for enemy in self.handler.alive_npc_list:
                    if self.collided_with(enemy):
                        if 'Pinky' in str(type(enemy)) and enemy.avoid_bullet():
                            self.damage = 0
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
                    self.handler.add_sprite(Particle(self.game, (self.x, self.y, self.z), [0.05, 0.05], 1))
                    sprite.health -= self.damage
                    self.delete = True

            # Calculate cosine of vertical angle once per frame, for reusing
            cos_angle_ver = math.cos(self.angle_ver)
            # Calculate relative velocity for next frame
            dx = self.speed * math.cos(self.angle_hor) * cos_angle_ver * self.game.dt
            dy = self.speed * math.sin(self.angle_hor) * cos_angle_ver * self.game.dt
            dz = self.speed * math.sin(self.angle_ver) * self.game.dt

            # Check for collision
            res = resolve_collision(self.x, self.y, dx, dy, self.game.map, 0.01)
            if res.collided and self.z < 1:
                for i in range(5):
                    self.handler.add_sprite(
                        Particle(self.game, (res.x, res.y, self.z - dz), [0.05, 0.05], res.collided))
                self.game.sound.play_sfx("Bullet in wall")
                self.delete = True

            self.x = res.x
            self.y = res.y
            self.z += dz
        else:
            self.delete = True

    def collided_with(self, other):
        collision = [False, False, False]
        if other.x - (other.width / 4) <= self.x + self.width and other.x + (other.width / 3) >= self.x:
            collision[0] = True
        if other.y - (other.width / 4) <= self.y + self.width and other.y + (other.width / 3) >= self.y:
            collision[1] = True
        if other.z <= self.z <= other.z + other.height:
            collision[2] = True
        return all(collision)
