from sprites.sprite import Sprite
import math

class ShotgunPickupAmmo(Sprite):
    def __init__(self, game, path='resources/sprites/static_sprites/pickups/ammo_shotgun.png',
                 pos=(2.5, 3), scale=0.3, shift=1.1):
        super().__init__(game, path, pos, scale, shift)
        self.picked = False

    def update(self):
        super().update()

        dx = self.x - self.player.get_pos[0]
        dy = self.y - self.player.get_pos[1]
        d = math.sqrt(dx * dx + dy * dy)
        if d < 0.5:
            self.game.weapon.add_bullets("Shotgun", 10)
            sound = self.game.sound
            sound.pickup_sound(sound.pickup_ammo)
            self.picked = True
