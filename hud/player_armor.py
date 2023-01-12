class ArmorBar:
    def __init__(self, game, hud):
        # Init main variables
        self.game = game
        self.hud = hud

        # Init armor icon and bar variables
        self.armor_icon_width = 0
        self.armor_icon_height = 0
        self.armor_bar_width = 0
        self.armor_bar_height = 0
        self.armor_bar_hp = 0
        self.armor_text = None

        # Load armor icon texture
        self.game.renderer.load_texture_from_file("resources/icons/gui_armor.png")

        self.armor = 0

    def draw(self):
        self.game.renderer.draw_rect(
            self.hud.margin,
            self.game.height - self.armor_icon_height * 2 - self.hud.margin,
            self.armor_icon_width,
            self.armor_icon_height,
            "resources/icons/gui_armor.png"
        )
        self.game.renderer.draw_rect(
            self.hud.margin + self.armor_icon_width + 5,
            self.game.height - self.armor_icon_height * 2 - self.hud.margin,
            self.armor_bar_width,
            self.armor_bar_height,
            color=(255, 255, 255, 20)
        )
        self.game.renderer.draw_rect(
            self.hud.margin + self.armor_icon_width + 5,
            self.game.height - self.armor_icon_height * 2 - self.hud.margin,
            self.armor_bar_hp,
            self.armor_bar_height,
            color=(12, 32, 100, 200)
        )

        self.game.renderer.draw_rect(
            self.hud.margin + self.armor_icon_width + 5 + self.armor_bar_width / 2 - self.armor_text.get_width() / 2,
            self.game.height - self.armor_icon_height * 2 - self.hud.margin,
            self.armor_text.get_width(),
            self.armor_text.get_height(),
            "armor_text"
        )

    def on_change(self):
        self.update_armorbar_size()
        self.update_armorbar_info(self.armor)

    def update_armorbar_size(self):
        # Recalculate armor icon size
        self.armor_icon_width = self.game.width / 40
        self.armor_icon_height = self.game.height / 25

        # Recalculate armor bar size
        self.armor_bar_width = self.game.width / 8
        self.armor_bar_height = self.game.height / 25
        self.update_armorbar_info(self.armor)

    def update_armorbar_info(self, armor):
        # Assign argument armor to variable
        self.armor = armor

        # Update armor text information
        self.armor_bar_hp = (self.armor_bar_width / 100) * self.armor
        self.armor_text = self.game.fonts[1].render(str(self.armor), True, (0, 0, 64))
        self.game.renderer.load_texture_from_surface("armor_text", self.armor_text)
