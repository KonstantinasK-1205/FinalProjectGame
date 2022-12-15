from sprites.sprite import Sprite


class PickupHealth(Sprite):
    def __init__(self, game, pos, scale=0.3):
        super().__init__(game, pos, scale)
        self.load_texture("resources/sprites/static_sprites/pickups/health.png")

    def update(self):
        super().update()

        d = int(abs(self.player.exact_pos[0] - self.x) + abs(self.player.exact_pos[1] - self.y))
        if d == 0 and self.player.health < 100:
            self.player.add_health(25)
            self.game.sound.pickup_health.play()
            self.delete = True
