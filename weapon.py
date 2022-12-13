from sprites.sprite import *
from Bullet import *


def load_images(weapon, images, scale=0.4):
    loaded_images = deque()
    for image in images:
        full_path = "resources/sprites/weapon/" + weapon + "/" + str(image) + ".png"
        if os.path.exists(full_path):
            img = pg.image.load(full_path).convert_alpha()
        else:
            break
        img = pg.transform.smoothscale(img, (img.get_width() * scale, img.get_height() * scale))
        loaded_images.append(img)
    return loaded_images


class Weapon:
    def __init__(self, game):
        self.game = game
        self.current_weapon = "Shotgun"
        self.current_state = "Standby"
        self.weapon_info = {
            "Shotgun": {
                "Unlocked": True,
                "Standby": {
                    "Sprites": load_images("shotgun", [0]),
                    "Damage": 0,
                    "Speed": 1,
                    "Accuracy": 100
                },
                "Melee": {
                    "Sprites": load_images("shotgun", ["m_1", "m_2"]),
                    "Damage": 10,
                    "Speed": 210,
                    "Accuracy": 90
                },
                "Fire": {
                    "Sprites": load_images("shotgun", [1, 2, 3, 4, 5]),
                    "Damage": 70,
                    "Speed": 170,
                    "Accuracy": 80,
                    "Currently in Cartridge": 1,
                    "Maximum in Cartridge": 1,
                    "Bullet Left": 10
                }
            },
            "Machinegun": {
                "Unlocked": False,
                "Standby": {
                    "Sprites": load_images("machinegun", [0], 3.5),
                    "Damage": 0,
                    "Speed": 1,
                },
                "Fire": {
                    "Sprites": load_images("machinegun", [1, 2, 3], 3.5),
                    "Damage": 50,
                    "Speed": 50,
                    "Accuracy": 40,
                    "Currently in Cartridge": 0,
                    "Maximum in Cartridge": 50,
                    "Bullet Left": 0
                }
            }
        }
        self.cur_display = self.weapon_info[self.current_weapon][self.current_state]["Sprites"]
        self.weapon_pos = (HALF_WIDTH - self.cur_display[0].get_width() // 2,
                           HEIGHT - self.cur_display[0].get_height())

        self.fired = False
        self.damage_buff = 1

        self.current_time = 0
        self.previous_shot = 0
        self.frame_counter = 0
        self.animation_trigger = False
        self.animation_time_prev = pg.time.get_ticks()

    def handle_events(self, event):
        if event.type == pg.KEYUP:
            if event.key == pg.K_1:
                self.change_weapon("Shotgun")
            if event.key == pg.K_2:
                if self.weapon_info["Machinegun"]["Unlocked"]:
                    self.change_weapon("Machinegun")
            if event.key == pg.K_r:
                self.reload()

        if event.type == pg.MOUSEBUTTONUP:
            self.fired = False

        if event.type == pg.MOUSEBUTTONDOWN:
            weapon = self.weapon_info[self.current_weapon]["Fire"]
            if event.button == 1:
                if self.current_time - self.previous_shot > weapon["Speed"] * 5:
                    if weapon["Currently in Cartridge"] > 0:
                        self.fired = True
                        self.current_state = "Fire"
                        self.frame_counter = 0
                        weapon["Currently in Cartridge"] -= 1
                        self.game.sound.shotgun_fire.play()
                        self.create_bullet()
                        self.previous_shot = pg.time.get_ticks()
                    else:
                        self.reload()
                        if weapon["Bullet Left"] < 1 and weapon["Currently in Cartridge"] < 1:
                            self.game.sound.shotgun_empty.play()

            if event.button == 3 and self.current_weapon == "Shotgun":
                if self.current_time - self.previous_shot > self.weapon_info["Shotgun"]["Melee"]["Speed"] * 5:
                    self.fired = True
                    self.current_state = "Melee"
                    self.frame_counter = 0
                    self.game.sound.shotgun_melee.play()

    def update(self):
        self.current_time = pg.time.get_ticks()
        self.animate()

    def draw(self):
        self.game.screen.blit(self.cur_display[0], self.weapon_pos)

    def reload(self):
        weapon = self.weapon_info[self.current_weapon]["Fire"]
        if not weapon["Currently in Cartridge"] == weapon["Maximum in Cartridge"]:
            if weapon["Bullet Left"] > weapon["Maximum in Cartridge"]:
                weapon["Currently in Cartridge"] = weapon["Maximum in Cartridge"]
                weapon["Bullet Left"] -= weapon["Maximum in Cartridge"]
            else:
                weapon["Currently in Cartridge"] = weapon["Bullet Left"]
                weapon["Bullet Left"] = 0

    # Getters
    def get_accuracy(self):
        return self.weapon_info[self.current_weapon][self.current_state]["Accuracy"]

    def get_damage(self):
        return self.weapon_info[self.current_weapon][self.current_state]["Damage"]

    def get_cartridge_bullet_left(self):
        return self.weapon_info[self.current_weapon]["Fire"]["Currently in Cartridge"]

    def get_total_bullet_left(self):
        return self.weapon_info[self.current_weapon]["Fire"]["Bullet Left"]

    # Setters
    def set_damage_buff(self, buff_val):
        for weapon in self.weapon_info:
            for attack in self.weapon_info[weapon]:
                if not attack == "Unlocked":
                    self.weapon_info[weapon][attack]["Damage"] = self.weapon_info[weapon][attack]["Damage"] * buff_val

    # Other Functions
    def add_bullets(self, weapon, number):
        if not self.weapon_info[weapon]["Unlocked"]:
            self.weapon_info[weapon]["Unlocked"] = True
        self.weapon_info[weapon]["Fire"]["Bullet Left"] += number

    def create_bullet(self):
        weapon = self.weapon_info[self.current_weapon]["Fire"]
        angle = self.game.player.angle + math.pi * 2
        self.game.object_handler.add_bullet(Bullet(self.game, self.game.player.get_pos, weapon["Damage"], angle, 'player'))

    def change_weapon(self, weapon):
        self.current_weapon = weapon
        self.cur_display = self.weapon_info[self.current_weapon][self.current_state]["Sprites"]
        if weapon == 'Shotgun':
            self.weapon_pos = (HALF_WIDTH - self.cur_display[0].get_width() // 2,
                               HEIGHT - self.cur_display[0].get_height())
        elif weapon == 'Machinegun':
            self.weapon_pos = (HALF_WIDTH / 1.6 - self.cur_display[0].get_width() // 2,
                               HEIGHT - self.cur_display[0].get_height())

    def animate(self):
        # Make animation
        self.animation_timer()
        if self.animation_trigger:
            self.weapon_info[self.current_weapon][self.current_state]["Sprites"].rotate(-1)
            self.cur_display = self.weapon_info[self.current_weapon][self.current_state]["Sprites"]
            self.frame_counter += 1
            if self.frame_counter == len(self.weapon_info[self.current_weapon][self.current_state]["Sprites"]):
                self.frame_counter = 0
                self.fired = False
                self.current_state = "Standby"
                self.cur_display = self.weapon_info[self.current_weapon]["Standby"]["Sprites"]

    def animation_timer(self):
        # Check for animation timer
        self.animation_trigger = False
        time_now = pg.time.get_ticks()
        if time_now - self.animation_time_prev > self.weapon_info[self.current_weapon][self.current_state]["Speed"]:
            self.animation_time_prev = time_now
            self.animation_trigger = True
