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

        self.current_weapon = self.saved_current_weapon = "Empty"
        self.current_state = self.saved_current_state = "Standby"
        self.current_index = 0

        self.weapon_info = self.saved_weapons = {}
        self.weapon_info.update(Empty(game).weapon_info)
        self.weapon_info.update(Pitchfork(game).weapon_info)
        self.weapon_info.update(Revolver(game).weapon_info)
        self.weapon_info.update(DoubleShotgun(game).weapon_info)
        self.weapon_info.update(AutomaticRifle(game).weapon_info)

        self.sprite = self.saved_sprite = self.selected_weapon_info()["Sprites"][0]
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

        if event.type == pg.MOUSEBUTTONUP:
            if event.button == 1:
                self.mouse_down = False

        elif event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
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

        self.current_state = self.animation.animate(self.selected_weapon_info())
        self.animation.check_animation_time(self.selected_weapon_info())

        if self.mouse_down and not self.animation.currently_playing:
            weapon = self.weapon_info[self.current_weapon]["Fire"]
            weapon_type = self.weapon_info[self.current_weapon]["Type"]

            # If weapon type semi, fire single time and make user press mouse again
            if not weapon_type == "Auto" or weapon["Cartridge Contains"] < 1:
                self.mouse_down = False

            if self.current_time - self.last_shot > weapon["Speed"]:
                if weapon["Cartridge Contains"] > 0:
                    self.fired = True
                    self.change_state("Fire")
                    weapon["Cartridge Contains"] -= weapon["Bullet Per Shot"]
                    if weapon["Bullet Per Shot"] > 1:
                        for bullet in range(weapon["Bullet Per Shot"]):
                            accuracy = random.uniform(-weapon["Bullet Offset"], weapon["Bullet Offset"])
                            self.create_bullet(accuracy)
                    else:
                        self.create_bullet()
                    self.game.sound.play_sfx(self.current_weapon + " " + self.current_state)
                    self.last_shot = pg.time.get_ticks()
                elif weapon["Bullet Left"] > 1:
                    # Automatically reload weapon if current cartridge empty
                    self.reload()
                else:
                    if not weapon_type == "Melee":
                        self.game.sound.play_sfx("Weapon Empty")

    def draw(self):
        self.reset_weapon_pos()
        self.game.renderer.draw_rect(
            self.weapon_pos[0],
            self.weapon_pos[1],
            self.game.renderer.get_texture_width(self.animation.sprite),
            self.game.renderer.get_texture_height(self.animation.sprite),
            self.animation.sprite
        )

    def reset_weapon_pos(self):
        self.weapon_pos = (self.game.width / 2 - self.game.renderer.get_texture_width(self.animation.sprite) // 2,
                           self.game.height - self.game.renderer.get_texture_height(self.animation.sprite))

    def change_state(self, state):
        self.current_state = state
        self.animation.change_animation(state, self.selected_weapon_info()["Sprites"])

    def reload(self):
        if not self.animation.currently_playing:
            weapon = self.weapon_info[self.current_weapon]["Fire"]
            if weapon["Bullet Left"] > 1:
                if not weapon["Cartridge Contains"] == weapon["Cartridge Holds"]:
                    self.change_state("Reload")
                    self.game.sound.play_sfx(self.current_weapon + " " + self.current_state)
                    if weapon["Bullet Left"] > weapon["Cartridge Holds"]:
                        weapon["Cartridge Contains"] = weapon["Cartridge Holds"]
                        weapon["Bullet Left"] -= weapon["Cartridge Holds"]
                    else:
                        weapon["Cartridge Contains"] = weapon["Bullet Left"]
                        weapon["Bullet Left"] = 0

    # Getters
    def get_accuracy(self):
        return self.selected_weapon_info()["Accuracy"]

    def get_damage(self):
        return self.selected_weapon_info()["Damage"]

    def get_cartridge_bullet_left(self):
        return self.weapon_info[self.current_weapon]["Fire"]["Cartridge Contains"]

    def get_total_bullet_left(self):
        return self.weapon_info[self.current_weapon]["Fire"]["Bullet Left"]

    def get_current_weapon_type(self):
        return self.weapon_info[self.current_weapon]["Type"]

    def selected_weapon_info(self):
        return self.weapon_info[self.current_weapon][self.current_state]

    # Setters
    def set_damage_buff(self, buff_val):
        for weapon in self.weapon_info:
            if not self.weapon_info[weapon]["Unlocked"]:
                self.weapon_info[weapon]["Fire"]["Damage"] = self.weapon_info[weapon]["Fire"]["Damage"] * buff_val

    # Other Functions
    def add_bullets(self, weapon, number):
        self.weapon_info[weapon]["Fire"]["Bullet Left"] += number

    def create_bullet(self, spread=None):
        weapon = self.weapon_info[self.current_weapon]["Fire"]
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

    def change_weapon(self, weapon):
        if not self.animation.currently_playing:
            if self.weapon_info[weapon]["Unlocked"]:
                self.current_weapon = weapon
                self.animation.sprite = self.selected_weapon_info()["Sprites"][0]

    def unlock(self, weapon):
        self.weapon_info[weapon]["Unlocked"] = True
        self.current_weapon = weapon

    def save_weapon_info(self):
        self.saved_weapons = copy.deepcopy(self.weapon_info)
        self.saved_current_weapon = self.current_weapon
        self.saved_current_state = self.current_state
        self.saved_cur_display = self.animation.sprite

    def load_weapon_info(self):
        self.weapon_info.clear()
        self.weapon_info = copy.deepcopy(self.saved_weapons)
        self.current_weapon = self.saved_current_weapon
        self.current_state = self.saved_current_state
        self.animation.sprite = self.saved_cur_display
