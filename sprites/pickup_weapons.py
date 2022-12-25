from sprites.sprite import Sprite


class PitchforkPickup(Sprite):
    def __init__(self, game, pos):
        super().__init__(game, pos, [0.6])
        self.weapon_picked = False
        self.load_texture("resources/sprites/pickups/special/corpse_pitchfork.png")
        self.type = "Weapon"

    def update(self):
        super().update()

        if self.distance_from(self.player) < 0.5 and not self.weapon_picked:
            self.load_texture("resources/sprites/pickups/special/corpse_empty.png")
            self.game.weapon.unlock("Pitchfork")
            self.weapon_picked = True


class RevolverPickup(Sprite):
    def __init__(self, game, pos):
        super().__init__(game, pos, [0.2])
        self.load_texture("resources/sprites/weapon/revolver/icon.png")
        self.type = "Weapon"

    def update(self):
        super().update()

        if self.distance_from(self.player) < 0.5:
            self.game.weapon.unlock("Revolver")
            self.delete = True


class DoubleShotgunPickup(Sprite):
    def __init__(self, game, pos):
        super().__init__(game, pos, [0.25])
        self.load_texture("resources/sprites/weapon/double_shotgun/icon.png")
        self.type = "Weapon"

    def update(self):
        super().update()

        if self.distance_from(self.player) < 0.5:
            self.game.weapon.unlock("Double Shotgun")
            self.delete = True


class AutomaticRiflePickup(Sprite):
    def __init__(self, game, pos):
        super().__init__(game, pos, [0.25])
        self.load_texture("resources/sprites/weapon/automatic_rifle/icon.png")
        self.type = "Weapon"

    def update(self):
        super().update()

        if self.distance_from(self.player) < 0.5:
            self.game.weapon.unlock("Automatic Rifle")
            self.delete = True
