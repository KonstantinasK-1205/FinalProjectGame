from sprites.sprite import Sprite


class MachinegunPickupAmmo(Sprite):
    def __init__(self, game, pos, scale=0.3):
        super().__init__(game, pos, scale)
        self.load_texture("resources/sprites/static_sprites/pickups/ammo_machinegun.png")

    def update(self):
        super().update()

        if self.distance_from(self.player) < 0.5:
            self.game.weapon.add_bullets("Machinegun", 50)
            self.game.sound.play_sfx("Pickup ammo")
            self.delete = True
