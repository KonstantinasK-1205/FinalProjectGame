class ObjectHandler:
    def __init__(self, game):
        self.game = game
        self.npc_list = []
        self.pickup_list = []
        self.sprite_list = []
        self.bullet_list = []
        self.alive_npc_list = []
        self.killed = 0

        self.map_change = False
        self.map_change_wait_ms = 0

    def update(self):
        for npc in self.npc_list:
            npc.update()
            if npc in self.alive_npc_list and npc.dead:
                self.alive_npc_list.pop(self.alive_npc_list.index(npc))
                self.killed += 1

        for pickup in self.pickup_list:
            pickup.update()
        self.pickup_list = [pickup for pickup in self.pickup_list if not pickup.delete]

        for sprite in self.sprite_list:
            sprite.update()
        self.sprite_list = [sprite for sprite in self.sprite_list if not sprite.delete]

        for bullet in self.bullet_list:
            bullet.update()
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
        for npc in self.npc_list:
            npc.draw()
        for bullet in self.bullet_list:
            bullet.draw()
        for pickup in self.pickup_list:
            pickup.draw()
        for sprite in self.sprite_list:
            sprite.draw()

    def add_npc(self, npc):
        self.npc_list.append(npc)
        self.alive_npc_list.append(npc)
        self.game.map.enemy_amount += 1

    def add_pickup(self, pickup):
        self.pickup_list.append(pickup)

    def add_sprite(self, sprite):
        self.sprite_list.append(sprite)

    def add_bullet(self, bullet):
        self.bullet_list.append(bullet)

    def reset(self):
        self.npc_list = []
        self.pickup_list = []
        self.sprite_list = []
        self.alive_npc_list = []
