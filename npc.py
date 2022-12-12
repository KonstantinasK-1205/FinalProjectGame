from settings import *
from sprites.animated_sprite import AnimatedSprite
from Bullet import *


class NPC(AnimatedSprite):
    def __init__(self, game, path='resources/sprites/npc/soldier/0.png', pos=(3, 3),
                 scale=0.6, shift=0.38, animation_time=180):
        super().__init__(game, path, pos, scale, shift, animation_time)
        self.attack_images = self.get_images(self.path + '/attack')
        self.death_images = self.get_images(self.path + '/death')
        self.idle_images = self.get_images(self.path + '/idle')
        self.pain_images = self.get_images(self.path + '/pain')
        self.walk_images = self.get_images(self.path + '/walk')

        self.attack_dist = random.randint(3, 6)
        self.speed = 0.03
        self.size = 50
        self.health = 100
        self.damage = random.randint(3, 10)
        self.accuracy = random.uniform(0.60, 0.80)
        self.alive = True
        self.pain = False
        self.ray_cast_value = False
        self.frame_counter = 0
        self.player_search_trigger = False
        self.death_animation_started = False
        self.angle = 0

    def update(self):
        self.check_animation_time()
        self.get_sprite()
        self.run_logic()

    def is_alive(self):
        return self.alive

    def movement(self):
        next_pos = self.game.pathfinding.get_path(self.map_pos, self.game.player.get_map_pos)
        next_x, next_y = next_pos
        if next_pos not in self.game.object_handler.npc_positions:
            dx = math.cos(self.angle) * self.speed
            dy = math.sin(self.angle) * self.speed

            if not self.game.map.is_wall(int(self.x + dx * self.size), int(self.y)):
                self.x += dx
            if not self.game.map.is_wall(int(self.x), int(self.y + dy * self.size)):
                self.y += dy
            self.angle = math.atan2(self.game.player.pos_y - self.y, self.game.player.pos_x - self.x)

    def attack(self):
        if self.animation_trigger:
            self.game.sound.play_sound(self.game.sound.npc_attack[random.randint(0, 1)],
                                       (self.x, self.y),
                                       self.game.player.get_pos)
           # if random.random() < self.accuracy:
            self.create_bullet()

    def create_bullet(self):
        print("Creating bullet on X: " + str(int(self.x)) + " | Y: " + str(int(self.y)))
        self.game.object_handler.add_bullet(Bullet(self.game, self.map_pos, self.damage, self.angle, 'enemy'))

    def animate_death(self):
        if not self.alive:
            if self.animation_trigger and self.frame_counter < len(self.death_images):
                self.death_animation_started = True
                self.death_images.rotate(-1)
                self.image = self.death_images[0]
                self.frame_counter += 1

    def animate_pain(self):
        self.animate(self.pain_images)
        if self.animation_trigger:
            self.pain = False

    def apply_damage(self, damage):
        self.pain = True
        self.health -= damage
        if self.health > 1:
            self.game.sound.play_sound(self.game.sound.npc_pain[random.randint(0, 2)],
                                       (self.x, self.y),
                                       self.game.player.get_pos)
        else:
            self.alive = False
            self.game.sound.play_sound(self.game.sound.npc_death[random.randint(0, 3)],
                                       (self.x, self.y),
                                       self.game.player.get_pos)

    def run_logic(self):
        if self.alive:
            self.ray_cast_value = self.ray_cast_player_npc()

            if self.pain:
                self.animate_pain()

            elif self.ray_cast_value:
                self.player_search_trigger = True

                if self.dist < self.attack_dist:
                    if random.randint(0, 30) < 10:
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

    @property
    def map_pos(self):
        return int(self.x), int(self.y)

    def ray_cast_player_npc(self):
        if self.game.player.get_map_pos == self.map_pos:
            return True

        wall_dist_v, wall_dist_h = 0, 0
        player_dist_v, player_dist_h = 0, 0

        ox, oy = self.game.player.get_pos
        x_map, y_map = self.game.player.get_map_pos

        ray_angle = self.theta

        sin_a = math.sin(ray_angle)
        cos_a = math.cos(ray_angle)

        # horizontals
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
            if tile_hor == self.map_pos:
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
            if tile_vert == self.map_pos:
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


class SoldierNPC(NPC):
    def __init__(self, game, path='resources/sprites/npc/soldier/0.png', pos=(10.5, 5.5),
                 scale=0.6, shift=0.38, animation_time=180):
        super().__init__(game, path, pos, scale, shift, animation_time)
