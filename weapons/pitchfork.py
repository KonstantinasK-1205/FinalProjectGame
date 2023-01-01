from sprites.sprite import *


class Pitchfork:
    def __init__(self, game):
        self.weapon_info = {
            "Pitchfork": {
                "Type": "Melee",
                "Unlocked": False,
                "Idle": {
                    "Frames": Sprite(game).load_weapon_images("pitchfork", [0]),
                    "Speed": 100,
                },
                "Reload": {
                    "Frames": Sprite(game).load_weapon_images("pitchfork", [0]),
                    "Speed": 100,
                },
                "Fire": {
                    "Frames": Sprite(game).load_weapon_images("pitchfork", ["a1"]),
                    "Damage": 10,
                    "Speed": 500,
                    "Cartridge Contains": 9999,
                    "Cartridge Holds": 9999,
                    "Bullet Per Shot": 1,
                    "Bullet Left": 9999,
                    "Bullet Lifetime": 50,
                    "Bullet Velocity": 0.025,
                    "Texture": "resources/sprites/projectile/empty.png",
                    "Texture Size": [1, 1]
                }
            }
        }
