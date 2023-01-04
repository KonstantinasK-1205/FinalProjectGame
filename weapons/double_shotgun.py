class DoubleShotgun:
    def __init__(self, game):
        path = "resources/sprites/weapon/double_shotgun/"
        self.weapon_info = {
            "Double Shotgun": {
                "Type": "Semi",
                "Unlocked": False,
                "Idle": {
                    "Frames": game.sprite_manager.load_single_image("Double Shotgun Idle", path + "idle.png"),
                    "Speed": 0
                },
                "Reload": {
                    "Frames": game.sprite_manager.load_multiple_images("Double Shotgun Reload", path + "Reload/"),
                    "Speed": 160
                },
                "Fire": {
                    "Frames": game.sprite_manager.load_multiple_images("Double Shotgun Fire", path + "Fire/"),
                    "Damage": 35,
                    "Speed": 140,
                    "Cartridge Contains": 0,
                    "Cartridge Holds": 2,
                    "Bullet Per Shot": 2,
                    "Bullet Left": 18,
                    "Bullet Lifetime": 500,
                    "Bullet Velocity": 0.03,
                    "Bullet Offset": 0.1,
                    "Texture": "resources/sprites/projectile/empty.png",
                    "Texture Size": [1, 1]
                }
            }
        }
