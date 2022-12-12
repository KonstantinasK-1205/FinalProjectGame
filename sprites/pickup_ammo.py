from sprites.sprite import Sprite


class PickupArmor(Sprite):
    def __init__(self, game, path='resources/sprites/static_sprites/pickups/armor.png',
                 pos=(2.5, 3), scale=0.3, shift=1.1):
        super().__init__(game, path, pos, scale, shift)
        self.picked = False

    def update(self):
        super().update()

        dx = self.x - self.player.get_pos[0]
        dy = self.y - self.player.get_pos[1]
        d = math.sqrt(dx * dx + dy * dy)
        if d < 0.5 and self.player.armor < 100:
            self.player.add_armor(25)
            sound = self.game.sound
            sound.pickup_sound(sound.pickup_armor)
            self.picked = True
