from sprites.sprite import Sprite


class WeaponPickup(Sprite):
    def __init__(self, game, pos, weapon):
        super().__init__(game, pos, [0.6, 0.6])
        self.game = game
        self.weapon = weapon
        self.weapon_picked = False
        self.delete_on_pickup = True

        if "Pitchfork" == weapon:
            path = "resources/sprites/pickups/special/corpse_empty.png"
            game.sprite_manager.load_single_image("corpse without pitchfork", path)
            path = "resources/sprites/pickups/special/corpse_pitchfork.png"
            self.sprite = game.sprite_manager.load_single_image("corpse with pitchfork", path)[0]
            self.delete_on_pickup = False
            self.size = [0.6, 0.6]

        elif "Revolver" == weapon:
            path = "resources/sprites/weapon/revolver/icon.png"
            self.sprite = game.sprite_manager.load_single_image("revolver icon", path)[0]
            self.size = [0.2, 0.2]

        elif "Double Shotgun" == weapon:
            path = "resources/sprites/weapon/double_shotgun/icon.png"
            self.sprite = game.sprite_manager.load_single_image("double_shotgun icon", path)[0]
            self.size = [0.25, 0.25]

        elif "Automatic Rifle" == weapon:
            path = "resources/sprites/weapon/automatic_rifle/icon.png"
            self.sprite = game.sprite_manager.load_single_image("automatic_rifle icon", path)[0]
            self.size = [0.25, 0.25]

        self.type = "Weapon"

    def update(self):
        if not self.weapon_picked and self.distance_from(self.player) < 0.5:
            if self.delete_on_pickup:
                self.delete = True
            else:
                self.weapon_picked = True
                self.sprite = self.game.sprite_manager.get_sprite("corpse without pitchfork")
            self.weapon_picked = True
            self.game.weapon.unlock(self.weapon)
            self.game.object_handler.update_pickup_list()
