from sprites.sprite import Sprite
from sprites.animation_manager import *
import random
import math


class Tree(Sprite):
    def __init__(self, game, pos):
        variety = random.randint(0, 8) / 10
        super().__init__(game, pos, [0.7 + variety, 1.3 + variety])
        game.sprite_manager.load_single_image("Tree", "resources/sprites/environment/tree0.png")
        self.sprite = game.sprite_manager.get_sprite("Tree")


class Cross(Sprite):
    def __init__(self, game, pos):
        super().__init__(game, pos, [0.4, 0.6])
        game.sprite_manager.load_single_image("Cross Front", "resources/sprites/environment/Cross/0.png")
        game.sprite_manager.load_single_image("Cross Angle", "resources/sprites/environment/Cross/1.png")
        game.sprite_manager.load_single_image("Cross Side", "resources/sprites/environment/Cross/2.png")
        self.sprite = game.sprite_manager.get_sprite("Cross Front")
        self.front = "Cross Front"
        self.angle = "Cross Angle"
        self.side = "Cross Side"

    def draw(self):
        # For future, make sprite show specific sprite
        self.game.renderer.draw_sprite(self.pos, self.size, self.sprite, angle=0)


class Fence(Cross):
    def __init__(self, game, pos):
        super().__init__(game, pos)
        self.size = [1.1, 1]
        game.sprite_manager.load_single_image("Fence Front", "resources/sprites/environment/Fence/0.png")
        game.sprite_manager.load_single_image("Fence Angle", "resources/sprites/environment/Fence/1.png")
        game.sprite_manager.load_single_image("Fence Side", "resources/sprites/environment/Fence/2.png")
        self.sprite = game.sprite_manager.get_sprite("Fence Front")
        self.front = "Fence Front"
        self.angle = "Fence Angle"
        self.side = "Fence Side"

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
