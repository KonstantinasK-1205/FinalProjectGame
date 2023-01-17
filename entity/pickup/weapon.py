from sprites.sprite import Sprite


class Pitchfork(Sprite):
    def __init__(self, game, pos):
        super().__init__(game, pos, [0.6, 0.6])
        self.game = game
        self.weapon_picked = False

        path = "resources/sprites/pickups/special/corpse_empty.png"
        game.sprite_manager.load_single_image("corpse without pitchfork", path)
        path = "resources/sprites/pickups/special/corpse_pitchfork.png"

        self.sprite = game.sprite_manager.load_single_image("corpse with pitchfork", path)[0]
        self.type = "Weapon"

    def update(self):
        if not self.weapon_picked and self.distance_from(self.player) < 0.5:
            self.sprite = self.game.sprite_manager.get_sprite("corpse without pitchfork")
            self.weapon_picked = True
            self.game.weapon.unlock("Pitchfork")


class Revolver(Sprite):
    def __init__(self, game, pos):
        super().__init__(game, pos, [0.2, 0.2])
        path = "resources/sprites/weapon/revolver/icon.png"
        self.sprite = game.sprite_manager.load_single_image("revolver icon", path)[0]
        self.type = "Weapon"

    def update(self):
        if self.distance_from(self.player) < 0.5:
            self.delete = True
            self.game.weapon.unlock("Revolver")
            self.game.object_handler.update_pickup_list()


class DoubleShotgun(Sprite):
    def __init__(self, game, pos):
        super().__init__(game, pos, [0.25, 0.25])
        path = "resources/sprites/weapon/double_shotgun/icon.png"
        self.sprite = game.sprite_manager.load_single_image("double_shotgun icon", path)[0]
        self.type = "Weapon"

    def update(self):
        if self.distance_from(self.player) < 0.5:
            self.delete = True
            self.game.weapon.unlock("Double Shotgun")
            self.game.object_handler.update_pickup_list()


class AutomaticRifle(Sprite):
    def __init__(self, game, pos):
        super().__init__(game, pos, [0.25, 0.25])
        path = "resources/sprites/weapon/automatic_rifle/icon.png"
        self.sprite = game.sprite_manager.load_single_image("automatic_rifle icon", path)[0]
        self.type = "Weapon"

    def update(self):
        if self.distance_from(self.player) < 0.5:
            self.delete = True
            self.game.weapon.unlock("Automatic Rifle")
            self.game.object_handler.update_pickup_list()
