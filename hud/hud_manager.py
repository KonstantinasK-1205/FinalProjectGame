from hud.minimap import *
from hud.player_hp import *
from hud.player_armor import *
from hud.weapons_stat import *


class Hud:
    def __init__(self, game):
        # Init main variables
        self.game = game
        self.margin = 0

        # Create and init all HUD elements
        self.healthbar = HealthBar(game, self)
        self.armorbar = ArmorBar(game, self)
        self.weapons_hud = WeaponStats(game, self)
        self.minimap = Minimap(game, self)

    def on_resize(self):
        # Recalculate margin
        self.margin = self.game.width / 100

        # Update all elements
        self.healthbar.on_change()
        self.armorbar.on_change()
        self.minimap.on_change()

    def level_change(self, health, armor):
        # If level changes update hp and armor bar information only
        self.healthbar.update_healthbar_info(health)
        self.armorbar.update_armorbar_info(armor)

        # Minimap and enemy stats needs to be updated fully
        self.minimap.on_change()

    def draw_fps_counter(self):
        fps_counter = self.game.font_small.render("FPS: " + str(int(self.game.clock.get_fps())),
                                                  True,
                                                  (255, 255, 255))
        self.game.renderer.load_texture_from_surface("fps_counter", fps_counter)
        self.game.renderer.draw_rect(
            self.margin,
            self.margin,
            fps_counter.get_width(),
            fps_counter.get_height(),
            "fps_counter"
        )

    def draw(self, map_state):
        self.healthbar.draw()
        self.armorbar.draw()
        self.minimap.draw(map_state)
        if not self.game.weapon.current_weapon_type() == "Melee":
            self.weapons_hud.draw()
