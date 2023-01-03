from projectile import Projectile
from sprites.animation_manager import *
from sprites.sprite import *
from weapons.empty_hands import Empty
from weapons.pitchfork import Pitchfork
from weapons.revolver import Revolver
from weapons.double_shotgun import DoubleShotgun
from weapons.automatic_rifle import AutomaticRifle
import copy
import random


class Weapon:
    def __init__(self, game):
        self.game = game
        self.animation = Animation()

        # Load all weapons
        self.weapon_info = self.saved_weapons = {}
        self.weapon_info.update(Empty(game).weapon_info)
        self.weapon_info.update(Pitchfork(game).weapon_info)
        self.weapon_info.update(Revolver(game).weapon_info)
        self.weapon_info.update(DoubleShotgun(game).weapon_info)
        self.weapon_info.update(AutomaticRifle(game).weapon_info)

        # Set current weapon and its state
        self.selected_weapon = self.saved_current_weapon = "Empty"
        self.current_state = self.saved_current_state = "Idle"
        self.current_index = 0

        # Make animations ready to use
        self.animation.load_sprite_animations(self.current_weapon())
        self.animation.change_animation("Idle")
        self.sprite = self.saved_sprite = self.animation.get_sprite()

        self.weapon_pos = (0, 0)
        self.mouse_down = False
        self.fired = False
        self.damage_buff = 1

        self.current_time = 0
        self.last_shot = 0

    def handle_events(self, event):
        if event.type == pg.KEYUP:
            for index, name in enumerate(self.weapon_info):
                if event.key == pg.key.key_code(str(index)):
                    self.change_weapon(name)
                    self.current_index = index

            if event.key == pg.K_r:
                self.reload()

        elif event.type == pg.MOUSEBUTTONUP and event.button == 1:
            self.mouse_down = False

        elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            self.mouse_down = True

        elif event.type == pg.MOUSEWHEEL:
            self.current_index += event.y
            if self.current_index > len(self.weapon_info) - 1:
                self.current_index = 1
            elif self.current_index <= 0:
                self.current_index = len(self.weapon_info) - 1
            self.change_weapon(list(self.weapon_info)[self.current_index])

    def update(self):
        self.current_time = pg.time.get_ticks()

        self.animation.animate(self.game.dt)

        self.current_state = self.animation.get_state()
        self.sprite = self.animation.get_sprite()

        if self.mouse_down and not self.animation.is_playing():
            weapon = self.current_weapon()["Fire"]

            # If weapon type semi, fire single time and make user press mouse again
            if not self.current_weapon_type() == "Auto" or weapon["Cartridge Contains"] < 1:
                self.mouse_down = False

            if self.current_time - self.last_shot > weapon["Speed"]:
                if weapon["Cartridge Contains"] > 0:
                    self.fired = True
                    self.change_state("Fire")
                    weapon["Cartridge Contains"] -= weapon["Bullet Per Shot"]
                    if weapon["Bullet Per Shot"] > 1:
                        for bullet in range(weapon["Bullet Per Shot"]):
                            accuracy = random.uniform(-weapon["Bullet Offset"],
                                                      weapon["Bullet Offset"])
                            self.create_bullet(accuracy)
                            self.game.hud.weapons_hud.update_bullet_left(weapon["Cartridge Contains"],
                                                                         weapon["Bullet Left"])
                    else:
                        self.create_bullet()
                        self.game.hud.weapons_hud.update_bullet_left(weapon["Cartridge Contains"],
                                                                     weapon["Bullet Left"])
                    self.game.sound.play_sfx(self.selected_weapon + " " + self.current_state)
                    self.last_shot = pg.time.get_ticks()
                elif weapon["Bullet Left"] > 1:
                    # Automatically reload weapon if current cartridge empty
                    self.reload()
                else:
                    if not self.current_weapon_type() == "Melee":
                        self.game.sound.play_sfx("Weapon Empty")

    def draw(self):
        self.game.renderer.draw_rect(
            self.weapon_pos[0],
            self.weapon_pos[1],
            self.game.renderer.get_texture_width(self.sprite),
            self.game.renderer.get_texture_height(self.sprite),
            self.sprite
        )

    def reset_weapon_pos(self):
        self.weapon_pos = (self.game.width / 2 - self.game.renderer.get_texture_width(self.sprite) // 2,
                           self.game.height - self.game.renderer.get_texture_height(self.sprite))

    def change_state(self, state):
        self.current_state = state
        self.animation.change_animation(state)

    def reload(self):
        if not self.animation.is_playing():
            weapon = self.current_weapon()["Fire"]
            if weapon["Bullet Left"] > 1:
                if not weapon["Cartridge Contains"] == weapon["Cartridge Holds"]:
                    self.change_state("Reload")
                    self.game.sound.play_sfx(self.selected_weapon + " " + self.current_state)
                    if weapon["Bullet Left"] > weapon["Cartridge Holds"]:
                        weapon["Cartridge Contains"] = weapon["Cartridge Holds"]
                        weapon["Bullet Left"] -= weapon["Cartridge Holds"]
                    else:
                        weapon["Cartridge Contains"] = weapon["Bullet Left"]
                        weapon["Bullet Left"] = 0
                    self.game.hud.weapons_hud.update_bullet_left(weapon["Cartridge Contains"], weapon["Bullet Left"])

    # Other Functions
    def add_bullets(self, weapon, number):
        self.weapon_info[weapon]["Fire"]["Bullet Left"] += number
        self.game.hud.weapons_hud.update_bullet_left(self.bullet_left_in_weapon(), self.total_bullet_left())

    def create_bullet(self, spread=None):
        weapon = self.current_weapon()["Fire"]
        player = self.game.player
        handler = self.game.object_handler

        if spread:
            angle_hor = player.angle + spread
            angle_ver = -player.angle_ver + spread
        else:
            angle_hor = player.angle
            angle_ver = -player.angle_ver
        angle = [angle_hor, angle_ver]
        position = [player.x, player.y, player.z + (player.height / 2)]
        bullet_data = [weapon["Damage"], weapon["Bullet Velocity"], weapon["Bullet Lifetime"], "Player", 0.05, 0.05]
        handler.add_bullet(Projectile(self.game, position, angle, bullet_data))

    def unlock(self, weapon):
        self.weapon_info[weapon]["Unlocked"] = True
        self.change_weapon(weapon)
        self.game.hud.weapons_hud.weapon_unlocked(weapon, self.bullet_left_in_weapon(), self.total_bullet_left())

    def change_weapon(self, weapon):
        if self.weapon_info[weapon]["Unlocked"]:
            self.selected_weapon = weapon
            self.animation.load_sprite_animations(self.current_weapon())
            self.animation.change_animation("Idle")
            self.sprite = self.animation.get_sprite()
            self.reset_weapon_pos()
            self.game.hud.weapons_hud.update_current_weapon(weapon, self.bullet_left_in_weapon(),
                                                            self.total_bullet_left())

    def save_weapon_info(self):
        self.saved_weapons = copy.deepcopy(self.weapon_info)
        self.saved_current_weapon = self.selected_weapon
        self.saved_current_state = self.current_state
        self.saved_sprite = self.sprite

    def load_weapon_info(self):
        self.weapon_info.clear()
        self.weapon_info = copy.deepcopy(self.saved_weapons)
        self.selected_weapon = self.saved_current_weapon
        self.current_state = self.saved_current_state
        self.sprite = self.saved_sprite

    # Getters
    def current_weapon(self):
        return self.weapon_info[self.selected_weapon]

    def current_weapon_state(self):
        return self.current_weapon()[self.current_state]

    def current_weapon_accuracy(self):
        return self.current_weapon_state()["Accuracy"]

    def current_weapon_damage(self):
        return self.current_weapon_state()["Damage"]

    def current_weapon_type(self):
        return self.current_weapon()["Type"]

    def bullet_left_in_weapon(self):
        return self.current_weapon()["Fire"]["Cartridge Contains"]

    def total_bullet_left(self):
        return self.current_weapon()["Fire"]["Bullet Left"]

    # Setters
    def set_damage_buff(self, buff_val):
        for weapon in self.weapon_info:
            if not self.weapon_info[weapon]["Unlocked"]:
                self.weapon_info[weapon]["Fire"]["Damage"] = self.weapon_info[weapon]["Fire"]["Damage"] * buff_val
