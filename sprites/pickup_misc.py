from sprites.sprite import Sprite


class BonusLevel(Sprite):
    def __init__(self, game, pos):
        super().__init__(game, pos, [0.5, 0.5])
        path = "resources/sprites/pickups/misc/silver_card.png"
        self.sprite = game.sprite_manager.load_single_image("silver_card", path)[0]
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
        path = "resources/sprites/pickups/empty.png"
        self.sprite = game.sprite_manager.load_single_image("empty", path)[0]
        self.change_to = None
        self.type = "Other"

    def update(self):
        super().update()

        if self.distance_from(self.player) < 0.5 and self.game.map.next_level:
            self.game.next_level(self.game.map.next_level)
