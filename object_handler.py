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

        self.sprite_list = []
        self.npc_list = []
        self.alive_npc_list = []
        self.npc_positions = {}
        self.lastRespawned = pg.time.get_ticks()
        self.killed = 0

        self.game = ''
        self.gameMap = ''
        self.map_size = ''

        self.hpRestored = False
        self.dmgIncreased = False
        self.sprite_positions = []
        # Little bit more interesting spawning, but also more problematic
        # print("MAP Size X: " + str(self.map_size[0]) + " | Y: " + str(self.map_size[1]))

    def loadMap(self, game):
        self.game = game
        self.gameMap = Map(game)
        self.map_size = self.gameMap.get_size()

    def generatePickups(self):
        # Sprites on the Map
        for i in range(0, self.randomNum(15, 30)):
            newX = self.randomNum(0, self.map_size[0])
            newY = self.randomNum(0, self.map_size[1])
            if not (newX - 0.5, newY - 0.5) in self.sprite_positions:
                self.add_sprite(AnimatedSprite(self.game, pos=(newX - 0.5, newY - 0.5)))
                self.sprite_positions.append((newX - 0.5, newY - 0.5)) 


        # Spawn healthpacks
        for i in range(0, self.randomNum(15, 30)):
            newX = self.randomNum(0, self.map_size[0])
            newY = self.randomNum(0, self.map_size[1])
            if not (newX - 0.5, newY - 0.5) in self.sprite_positions:
                self.add_sprite(Healthpack(self.game, pos=(newX - 0.5, newY - 0.5)))
                self.sprite_positions.append((newX - 0.5, newY - 0.5)) 

        # Spawn pickable armors
        for i in range(0, self.randomNum(10, 20)):
            newX = self.randomNum(0, self.map_size[0])
            newY = self.randomNum(0, self.map_size[1])
            if not (newX - 0.5, newY - 0.5) in self.sprite_positions:
                self.add_sprite(Ammopack(self.game, pos=(newX - 0.5, newY - 0.5)))
                self.sprite_positions.append((newX - 0.5, newY - 0.5)) 
        
        # Spawn ammopacks
        for i in range(0, self.randomNum(25, 40)):
            newX = self.randomNum(0, self.map_size[0])
            newY = self.randomNum(0, self.map_size[1])
            if not (newX - 0.5, newY - 0.5) in self.sprite_positions:
                self.add_sprite(Armorpickup(self.game, pos=(newX - 0.5, newY - 0.5)))
                self.sprite_positions.append((newX - 0.5, newY - 0.5)) 

        cloRangeNPC = 0
        while cloRangeNPC < 5:
            newX = self.randomNum(4, math.floor(self.map_size[0] / 4))
            newY = self.randomNum(4, math.floor(self.map_size[1] / 6))
            if not self.gameMap.isWall(newX, newY):
                self.add_npc(NPC(self.game, pos=(float(newX + 0.5), float(newY + 0.5))))
                cloRangeNPC = cloRangeNPC + 1

        midRangeNPC = 0
        while midRangeNPC < 50:
            newX = self.randomNum(math.floor(self.map_size[0] / 4) + 1, math.floor(self.map_size[0] / 2))
            newY = self.randomNum(math.floor(self.map_size[1] / 6) + 1, math.floor(self.map_size[1] / 3))
            if not self.gameMap.isWall(newX, newY):
                self.add_npc(NPC(self.game, pos=(float(newX + 0.5), float(newY + 0.5))))
                midRangeNPC = midRangeNPC + 1

        farRangeNPC = 0
        while farRangeNPC < 40:
            newX = self.randomNum(math.floor(self.map_size[0] / 2) + 1, self.map_size[0])
            newY = self.randomNum(math.floor(self.map_size[1] / 3) + 1, self.map_size[1])
            if not self.gameMap.isWall(newX, newY):
                self.add_npc(NPC(self.game, pos=(float(newX + 0.5), float(newY + 0.5))))
                farRangeNPC = farRangeNPC + 1

    def killReward(self):
        reward = self.killed
        if reward > 15 and not self.hpRestored:
            self.game.player.set_health(200)
            self.game.sound.hpHealed.play()
            self.hpRestored = True

        if reward > 20 and not self.dmgIncreased:
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

        time_now = pg.time.get_ticks()
        if time_now - self.lastRespawned > 15000:
            while True:
                newX = self.randomNum(0, self.map_size[0])
                newY = self.randomNum(0, self.map_size[1])
                if not self.gameMap.isWall(newX, newY):
                    self.add_npc(NPC(self.game, pos=(float(newX + 0.5), float(newY + 0.5))))
                    break
            self.lastRespawned = time_now

    def add_npc(self, npc):
        self.npc_list.append(npc)
        self.alive_npc_list.append(npc)

    def add_sprite(self, sprite):
        self.sprite_list.append(sprite)

    def randomNum(self, minNum, maxNum):
        return random.randint(minNum, maxNum)

    def reset(self):
        self.sprite_list = []
        self.npc_list = []
        self.alive_npc_list = []
        self.npc_positions = {}
