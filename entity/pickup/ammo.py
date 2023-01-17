from sprites.sprite import Sprite


class Pistol(Sprite):
    def __init__(self, game, pos, amount=24):
        super().__init__(game, pos, [0.3, 0.3])
        path = "resources/sprites/pickups/ammo/pistol.png"
        self.sprite = game.sprite_manager.load_single_image("pistol", path)[0]
        self.amount = amount
        self.type = "Ammo"

    def update(self):
        if self.distance_from(self.player) < 0.5:
            self.delete = True
            self.game.sound.play_sfx("Pickup ammo")
            self.game.weapon.add_bullets("Revolver", self.amount)
            self.game.object_handler.update_pickup_list()


class Shotgun(Sprite):
    def __init__(self, game, pos, amount=30):
        super().__init__(game, pos, [0.3, 0.3])
        path = "resources/sprites/pickups/ammo/shotgun.png"
        self.sprite = game.sprite_manager.load_single_image("shotgun", path)[0]
        self.amount = amount
        self.type = "Ammo"

    def update(self):
        if self.distance_from(self.player) < 0.5:
            self.delete = True
            self.game.sound.play_sfx("Pickup ammo")
            self.game.weapon.add_bullets("Double Shotgun", self.amount)
            self.game.object_handler.update_pickup_list()


class Rifle(Sprite):
    def __init__(self, game, pos, amount=60):
        super().__init__(game, pos, [0.3, 0.3])
        path = "resources/sprites/pickups/ammo/rifle.png"
        self.sprite = game.sprite_manager.load_single_image("rifle", path)[0]
        self.amount = amount
        self.type = "Ammo"

    def update(self):
        if self.distance_from(self.player) < 0.5:
            self.delete = True
            self.game.sound.play_sfx("Pickup ammo")
            self.game.weapon.add_bullets("Automatic Rifle", self.amount)
            self.game.object_handler.update_pickup_list()
