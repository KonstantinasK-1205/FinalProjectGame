from sprites.sprite import Sprite
from sprites.animation_manager import *
import random


class Tree(Sprite):
    def __init__(self, game, pos):
        variety = random.randint(0, 8) / 10
        super().__init__(game, pos, [0.7 + variety, 1.3 + variety])
        game.sprite_manager.load_single_image("Tree", "resources/sprites/environment/tree0.png")
        self.sprite = game.sprite_manager.get_sprite("Tree")


class Corpse(Sprite):
    def __init__(self, game, pos):
        super().__init__(game, pos, [0.35, 0.25])
        corpse_no = str(random.randint(0, 2))
        corpse_path = "corpse" + corpse_no + ".png"
        game.sprite_manager.load_single_image("Corpse" + corpse_no, "resources/sprites/environment/" + corpse_path)
        self.sprite = game.sprite_manager.get_sprite("Corpse" + corpse_no)


class BigTorch(Sprite):
    def __init__(self, game, pos):
        super().__init__(game, pos, [0.3, 0.8])
        self.animation = Animation()
        self.current_animation = "Idle"
        path = "resources/sprites/environment/TorchBig/"
        self.states = {
            "Idle": {
                "Frames": game.sprite_manager.load_multiple_images("Big Torch Idle", path),
                "Speed": 140,
            }
        }
        self.animation.load_sprite_animations(self.states)
        self.animation.change_animation("Idle")
        self.sprite = self.animation.get_sprite()

    def update(self):
        self.animation.animate(self.game.dt)
        if self.animation.completed:
            self.animation.change_animation("Idle")

        self.current_state = self.animation.get_state()
        self.sprite = self.animation.get_sprite()

    def draw(self):
        self.game.renderer.draw_sprite(self.pos, self.size, self.sprite)


class SmallTorch(BigTorch):
    def __init__(self, game, pos):
        super().__init__(game, pos)
        self.size = [0.5, 0.6]
        path = "resources/sprites/environment/TorchSmall/"
        self.states = {
            "Idle": {
                "Frames": game.sprite_manager.load_multiple_images("Small Torch Idle", path),
                "Speed": 180,
            }
        }
        self.animation.load_sprite_animations(self.states)
        self.animation.change_animation("Idle")
        self.sprite = self.animation.get_sprite()
