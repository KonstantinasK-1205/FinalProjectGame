from hud.minimap import *
from hud.player_hp import *
from hud.player_armor import *
from hud.weapons_stat import *


class Hud:
    def __init__(self, game):
        self.game = game
        self.margin = 0

        self.healthbar = HealthBar(game, self)
        self.armorbar = ArmorBar(game, self)
        self.weapons_hud = WeaponStats(game, self)
        self.minimap = Minimap(game, self)

    def on_resize(self):
        self.healthbar.on_change()
        self.armorbar.on_change()
        self.minimap.on_change()

    def level_change(self):
        # If level changes update hp and armor bar information only
        self.healthbar.update_healthbar_info()
        self.armorbar.update_armorbar_info()

        # Minimap and enemy stats needs to be updated fully
        self.minimap.on_change()

    def draw_fps_counter(self):
        fps_counter = self.game.font_small.render("FPS: " + str(int(self.game.clock.get_fps())), True, (255, 255, 255))
        self.game.renderer.load_texture_from_surface("fps_counter", fps_counter)
        self.game.renderer.draw_rect(
            self.margin,
            self.margin,
            fps_counter.get_width(),
            fps_counter.get_height(),
            "fps_counter"
        )

    def draw(self, map_state):
        self.margin = self.game.width / 100

        self.healthbar.draw()
        self.armorbar.draw()
        self.minimap.draw(map_state)
        if not self.game.weapon.current_weapon_type() == "Melee":
            self.weapons_hud.draw()
