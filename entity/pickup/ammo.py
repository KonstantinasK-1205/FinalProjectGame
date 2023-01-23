from sprites.sprite import Sprite


class Ammo(Sprite):
    def __init__(self, game, pos, weapon, amount):
        super().__init__(game, pos, [0.15, 0.15])
        path = "resources/sprites/pickups/ammo/" + weapon + ".png"
        self.sprite = game.sprite_manager.load_single_image("Ammo " + weapon, path)[0]
        self.weapon = weapon
        self.amount = amount
        self.type = "Ammo"

    def update(self):
        if self.distance_from(self.player) < 0.5:
            self.delete = True
            self.game.sound.play_sfx("Pickup ammo")
            self.game.weapon.add_bullets(self.weapon, self.amount)
            self.game.object_handler.update_pickup_list()
