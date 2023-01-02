from npc.npc import NPC


class Soldier(NPC):
    def __init__(self, game, pos):
        super().__init__(game, pos, [0.6])

        # Primary stats
        self.health = 50
        self.speed = 0.002

        # Attack Stats
        self.damage = 12
        self.attack_distance = 6
        self.bullet_width = 0.5
        self.bullet_height = 0.5
        self.bullet_sprite = "resources/sprites/projectile/projectile0.png"
        self.bullet_speed = 0.005
        self.bullet_lifetime = 2000

        self.reaction_time = 1000

        # Animations
        sprite = self.game.sprite_manager
        path = "resources/sprites/npc/Soldier/"
        self.states = {
            "Idle": {
                "Frames": sprite.load_single_image("Soldier Idle", path + "idle.png"),
                "Speed": 0
            },
            "Walk": {
                "Frames": sprite.load_multiple_images("Soldier Walk", path + "Walk/"),
                "Speed": 180
            },
            "Attack": {
                "Frames": sprite.load_multiple_images("Soldier Attack", path + "Attack/"),
                "Speed": 300,
                "Attack Speed": 600,
            },
            "Pain": {
                "Frames": sprite.load_multiple_images("Soldier Pain", path + "Pain/"),
                "Speed": 300,
            },
            "Death": {
                "Frames": sprite.load_multiple_images("Soldier Death", path + "Death/"),
                "Speed": 120,
            }
        }
        self.animation.load_sprite_animations(self.states)
        self.animation.change_animation("Idle")
