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
