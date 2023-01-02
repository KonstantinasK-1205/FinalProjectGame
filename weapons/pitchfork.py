class Pitchfork:
    def __init__(self, game):
        path = "resources/sprites/weapon/pitchfork/"
        self.weapon_info = {
            "Pitchfork": {
                "Type": "Melee",
                "Unlocked": False,
                "Idle": {
                    "Frames": game.sprite_manager.load_single_image("Pitchfork Idle", path + "idle.png"),
                    "Speed": 0
                },
                "Reload": {
                    "Frames": game.sprite_manager.load_single_image("Pitchfork Idle", path + "idle.png"),
                    "Speed": 0
                },
                "Fire": {
                    "Frames": game.sprite_manager.load_multiple_images("Pitchfork Fire", path + "Fire/"),
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
