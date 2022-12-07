from sprite_object import *

class Weapon():
    def __init__(self, game):
        #self.images = deque(
        #    [pg.transform.smoothscale(img, (self.image.get_width() * scale, self.image.get_height() * scale))
        #     for img in self.images])
        # Standby Image
        self.game = game
        self.standby_animation = deque()
        self.standby_animation.append(self.load_image("resources/sprites/weapon/shotgun/0.png"))
        # Fire Animation
        self.fire_animation = deque()
        self.fire_animation.append(self.load_image("resources/sprites/weapon/shotgun/1.png"))
        self.fire_animation.append(self.load_image("resources/sprites/weapon/shotgun/2.png"))
        self.fire_animation.append(self.load_image("resources/sprites/weapon/shotgun/3.png"))
        self.fire_animation.append(self.load_image("resources/sprites/weapon/shotgun/4.png"))
        self.fire_animation.append(self.load_image("resources/sprites/weapon/shotgun/5.png"))
        self.fire_animation_speed = 130
        # Meleee Animation
        self.melee_animation = deque()
        self.melee_animation.append(self.load_image("resources/sprites/weapon/shotgun/m_1.png"))
        self.melee_animation.append(self.load_image("resources/sprites/weapon/shotgun/m_2.png"))
        self.melee_animation_speed = 100

        self.damage = 70
        self.buff = 1
        self.reloading = False
        self.frame_counter = 0
        self.animation_trigger = False
        self.animation_time_prev = pg.time.get_ticks()
        self.weapon_pos = (HALF_WIDTH - self.standby_animation[0].get_width() // 2, HEIGHT - self.standby_animation[0].get_height())
        self.currently_draw = self.standby_animation
        self.current_state = "Standby"

    def set_buff(self, number):
        self.buff = number

    def animate(self, state="Standby"):
        # Set all variables
        weapon_animation = self.fire_animation_speed
        if state == "Fire":
            self.current_state = "Fire"
            self.damage = 60 * self.buff
            images = self.fire_animation
            weapon_animation = self.fire_animation_speed
        elif state == "Melee":
            self.current_state = "Melee"
            self.damage = 80 * self.buff
            images = self.melee_animation
            weapon_animation = self.melee_animation_speed

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
                    self.current_state = "Standby"
                    self.currently_draw = self.standby_animation


    def draw(self):
        self.game.screen.blit(self.currently_draw[0], self.weapon_pos)

    def update(self, state="Standby"):
        self.animate(state)

    def load_image(self, path, scale=0.4):
        if os.path.isfile(path) and os.path.exists(path):
            img = pg.image.load(path).convert_alpha()
        img = pg.transform.smoothscale(img,(img.get_width() * scale, img.get_height() * scale))
        return img
