from sprites.sprite import Sprite


class PitchforkPickup(Sprite):
    def __init__(self, game, pos):
        super().__init__(game, pos, [0.6])
        self.game = game
        self.weapon_picked = False
        path = "resources/sprites/pickups/special/corpse_empty.png"
        game.sprite_manager.load_single_image("corpse without pitchfork", path)
        path = "resources/sprites/pickups/special/corpse_pitchfork.png"
        self.texture_path = game.sprite_manager.load_single_image("corpse with pitchfork", path)[0]
        self.type = "Weapon"

    def update(self):
        super().update()

        if self.distance_from(self.player) < 0.5 and not self.weapon_picked:
            self.texture_path = self.game.sprite_manager.get_sprite("corpse without pitchfork")
            self.game.weapon.unlock("Pitchfork")
            self.weapon_picked = True


class RevolverPickup(Sprite):
    def __init__(self, game, pos):
        super().__init__(game, pos, [0.2])
        path = "resources/sprites/weapon/revolver/icon.png"
        self.texture_path = game.sprite_manager.load_single_image("revolver icon", path)[0]
        self.type = "Weapon"

    def update(self):
        super().update()

        if self.distance_from(self.player) < 0.5:
            self.game.weapon.unlock("Revolver")
            self.delete = True


class DoubleShotgunPickup(Sprite):
    def __init__(self, game, pos):
        super().__init__(game, pos, [0.25])
        path = "resources/sprites/weapon/double_shotgun/icon.png"
        self.texture_path = game.sprite_manager.load_single_image("double_shotgun icon", path)[0]
        self.type = "Weapon"

    def update(self):
        super().update()

        if self.distance_from(self.player) < 0.5:
            self.game.weapon.unlock("Double Shotgun")
            self.delete = True


class AutomaticRiflePickup(Sprite):
    def __init__(self, game, pos):
        super().__init__(game, pos, [0.25])
        path = "resources/sprites/weapon/automatic_rifle/icon.png"
        self.texture_path = game.sprite_manager.load_single_image("automatic_rifle icon", path)[0]
        self.type = "Weapon"

    def update(self):
        super().update()

        if self.distance_from(self.player) < 0.5:
            self.game.weapon.unlock("Automatic Rifle")
            self.delete = True
