from sprites.sprite import *


class DoubleShotgun:
    def __init__(self, game):
        self.weapon_info = {
            "Double Shotgun": {
                "Type": "Semi",
                "Unlocked": False,
                "Idle": {
                    "Frames": Sprite(game).load_weapon_images("double_shotgun", [0]),
                    "Speed": 0,
                },
                "Reload": {
                    "Frames": Sprite(game).load_weapon_images("double_shotgun", ["r0", "r1", "r2", "r3",
                                                                                  "r4", "r5", "r6"]),
                    "Speed": 160,
                },
                "Fire": {
                    "Frames": Sprite(game).load_weapon_images("double_shotgun", ["a0", "a1"]),
                    "Damage": 35,
                    "Speed": 140,
                    "Cartridge Contains": 0,
                    "Cartridge Holds": 2,
                    "Bullet Per Shot": 2,
                    "Bullet Left": 12,
                    "Bullet Lifetime": 500,
                    "Bullet Velocity": 0.03,
                    "Bullet Offset": 0.1,
                    "Texture": "resources/sprites/projectile/empty.png",
                    "Texture Size": [1, 1]
                }
            }
        }
