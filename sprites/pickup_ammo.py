from sprites.sprite import Sprite


class PistolAmmo(Sprite):
    def __init__(self, game, pos, scale=[0.3]):
        super().__init__(game, pos, scale)
        self.load_texture("resources/sprites/pickups/ammo/pistol.png")

    def update(self):
        super().update()

        if self.distance_from(self.player) < 0.5:
            self.game.weapon.add_bullets("Revolver", 24)
            self.game.sound.play_sfx("Pickup ammo")
            self.delete = True


class ShotgunAmmo(Sprite):
    def __init__(self, game, pos, scale=[0.3]):
        super().__init__(game, pos, scale)
        self.load_texture("resources/sprites/pickups/ammo/shotgun.png")

    def update(self):
        super().update()

        if self.distance_from(self.player) < 0.5:
            self.game.weapon.add_bullets("Double Shotgun", 30)
            self.game.sound.play_sfx("Pickup ammo")
            self.delete = True


class RifleAmmo(Sprite):
    def __init__(self, game, pos, scale=[0.3]):
        super().__init__(game, pos, scale)
        self.load_texture("resources/sprites/pickups/ammo/rifle.png")

    def update(self):
        super().update()

        if self.distance_from(self.player) < 0.5:
            self.game.weapon.add_bullets("Automatic Rifle", 60)
            self.game.sound.play_sfx("Pickup ammo")
            self.delete = True
