from sprite_object import *


def load_images(images, scale=0.4):
    loaded_images = deque()
    for image in images:
        full_path = "resources/sprites/weapon/shotgun/" + str(image) + ".png"
        if os.path.isfile(full_path) and os.path.exists(full_path):
            img = pg.image.load(full_path).convert_alpha()
        else:
            break
        img = pg.transform.smoothscale(img, (img.get_width() * scale, img.get_height() * scale))
        loaded_images.append(img)
    return loaded_images


class Weapon:
    def __init__(self, game):
        self.game = game
        self.standby_animation = load_images([0])
        # Fire Animation
        self.fire_animation = load_images([1, 2, 3, 4, 5])
        self.fire_animation_speed = 170
        # Melee Animation
        self.melee_animation = load_images(["m_1", "m_2"])
        self.melee_animation_speed = 120

        self.damage = 70
        self.damage_buff = 1
        self.reloading = False
        self.frame_counter = 0
        self.animation_trigger = False
        self.animation_time_prev = pg.time.get_ticks()
        self.weapon_pos = (HALF_WIDTH - self.standby_animation[0].get_width() // 2,
                           HEIGHT - self.standby_animation[0].get_height())
        self.currently_draw = self.standby_animation

    def set_damage_buff(self, number):
        self.damage_buff = number

    def animate(self, state="Standby"):
        # Set all variables
        if state == "Fire":
            self.damage = 60 * self.damage_buff
            images = self.fire_animation
            weapon_animation = self.fire_animation_speed
        elif state == "Melee":
            self.damage = 80 * self.damage_buff
            images = self.melee_animation
            weapon_animation = self.melee_animation_speed
        else:
            images = self.standby_animation
            weapon_animation = self.fire_animation_speed

        # Check for animation timer
        self.animation_trigger = False
        time_now = pg.time.get_ticks()
        if time_now - self.animation_time_prev > weapon_animation:
            self.animation_time_prev = time_now
            self.animation_trigger = True

        # Make animation
        if self.reloading:
            self.game.player.fired = False
            if self.animation_trigger:
                images.rotate(-1)
                self.currently_draw = images
                self.frame_counter += 1
                if self.frame_counter == len(images):
                    self.frame_counter = 0
                    self.reloading = False
                    self.game.player.weapon_attack = "Standby"
                    self.currently_draw = self.standby_animation

    def draw(self):
        self.game.screen.blit(self.currently_draw[0], self.weapon_pos)

    def update(self, state="Standby"):
        self.animate(state)
