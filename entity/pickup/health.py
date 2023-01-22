from sprites.sprite import Sprite


class Health(Sprite):
    def __init__(self, game, pos, amount=25):
        super().__init__(game, pos, [0.3, 0.3])
        path = "resources/sprites/pickups/health.png"
        self.sprite = game.sprite_manager.load_single_image("Healthpack", path)[0]
        self.amount = amount
        self.type = "Player"

    def update(self):
        if self.distance_from(self.player) < 0.5 and self.player.health < 100:
            self.delete = True
            self.player.add_health(self.amount)
            self.game.sound.play_sfx("Pickup health")
            self.game.object_handler.update_pickup_list()
