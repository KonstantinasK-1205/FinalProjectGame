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


class LevelChangeChunk(Sprite):
    def __init__(self, game, pos, scale=None):
        if not scale:
            scale = [0.5, 0.5]
        super().__init__(game, pos, scale)
        self.load_texture("resources/sprites/pickups/empty.png")
        self.change_to = None
        if "Level1" in self.game.current_map:
            self.change_to = "resources/levels/T_Level2.txt"
        else:
            self.change_to = "resources/levels/T_Level1.txt"

    def update(self):
        super().update()

        if self.distance_from(self.player) < 0.5:
            self.game.next_level(self.change_to)

