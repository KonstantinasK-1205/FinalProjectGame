class HealthBar:
    def __init__(self, game, hud):
        self.game = game
        self.hud = hud

        self.health_icon_width = 0
        self.health_icon_height = 0
        self.health_bar_width = 0
        self.health_bar_height = 0
        self.health_bar_hp = 0
        self.health_text = None

        self.game.renderer.load_texture_from_file("resources/icons/gui_health.png")

    def draw(self):
        self.game.renderer.draw_rect(
            self.hud.margin,
            self.game.height - self.health_icon_height - self.hud.margin,
            self.health_icon_width,
            self.health_icon_height,
            "resources/icons/gui_health.png"
        )
        self.game.renderer.draw_rect(
            self.hud.margin + self.health_icon_width + 5,
            self.game.height - self.health_icon_height - self.hud.margin,
            self.health_bar_width,
            self.health_bar_height,
            color=(128, 128, 128, 20)
        )
        self.game.renderer.draw_rect(
            self.hud.margin + self.health_icon_width + 5,
            self.game.height - self.health_icon_height - self.hud.margin,
            self.health_bar_hp,
            self.health_bar_height,
            color=(6, 100, 32, 200)
        )

        self.game.renderer.draw_rect(
            self.hud.margin + self.health_icon_width + 5 + self.health_bar_width / 2 - self.health_text.get_width() / 2,
            self.game.height - self.health_icon_height - self.hud.margin,
            self.health_text.get_width(),
            self.health_text.get_height(),
            "health_text"
        )

    def on_change(self):
        self.update_healthbar_size()
        self.update_healthbar_info()

    def update_healthbar_size(self):
        # Recalculate health icon size
        self.health_icon_width = self.game.width / 40
        self.health_icon_height = self.game.height / 25

        # Recalculate health bar size
        self.health_bar_width = self.game.width / 8
        self.health_bar_height = self.game.height / 25
        self.update_healthbar_info()

    def update_healthbar_info(self):
        self.health_text = self.game.font_small.render(str(self.game.player.health), True, (0, 64, 0))
        self.game.renderer.load_texture_from_surface("health_text", self.health_text)
        self.health_bar_hp = (self.health_bar_width / 100) * self.game.player.health
