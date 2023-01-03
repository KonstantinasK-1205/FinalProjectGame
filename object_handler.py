from settings import *


class ObjectHandler:
    def __init__(self, game):
        self.game = game
        self.npc_list = []
        self.pickup_list = []
        self.sprite_list = []
        self.bullet_list = []
        self.alive_npc_list = []
        self.npc_positions = []
        self.killed = 0

        self.dmgIncreased = False

        self.map_change = False
        self.map_change_wait_ms = 0

    def kill_reward(self):
        reward = self.killed
        if self.game.map.enemy_amount > 10 and reward > int(self.game.map.enemy_amount / 1.5) and not self.dmgIncreased:
            self.game.weapon.set_damage_buff(1.5)
            self.game.sound.play_sfx("Player dmg buff")
            self.dmgIncreased = True

        if reward >= self.game.map.enemy_amount:
            self.map_change = True

    def update(self):
        self.npc_positions = [npc.grid_pos for npc in self.npc_list if npc.alive]
        for npc in self.npc_list:
            npc.update()
            if npc in self.alive_npc_list and npc.dead:
                self.alive_npc_list.pop(self.alive_npc_list.index(npc))
                self.killed += 1
                self.game.hud.minimap.update_enemy_stats()

        for pickup in self.pickup_list:
            pickup.update()
        self.pickup_list = [pickup for pickup in self.pickup_list if not pickup.delete]

        for sprite in self.sprite_list:
            sprite.update()
        self.sprite_list = [sprite for sprite in self.sprite_list if not sprite.delete]

        for bullet in self.bullet_list:
            bullet.update()
        self.bullet_list = [bullet for bullet in self.bullet_list if not bullet.delete]

        self.kill_reward()

        if self.game.player.health <= 0:
            self.game.current_state = "Game over"

        if self.map_change:
            self.map_change_wait_ms = self.map_change_wait_ms + self.game.dt
            if self.map_change_wait_ms >= MAP_CHANGE_WAIT_MS:
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
        self.npc_positions = []
