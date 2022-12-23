from sprites.sprite import Sprite


class PitchforkPickup(Sprite):
    def __init__(self, game, pos, scale=[0.6]):
        super().__init__(game, pos, scale)
        self.weapon_picked = False
        self.load_texture("resources/sprites/pickups/special/corpse_pitchfork.png")

    def update(self):
        super().update()

        if self.distance_from(self.player) < 0.5 and not self.weapon_picked:
            self.load_texture("resources/sprites/pickups/special/corpse_empty.png")
            self.game.weapon.unlock("Pitchfork")
            self.weapon_picked = True


class RevolverPickup(Sprite):
    def __init__(self, game, pos, scale=[0.2]):
        super().__init__(game, pos, scale)
        self.load_texture("resources/sprites/weapon/revolver/icon.png")

    def update(self):
        super().update()

        if self.distance_from(self.player) < 0.5:
            self.game.weapon.unlock("Revolver")
            self.delete = True


class DoubleShotgunPickup(Sprite):
    def __init__(self, game, pos, scale=[0.25]):
        super().__init__(game, pos, scale)
        self.load_texture("resources/sprites/weapon/double_shotgun/icon.png")

    def update(self):
        super().update()

        if self.distance_from(self.player) < 0.5:
            self.game.weapon.unlock("Double Shotgun")
            self.delete = True


class AutomaticRiflePickup(Sprite):
    def __init__(self, game, pos, scale=[0.25]):
        super().__init__(game, pos, scale)
        self.load_texture("resources/sprites/weapon/automatic_rifle/icon.png")

    def update(self):
        super().update()

        if self.distance_from(self.player) < 0.5:
            self.game.weapon.unlock("Automatic Rifle")
            self.delete = True
