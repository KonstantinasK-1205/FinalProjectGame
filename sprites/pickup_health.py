from sprites.sprite import Sprite


class PickupHealth(Sprite):
    def __init__(self, game, pos, scale=[0.3]):
        super().__init__(game, pos, scale)
        self.load_texture("resources/sprites/pickups/health.png")

    def update(self):
        super().update()

        if self.distance_from(self.player) < 0.5 and self.player.health < 100:
            self.player.add_health(25)
            self.game.sound.play_sfx("Pickup health")
            self.delete = True
