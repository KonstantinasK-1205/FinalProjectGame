from map import *


class ObjectHandler:
    def __init__(self):
        self.npc_list = []
        self.sprite_list = []
        self.alive_npc_list = []
        self.npc_positions = {}
        self.killed = 0

        self.game = None
        self.gameMap = None
        self.map_size = None

        self.hpRestored = False
        self.dmgIncreased = False

        self.map_change = False
        self.map_change_wait_ms = 0

    def load_map(self, game):
        self.game = game
        self.gameMap = Map(game)
        self.map_size = self.gameMap.get_size()

    def kill_reward(self):
        reward = self.killed
        if self.game.map.enemy_amount > 10 and reward > int(self.game.map.enemy_amount / 4) and not self.hpRestored:
            self.game.player.add_health(25)
            self.game.sound.player_healed.play()
            self.hpRestored = True

        if self.game.map.enemy_amount > 10 and reward > int(self.game.map.enemy_amount / 1.5) and not self.dmgIncreased:
            self.game.weapon.set_damage_buff(1.5)
            self.game.sound.buff_damage.play()
            self.dmgIncreased = True

        if reward >= self.game.map.enemy_amount:
            self.map_change = True
            self.map_change_wait_s = 0

    def update(self, dt):
        self.kill_reward()
        self.npc_positions = {npc.map_pos for npc in self.npc_list if npc.alive}
        self.handle_pickups()

        for npc in self.npc_list:
            npc.update()

        for npc in self.alive_npc_list:
            if not npc.is_alive():
                self.alive_npc_list.pop(self.alive_npc_list.index(npc))
                self.killed = self.killed + 1

        if self.map_change:
            self.map_change_wait_ms = self.map_change_wait_ms + dt
            print("Waiting for map change " + str(self.map_change_wait_s))
            if self.map_change_wait_ms >= MAP_CHANGE_WAIT_MS:
                self.map_change = False
                if len(self.game.map_lists) > 1:
                    self.game.map_lists.pop(0)
                    self.game.current_state = "Loading"
                    self.game.new_game("resources/levels/" + str(self.game.map_lists[0]) + ".txt")
                else:
                    self.game.current_state = "Win"

    def handle_pickups(self):
        # Create new array in which we will store
        # index of element we remove
        remove = []
        for index, sprite in enumerate(self.sprite_list):
            # If sprite wasn't used just update it,
            # otherwise add to remove array
            if not sprite.picked:
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

    def reset(self):
        self.npc_list = []
        self.sprite_list = []
        self.alive_npc_list = []
        self.npc_positions = {}
