from sprites.sprite import Sprite


class Armor(Sprite):
    def __init__(self, game, pos, amount=25):
        super().__init__(game, pos, [0.3, 0.3])
        path = "resources/sprites/pickups/armor.png"
        self.sprite = game.sprite_manager.load_single_image("Armor", path)[0]
        self.amount = amount
        self.type = "Player"

    def update(self):
        if self.distance_from(self.player) < 0.5 and self.player.armor < 100:
            self.delete = True
            self.player.add_armor(self.amount)
            self.game.sound.play_sfx("Pickup armor")
            self.game.object_handler.update_pickup_list()
