from entity.npc.enemy_base import Enemy


class Zombie(Enemy):
    def __init__(self, game, pos):
        super().__init__(game, pos, [0, 0, 0])

        self.size = [0.6, 0.6]

        # Stats
        self.health = 20
        self.speed = 0.0006

        # Attack stats
        self.damage = 8  # How much damage should enemy do to player

        self.fire_cooldown = 10  # Cooldown before enemy can shoot again
        self.last_fire_time = 0  # Reset timer, when enemy fired

        self.bullet_in_gun = 9999  # How much enemy has bullet in gun at moment
        self.bullet_in_total = 9999  # How much enemy has bullet in total
        self.bullet_per_shot = 1  # How many bullets fired per shot
        self.bullet_after_reload = 999  # How many bullets should add after reload
        self.bullet_reset_amount = 999  # How many bullets should enemy have, after being empty
        self.reload_duration = 0  # How long should enemy reload

        # Features
        self.wandering_cooldown = (60 / self.speed / 30)
        self.can_detect_obstructed = True
        self.detect_range = 2  # Range on which enemy can detect player through walls ( if he has ability )

        # Animations
        path = "resources/sprites/npc/Zombie/"
        self.states = {
            "Idle": {
                "Frames": self.sprite_manager.load_single_image("Zombie Idle", path + "idle.png"),
                "Speed": 0
            },
            "Walk": {
                "Frames": self.sprite_manager.load_multiple_images("Zombie Walk", path + "Walk/"),
                "Speed": 200
            },
            "Attack": {
                "Frames": self.sprite_manager.load_multiple_images("Zombie Attack", path + "Attack/"),
                "Speed": 200,
                "Attack Speed": 600,
            },
            "Pain": {
                "Frames": self.sprite_manager.load_multiple_images("Zombie Pain", path + "Pain/"),
                "Speed": 300,
            },
            "Death": {
                "Frames": self.sprite_manager.load_multiple_images("Zombie Death", path + "Death/"),
                "Speed": 120,
            }
        }
        self.animation.load_sprite_animations(self.states)
        self.animation.change_animation("Idle")

        # Sounds
        self.sfx_attack = "Zombie attack"
        self.sfx_pain = "Zombie pain"
        self.sfx_death = "Zombie death"
