import sys
import pygame as pg
from player import *
from raycasting import *
from object_renderer import *
from sprite_object import *
from object_handler import *
from map import *
from weapon import *
from sound import *
from pathfinding import *

class Game:
    def __init__(self):
        pg.init()

        self.map_lists = ["level1", "level2", "level3"]

        self.screen = pg.display.set_mode(RES)
        self.clock = pg.time.Clock()
        self.delta_time = 1
        self.global_trigger = False
        self.new_game()

        self.unpause()

    def new_game(self, level="resources/levels/level1.txt"):
        self.player = Player(self)
        self.object_handler = ObjectHandler(self)
        self.object_renderer = ObjectRenderer(self)
        self.raycasting = RayCasting(self)
        self.weapon = Weapon(self)
        self.sound = Sound(self)
        self.map = Map(self)
        self.map.get_map(level)
        self.pathfinding = PathFinding(self)

        self.object_handler.loadMap(self)

    def update(self):
        if not self.paused:
            self.raycasting.update()
            self.object_handler.update()
            self.player.update()
            self.delta_time = self.clock.tick(FPS)

    def draw(self):
        pg.display.flip()
        self.object_renderer.draw()        
        self.weapon.draw()

    def check_events(self):
        self.global_trigger = False
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                self.pause()
            elif event.type == pg.MOUSEBUTTONUP and event.button == 1:
                self.unpause()

            if not self.paused:
                self.player.handle_events(event)

    def pause(self):
        self.paused = True

        pg.mouse.set_visible(True)
        pg.event.set_grab(False)

    def unpause(self):
        self.paused = False

        pg.mouse.set_visible(False)
        pg.event.set_grab(True)

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()

if __name__ == '__main__':
    game = Game()
    game.run()
