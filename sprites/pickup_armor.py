from sprites.sprite import Sprite


class PickupArmor(Sprite):
    def __init__(self, game, pos, scale=0.3):
        super().__init__(game, pos, scale)
        self.load_texture("resources/sprites/static_sprites/pickups/armor.png")

    def update(self):
        super().update()

        if self.distance_from(self.player) < 0.5 and self.player.armor < 100:
            self.player.add_armor(25)
            self.game.sound.play_sfx("Pickup armor")
            self.delete = True
