from sprites.sprite import Sprite
from sprites.animation_manager import *
import random


class Tree(Sprite):
    def __init__(self, game, pos):
        variety = random.randint(0, 8) / 10
        super().__init__(game, pos, [0.7 + variety, 1.3 + variety])
        self.load_texture("resources/sprites/environment/tree0.png")


class BigTorch(Sprite):
    def __init__(self, game, pos):
        super().__init__(game, pos, [0.3, 0.8])
        self.animation = Animation()
        self.spritesheet = self.load_image("resources/sprites/environment/torch_big.png")
        self.current_animation = "Idle"
        self.animations = {
            "Idle": {
                "Frames": super().images_at("Big Torch Idle",
                                            [(0, 0, 48, 159),
                                             (48, 0, 48, 159),
                                             (96, 0, 48, 159),
                                             (144, 0, 48, 159)]),
                "Speed": 140,
            }
        }
        self.animation.load_sprite_animations(self.animations)
        self.animation.change_animation("Idle")
        self.sprite = self.animation.get_sprite()

    def update(self):
        self.animation.animate(self.game.dt)
        if self.animation.completed:
            self.animation.change_animation("Idle")

        self.current_state = self.animation.get_state()
        self.sprite = self.animation.get_sprite()

    def draw(self):
        self.game.renderer.draw_sprite(self.x, self.y, self.z, self.width, self.height, self.sprite)


class SmallTorch(BigTorch):
    def __init__(self, game, pos):
        super().__init__(game, pos)
        self.width = 0.5
        self.height = 0.6
        self.spritesheet = self.load_image("resources/sprites/environment/torch_small.png")
        self.animations = {
            "Idle": {
                "Frames": super().images_at("Small Torch Idle",
                                            [(0, 0, 48, 64),
                                             (48, 0, 48, 64),
                                             (96, 0, 48, 64),
                                             (144, 0, 48, 64)]),
                "Speed": 180,
            }
        }
        self.animation.load_sprite_animations(self.animations)
        self.animation.change_animation("Idle")
        self.sprite = self.animation.get_sprite()


class Corpse(Sprite):
    def __init__(self, game, pos):
        super().__init__(game, pos, [0.35, 0.25])
        corpse_sprite = random.randint(0, 2)
        self.load_texture("resources/sprites/environment/corpse" + str(corpse_sprite) + ".png")
