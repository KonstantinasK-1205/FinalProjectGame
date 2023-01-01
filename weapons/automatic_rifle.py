from sprites.sprite import *


class AutomaticRifle:
    def __init__(self, game):
        self.weapon_info = {
            "Automatic Rifle": {
                "Type": "Auto",
                "Unlocked": False,
                "Idle": {
                    "Frames": Sprite(game).load_weapon_images("automatic_rifle", [0]),
                    "Speed": 0,
                },
                "Reload": {
                    "Frames": Sprite(game).load_weapon_images("automatic_rifle", ["r0", "r1", "r2", "r3", "r4", "r5",
                                                                                   "r6", "r7", "r8", "r9", "r10"]),
                    "Speed": 160,
                },
                "Fire": {
                    "Frames": Sprite(game).load_weapon_images("automatic_rifle", ["a0", "a1"]),
                    "Damage": 20,
                    "Speed": 50,
                    "Cartridge Contains": 0,
                    "Cartridge Holds": 30,
                    "Bullet Per Shot": 1,
                    "Bullet Left": 30,
                    "Bullet Lifetime": 700,
                    "Bullet Velocity": 0.06,
                    "Bullet Offset": 0.02,
                    "Texture": "resources/sprites/projectile/empty.png",
                    "Texture Size": [1, 1]
                }
            }
        }
