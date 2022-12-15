from Bullet import *
from npc.reaper import Reaper
from npc.soldier import Soldier
from sprites.sprite import Sprite
from sprites.pickup_ammo_machinegun import MachinegunPickupAmmo
from sprites.pickup_ammo_shotgun import ShotgunPickupAmmo
from sprites.pickup_armor import PickupArmor
from sprites.pickup_health import PickupHealth


class Map:
    def __init__(self, game):
        self.game = game
        self.width = 0
        self.height = 0
        self.data = []
        self.enemy_amount = 0
        self.map_loaded = False

    def get_map(self, path):
        self.width = 0
        self.height = 0
        self.data = []
        self.enemy_amount = 0
        self.map_loaded = False

        # In case a map was already loaded, remove old objects
        self.game.object_handler.reset()

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

        # Read map data
        map_file.seek(0)
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

                # world_map should only contain ints which refer to wall texture
                # index
                if char.isdigit():
                    self.data[x + y * self.width] = int(char)
                elif char == "p":
                    self.game.player.set_spawn(x + 0.5, y + 0.5)
                elif char == "e":
                    self.game.object_handler.add_npc(Soldier(self.game, pos=(x + 0.5, y + 0.5)))
                    self.enemy_amount += 1
                elif char == "r":
                    self.game.object_handler.add_npc(Reaper(self.game, pos=(x + 0.5, y + 0.5)))
                    self.enemy_amount += 1
                elif char == "c":
                    self.game.object_handler.add_sprite(Sprite(self.game, pos=(x + 0.5, y + 0.5)))
                elif char == "h":
                    self.game.object_handler.add_sprite(PickupHealth(self.game, pos=(x + 0.5, y + 0.5)))
                elif char == "b":
                    self.game.object_handler.add_sprite(ShotgunPickupAmmo(self.game, pos=(x + 0.5, y + 0.5)))
                elif char == "m":
                    self.game.object_handler.add_sprite(MachinegunPickupAmmo(self.game, pos=(x + 0.5, y + 0.5)))
                elif char == "a":
                    self.game.object_handler.add_sprite(PickupArmor(self.game, pos=(x + 0.5, y + 0.5)))
                x += 1
            y += 1

            self.map_loaded = True

    def is_wall(self, x, y):
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return True
        return self.data[int(x) + int(y) * self.width] != 0

    def get_enemy_amount(self):
        return self.enemy_amount

    def get_size(self):
        return self.width, self.height
