from sprites.sprite import Sprite


class PickupArmor(Sprite):
    def __init__(self, game, path='resources/sprites/static_sprites/pickups/armor.png',
                 pos=(0, 0), scale=0.3, shift=1.1):
        super().__init__(game, path, pos, scale, shift)

        self.width = scale
        self.height = scale

    def update(self):
        super().update()

        d = int(abs(self.player.exact_pos[0] - self.x) + abs(self.player.exact_pos[1] - self.y))
        if d == 0 and self.player.armor < 100:
            self.player.add_armor(25)
            sound = self.game.sound
            sound.pickup_sound(sound.pickup_armor)
            self.delete = True
