import pygame as pg


class Sound:
    def __init__(self):
        pg.mixer.init()
        self.path = 'resources/sound/'
        self.sound_in_queue = []

        # Weapon Sounds
        self.bullet_wall = pg.mixer.Sound(self.path + 'bullet_to_wall.wav')
        self.machgun_fire = pg.mixer.Sound(self.path + 'weapon_machinegun_fire.wav')
        self.shotgun_fire = pg.mixer.Sound(self.path + 'weapon_shotgun_fire.wav')
        self.shotgun_empty = pg.mixer.Sound(self.path + 'weapon_shotgun_empty.wav')
        self.shotgun_melee = pg.mixer.Sound(self.path + 'weapon_shotgun_melee.wav')

        # NPC Sounds
        self.npc_zombie_pain = pg.mixer.Sound(self.path + 'npc_zombie_pain.wav')
        self.npc_zombie_death = pg.mixer.Sound(self.path + 'npc_zombie_death.wav')
        self.npc_zombie_attack = pg.mixer.Sound(self.path + 'npc_zombie_attack.wav')

        self.npc_battlelord_pain = pg.mixer.Sound(self.path + 'npc_battlelord_pain.wav')
        self.npc_battlelord_death = pg.mixer.Sound(self.path + 'npc_battlelord_death.wav')
        self.npc_battlelord_attack = pg.mixer.Sound(self.path + 'npc_battlelord_attack.wav')

        self.npc_soldier_pain = pg.mixer.Sound(self.path + 'npc_soldier_pain.wav')
        self.npc_soldier_death = pg.mixer.Sound(self.path + 'npc_soldier_death.wav')
        self.npc_soldier_attack = pg.mixer.Sound(self.path + 'npc_soldier_attack.wav')

        self.npc_reaper_pain = pg.mixer.Sound(self.path + 'npc_reaper_pain.wav')
        self.npc_reaper_death = pg.mixer.Sound(self.path + 'npc_reaper_death.wav')
        self.npc_reaper_attack = pg.mixer.Sound(self.path + 'npc_reaper_attack.wav')
        self.npc_reaper_teleportation = pg.mixer.Sound(self.path + 'npc_reaper_teleportation.wav')

        # Player Sounds
        self.player_pain = pg.mixer.Sound(self.path + 'player_pain_1.wav')
        self.buff_damage = pg.mixer.Sound(self.path + 'buff_damage.wav')

        # Pickup Sounds
        self.pickup_ammo = pg.mixer.Sound(self.path + 'pickup_ammo.wav')
        self.pickup_health = pg.mixer.Sound(self.path + 'pickup_health.wav')
        self.pickup_armor = pg.mixer.Sound(self.path + 'pickup_armor.wav')

        # Lose and win sounds
        self.lose = pg.mixer.Sound(self.path + 'lose.wav')
        self.win = pg.mixer.Sound(self.path + 'win.wav')

    def update(self):
        if len(self.sound_in_queue) > 0:
            self.play_queue()

    def play_sound(self, sound, src_distance, dst_distance):
        x_diff = abs(src_distance[0] - dst_distance[0])
        y_diff = abs(src_distance[1] - dst_distance[1])
        if (x_diff + y_diff) < 1:
            normalized = 1
        else:
            normalized = 0.9 - ((x_diff + y_diff) / 10)
        sound.set_volume(normalized)
        sound.play()

    def pickup_sound(self, sound):
        if not pg.mixer.get_busy():
            sound.play()
        else:
            if sound not in self.sound_in_queue:
                self.sound_in_queue.append(sound)

    def play_queue(self):
        if not pg.mixer.get_busy():
            self.sound_in_queue[0].play()
            self.sound_in_queue.pop(0)
