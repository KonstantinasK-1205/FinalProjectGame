import sys
import pygame as pg
from map import *
from player import *
from raycasting import *
from object_renderer import *
from sprite_object import *
from object_handler import *
from weapon import *
from sound import *
from pathfinding import *

class Game:
    def __init__(self):
        pg.init()
        pg.mouse.set_visible(False)
        pg.event.set_grab(True)
        self.screen = pg.display.set_mode(RES)
        self.clock = pg.time.Clock()
        self.delta_time = 1
        self.global_trigger = False
        self.new_game()

    def new_game(self):
        self.player = Player(self)
        self.map = Map(self)
        self.object_renderer = ObjectRenderer(self)
        self.raycasting = RayCasting(self)
        self.object_handler = ObjectHandler(self)
        self.weapon = Weapon(self)
        self.sound = Sound(self)
        self.pathfinding = PathFinding(self)

    def update(self):
        self.raycasting.update()
        self.object_handler.update()
        self.player.update()
        self.delta_time = self.clock.tick(FPS)
        pg.display.set_caption(f'{self.delta_time :.1f}')

    def draw(self):
        pg.display.flip()
        self.object_renderer.draw()        
        self.weapon.draw()

    def check_events(self):
         self.global_trigger = False
         for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                 pg.quit()
                 sys.exit()
            self.player.handle_events(event)

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()

if __name__ == '__main__':
    game = Game()
    game.run()
