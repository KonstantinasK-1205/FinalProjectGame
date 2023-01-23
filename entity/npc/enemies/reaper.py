from entity.npc.enemy_base import Enemy
import random


class Reaper(Enemy):
    def __init__(self, game, pos, alive=True):
        super().__init__(game, pos, [0, 0, 0], alive)

        # Position and scale
        self.pos[2] = random.uniform(0.3, 0.6)
        self.size = [0.6, 0.6]

        # Stats
        self.max_health = 200
        self.health = self.max_health if alive else 0
        self.speed = 0.002

        # Attack stats
        self.damage = 20  # How much damage should enemy do to player

        self.fire_cooldown = 20  # Cooldown before enemy can shoot again
        self.last_fire_time = 0  # Reset timer, when enemy fired

        self.bullet_in_gun = 9999  # How much enemy has bullet in gun at moment
        self.bullet_in_total = 9999  # How much enemy has bullet in total
        self.bullet_per_shot = 1  # How many bullets fired per shot
        self.bullet_after_reload = 999  # How many bullets should add after reload
        self.bullet_reset_amount = 999  # How many bullets should enemy have, after being empty
        self.reload_duration = 0  # How long should enemy reload

        # Projectile stats
        self.projectile_lifetime = 200

        # Features
        self.attack_range = 1

        self.wandering_cooldown = (60 / self.speed / 30)
        self.can_detect_obstructed = True
        self.detect_range = 3  # Range on which enemy can detect player through walls ( if he has ability )

        # Animations
        path = "resources/sprites/npc/Reaper/"
        self.states = {
            "Idle": {
                "Frames": self.sprite_manager.load_single_image("Reaper Idle", path + "idle.png"),
                "Speed": 0
            },
            "Walk": {
                "Frames": self.sprite_manager.load_multiple_images("Reaper Walk", path + "Walk/"),
                "Speed": 180
            },
            "Attack": {
                "Frames": self.sprite_manager.load_multiple_images("Reaper Attack", path + "Attack/"),
                "Speed": 140,
                "Attack Speed": 800,
            },
            "Pain": {
                "Frames": self.sprite_manager.load_multiple_images("Reaper Pain", path + "Pain/"),
                "Speed": 300,
            },
            "Death": {
                "Frames": self.sprite_manager.load_multiple_images("Reaper Death", path + "Death/"),
                "Speed": 120,
            },
            "Teleportation": {
                "Frames": self.sprite_manager.load_multiple_images("Reaper Teleportation", path + "Teleportation/"),
                "Speed": 150,
            }
        }
        self.animation.load_sprite_animations(self.states)
        self.animation.change_animation("Idle")

        # Sounds
        self.sfx_attack = "Reaper attack"
        self.sfx_pain = "Reaper pain"
        self.sfx_death = "Reaper death"
        self.sfx_teleportation = "Reaper teleportation"

        # Teleportation variables
        self.teleported = False
        self.teleportation_begin = False
        self.ready_for_teleportation = False
        self.last_teleportation_time = 0
        self.teleportation_cooldown = 2000
        self.last_attack = 0

        # Test
        self.revived_used = False

    def update(self):
        super().update()
        if self.alive and 50 < self.health < 180:
            if not self.revived_used:
                for enemy in self.game.object_handler.npc_list:
                    if not enemy.alive:
                        if self.distance_from(enemy) < 5:
                            enemy.alive = True
                            enemy.health = enemy.max_health
                            enemy.change_state("Death")
                self.revived_used = True
                self.game.object_handler.update_npc_list()

#    def movement(self):
#        # If teleported or player is further than 3 blocks
#        if self.distance_from_player > 3 or self.teleportation_begin:
#            self.change_state("Teleportation")
#        else:
#            super().movement()
#
#    def update(self):
#        super().update()
#        if self.alive:
#            if self.current_state == "Teleportation" and self.animation.completed:
#                self.teleport()
#                self.last_attack = pg.time.get_ticks()
#
#            if self.current_time - self.last_teleportation_time > self.teleportation_cooldown:
#                self.teleported = False
#
#            if self.current_time - self.last_attack > 6000 and 1 < self.distance_from_player < 3:
#                self.change_state("Teleportation")
#
#    def attack(self):
#        super().attack()
#        self.last_attack = pg.time.get_ticks()
#
#    def teleport(self):
#        while 1:
#            next_x = self.player.x - random.randint(-1, 1)
#            next_y = self.player.y - random.randint(-1, 1)
#            if not self.game.map.is_wall(next_x, next_y):
#                self.x = next_x
#                self.y = next_y
#                break
#
#        self.last_teleportation_time = pg.time.get_ticks()
#        self.game.sound.play_sfx(self.sfx_teleportation, [self.exact_pos, self.player.exact_pos])
#        self.angle = math.atan2(self.player.y - self.y, self.player.x - self.x)
#        self.teleported = True
#        self.teleportation_begin = False
#        self.ready_for_teleportation = False
#        self.change_state("Idle")
#
