from entity.npc.enemy_base import Enemy


class Pinky(Enemy):
    def __init__(self, game, pos, alive=True):
        super().__init__(game, pos, [0, 0, 0], alive)
        self.size = [0.6, 0.6]

        # Stats
        self.max_health = 450
        self.health = self.max_health if alive else 0
        self.speed = 0.003

        # Attack stats
        self.damage = 14  # How much damage should enemy do to player

        self.fire_cooldown = 5  # Cooldown before enemy can shoot again
        self.last_fire_time = 0  # Reset timer, when enemy fired

        self.bullet_in_gun = 9999  # How much enemy has bullet in gun at moment
        self.bullet_in_total = 9999  # How much enemy has bullet in total
        self.bullet_per_shot = 1  # How many bullets fired per shot
        self.bullet_after_reload = 999  # How many bullets should add after reload
        self.bullet_reset_amount = 999  # How many bullets should enemy have, after being empty
        self.reload_duration = 0  # How long should enemy reload

        # Projectile stats
        self.projectile_lifetime = 150

        # Features
        self.wandering_cooldown = (60 / self.speed / 30)
        self.can_detect_obstructed = True
        self.detect_range = 5  # Range on which enemy can detect player through walls ( if he has ability )

        # Animations
        path = "resources/sprites/npc/Pinky/"
        self.states = {
            "Idle": {
                "Frames": self.sprite_manager.load_single_image("Pinky Idle", path + "idle.png"),
                "Speed": 0
            },
            "Walk": {
                "Frames": self.sprite_manager.load_multiple_images("Pinky Walk", path + "Walk/"),
                "Speed": 120
            },
            "Attack": {
                "Frames": self.sprite_manager.load_multiple_images("Pinky Attack", path + "Attack/"),
                "Speed": 150,
                "Attack Speed": 900,
            },
            "Pain": {
                "Frames": self.sprite_manager.load_multiple_images("Pinky Pain", path + "Pain/"),
                "Speed": 150,
            },
            "Death": {
                "Frames": self.sprite_manager.load_multiple_images("Pinky Death", path + "Death/"),
                "Speed": 120,
            },
            "Stomp": {
                "Frames": self.sprite_manager.load_multiple_images("Pinky Stomp", path + "Stomp/"),
                "Speed": 400,
            }
        }
        self.animation.load_sprite_animations(self.states)
        self.animation.change_animation("Idle")
