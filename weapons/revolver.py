class Revolver:
    def __init__(self, game):
        path = "resources/sprites/weapon/revolver/"
        self.weapon_info = {
            "Revolver": {
                "Type": "Semi",
                "Unlocked": False,
                "Idle": {
                    "Frames": game.sprite_manager.load_single_image("Revolver Idle", path + "idle.png"),
                    "Speed": 0
                },
                "Reload": {
                    "Frames": game.sprite_manager.load_multiple_images("Revolver Reload", path + "Reload/"),

                    "Speed": 230
                },
                "Fire": {
                    "Frames": game.sprite_manager.load_multiple_images("Revolver Fire", path + "Fire/"),
                    "Damage": 24,
                    "Speed": 170,
                    "Cartridge Contains": 0,
                    "Cartridge Holds": 8,
                    "Bullet Per Shot": 1,
                    "Bullet Left": 36,
                    "Bullet Lifetime": 300,
                    "Bullet Velocity": 0.05,
                    "Bullet Offset": 0,
                    "Texture": "resources/sprites/projectile/empty.png",
                    "Texture Size": [1, 1]
                }
            }
        }
