from entity.custom_wall import *

from npc.battlelord import *
from npc.lostsoul import *
from npc.pinky import *
from npc.reaper import *
from npc.soldier import *
from npc.zombie import *

from sprites.sprite import Sprite
from sprites.pickup_ammo import *
from sprites.environment_assets import *
from sprites.pickup_misc import *
from sprites.pickup_armor import PickupArmor
from sprites.pickup_health import PickupHealth
from sprites.pickup_weapons import *
from sprites.enemies_spawns import *


class Map:
    def __init__(self, game):
        self.game = game
        self.width = 0
        self.height = 0
        self.data = []
        self.data_visited = []
        self.enemy_amount = 0
        self.map_loaded = False
        self.next_level = None

    def get_map(self, level):
        self.width = 0
        self.height = 0
        self.data = []
        self.enemy_amount = 0
        self.map_loaded = False

        # In case a map was already loaded, remove old objects
        self.game.object_handler.reset()
        self.next_level = None

        path = "resources/levels/" + level + ".txt"
        map_file = open(path, "r")

        # Find map size
        y = 0
        while line := map_file.readline():
            x = 0
            skip = False
            for char in line:
                # Magic fix for tab separated files
                if "\t" in line:
                    if skip:
                        skip = False
                        continue
                    elif not char == "\t":
                        skip = True
                x += 1
                self.width = max(self.width, x)
            y += 1
        self.height = y

        self.data = [0] * self.width * self.height
        self.data_visited = [False] * self.width * self.height
        handler = self.game.object_handler

        # Read map data
        map_file.seek(0)
        y = 0
        while line := map_file.readline():
            x = 0
            skip = False
            if "Player HP:" in line:
                self.game.player.health = int(line.split(': ')[1])
                continue
            if "Player Armor:" in line:
                self.game.player.armor = int(line.split(': ')[1])
                continue
            if "Weapon" in line:
                parameter = line.split(': ')[1].lstrip()
                parameter = parameter.split(",")
                if parameter[0] in self.game.weapon.weapon_info:
                    weapon = self.game.weapon.weapon_info[parameter[0]]
                    if len(parameter) >= 2:
                        weapon["Unlocked"] = parameter[1].replace("\n", "")
                    if len(parameter) >= 3:
                        weapon["Fire"]["Bullet Left"] = int(parameter[2])
                    if len(parameter) >= 4:
                        weapon["Fire"]["Cartridge Contains"] = int(parameter[3])
                else:
                    print("Error while loading " + path)
                    print("-> Couldn't find weapon " + parameter[0])
                continue
            if "Next Level" in line:
                if "None" in line:
                    self.next_level = None
                else:
                    self.next_level = line.split(': ')[1].replace("\n", "")
                continue
            for char in line:
                # Magic fix for tab separated files
                if "\t" in line:
                    if skip:
                        skip = False
                        continue
                    elif not char == "\t":
                        skip = True

                # world_map should only contain ints which refer to wall texture
                # index
                pos = (x + 0.5, y + 0.5)
                if char.isdigit():
                    self.data[x + y * self.width] = int(char)

                # Player and Enemies
                elif char == "O":
                    self.game.player.set_spawn(pos[0], pos[1])
                elif char == "Z":
                    handler.add_npc(Zombie(self.game, pos))
                elif char == "X":
                    handler.add_npc(Soldier(self.game, pos))
                elif char == "C":
                    handler.add_npc(Pinky(self.game, pos))
                elif char == "V":
                    handler.add_npc(LostSoul(self.game, pos))
                elif char == "B":
                    handler.add_npc(Reaper(self.game, pos))
                elif char == "N":
                    handler.add_npc(Battlelord(self.game, pos))

                # Pickups stats
                elif char == "q":
                    handler.add_pickup(PickupHealth(self.game, pos))
                elif char == "w":
                    handler.add_pickup(PickupArmor(self.game, pos))

                # Pickups weapons
                elif char == "a":
                    handler.add_pickup(PitchforkPickup(self.game, pos))
                elif char == "s":
                    handler.add_pickup(RevolverPickup(self.game, pos))
                elif char == "d":
                    handler.add_pickup(DoubleShotgunPickup(self.game, pos))
                elif char == "f":
                    handler.add_pickup(AutomaticRiflePickup(self.game, pos))

                # Pickups ammo
                elif char == "S":
                    handler.add_pickup(PistolAmmo(self.game, pos))
                elif char == "D":
                    handler.add_pickup(ShotgunAmmo(self.game, pos))
                elif char == "F":
                    handler.add_pickup(RifleAmmo(self.game, pos))

                # Sprites / Decoration
                elif char == "!":
                    handler.add_sprite(Tree(self.game, pos))
                elif char == "@":
                    handler.add_sprite(BigTorch(self.game, pos))
                elif char == "#":
                    handler.add_sprite(SmallTorch(self.game, pos))
                elif char == "*":
                    handler.add_sprite(Corpse(self.game, pos))
                elif char == "-":
                    handler.add_sprite(BonusLevel(self.game, pos))
                elif char == "]":
                    handler.add_sprite(LevelChangeChunk(self.game, pos))
                elif char == "[":
                    handler.add_sprite(BreakableWall(self.game, (x, y)))

                # Spawns
                elif char == ",":
                    handler.add_sprite(ZombieSpawn(self.game, pos))
                x += 1
            y += 1

            self.map_loaded = True
        self.game.renderer.update_map()

    def get_tile(self, x, y):
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return 0
        return self.data[int(x) + int(y) * self.width]

    def is_wall(self, x, y):
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return True
        return self.data[int(x) + int(y) * self.width] != 0

    def is_visited(self, x, y):
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return False
        return self.data_visited[int(x) + int(y) * self.width] == True

    def set_visited(self, x, y, value=True):
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return
        self.data_visited[int(x) + int(y) * self.width] = value

    @property
    def size(self):
        return self.width, self.height
