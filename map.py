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

        self.size = (0, 0)

        self.floors = []
        self.walls = []
        self.visited = []

        self.enemy_amount = 0
        self.next_level = None

        self.created = False

    def create(self, size):
        self.size = size

        self.floors = [0] * self.size[0] * self.size[1]
        self.walls = [0] * self.size[0] * self.size[1]
        self.visited = [False] * self.size[0] * self.size[1]

        self.enemy_amount = 0
        self.next_level = None

        self.created = True

        self.game.object_handler.reset()

    def resize(self, size):
        new_size = size
        new_floors = [0] * self.size[0] * self.size[1]
        new_walls = [0] * self.size[0] * self.size[1]
        new_visited = [False] * self.size[0] * self.size[1]

        overlap_size = (
            min(self.size[0], new_size[0]),
            min(self.size[1], new_size[1])
        )
        for i in range(overlap_size[1]):
            for j in range(overlap_size[0]):
                new_floors[j + i * new_size[0]] = self.floors[j + i * self.size[0]]
                new_walls[j + i * new_size[0]] = self.walls[j + i * self.size[0]]
                new_visited[j + i * new_size[0]] = self.visited[j + i * self.size[0]]

        self.size = new_size
        self.floors = new_floors
        self.walls = new_walls
        self.visited = new_visited

    def load(self, filename):
        path = "resources/levels/" + filename + ".txt"
        map_file = open(path, "r")

        # Find map size
        width = 0
        height = 0

        y = 0
        while line := map_file.readline():
            # Skip lines with map constants
            if ": " in line:
                continue

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
                width = max(width, x)
            y += 1
        height = y

        self.create((width, height))

        # Read map data
        handler = self.game.object_handler

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
                    self.walls[x + y * self.size[0]] = int(char)
                else:
                    self.floors[x + y * self.size[0]] = 1

                # Player and Enemies
                if char == "O":
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

                # Floor 2 (testing)
                elif char == "_":
                    self.floors[x + y * self.size[0]] = 2
                x += 1
            y += 1

        self.game.renderer.update_map_vbos()

    def is_floor(self, x, y):
        if x < 0 or x >= self.size[0] or y < 0 or y >= self.size[1]:
            return True
        return self.floors[int(x) + int(y) * self.size[0]] != 0

    def get_floor(self, x, y):
        if x < 0 or x >= self.size[0] or y < 0 or y >= self.size[1]:
            return 0
        return self.floors[int(x) + int(y) * self.size[0]]

    def is_wall(self, x, y):
        if x < 0 or x >= self.size[0] or y < 0 or y >= self.size[1]:
            return True
        return self.walls[int(x) + int(y) * self.size[0]] != 0

    def get_wall(self, x, y):
        if x < 0 or x >= self.size[0] or y < 0 or y >= self.size[1]:
            return 0
        return self.walls[int(x) + int(y) * self.size[0]]

    def is_visited(self, x, y):
        if x < 0 or x >= self.size[0] or y < 0 or y >= self.size[1]:
            return False
        return self.visited[int(x) + int(y) * self.size[0]] == True

    def set_visited(self, x, y, value=True):
        if x < 0 or x >= self.size[0] or y < 0 or y >= self.size[1]:
            return
        self.visited[int(x) + int(y) * self.size[0]] = value

    @property
    def width(self):
        return self.size[0]

    @property
    def height(self):
        return self.size[1]
