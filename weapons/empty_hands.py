from sprites.sprite import *


class Empty:
    def __init__(self, game):
        self.weapon_info = {
            "Empty": {
                "Unlocked": True,
                "Type": "Melee",
                "Standby": {
                    "Sprites": Sprite(game).load_weapon_images("empty", [0]),
                    "Speed": 100,
                },
                "Reload": {
                    "Sprites": Sprite(game).load_weapon_images("empty", [0]),
                    "Speed": 100,
                },
                "Fire": {
                    "Sprites": Sprite(game).load_weapon_images("empty", [0]),
                    "Damage": 0,
                    "Speed": 100,
                    "Cartridge Contains": 0,
                    "Cartridge Holds": 0,
                    "Bullet Per Shot": 1,
                    "Bullet Left": 0,
                    "Bullet Lifetime": 0,
                    "Bullet Velocity": 0.005,
                    "Bullet Offset": 0
                }
            }
        }
