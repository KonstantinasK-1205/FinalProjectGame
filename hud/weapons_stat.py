class WeaponStats:
    def __init__(self, game, hud):
        # Init main variables
        self.game = game
        self.hud = hud

        # Load all weapon icons
        self.game.renderer.load_texture_from_file("resources/sprites/weapon/empty/idle.png")
        self.game.renderer.load_texture_from_file("resources/sprites/weapon/pitchfork/icon.png")
        self.game.renderer.load_texture_from_file("resources/sprites/weapon/revolver/icon.png")
        self.game.renderer.load_texture_from_file("resources/sprites/weapon/double_shotgun/icon.png")
        self.game.renderer.load_texture_from_file("resources/sprites/weapon/automatic_rifle/icon.png")

        # Set variables for weapon icon
        self.weapon_sprite_width = 64
        self.weapon_sprite_height = 64
        self.current_selected_weapon = "Empty"

        # Set variables for bullet text
        self.cartridge_bullet_left = None
        self.total_bullet_left = None

    def draw(self):
        # We center everything using weapon sprite, so calculate once each tick
        weapon_sprite_pos_x = self.game.width - self.weapon_sprite_width - self.hud.margin
        weapon_sprite_pos_y = self.game.height - self.weapon_sprite_height - self.hud.margin
        self.game.renderer.draw_rect(
            weapon_sprite_pos_x,
            weapon_sprite_pos_y,
            self.weapon_sprite_width,
            self.weapon_sprite_height,
            self.current_selected_weapon
        )

        self.game.renderer.draw_rect(
            weapon_sprite_pos_x - (self.cartridge_bullet_left.get_width() + self.hud.margin),
            weapon_sprite_pos_y,
            self.cartridge_bullet_left.get_width(),
            self.cartridge_bullet_left.get_height(),
            "cartridge_bullet"
        )

        self.game.renderer.draw_rect(
            weapon_sprite_pos_x - (self.total_bullet_left.get_width() + self.hud.margin),
            weapon_sprite_pos_y + (self.weapon_sprite_height / 2),
            self.total_bullet_left.get_width(),
            self.total_bullet_left.get_height(),
            "total_bullet"
        )

    def on_change(self):
        pass

    def update_bullet_left(self, cartridge, overall):
        self.cartridge_bullet_left = self.game.fonts[1].render(str(cartridge), True, (255, 255, 255))
        self.game.renderer.load_texture_from_surface("cartridge_bullet", self.cartridge_bullet_left)

        self.total_bullet_left = self.game.fonts[2].render(str(overall), True, (180, 180, 180))
        self.game.renderer.load_texture_from_surface("total_bullet", self.total_bullet_left)

    def update_current_weapon(self, weapon, cartridge, overall):
        if weapon == "Empty":
            self.current_selected_weapon = "resources/sprites/weapon/empty/idle.png"
        elif weapon == "Pitchfork":
            self.current_selected_weapon = "resources/sprites/weapon/pitchfork/icon.png"
        elif weapon == "Revolver":
            self.current_selected_weapon = "resources/sprites/weapon/revolver/icon.png"
        elif weapon == "Double Shotgun":
            self.current_selected_weapon = "resources/sprites/weapon/double_shotgun/icon.png"
        elif weapon == "Automatic Rifle":
            self.current_selected_weapon = "resources/sprites/weapon/automatic_rifle/icon.png"
        self.update_bullet_left(cartridge, overall)

    def weapon_unlocked(self, weapon, cartridge, overall):
        self.update_current_weapon(weapon, cartridge, overall)
        pass
