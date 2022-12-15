from sprites.sprite import Sprite


class PickupArmor(Sprite):
    def __init__(self, game, pos, scale=0.3):
        super().__init__(game, pos, scale)
        self.load_texture("resources/sprites/static_sprites/pickups/armor.png")

    def update(self):
        super().update()

        d = int(abs(self.player.exact_pos[0] - self.x) + abs(self.player.exact_pos[1] - self.y))
        if d == 0 and self.player.armor < 100:
            self.player.add_armor(25)
            sound = self.game.sound
            sound.pickup_sound(sound.pickup_armor)
            self.delete = True
