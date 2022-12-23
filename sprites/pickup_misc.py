from sprites.sprite import Sprite
import random


class BonusLevel(Sprite):
    def __init__(self, game, pos, scale=None):
        if not scale:
            scale = [0.5, 0.5]
        super().__init__(game, pos, scale)
        self.load_texture("resources/sprites/pickups/misc/silver_card.png")

    def update(self):
        super().update()

        if self.distance_from(self.player) < 0.5:
            self.game.map_lists.append("Level6")
            self.game.sound.play_sfx("Player dmg buff")
            self.delete = True
