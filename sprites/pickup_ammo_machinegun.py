from sprites.sprite import Sprite


class MachinegunPickupAmmo(Sprite):
    def __init__(self, game, pos, scale=0.3):
        super().__init__(game, pos, scale)
        self.load_texture("resources/sprites/static_sprites/pickups/ammo_machinegun.png")

    def update(self):
        super().update()

        d = int(abs(self.player.exact_pos[0] - self.x) + abs(self.player.exact_pos[1] - self.y))
        if d == 0:
            self.game.weapon.add_bullets("Machinegun", 50)
            sound = self.game.sound
            sound.pickup_sound(sound.pickup_ammo)
            self.delete = True
