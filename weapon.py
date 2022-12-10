from sprite_object import *


def load_images(images, scale=0.4):
    loaded_images = deque()
    for image in images:
        full_path = "resources/sprites/weapon/shotgun/" + str(image) + ".png"
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

        self.current_state = "Standby"
        self.weapon_info = {
            "Standby": {
                "Sprites": load_images([0]),
                "Damage": 0,
                "Speed": 1,
            },
            "Melee": {
                "Sprites": load_images(["m_1", "m_2"]),
                "Damage": 24,
                "Speed": 210,
            },
            "Fire": {
                "Sprites": load_images([1, 2, 3, 4, 5]),
                "Damage": 70,
                "Speed": 170,
                "Bullet Left": 10
            }
        }
        self.cur_display = self.weapon_info[self.current_state]["Sprites"]
        self.weapon_pos = (HALF_WIDTH - self.cur_display[0].get_width() // 2,
                           HEIGHT - self.cur_display[0].get_height())

        self.fired = False
        self.damage_buff = 1

        self.reloading = False
        self.frame_counter = 0
        self.animation_trigger = False
        self.animation_time_prev = pg.time.get_ticks()

    def handle_events(self, event):
        if event.type == pg.MOUSEBUTTONDOWN and not self.reloading:
            if event.button == 1:
                if self.weapon_info["Fire"]["Bullet Left"] > 0:
                    self.fired = True
                    self.reloading = True
                    self.current_state = "Fire"
                    self.weapon_info["Fire"]["Bullet Left"] -= 1
                    self.game.sound.shotgun_fire.play()
                else:
                    self.game.sound.shotgun_empty.play()

            if event.button == 3:
                self.fired = True
                self.reloading = True
                self.current_state = "Melee"
                self.game.sound.shotgun_melee.play()

    def update(self):
        self.animate()

    def draw(self):
        self.game.screen.blit(self.cur_display[0], self.weapon_pos)

    # Getters
    def get_damage(self):
        return self.weapon_info[self.current_state]["Damage"]

    def get_bullet_left(self):
        return self.weapon_info["Fire"]["Bullet Left"]

    # Setters
    def set_damage_buff(self, buff_val):
        for attack in self.weapon_info:
            self.weapon_info[attack]["Damage"] = self.weapon_info[attack]["Damage"] * buff_val

    # Other Functions
    def add_bullets(self, number):
        self.weapon_info["Fire"]["Bullet Left"] += number

    def animate(self):
        # Make animation
        if self.reloading:
            self.fired = False
            self.animation_timer()
            if self.animation_trigger:
                self.weapon_info[self.current_state]["Sprites"].rotate(-1)
                self.cur_display = self.weapon_info[self.current_state]["Sprites"]
                self.frame_counter += 1
                if self.frame_counter == len(self.weapon_info[self.current_state]["Sprites"]):
                    self.frame_counter = 0
                    self.reloading = False
                    self.current_state = "Standby"
                    self.cur_display = self.weapon_info["Standby"]["Sprites"]

    def animation_timer(self):
        # Check for animation timer
        self.animation_trigger = False
        time_now = pg.time.get_ticks()
        if time_now - self.animation_time_prev > self.weapon_info[self.current_state]["Speed"]:
            self.animation_time_prev = time_now
            self.animation_trigger = True
