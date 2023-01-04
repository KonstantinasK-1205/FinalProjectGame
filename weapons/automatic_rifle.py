class AutomaticRifle:
    def __init__(self, game):
        path = "resources/sprites/weapon/automatic_rifle/"
        self.weapon_info = {
            "Automatic Rifle": {
                "Type": "Auto",
                "Unlocked": False,
                "Idle": {
                    "Frames": game.sprite_manager.load_single_image("Automatic Rifle Idle", path + "idle.png"),
                    "Speed": 0
                },
                "Reload": {
                    "Frames": game.sprite_manager.load_multiple_images("Automatic Rifle Reload", path + "Reload/"),
                    "Speed": 160
                },
                "Fire": {
                    "Frames": game.sprite_manager.load_multiple_images("Automatic Rifle Fire", path + "Fire/"),
                    "Damage": 20,
                    "Speed": 50,
                    "Cartridge Contains": 0,
                    "Cartridge Holds": 30,
                    "Bullet Per Shot": 1,
                    "Bullet Left": 45,
                    "Bullet Lifetime": 700,
                    "Bullet Velocity": 0.06,
                    "Bullet Offset": 0.02,
                    "Texture": "resources/sprites/projectile/empty.png",
                    "Texture Size": [1, 1]
                }
            }
        }
