from sprites.sprite import *


class AutomaticRifle:
    def __init__(self, game):
        self.weapon_info = {
            "Automatic Rifle": {
                "Type": "Auto",
                "Unlocked": False,
                "Standby": {
                    "Sprites": Sprite(game).load_weapon_images("automatic_rifle", [0]),
                    "Speed": 200,
                },
                "Reload": {
                    "Sprites": Sprite(game).load_weapon_images("automatic_rifle", ["r0", "r1", "r2", "r3", "r4", "r5",
                                                                                   "r6", "r7", "r8", "r9", "r10"]),
                    "Animation Speed": 240,
                    "Speed": 160,
                },
                "Fire": {
                    "Sprites": Sprite(game).load_weapon_images("automatic_rifle", ["a0", "a1"]),
                    "Damage": 25,
                    "Speed": 80,
                    "Cartridge Contains": 0,
                    "Cartridge Holds": 30,
                    "Bullet Per Shot": 1,
                    "Bullet Left": 30,
                    "Bullet Lifetime": 800,
                    "Bullet Velocity": 0.05,
                    "Bullet Offset": 0.02
                }
            }
        }
