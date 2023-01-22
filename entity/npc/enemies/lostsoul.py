from entity.npc.enemy_base import Enemy
import random


class LostSoul(Enemy):
    def __init__(self, game, pos, alive=True):
        super().__init__(game, pos, [0, 0, 0], alive)

        self.pos[2] = random.uniform(0.5, 0.8)
        self.size = [0.6, 0.6]

        # Primary stats
        self.max_health = 20
        self.health = self.max_health if alive else 0
        self.speed = 0.006

        # Attack stats
        self.damage = 35  # How much damage should enemy do to player

        self.fire_cooldown = 1  # Cooldown before enemy can shoot again
        self.last_fire_time = 0  # Reset timer, when enemy fired

        self.bullet_in_gun = 9999  # How much enemy has bullet in gun at moment
        self.bullet_in_total = 9999  # How much enemy has bullet in total
        self.bullet_per_shot = 1  # How many bullets fired per shot
        self.bullet_after_reload = 999  # How many bullets should add after reload
        self.bullet_reset_amount = 999  # How many bullets should enemy have, after being empty
        self.reload_duration = 0  # How long should enemy reload
        self.is_reloading = False

        # Features
        self.wandering_cooldown = (60 / self.speed / 30)
        self.attack_range = 1  # Range on which enemy starts to attack

        self.can_rush = True
        self.rushing_time = 0
        self.rushing_cooldown = 50
        self.rushing_stop_after = 100

        self.take_damage_on_attack = True
        self.damage_on_attack = 100

        # Animations
        path = "resources/sprites/npc/LostSoul/"
        self.states = {
            "Idle": {
                "Frames": self.sprite_manager.load_single_image("LostSoul Idle", path + "idle.png"),
                "Speed": 0
            },
            "Walk": {
                "Frames": self.sprite_manager.load_multiple_images("LostSoul Walk", path + "Walk/"),
                "Speed": 180
            },
            "Attack": {
                "Frames": self.sprite_manager.load_multiple_images("LostSoul Attack", path + "Attack/"),
                "Speed": 20,
                "Attack Speed": 100
            },
            "Pain": {
                "Frames": self.sprite_manager.load_multiple_images("LostSoul Pain", path + "Pain/"),
                "Speed": 300
            },
            "Death": {
                "Frames": self.sprite_manager.load_multiple_images("LostSoul Death", path + "Death/"),
                "Speed": 120
            }
        }
        self.animation.load_sprite_animations(self.states)
        self.animation.change_animation("Idle")
