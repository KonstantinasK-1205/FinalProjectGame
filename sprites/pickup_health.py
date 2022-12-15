from sprites.sprite import Sprite


class PickupHealth(Sprite):
    def __init__(self, game, path='resources/sprites/static_sprites/pickups/health.png',
                 pos=(0, 0), scale=0.3, shift=1.1):
        super().__init__(game, path, pos, scale, shift)

        self.width = scale
        self.height = scale

    def update(self):
        super().update()

        d = int(abs(self.player.exact_pos[0] - self.x) + abs(self.player.exact_pos[1] - self.y))
        if d == 0 and self.player.health < 100:
            self.player.add_health(25)
            self.game.sound.pickup_health.play()
            self.delete = True
