import random
import pygame as pg


class Sound:
    def __init__(self, game):
        self.game = game

        pg.mixer.init()
        # Init sound channels
        self.weapon_channel = pg.mixer.Channel(0)
        self.npc_channel = pg.mixer.Channel(1)
        self.pickup_channel = pg.mixer.Channel(2)
        self.extra_channel = pg.mixer.Channel(3)

        self.master_vol = 1.0
        self.path = 'resources/sound/'
        self.play_music()
        self.sound_in_queue = []
        self.sound_db = {
            # Weapon sounds
            "Pitchfork Fire": ["Weapon", pg.mixer.Sound(self.path + 'weapon_pitchfork_fire.wav')],
            "Revolver Fire": ["Weapon", pg.mixer.Sound(self.path + 'weapon_pistol_fire.wav')],
            "Double Shotgun Fire": ["Weapon", pg.mixer.Sound(self.path + 'weapon_shotgun_fire.wav')],
            "Automatic Rifle Fire": ["Weapon", pg.mixer.Sound(self.path + 'weapon_rifle_fire.wav')],
            "Revolver Reload": ["Weapon", pg.mixer.Sound(self.path + 'weapon_pistol_reload.wav')],
            "Double Shotgun Reload": ["Weapon", pg.mixer.Sound(self.path + 'weapon_shotgun_reload.wav')],
            "Automatic Rifle Reload": ["Weapon", pg.mixer.Sound(self.path + 'weapon_rifle_reload.wav')],
            "Weapon Empty": ["Weapon", pg.mixer.Sound(self.path + 'weapon_empty.wav')],
            # NPC sounds
            "Zombie pain": ["Entity", pg.mixer.Sound(self.path + 'npc_zombie_pain.wav')],
            "Zombie death": ["Entity",
                             [pg.mixer.Sound(self.path + 'npc_zombie_death.wav'),
                              pg.mixer.Sound(self.path + 'npc_soldier_death.wav')]],
            "Zombie attack": ["Entity", pg.mixer.Sound(self.path + 'npc_zombie_attack.wav')],
            "Soldier pain": ["Entity", pg.mixer.Sound(self.path + 'npc_soldier_pain.wav')],
            "Soldier death": ["Entity", pg.mixer.Sound(self.path + 'npc_soldier_death.wav')],
            "Soldier attack": ["Entity", pg.mixer.Sound(self.path + 'npc_soldier_attack.wav')],
            "Battlelord pain": ["Entity", pg.mixer.Sound(self.path + 'npc_battlelord_pain.wav')],
            "Battlelord death": ["Entity", pg.mixer.Sound(self.path + 'npc_battlelord_death.wav')],
            "Battlelord attack": ["Entity", pg.mixer.Sound(self.path + 'npc_battlelord_attack.wav')],
            "Reaper pain": ["Entity", pg.mixer.Sound(self.path + 'npc_reaper_pain.wav')],
            "Reaper death": ["Entity", pg.mixer.Sound(self.path + 'npc_reaper_death.wav')],
            "Reaper attack": ["Entity", pg.mixer.Sound(self.path + 'npc_reaper_attack.wav')],
            "Reaper teleportation": ["Entity", pg.mixer.Sound(self.path + 'npc_reaper_teleportation.wav')],
            # Pickup sounds
            "Pickup ammo": ["Pickup", pg.mixer.Sound(self.path + 'pickup_ammo.wav')],
            "Pickup armor": ["Pickup", pg.mixer.Sound(self.path + 'pickup_armor.wav')],
            "Pickup health": ["Pickup", pg.mixer.Sound(self.path + 'pickup_health.wav')],
            # Player sounds
            "Player pain": ["Entity", pg.mixer.Sound(self.path + 'player_pain_1.wav')],
            "Player dmg buff": ["Entity", pg.mixer.Sound(self.path + 'buff_damage.wav')],
            # World sounds
            "Bullet in wall": ["Extra", pg.mixer.Sound(self.path + 'bullet_to_wall.wav')],
            # State sounds
            "Lose": ["Extra", pg.mixer.Sound(self.path + 'lose.wav')],
            "Win": ["Extra", pg.mixer.Sound(self.path + 'win.wav')],
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
        if (not self.game.settings_manager.settings["sound"]) or self.master_vol <= 0:
            return

        if sound in self.sound_db:
            category = self.sound_db[sound][0]
            sound = self.sound_db[sound][1]
            if type(sound) == list:
                sound = sound[random.randint(0, len(sound) - 1)]
            sound.set_volume(self.master_vol)
            if distance is not None:
                x_diff = abs(distance[0][0] - distance[1][0])
                y_diff = abs(distance[0][1] - distance[1][1])
                if (x_diff + y_diff) < 1:
                    normalized = self.master_vol
                else:
                    normalized = (self.master_vol - 0.1) - ((x_diff + y_diff) / 10)
                sound.set_volume(normalized)
            # Play each sound in their channel to prevent overloading SFX in channel
            if category == "Weapon":
                self.weapon_channel.play(sound)
            elif category == "Entity":
                self.npc_channel.play(sound)
            elif category == "Pickup":
                self.pickup_channel.play(sound)
            elif category == "Extra":
                self.extra_channel.play(sound)
            else:
                sound.play()
        else:
            print("sound.py: Sound doesn't exist - " + sound)

    def play_music(self):
        if not self.game.settings_manager.settings["music"] or pg.mixer_music.get_busy():
            return

        pg.mixer.music.load(self.path + "soundtrack.wav")
        pg.mixer_music.play(-1)

    def stop_music(self):
        pg.mixer_music.stop()

    def change_vol(self, num):
        self.master_vol += num
        if self.master_vol > 100:
            self.master_vol = 100
        elif self.master_vol < 0:
            self.master_vol = 0
