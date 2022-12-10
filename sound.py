import pygame as pg


class Sound:
    def __init__(self):
        pg.mixer.init()
        self.path = 'resources/sound/'

        # Weapon Sounds
        self.shotgun_fire = pg.mixer.Sound(self.path + 'weapon_shotgun_fire.wav')
        self.shotgun_melee = pg.mixer.Sound(self.path + 'weapon_shotgun_melee.wav')

        # NPC Sounds
        self.npc_pain = pg.mixer.Sound(self.path + 'npc_pain.wav')
        self.npc_death = pg.mixer.Sound(self.path + 'npc_death.wav')
        self.npc_attack = pg.mixer.Sound(self.path + 'npc_attack.wav')

        # Player Sounds
        self.player_healed = pg.mixer.Sound(self.path + 'player_healed.wav')
        self.player_pain = pg.mixer.Sound(self.path + 'player_pain.wav')
        self.buff_damage = pg.mixer.Sound(self.path + 'buff_damage.wav')

        # Pickup Sounds
        self.pickup_ammo = pg.mixer.Sound(self.path + 'pickup_ammo.wav')
        self.pickup_health = pg.mixer.Sound(self.path + 'pickup_health.wav')
        self.pickup_armor = pg.mixer.Sound(self.path + 'pickup_armor.wav')

        # Lose and win sounds
        self.lose = pg.mixer.Sound(self.path + 'lose.wav')
        self.win = pg.mixer.Sound(self.path + 'win.wav')
