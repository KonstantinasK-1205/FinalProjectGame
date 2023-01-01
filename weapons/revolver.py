from sprites.sprite import *


class Revolver:
    def __init__(self, game):
        self.weapon_info = {
            "Revolver": {
                "Type": "Semi",
                "Unlocked": False,
                "Idle": {
                    "Frames": Sprite(game).load_weapon_images("revolver", [0]),
                    "Speed": 0,
                },
                "Reload": {
                    "Frames": Sprite(game).load_weapon_images("revolver", ["r0", "r1", "r2", "r3", "r4",
                                                                           "r5", "r6", "r7", "r8"]),
                    "Speed": 230,
                },
                "Fire": {
                    "Frames": Sprite(game).load_weapon_images("revolver", ["a0", "a1", "a2"]),
                    "Damage": 24,
                    "Speed": 170,
                    "Cartridge Contains": 0,
                    "Cartridge Holds": 8,
                    "Bullet Per Shot": 1,
                    "Bullet Left": 8,
                    "Bullet Lifetime": 300,
                    "Bullet Velocity": 0.05,
                    "Bullet Offset": 0,
                    "Texture": "resources/sprites/projectile/empty.png",
                    "Texture Size": [1, 1]
                }
            }
        }
