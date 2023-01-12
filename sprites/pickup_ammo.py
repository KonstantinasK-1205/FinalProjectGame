from sprites.sprite import Sprite


class PistolAmmo(Sprite):
    def __init__(self, game, pos, amount=24):
        super().__init__(game, pos, [0.3, 0.3])
        path = "resources/sprites/pickups/ammo/pistol.png"
        self.sprite = game.sprite_manager.load_single_image("pistol", path)[0]
        self.type = "Ammo"
        self.amount = amount

    def update(self):
        super().update()

        if self.distance_from(self.player) < 0.5:
            self.game.weapon.add_bullets("Revolver", self.amount)
            self.game.sound.play_sfx("Pickup ammo")
            self.delete = True


class ShotgunAmmo(Sprite):
    def __init__(self, game, pos, amount=30):
        super().__init__(game, pos, [0.3, 0.3])
        path = "resources/sprites/pickups/ammo/shotgun.png"
        self.sprite = game.sprite_manager.load_single_image("shotgun", path)[0]
        self.type = "Ammo"
        self.amount = amount

    def update(self):
        super().update()

        if self.distance_from(self.player) < 0.5:
            self.game.weapon.add_bullets("Double Shotgun", self.amount)
            self.game.sound.play_sfx("Pickup ammo")
            self.delete = True


class RifleAmmo(Sprite):
    def __init__(self, game, pos, amount=60):
        super().__init__(game, pos, [0.3, 0.3])
        path = "resources/sprites/pickups/ammo/rifle.png"
        self.sprite = game.sprite_manager.load_single_image("rifle", path)[0]
        self.type = "Ammo"
        self.amount = amount

    def update(self):
        super().update()

        if self.distance_from(self.player) < 0.5:
            self.game.weapon.add_bullets("Automatic Rifle", self.amount)
            self.game.sound.play_sfx("Pickup ammo")
            self.delete = True
