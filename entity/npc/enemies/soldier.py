from entity.npc.enemy_base import Enemy


class Soldier(Enemy):
    def __init__(self, game, pos, alive=True):
        super().__init__(game, pos, [0, 0, 0], alive)

        self.size = [0.6, 0.6]

        # Stats
        self.max_health = 50
        self.health = self.max_health if alive else 0

        self.speed = 0.002

        # Attack stats
        self.damage = 12  # How much damage should enemy do to player

        self.fire_cooldown = 40  # Cooldown before enemy can shoot again
        self.last_fire_time = 0  # Reset timer, when enemy fired

        self.bullet_in_gun = 6  # How much enemy has bullet in gun at moment
        self.bullet_in_total = 4  # How much enemy has bullet in total
        self.bullet_per_shot = 1  # How many bullets fired per shot
        self.bullet_after_reload = 4  # How many bullets should add after reload
        self.bullet_reset_amount = 6  # How many bullets should enemy have, after being empty
        self.reload_duration = 150  # How long should enemy reload
        self.is_reloading = False

        # Projectile stats
        self.projectile_size = [0.25, 0.25]
        self.projectile_sprite = "resources/sprites/projectile/projectile0.png"
        self.projectile_speed = 0.005
        self.projectile_lifetime = 2000

        # Features
        self.wandering_cooldown = (60 / self.speed / 30)
        self.attack_range = 6  # Range on which enemy starts to attack

        self.can_drop_ammo_on_death = True
        self.droppable_ammo = "Shotgun"
        self.ammo_dropped = False

        # Animations
        path = "resources/sprites/npc/Soldier/"
        self.states = {
            "Idle": {
                "Frames": self.sprite_manager.load_single_image("Soldier Idle", path + "idle.png"),
                "Speed": 0
            },
            "Walk": {
                "Frames": self.sprite_manager.load_multiple_images("Soldier Walk", path + "Walk/"),
                "Speed": 180
            },
            "Attack": {
                "Frames": self.sprite_manager.load_multiple_images("Soldier Attack", path + "Attack/"),
                "Speed": 300,
                "Attack Speed": 600,
            },
            "Pain": {
                "Frames": self.sprite_manager.load_multiple_images("Soldier Pain", path + "Pain/"),
                "Speed": 300,
            },
            "Death": {
                "Frames": self.sprite_manager.load_multiple_images("Soldier Death", path + "Death/"),
                "Speed": 120,
            }
        }
        self.animation.load_sprite_animations(self.states)
        self.animation.change_animation("Idle")
