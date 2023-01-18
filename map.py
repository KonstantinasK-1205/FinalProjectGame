from entity.custom_wall import *

from entity.npc.enemies.battlelord import *
from entity.npc.enemies.lostsoul import *
from entity.npc.enemies.pinky import *
from entity.npc.enemies.reaper import *
from entity.npc.enemies.soldier import *

from entity.pickup.ammo import *
from entity.pickup.misc import *
from entity.pickup.armor import *
from entity.pickup.health import *
from entity.pickup.weapon import *

from sprites.enemies_spawns import *
from sprites.environment_assets import *


class Map:
    def __init__(self, game):
        self.game = game

        self.size = (0, 0)

        self.floors = []
        self.walls = []
        self.entities = []
        self.visited = []
        self.properties = []

        self.enemy_amount = 0
        self.next_level = None

        self.created = False

    def reset(self):
        self.size = (0, 0)

        self.floors = []
        self.walls = []
        self.entities = []
        self.visited = []
        self.properties = []

        self.enemy_amount = 0
        self.next_level = None

        self.created = False

    def create(self, size):
        self.size = size

        self.floors = [0] * self.size[0] * self.size[1]
        self.walls = [0] * self.size[0] * self.size[1]
        self.entities = [""] * self.size[0] * self.size[1]
        self.visited = [False] * self.size[0] * self.size[1]
        self.properties = []

        self.enemy_amount = 0
        self.next_level = None

        self.created = True

        self.game.object_handler.reset()

    def resize(self, size):
        new_size = size
        new_floors = [0] * new_size[0] * new_size[1]
        new_walls = [0] * new_size[0] * new_size[1]
        new_entities = [""] * new_size[0] * new_size[1]
        new_visited = [False] * new_size[0] * new_size[1]

        overlap_size = (
            min(self.size[0], new_size[0]),
            min(self.size[1], new_size[1])
        )
        for i in range(overlap_size[1]):
            for j in range(overlap_size[0]):
                new_floors[j + i * new_size[0]] = self.floors[j + i * self.size[0]]
                new_walls[j + i * new_size[0]] = self.walls[j + i * self.size[0]]
                new_entities[j + i * new_size[0]] = self.entities[j + i * self.size[0]]
                new_visited[j + i * new_size[0]] = self.visited[j + i * self.size[0]]

        self.size = new_size
        self.floors = new_floors
        self.walls = new_walls
        self.entities = new_entities
        self.visited = new_visited

    def load(self, filename):
        path = "resources/levels/" + filename + ".txt"
        map_file = open(path, "r")

        # Find map size
        line = map_file.readline()
        if line.find("Map Width: ") != 0:
            return
        width = int(line.split(": ")[1])

        line = map_file.readline()
        if line.find("Map Height: ") != 0:
            return
        height = int(line.split(": ")[1])

        self.create([width, height])

        # Read map properties
        while line := map_file.readline():
            # Strip the line separator
            line = line[:-1]

            # Properties end on blank line
            if line == "":
                break

            # Add properties line to list (used by map editor)
            self.properties.append(line)

            # Parse properties
            if line.find("Player HP: ") == 0:
                self.game.player.health = int(line.split(": ")[1])
            elif line.find("Player Armor: ") == 0:
                self.game.player.armor = int(line.split(": ")[1])
            elif line.find("Weapon: ") == 0:
                parameter = line.split(": ")[1].split(",")
                if parameter[0] in self.game.weapon.weapon_info:
                    weapon = self.game.weapon.weapon_info[parameter[0]]
                    if len(parameter) >= 2:
                        weapon["Unlocked"] = parameter[1].replace("\n", "")
                    if len(parameter) >= 3:
                        weapon["Fire"]["Bullet Left"] = int(parameter[2])
                    if len(parameter) >= 4:
                        weapon["Fire"]["Cartridge Contains"] = int(parameter[3])
                else:
                    print("map.py: Error while loading - " + path + ", couldn't find weapon - " + parameter[0])
            elif line.find("Next Level: ") == 0:
                if "None" in line:
                    self.next_level = None
                else:
                    self.next_level = line.split(': ')[1]

        # Read floor map
        for y in range(height):
            line = map_file.readline()[:-1].split(" ")
            for x in range(width):
                self.floors[x + y * width] = int(line[x])

        # Read wall and entity map
        for y in range(height):
            line = map_file.readline()[:-1].split(" ")
            for x in range(width):
                char = line[x]

                if char.isdigit():
                    self.walls[x + y * width] = int(char)
                    continue

                self.entities[x + y * width] = char

                # Entities are added to tile centers
                pos = [x + 0.5, y + 0.5, 0]

                handler = self.game.object_handler

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
                    handler.add_pickup(Health(self.game, pos))
                elif char == "w":
                    handler.add_pickup(Armor(self.game, pos))

                # Pickups weapons
                elif char == "a":
                    handler.add_pickup(Pitchfork(self.game, pos))
                elif char == "s":
                    handler.add_pickup(Pistol(self.game, pos))
                elif char == "d":
                    handler.add_pickup(DoubleShotgun(self.game, pos))
                elif char == "f":
                    handler.add_pickup(AutomaticRifle(self.game, pos))

                # Pickups ammo
                elif char == "S":
                    handler.add_pickup(Revolver(self.game, pos))
                elif char == "D":
                    handler.add_pickup(Shotgun(self.game, pos))
                elif char == "F":
                    handler.add_pickup(Rifle(self.game, pos))
                elif char == "-":
                    handler.add_pickup(BonusLevel(self.game, pos))
                elif char == "]":
                    handler.add_pickup(LevelChange(self.game, pos))

                # Sprites / Decoration
                elif char == "!":
                    handler.add_sprite(Tree(self.game, pos))
                elif char == "@":
                    handler.add_sprite(BigTorch(self.game, pos))
                elif char == "#":
                    handler.add_sprite(SmallTorch(self.game, pos))
                elif char == "*":
                    handler.add_sprite(Corpse(self.game, pos))
                elif char == "[":
                    handler.add_interactive_sprite(BreakableWall(self.game, [x, y, 0]))

                # Spawns
                elif char == ",":
                    handler.add_sprite(ZombieSpawn(self.game, pos))

        self.game.renderer.update_map_vbos()

    def save(self, filename):
        path = "resources/levels/" + filename + ".txt"
        map_file = open(path, "w")

        # Write map size
        map_file.write("Map Width: " + str(self.width) + "\n")
        map_file.write("Map Height: " + str(self.height) + "\n")

        # Write map properties
        for p in self.properties:
            map_file.write(p + "\n")

        # End propreties with a blank line
        map_file.write("\n")

        # Write floors map
        for y in range(self.height):
            for x in range(self.width):
                if x > 0:
                    map_file.write(" ")
                map_file.write(str(self.floors[x + y * self.width]))
            map_file.write("\n")

        # Write wall and entity map
        for y in range(self.height):
            for x in range(self.width):
                if x > 0:
                    map_file.write(" ")
                if self.entities[x + y * self.width]:
                    map_file.write(self.entities[x + y * self.width])
                else:
                    map_file.write(str(self.walls[x + y * self.width]))
            map_file.write("\n")

    def is_floor(self, x, y):
        if x < 0 or x >= self.size[0] or y < 0 or y >= self.size[1]:
            return True
        return self.floors[int(x) + int(y) * self.size[0]] != 0

    def get_floor(self, x, y):
        if x < 0 or x >= self.size[0] or y < 0 or y >= self.size[1]:
            return 0
        return self.floors[int(x) + int(y) * self.size[0]]

    def set_floor(self, x, y, floor):
        if x < 0 or x >= self.size[0] or y < 0 or y >= self.size[1]:
            return 0
        self.floors[int(x) + int(y) * self.size[0]] = floor

    def is_wall(self, x, y):
        if x < 0 or x >= self.size[0] or y < 0 or y >= self.size[1]:
            return True
        return self.walls[int(x) + int(y) * self.size[0]] != 0

    def get_wall(self, x, y):
        if x < 0 or x >= self.size[0] or y < 0 or y >= self.size[1]:
            return 0
        return self.walls[int(x) + int(y) * self.size[0]]

    def set_wall(self, x, y, wall):
        if x < 0 or x >= self.size[0] or y < 0 or y >= self.size[1]:
            return 0
        self.walls[int(x) + int(y) * self.size[0]] = wall

    def get_entity(self, x, y):
        if x < 0 or x >= self.size[0] or y < 0 or y >= self.size[1]:
            return 0
        return self.entities[int(x) + int(y) * self.size[0]]

    def set_entity(self, x, y, entity):
        if x < 0 or x >= self.size[0] or y < 0 or y >= self.size[1]:
            return 0
        self.entities[int(x) + int(y) * self.size[0]] = entity

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
