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

        # Animation variables
        self.spritesheet = self.load_image("resources/sprites/npc/Soldier_Spritesheet.png")
        self.current_animation = "Idle"
        self.animations = {
            "Idle": {
                "Frames": self.images_at("Soldier_Idle",
                                         [(0, 0, 64, 64)]),
                "Counter": 0,
                "Animation Speed": 180,
                "Animation Completed": False,
            },
            "Walk": {
                "Frames": self.images_at("Soldier_Walk",
                                         [(0, 64, 64, 64),
                                          (64, 64, 64, 64),
                                          (128, 64, 64, 64),
                                          (192, 64, 64, 64)]),
                "Counter": 0,
                "Animation Speed": 180,
                "Animation Completed": False,
            },
            "Attack": {
                "Frames": self.images_at("Soldier_Attack",
                                         [(0, 256, 64, 64),
                                          (64, 256, 64, 64)]),
                "Counter": 0,
                "Animation Speed": 400,
                "Attack Speed": 800,
                "Animation Completed": False,
            },
            "Pain": {
                "Frames": self.images_at("Soldier_Pain",
                                         [(0, 320, 64, 64)]),
                "Counter": 0,
                "Animation Speed": 300,
                "Animation Completed": False,
            },
            "Death": {
                "Frames": self.images_at("Soldier_Death",
                                         [(0, 384, 64, 64),
                                          (64, 384, 64, 64),
                                          (128, 384, 64, 64),
                                          (192, 384, 64, 64),
                                          (256, 384, 64, 64),
                                          (320, 384, 64, 64)]),
                "Counter": 0,
                "Animation Speed": 120,
                "Animation Completed": False,
            }
        }
