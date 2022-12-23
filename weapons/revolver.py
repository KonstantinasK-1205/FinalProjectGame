from sprites.sprite import *


class Revolver:
    def __init__(self, game):

        self.weapon_info = {
            "Revolver": {
                "Type": "Semi",
                "Unlocked": False,
                "Standby": {
                    "Sprites": Sprite(game).load_weapon_images("revolver", [0]),
                    "Speed": 100,
                },
                "Reload": {
                    "Sprites": Sprite(game).load_weapon_images("revolver", ["r0", "r1", "r2", "r3", "r4",
                                                                            "r5", "r6", "r7", "r8"]),
                    "Speed": 200,
                },
                "Fire": {
                    "Sprites": Sprite(game).load_weapon_images("revolver", ["a0", "a1", "a2"]),
                    "Damage": 32,
                    "Speed": 150,
                    "Cartridge Contains": 0,
                    "Cartridge Holds": 8,
                    "Bullet Per Shot": 1,
                    "Bullet Left": 8,
                    "Bullet Lifetime": 600,
                    "Bullet Velocity": 0.04,
                    "Bullet Offset": 0
                }
            }
        }