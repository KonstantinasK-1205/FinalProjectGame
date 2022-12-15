from Bullet import *
from settings import *
from sprites.animated_sprite import AnimatedSprite
import random


class NPC(AnimatedSprite):
    def __init__(self, game, path='resources/sprites/npc/soldier/0.png', pos=(3, 3),
                 scale=0.6, shift=0.38, animation_time=180):
        super().__init__(game, path, pos, scale, shift, animation_time)

        self.width = 0.3
        self.height = 0.6
        self.z = -0.05

        # NPC base stats
        self.pain = False
        self.alive = True
        self.health = 100
        self.speed = 0.03
        self.damage = 0
        self.attack_dist = 0
        self.shoot_delay = 250
        self.bullet_lifetime = 0

        # NPC animation variables
        self.frame_counter = 0
        self.attack_images = self.get_images(self.path + '/attack')
        self.death_images = self.get_images(self.path + '/death')
        self.idle_images = self.get_images(self.path + '/idle')
        self.pain_images = self.get_images(self.path + '/pain')
        self.walk_images = self.get_images(self.path + '/walk')

        self.size = 50
        self.ray_cast_value = False
        self.player_search_trigger = False
        self.angle = 0
        self.current_time = 0
        self.previous_shot = 0

    def update(self):
        self.current_time = pg.time.get_ticks()
        self.check_animation_time()
        self.run_logic()

    def run_logic(self):
        if self.alive:
            self.ray_cast_value = self.ray_cast_player_npc()

            if self.pain:
                self.animate_pain()

            elif self.ray_cast_value:
                self.player_search_trigger = True

                dist = math.hypot(self.x - self.player.pos_x, self.y - self.player.pos_y)
                if dist < self.attack_dist:
                    if self.current_time - self.previous_shot > self.shoot_delay * 5:
                        self.animate(self.attack_images)
                        self.attack()
                else:
                    self.animate(self.walk_images)
                    self.movement()

            elif self.player_search_trigger:
                self.animate(self.walk_images)
                self.movement()

            else:
                self.animate(self.idle_images)
        else:
            self.animate_death()

    # Attack
    def attack(self):
        if self.animation_trigger:
            self.create_bullet()
            self.game.sound.play_sound(self.game.sound.npc_attack[random.randint(0, 1)],
                                       self.grid_pos, self.player.exact_pos)
            self.previous_shot = pg.time.get_ticks()

    def create_bullet(self):
        # Add damage reduction based on how far Player from npc
        distance = abs(self.player.grid_pos[0] - self.grid_pos[0]) + abs(self.player.grid_pos[1] - self.grid_pos[1])
        if self.damage > distance:
            damage = int(self.damage - distance)
        else:
            damage = 0
        # Calculate enemy angle, so bullet flies exactly where NPC is looking
        angle = math.atan2(self.player.grid_pos[1] - self.grid_pos[1],
                           self.player.grid_pos[0] - self.grid_pos[0])
        self.game.object_handler.add_bullet(Bullet(self.game, self.grid_pos,
                                                   damage, angle, 'enemy', self.bullet_lifetime))

    def apply_damage(self, damage):
        self.pain = True
        self.health -= damage
        if self.health > 1:
            self.game.sound.play_sound(self.game.sound.npc_pain[random.randint(0, 2)],
                                       self.grid_pos, self.player.grid_pos)
        else:
            self.alive = False
            self.game.sound.play_sound(self.game.sound.npc_death[random.randint(0, 3)],
                                       self.grid_pos, self.player.grid_pos)

    # Movement
    def movement(self):
        next_pos = self.game.pathfinding.get_path(self.grid_pos, self.player.grid_pos)
        if next_pos not in self.game.object_handler.npc_positions:
            dx = math.cos(self.angle) * self.speed
            dy = math.sin(self.angle) * self.speed

            if not self.game.map.is_wall(int(self.x + dx * self.size), int(self.y)):
                self.x += dx
            if not self.game.map.is_wall(int(self.x), int(self.y + dy * self.size)):
                self.y += dy
            self.angle = math.atan2(self.player.exact_pos[1] - self.exact_pos[1],
                                    self.player.exact_pos[0] - self.exact_pos[0])

    # Animations
    def animate_pain(self):
        self.animate(self.pain_images)
        if self.animation_trigger:
            self.pain = False

    def animate_death(self):
        if self.is_dead:
            if self.animation_trigger and self.frame_counter < len(self.death_images) - 1:
                self.frame_counter += 1
                self.death_images.rotate(-1)
                self.texture_path = self.death_images[0]

    # Ray casting
    def ray_cast_player_npc(self):
        if self.player.grid_pos == self.grid_pos:
            return True

        wall_dist_v, wall_dist_h = 0, 0
        player_dist_v, player_dist_h = 0, 0

        ox, oy = self.player.exact_pos
        x_map, y_map = self.player.grid_pos

        ray_angle = math.atan2(self.y - self.player.pos_y, self.x - self.player.pos_x)

        sin_a = math.sin(ray_angle)
        cos_a = math.cos(ray_angle)

        # Horizontals
        y_hor, dy = (y_map + 1, 1) if sin_a > 0 else (y_map - 1e-6, -1)

        # Fixes crash, when Sin reaches 0, game crashes, this one line fix it
        if sin_a == 0.0:
            sin_a = 0.0000000000001
        depth_hor = (y_hor - oy) / sin_a
        x_hor = ox + depth_hor * cos_a

        delta_depth = dy / sin_a
        dx = delta_depth * cos_a

        for i in range(MAX_DEPTH):
            tile_hor = int(x_hor), int(y_hor)
            if tile_hor == self.grid_pos:
                player_dist_h = depth_hor
                break
            if tile_hor in self.game.map.world_map:
                wall_dist_h = depth_hor
                break
            x_hor += dx
            y_hor += dy
            depth_hor += delta_depth

        # Verticals
        x_vert, dx = (x_map + 1, 1) if cos_a > 0 else (x_map - 1e-6, -1)

        depth_vert = (x_vert - ox) / cos_a
        y_vert = oy + depth_vert * sin_a

        delta_depth = dx / cos_a
        dy = delta_depth * sin_a

        for i in range(MAX_DEPTH):
            tile_vert = int(x_vert), int(y_vert)
            if tile_vert == self.grid_pos:
                player_dist_v = depth_vert
                break
            if tile_vert in self.game.map.world_map:
                wall_dist_v = depth_vert
                break
            x_vert += dx
            y_vert += dy
            depth_vert += delta_depth

        player_dist = max(player_dist_v, player_dist_h)
        wall_dist = max(wall_dist_v, wall_dist_h)

        if 0 < player_dist < wall_dist or not wall_dist:
            return True
        return False

    # Getters
    @property
    def exact_pos(self):
        return self.x, self.y

    @property
    def grid_pos(self):
        return int(self.x), int(self.y)

    @property
    def is_alive(self):
        return self.alive

    @property
    def is_dead(self):
        return not self.alive
