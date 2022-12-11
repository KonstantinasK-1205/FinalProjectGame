from sprites.sprite import Sprite
import math

class PickupHealth(Sprite):
    def __init__(self, game, path='resources/sprites/static_sprites/pickups/health.png',
                 pos=(2.5, 3), scale=0.3, shift=1.1):
        super().__init__(game, path, pos, scale, shift)
        self.picked = False

    def update(self):
        super().update()

        dx = self.x - self.player.get_pos[0]
        dy = self.y - self.player.get_pos[1]
        d = math.sqrt(dx * dx + dy * dy)
        if d < 0.5 and self.player.health < 100:
            self.player.add_health(25)
            self.game.sound.pickup_health.play()
            self.picked = True
