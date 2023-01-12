from sprites.sprite import Sprite


class PickupArmor(Sprite):
    def __init__(self, game, pos):
        super().__init__(game, pos, [0.3, 0.3])
        path = "resources/sprites/pickups/armor.png"
        self.sprite = game.sprite_manager.load_single_image("Armor", path)[0]
        self.type = "Player"

    def update(self):
        super().update()

        if self.distance_from(self.player) < 0.5 and self.player.armor < self.player.max_armor:
            self.player.add_armor(25)
            self.game.sound.play_sfx("Pickup armor")
            self.delete = True
