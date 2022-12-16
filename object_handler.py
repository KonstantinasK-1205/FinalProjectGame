from map import *
from settings import *


class ObjectHandler:
    def __init__(self):
        self.npc_list = []
        self.sprite_list = []
        self.bullet_list = []
        self.alive_npc_list = []
        self.npc_positions = {}
        self.killed = 0

        self.game = None
        self.gameMap = None

        self.dmgIncreased = False

        self.map_change = False
        self.map_change_wait_ms = 0

    def load_map(self, game):
        self.game = game
        self.gameMap = Map(game)

    def kill_reward(self):
        reward = self.killed
        if self.game.map.enemy_amount > 10 and reward > int(self.game.map.enemy_amount / 1.5) and not self.dmgIncreased:
            self.game.weapon.set_damage_buff(1.5)
            self.game.sound.buff_damage.play()
            self.dmgIncreased = True

        if reward >= self.game.map.enemy_amount:
            self.map_change = True
            self.map_change_wait_s = 0

    def update(self, dt):
        self.kill_reward()
        self.npc_positions = {npc.grid_pos for npc in self.npc_list if npc.alive}
        self.handle_pickups()
        self.handle_bullets()

        for npc in self.npc_list:
            npc.update()

        for npc in self.alive_npc_list:
            if npc.dead:
                self.alive_npc_list.pop(self.alive_npc_list.index(npc))
                self.killed = self.killed + 1

        if self.map_change:
            self.map_change_wait_ms = self.map_change_wait_ms + dt
            if self.map_change_wait_ms >= MAP_CHANGE_WAIT_MS:
                self.map_change = False
                if len(self.game.map_lists) > 1:
                    self.game.map_lists.pop(0)
                    self.game.current_state = "Loading"
                    self.game.new_game("resources/levels/" + str(self.game.map_lists[0]) + ".txt")
                else:
                    self.game.current_state = "Win"

    def draw(self):
        for npc in self.npc_list:
            npc.draw()
        for sprite in self.sprite_list:
            sprite.draw()

    def handle_bullets(self):
        # Create new array in which we will store
        # index of element we remove
        remove = []
        for index, bullet in enumerate(self.bullet_list):
            # If sprite wasn't used just update it,
            # otherwise add to remove array
            if not bullet.collided:
                bullet.update()
            else:
                remove.append(index)

        # Iterate each remove element and remove
        # each sprite from main array
        for index in remove[::-1]:
            self.bullet_list.pop(index)

    def handle_pickups(self):
        # Create new array in which we will stores
        # index of element we remove
        remove = []
        for index, sprite in enumerate(self.sprite_list):
            # If sprite wasn't used just update it,
            # otherwise add to remove array
            if not sprite.delete:
                sprite.update()
            else:
                remove.append(index)

        # Iterate each remove element and remove
        # each sprite from main array
        for index in remove:
            self.sprite_list.pop(index)

    def add_npc(self, npc):
        self.npc_list.append(npc)
        self.alive_npc_list.append(npc)

    def add_sprite(self, sprite):
        self.sprite_list.append(sprite)

    def add_bullet(self, bullet):
        self.bullet_list.append(bullet)

    def reset(self):
        self.npc_list = []
        self.sprite_list = []
        self.alive_npc_list = []
        self.npc_positions = {}
