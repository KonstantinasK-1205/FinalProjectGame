from sprites.sprite import Sprite


class BonusLevel(Sprite):
    def __init__(self, game, pos):
        super().__init__(game, pos, [0.5, 0.5])
        self.load_texture("resources/sprites/pickups/misc/silver_card.png")
        self.type = "Other"

    def update(self):
        super().update()

        if self.distance_from(self.player) < 0.5:
            self.game.map.next_level = "Level6"
            self.game.sound.play_sfx("Player dmg buff")
            self.delete = True


class LevelChangeChunk(Sprite):
    def __init__(self, game, pos):
        super().__init__(game, pos, [0.5, 0.5])
        self.load_texture("resources/sprites/pickups/empty.png")
        self.change_to = None
        self.type = "Other"

    def update(self):
        super().update()

        if self.distance_from(self.player) < 0.5:
            self.game.next_level(self.game.map.next_level)
