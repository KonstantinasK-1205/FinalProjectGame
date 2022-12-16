from sprites.sprite import Sprite


class ShotgunPickupAmmo(Sprite):
    def __init__(self, game, pos, scale=0.3):
        super().__init__(game, pos, scale)
        self.load_texture("resources/sprites/static_sprites/pickups/ammo_shotgun.png")

    def update(self):
        super().update()

        if self.distance_from(self.player) < 0.5:
            self.game.weapon.add_bullets("Shotgun", 10)
            sound = self.game.sound
            sound.pickup_sound(sound.pickup_ammo)
            self.delete = True
