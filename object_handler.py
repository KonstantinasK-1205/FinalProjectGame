from sprite_object import *
from npc import *
from map import *
import random
import math

class ObjectHandler:
    def __init__(self, game):
        # Sprite variables
        self.npc_sprite_path = 'resources/sprites/npc/'
        self.static_sprite_path = 'resources/sprites/static_sprites/'
        self.anim_sprite_path = 'resources/sprites/animated_sprites/'

        self.npc_list = []
        self.sprite_list = []
        self.alive_npc_list = []
        self.npc_positions = {}
        self.killed = 0

        self.game = ''
        self.gameMap = ''
        self.map_size = ''

        self.hpRestored = False
        self.dmgIncreased = False

    def loadMap(self, game):
        self.game = game
        self.gameMap = Map(game)
        self.map_size = self.gameMap.get_size()

    def killReward(self):
        reward = self.killed
        if reward > int(self.game.map.enemy_amount / 4) and not self.hpRestored:
            self.game.player.set_health(200)
            self.game.sound.hpHealed.play()
            self.hpRestored = True

        if reward > int(self.game.map.enemy_amount / 2) and not self.dmgIncreased:
            self.game.weapon.set_buff(1.3)
            self.game.sound.dmgIncrease.play()
            self.dmgIncreased = True

    def update(self):
        self.killReward()
        self.npc_positions = {npc.map_pos for npc in self.npc_list if npc.alive}
        [sprite.update() for sprite in self.sprite_list]
        for npc in self.npc_list:
            npc.update()

        for npc in self.alive_npc_list:
            if not npc.isAlive():
                self.alive_npc_list.pop(self.alive_npc_list.index(npc))
                self.killed = self.killed + 1

    def add_npc(self, npc):
        self.npc_list.append(npc)
        self.alive_npc_list.append(npc)

    def add_sprite(self, sprite):
        self.sprite_list.append(sprite)

    def randomNum(self, minNum, maxNum):
        return random.randint(minNum, maxNum)

    def reset(self):
        self.npc_list = []
        self.sprite_list = []
        self.alive_npc_list = []
        self.npc_positions = {}