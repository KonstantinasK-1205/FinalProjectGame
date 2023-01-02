class Empty:
    def __init__(self, game):
        path = "resources/sprites/weapon/empty/"
        self.weapon_info = {
            "Empty": {
                "Unlocked": True,
                "Type": "Melee",
                "Idle": {
                    "Frames": game.sprite_manager.load_single_image("Empty Hand", path + "idle.png"),
                    "Speed": 0
                },
                "Reload": {
                    "Frames": game.sprite_manager.load_single_image("Empty Hand", path + "idle.png"),
                    "Speed": 0
                },
                "Fire": {
                    "Frames": game.sprite_manager.load_single_image("Empty Hand", path + "idle.png"),
                    "Damage": 0,
                    "Speed": 0,
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
