import pygame as pg
import math


class Sound:
    def __init__(self):
        pg.mixer.init()
        self.path = 'resources/sound/'

        # Weapon Sounds
        self.shotgun_fire = pg.mixer.Sound(self.path + 'weapon_shotgun_fire.wav')
        self.shotgun_empty = pg.mixer.Sound(self.path + 'weapon_shotgun_empty.wav')
        self.shotgun_melee = pg.mixer.Sound(self.path + 'weapon_shotgun_melee.wav')

        # NPC Sounds
        self.npc_pain = [
            pg.mixer.Sound(self.path + 'npc_pain_1.wav'),
            pg.mixer.Sound(self.path + 'npc_pain_2.wav'),
            pg.mixer.Sound(self.path + 'npc_pain_3.wav')
        ]
        self.npc_death = [
            pg.mixer.Sound(self.path + 'npc_death_1.wav'),
            pg.mixer.Sound(self.path + 'npc_death_2.wav'),
            pg.mixer.Sound(self.path + 'npc_death_3.wav'),
            pg.mixer.Sound(self.path + 'npc_death_4.wav')
        ]
        self.npc_attack = [
            pg.mixer.Sound(self.path + 'npc_attack_1.wav'),
            pg.mixer.Sound(self.path + 'npc_attack_2.wav')
        ]

        # Player Sounds
        self.player_pain = [
            pg.mixer.Sound(self.path + 'player_pain_1.wav'),
            pg.mixer.Sound(self.path + 'player_pain_2.wav')
        ]
        self.buff_damage = pg.mixer.Sound(self.path + 'buff_damage.wav')
        self.player_healed = pg.mixer.Sound(self.path + 'player_healed.wav')

        # Pickup Sounds
        self.pickup_ammo = pg.mixer.Sound(self.path + 'pickup_ammo.wav')
        self.pickup_health = pg.mixer.Sound(self.path + 'pickup_health.wav')
        self.pickup_armor = pg.mixer.Sound(self.path + 'pickup_armor.wav')

        # Lose and win sounds
        self.lose = pg.mixer.Sound(self.path + 'lose.wav')
        self.win = pg.mixer.Sound(self.path + 'win.wav')

    def play_sound(self, sound, src_distance, dst_distance):
        x_diff = abs(src_distance[0] - dst_distance[0])
        y_diff = abs(src_distance[1] - dst_distance[1])
        if (x_diff + y_diff) < 1:
            normalized = 1
        else:
            normalized = 0.9 - ((x_diff + y_diff) / 10)
        sound.set_volume(normalized)
        sound.play()
