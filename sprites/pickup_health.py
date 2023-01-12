from sprites.sprite import Sprite


class PickupHealth(Sprite):
    def __init__(self, game, pos):
        super().__init__(game, pos, [0.3, 0.3])
        path = "resources/sprites/pickups/health.png"
        self.sprite = game.sprite_manager.load_single_image("Healthpack", path)[0]
        self.type = "Player"

    def update(self):
        super().update()

        if self.distance_from(self.player) < 0.5 and self.player.health < self.player.max_health:
            self.player.add_health(25)
            self.game.sound.play_sfx("Pickup health")
            self.delete = True
