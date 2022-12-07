import pygame as pg

class Map:
    def __init__(self, game):
        self.game = game
        self.world_map = {}
        self.get_map()

    def get_map(self):
        map_file = open("resources/map.txt", "r")
        y = 0
        while line := map_file.readline():
            x = 0
            for char in line:
                # world_map should only contain ints which refer to wall texture
                # index
                if char.isdigit():
                    self.world_map[(x, y)] = int(char)
                elif char == "p":
                    self.game.player.set_spawn(x + 0.5, y + 0.5)
                x = x + 1
            y = y + 1

    def isWall(self, x, y):
        return (x, y) in self.world_map

    def get_size(self):
        xy_size = list(self.world_map.keys())[-1]
        x_size = xy_size[0]
        y_size = xy_size[1]
        return x_size, y_size
