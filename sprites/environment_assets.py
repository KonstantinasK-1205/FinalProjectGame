from sprites.sprite import Sprite
import random


class Tree(Sprite):
    def __init__(self, game, pos, scale=None):
        if not scale:
            variety = random.randint(0, 5) / 10
            scale = [0.7 + variety, 1.3 + variety]
        super().__init__(game, pos, scale)
        self.load_texture("resources/sprites/environment/tree0.png")


class BigTorch(Sprite):
    def __init__(self, game, pos, scale=None):
        if not scale:
            scale = [0.3, 0.8]
        super().__init__(game, pos, scale)
        self.spritesheet = self.load_image("resources/sprites/environment/torch_big.png")
        self.current_animation = "Idle"
        self.animations = {
            "Idle": {
                "Frames": super().images_at("Big Torch Idle",
                                            [(0, 0, 48, 159),
                                             (48, 0, 48, 159),
                                             (96, 0, 48, 159),
                                             (144, 0, 48, 159)]),
                "Counter": 0,
                "Animation Speed": 140,
                "Animation Completed": False
            }
        }


class SmallTorch(Sprite):
    def __init__(self, game, pos, scale=None):
        if not scale:
            scale = [0.5, 0.6]
        super().__init__(game, pos, scale)
        self.spritesheet = self.load_image("resources/sprites/environment/torch_small.png")
        self.current_animation = "Idle"
        self.animations = {
            "Idle": {
                "Frames": super().images_at("Small Torch Idle",
                                            [(0, 0, 48, 64),
                                             (48, 0, 48, 64),
                                             (96, 0, 48, 64),
                                             (144, 0, 48, 64)]),
                "Counter": 0,
                "Animation Speed": 180,
                "Animation Completed": False
            }
        }


class Corpse(Sprite):
    def __init__(self, game, pos, scale=None):
        if not scale:
            scale = [0.35, 0.25]
        super().__init__(game, pos, scale)
        corpse_sprite = random.randint(0, 2)
        self.load_texture("resources/sprites/environment/corpse" + str(corpse_sprite) + ".png")
