import copy
import random

from weapons.empty_hands import Empty
from weapons.pitchfork import Pitchfork
from weapons.revolver import Revolver
from weapons.double_shotgun import DoubleShotgun
from weapons.automatic_rifle import AutomaticRifle

from bullet import Bullet
from sprites.sprite import *
from collections import deque
import os
from copy import deepcopy


class Weapon:
    def __init__(self, game):
        self.game = game
        self.current_weapon = "Empty"
        self.current_state = "Standby"
        self.current_index = 0

        self.saved_weapons = {}
        self.weapon_info = {}
        self.weapon_info.update(Empty(game).weapon_info)
        self.weapon_info.update(Pitchfork(game).weapon_info)
        self.weapon_info.update(Revolver(game).weapon_info)
        self.weapon_info.update(DoubleShotgun(game).weapon_info)
        self.weapon_info.update(AutomaticRifle(game).weapon_info)

        self.WIDTH = self.game.width
        self.HEIGHT = self.game.height

        self.cur_display = self.weapon_info[self.current_weapon][self.current_state]["Sprites"][0]
        self.weapon_pos = (0, 0)

        self.mouse_down = False
        self.fired = False
        self.damage_buff = 1

        self.current_time = 0
        self.last_shot = 0

        self.play_next_frame = False
        self.currently_playing = False
        self.ready_for_animation = True
        self.animation_finished = True
        self.prev_frame_time = pg.time.get_ticks()
        self.animation_started_time = 0

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
                self.current_index = 0
            elif self.current_index < 0:
                self.current_index = len(self.weapon_info) - 1
            self.change_weapon(list(self.weapon_info)[self.current_index])

    def update(self):
        self.current_time = pg.time.get_ticks()
        self.check_animation_time()
        self.animate()
        if self.mouse_down and not self.currently_playing:
            weapon = self.weapon_info[self.current_weapon]["Fire"]
            weapon_type = self.weapon_info[self.current_weapon]["Type"]

            # If weapon type semi, fire single time and make user press mouse again
            if not weapon_type == "Auto" or weapon["Cartridge Contains"] < 1:
                self.mouse_down = False

            if self.current_time - self.last_shot > weapon["Speed"]:
                if weapon["Cartridge Contains"] > 0:
                    self.fired = True
                    self.change_animation("Fire")
                    weapon["Cartridge Contains"] -= weapon["Bullet Per Shot"]
                    if weapon["Bullet Per Shot"] > 1 or weapon_type == "Auto":
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
            self.weapon_pos[0] / self.WIDTH * self.game.width,
            self.weapon_pos[1] / self.HEIGHT * self.game.height,
            self.game.renderer.get_texture_width(self.cur_display) / self.WIDTH * self.game.width,
            self.game.renderer.get_texture_height(self.cur_display) / self.HEIGHT * self.game.height,
            self.cur_display
        )

    def reload(self):
        if not self.currently_playing:
            weapon = self.weapon_info[self.current_weapon]["Fire"]
            if weapon["Bullet Left"] > 1:
                if not weapon["Cartridge Contains"] == weapon["Cartridge Holds"]:
                    self.change_animation("Reload")
                    self.game.sound.play_sfx(self.current_weapon + " " + self.current_state)
                    if weapon["Bullet Left"] > weapon["Cartridge Holds"]:
                        weapon["Cartridge Contains"] = weapon["Cartridge Holds"]
                        weapon["Bullet Left"] -= weapon["Cartridge Holds"]
                    else:
                        weapon["Cartridge Contains"] = weapon["Bullet Left"]
                        weapon["Bullet Left"] = 0

    # Getters
    def get_accuracy(self):
        return self.weapon_info[self.current_weapon][self.current_state]["Accuracy"]

    def get_damage(self):
        return self.weapon_info[self.current_weapon][self.current_state]["Damage"]

    def get_cartridge_bullet_left(self):
        return self.weapon_info[self.current_weapon]["Fire"]["Cartridge Contains"]

    def get_total_bullet_left(self):
        return self.weapon_info[self.current_weapon]["Fire"]["Bullet Left"]

    def get_current_weapon_type(self):
        return self.weapon_info[self.current_weapon]["Type"]

    # Setters
    def set_damage_buff(self, buff_val):
        for weapon in self.weapon_info:
            if not self.weapon_info[weapon]["Unlocked"]:
                self.weapon_info[weapon]["Fire"]["Damage"] = self.weapon_info[weapon]["Fire"]["Damage"] * buff_val

    # Other Functions
    def add_bullets(self, weapon, number):
        self.weapon_info[weapon]["Fire"]["Bullet Left"] += number

    def create_bullet(self, dispersity=None):
        weapon = self.weapon_info[self.current_weapon]["Fire"]
        if dispersity:
            angle = self.game.player.angle + dispersity
            angle_ver = -self.game.player.angle_ver + dispersity
        else:
            angle = self.game.player.angle
            angle_ver = -self.game.player.angle_ver
        self.game.object_handler.add_bullet(Bullet(self.game,
                                                   self.game.player.exact_pos,
                                                   weapon["Damage"],
                                                   angle,
                                                   angle_ver,
                                                   'player',
                                                   weapon["Bullet Lifetime"],
                                                   weapon["Bullet Velocity"]))

    def change_weapon(self, weapon):
        if not self.currently_playing:
            if self.weapon_info[weapon]["Unlocked"]:
                self.current_weapon = weapon
                self.cur_display = self.weapon_info[self.current_weapon][self.current_state]["Sprites"][0]

    def unlock(self, weapon):
        self.weapon_info[weapon]["Unlocked"] = True
        self.current_weapon = weapon

    def reset_weapon_pos(self):
        self.weapon_pos = (self.WIDTH / 2 - self.game.renderer.get_texture_width(self.cur_display) // 2,
                           self.HEIGHT - self.game.renderer.get_texture_height(self.cur_display))

    def change_animation(self, state):
        self.current_state = state

        # Reset animation variables
        self.animation_started_time = pg.time.get_ticks()
        self.animation_finished = False
        self.currently_playing = True

        self.animate()

    def animate(self):
        weapon = self.weapon_info[self.current_weapon][self.current_state]

        if self.animation_finished:
            self.currently_playing = False
            self.current_state = "Standby"
            self.cur_display = weapon["Sprites"][0]
            return

        if self.play_next_frame:
            weapon["Sprites"].rotate(-1)
            self.cur_display = weapon["Sprites"][0]
            self.play_next_frame = False

    def check_animation_time(self):
        weapon = self.weapon_info[self.current_weapon][self.current_state]
        current_time = pg.time.get_ticks()

        if current_time - self.prev_frame_time > weapon["Speed"] \
                and not self.animation_finished:
            self.prev_frame_time = current_time
            self.play_next_frame = True

        if current_time - self.animation_started_time > len(weapon["Sprites"]) * weapon["Speed"] \
                and not self.animation_finished:
            self.animation_finished = True

    def save_weapon_info(self):
        self.saved_weapons = copy.deepcopy(self.weapon_info)

    def load_weapon_info(self):
        self.weapon_info.update(self.saved_weapons)
