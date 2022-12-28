from npc.npc import NPC


class Zombie(NPC):
    def __init__(self, game, pos):
        super().__init__(game, pos, [0.6])

        # Base stats
        self.health = 20
        self.speed = 0.0006

        # Attack stats
        self.damage = 8

        # Sounds
        self.sfx_attack = "Zombie attack"
        self.sfx_pain = "Zombie pain"
        self.sfx_death = "Zombie death"

        # Animations
        self.spritesheet = self.load_image("resources/sprites/npc/Zombie_Spritesheet.png")
        self.current_animation = "Idle"
        self.animations = {
            "Idle": {
                "Frames": self.images_at("Zombie_Idle",
                                         [(0, 0, 64, 64)]),
                "Counter": 0,
                "Animation Speed": 180,
                "Animation Completed": False,
            },
            "Walk": {
                "Frames": self.images_at("Zombie_Walk",
                                         [(0, 64, 64, 64),
                                          (64, 64, 64, 64),
                                          (128, 64, 64, 64),
                                          (192, 64, 64, 64)]),
                "Counter": 0,
                "Animation Speed": 180,
                "Animation Completed": False,
            },
            "Attack": {
                "Frames": self.images_at("Zombie_Attack",
                                         [(0, 128, 64, 64),
                                          (64, 128, 64, 64),
                                          (128, 128, 64, 64)]),
                "Counter": 0,
                "Animation Speed": 200,
                "Attack Speed": 600,
                "Animation Completed": False,
            },
            "Pain": {
                "Frames": self.images_at("Zombie_Pain",
                                         [(0, 192, 64, 64)]),
                "Counter": 0,
                "Animation Speed": 300,
                "Animation Completed": False,
            },
            "Death": {
                "Frames": self.images_at("Zombie_Death",
                                         [(0, 256, 64, 64),
                                          (64, 256, 64, 64),
                                          (128, 256, 64, 64),
                                          (192, 256, 64, 64),
                                          (256, 256, 64, 64)]),
                "Counter": 0,
                "Animation Speed": 120,
                "Animation Completed": False,
            }
        }
