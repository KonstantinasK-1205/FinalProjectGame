class ObjectHandler:
    def __init__(self, game):
        self.game = game

        self.npc_list = []
        self.alive_npc_list = []

        self.sprite_list = []
        self.interactive_sprite_list = []

        self.pickup_list = []
        self.bullet_list = []

        self.map_change = False
        self.map_change_wait_ms = 0

    def update(self):
        # Update all sprites / entities active in game
        [npc.update() for npc in self.npc_list]
        [bullet.update() for bullet in self.bullet_list]
        [pickup.update() for pickup in self.pickup_list]
        [sprite.update() for sprite in self.sprite_list]
        [sprite.update() for sprite in self.interactive_sprite_list]

        # Update bullet list, it is faster doing this here instead of
        # calling function in projectile class to update list
        self.bullet_list = [bullet for bullet in self.bullet_list if not bullet.delete]

        if self.game.player.health <= 0:
            self.game.current_state = "Lose"

        if self.map_change:
            self.map_change_wait_ms += self.game.dt
            if self.map_change_wait_ms >= 2000:
                self.map_change = False
                if self.game.map.next_level:
                    self.game.current_state = "Loading"
                    self.game.next_level(self.game.map.next_level)
                else:
                    self.game.current_state = "Win"

    def draw(self):
        [npc.draw() for npc in self.npc_list]
        [bullet.draw() for bullet in self.bullet_list]
        [pickup.draw() for pickup in self.pickup_list]
        [sprite.draw() for sprite in self.sprite_list]
        [sprite.draw() for sprite in self.interactive_sprite_list]

    def add_bullet(self, bullet):
        self.bullet_list.append(bullet)

    def add_npc(self, npc, alive=True):
        self.npc_list.append(npc)
        if alive:
            self.alive_npc_list.append(npc)
        self.game.map.enemy_amount += 1

    def add_pickup(self, pickup):
        self.pickup_list.append(pickup)

    def add_interactive_sprite(self, sprite):
        self.interactive_sprite_list.append(sprite)

    def add_sprite(self, sprite):
        self.sprite_list.append(sprite)

    def update_npc_list(self):
        self.alive_npc_list = [npc for npc in self.npc_list if npc.alive]

    def update_pickup_list(self):
        self.pickup_list = [pickup for pickup in self.pickup_list if not pickup.delete]

    def update_interactive_sprite_list(self):
        self.interactive_sprite_list = [sprite for sprite in self.interactive_sprite_list if not sprite.delete]

    def update_sprite_list(self):
        self.sprite_list = [sprite for sprite in self.sprite_list if not sprite.delete]

    def reset(self):
        self.npc_list = []
        self.pickup_list = []
        self.sprite_list = []
        self.alive_npc_list = []
        self.interactive_sprite_list = []
