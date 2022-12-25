from sprites.sprite import *


class Pitchfork:
    def __init__(self, game):
        self.weapon_info = {
            "Pitchfork": {
                "Type": "Melee",
                "Unlocked": False,
                "Standby": {
                    "Sprites": Sprite(game).load_weapon_images("pitchfork", [0]),
                    "Speed": 100,
                },
                "Reload": {
                    "Sprites": Sprite(game).load_weapon_images("pitchfork", [0]),
                    "Speed": 100,
                },
                "Fire": {
                    "Sprites": Sprite(game).load_weapon_images("pitchfork", ["a1"]),
                    "Damage": 9,
                    "Speed": 500,
                    "Cartridge Contains": 9999,
                    "Cartridge Holds": 9999,
                    "Bullet Per Shot": 1,
                    "Bullet Left": 9999,
                    "Bullet Lifetime": 250,
                    "Bullet Velocity": 0.005,
                }
            }
        }