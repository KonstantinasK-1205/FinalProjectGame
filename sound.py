import pygame as pg


class Sound:
    def __init__(self):
        pg.mixer.init()
        self.master_vol = 1.0
        self.sound_enabled = True
        self.path = 'resources/sound/'
        self.sound_in_queue = []
        self.sound_db = {
            # Weapon sounds
            "Shotgun Fire": pg.mixer.Sound(self.path + 'weapon_shotgun_fire.wav'),
            "Shotgun Empty": pg.mixer.Sound(self.path + 'weapon_shotgun_empty.wav'),
            "Shotgun Melee": pg.mixer.Sound(self.path + 'weapon_shotgun_melee.wav'),
            "Machinegun Fire": pg.mixer.Sound(self.path + 'weapon_machinegun_fire.wav'),
            # NPC sounds
            "Zombie pain": pg.mixer.Sound(self.path + 'npc_zombie_pain.wav'),
            "Zombie death": pg.mixer.Sound(self.path + 'npc_zombie_death.wav'),
            "Zombie attack": pg.mixer.Sound(self.path + 'npc_zombie_attack.wav'),
            "Soldier pain": pg.mixer.Sound(self.path + 'npc_soldier_pain.wav'),
            "Soldier death": pg.mixer.Sound(self.path + 'npc_soldier_death.wav'),
            "Soldier attack": pg.mixer.Sound(self.path + 'npc_soldier_attack.wav'),
            "Battlelord pain": pg.mixer.Sound(self.path + 'npc_battlelord_pain.wav'),
            "Battlelord death": pg.mixer.Sound(self.path + 'npc_battlelord_death.wav'),
            "Battlelord attack": pg.mixer.Sound(self.path + 'npc_battlelord_attack.wav'),
            "Reaper pain": pg.mixer.Sound(self.path + 'npc_reaper_pain.wav'),
            "Reaper death": pg.mixer.Sound(self.path + 'npc_reaper_death.wav'),
            "Reaper attack": pg.mixer.Sound(self.path + 'npc_reaper_attack.wav'),
            "Reaper teleportation": pg.mixer.Sound(self.path + 'npc_reaper_teleportation.wav'),
            # Pickup sounds
            "Pickup ammo": pg.mixer.Sound(self.path + 'pickup_ammo.wav'),
            "Pickup armor": pg.mixer.Sound(self.path + 'pickup_armor.wav'),
            "Pickup health": pg.mixer.Sound(self.path + 'pickup_health.wav'),
            # Player sounds
            "Player pain": pg.mixer.Sound(self.path + 'player_pain_1.wav'),
            "Player dmg buff": pg.mixer.Sound(self.path + 'buff_damage.wav'),
            # World sounds
            "Bullet in wall": pg.mixer.Sound(self.path + 'bullet_to_wall.wav'),
            # State sounds
            "Lose": pg.mixer.Sound(self.path + 'lose.wav'),
            "Win": pg.mixer.Sound(self.path + 'win.wav')
        }

    def update(self):
        if len(self.sound_in_queue) > 0:
            self.play_queue()

    def pickup_sound(self, sound):
        if not pg.mixer.get_busy():
            self.play_sfx(sound)
        else:
            if sound not in self.sound_in_queue:
                self.sound_in_queue.append(sound)

    def play_queue(self):
        if not pg.mixer.get_busy():
            self.play_sfx(self.sound_in_queue[0])
            self.sound_in_queue.pop(0)

    def play_sfx(self, sound, distance=None):
        if self.sound_enabled:
            if sound in self.sound_db:
                self.sound_db[sound].set_volume(self.master_vol)
                if distance is not None:
                    x_diff = abs(distance[0][0] - distance[1][0])
                    y_diff = abs(distance[0][1] - distance[1][1])
                    if (x_diff + y_diff) < 1:
                        normalized = self.master_vol
                    else:
                        normalized = (self.master_vol - 0.1) - ((x_diff + y_diff) / 10)
                    self.sound_db[sound].set_volume(normalized)
                self.sound_db[sound].play()
            else:
                print("Sound: " + str(sound) + "wasn't found!")

    def change_vol(self, num):
        self.master_vol += num
        if self.master_vol > 100:
            self.master_vol = 100

        if self.master_vol < 0:
            self.master_vol = 0
            self.sound_enabled = False
