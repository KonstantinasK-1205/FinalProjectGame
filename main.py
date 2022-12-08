import sys

from object_handler import *
from object_renderer import *
from pathfinding import *
from player import *
from raycasting import *
from sound import *
from weapon import *


class Game:
    def __init__(self):
        pg.init()

        # self.map_lists = ["Level1", "Level2", "Level3"]
        self.map_lists = ["T_Level1", "T_Level2", "T_Level3"]

        self.screen = pg.display.set_mode(RES)
        self.clock = pg.time.Clock()
        self.loading_screen_time = pg.time.get_ticks()
        self.delta_time = 1
        self.new_game("resources/levels/" + self.map_lists[0] + ".txt")

        self.unpause()

    def new_game(self, level="resources/levels/Level1.txt"):
        self.player = Player(self)
        self.object_handler = ObjectHandler()
        self.object_renderer = ObjectRenderer(self)
        self.map = Map(self)
        self.draw_loading_screen()

        self.raycasting = RayCasting(self)
        self.sound = Sound()
        self.weapon = Weapon(self)
        self.map.get_map(level)
        self.pathfinding = PathFinding(self)

        self.object_handler.load_map(self)
        if pg.time.get_ticks() - self.loading_screen_time < 500:
            pg.time.wait(500)

    def update(self):
        if not self.paused:
            self.raycasting.update()
            self.object_handler.update()
            self.player.update()
            self.delta_time = self.clock.tick(FPS)
            print(self.clock.get_fps())

    def draw_loading_screen(self):
        if not self.map.map_loaded:
            self.loading_screen_time = pg.time.get_ticks()
            self.object_renderer.draw_loading_state()
            pg.display.flip()

    def draw(self):
        if self.paused:
            self.object_renderer.draw_pause_state()
            pg.display.flip()
        else:
            pg.display.flip()
            self.object_renderer.draw()
            self.weapon.draw()

    def check_events(self):
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
