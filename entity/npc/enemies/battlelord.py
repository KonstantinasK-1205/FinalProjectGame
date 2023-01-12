from entity.npc.enemy_base import Enemy


class Battlelord(Enemy):
    def __init__(self, game, pos):
        super().__init__(game, pos, [0, 0, 0])

        # Position and scale
        self.size = [0.8, 0.9]

        # Stats
        self.health = 2200
        self.speed = 0.003

        # Attack stats
        self.damage = 10  # How much damage should enemy do to player

        self.fire_cooldown = 0  # Cooldown before enemy can shoot again
        self.last_fire_time = 0  # Reset timer, when enemy fired

        self.bullet_in_gun = 360  # How much enemy has bullet in gun at moment
        self.bullet_in_total = 1080  # How much enemy has bullet in total
        self.bullet_per_shot = 1  # How many bullets fired per shot
        self.bullet_after_reload = 1080  # How many bullets should add after reload
        self.bullet_reset_amount = 1080  # How many bullets should enemy have, after being empty
        self.reload_duration = 700  # How long should enemy reload

        # Projectile stats
        self.projectile_lifetime = 2000
        self.projectile_spread = [0.2, 0.2]  # Projectile spread from origin
        self.projectile_size = [0.01, 0.01]
        self.projectile_sprite = "resources/sprites/projectile/bullet.png"

        # Features
        self.attack_range = 8
        self.vision_range = 40

        self.wandering_cooldown = (60 / self.speed / 30)
        self.can_detect_obstructed = True
        self.detect_range = 3  # Range on which enemy can detect player through walls ( if he has ability )

        # Animations
        path = "resources/sprites/npc/Battlelord/"
        self.states = {
            "Idle": {
                "Frames": self.sprite_manager.load_single_image("Battlelord Idle", path + "idle.png"),
                "Speed": 0
            },
            "Walk": {
                "Frames": self.sprite_manager.load_multiple_images("Battlelord Walk", path + "Walk/"),
                "Speed": 180
            },
            "Attack": {
                "Frames": self.sprite_manager.load_multiple_images("Battlelord Attack", path + "Attack/"),
                "Speed": 10,
                "Attack Speed": 200
            },
            "Pain": {
                "Frames": self.sprite_manager.load_multiple_images("Battlelord Pain", path + "Pain/"),
                "Speed": 450
            },
            "Death": {
                "Frames": self.sprite_manager.load_multiple_images("Battlelord Death", path + "Death/"),
                "Speed": 200
            }
        }
        self.animation.load_sprite_animations(self.states)
        self.animation.change_animation("Idle")

        # Sound variables
        self.sfx_attack = "Battlelord attack"
        self.sfx_pain = "Battlelord pain"
        self.sfx_death = "Battlelord death"
