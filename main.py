import sys

from states import *
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

        self.is_running = True
        self.screen = pg.display.set_mode(RES)
        self.clock = pg.time.Clock()
        # self.map_lists = ["Level1", "Level2", "Level3"]
        self.map_lists = ["T_Level1", "T_Level2", "T_Level3"]
        self.current_state = "Intro"
        self.state = {
            "Intro": IntroState(self),
            "Loading": LoadingState(self),
            "Game": GameState(self),
            "Pause": PauseState(self),
            "Win": WinState(self),
            "Game over": LoseState(self)
        }

        self.delta_time = 1

        self.object_handler = ObjectHandler()
        self.object_renderer = ObjectRenderer(self)

        self.PRINTFPSEVENT = pg.USEREVENT + 1
        pg.time.set_timer(self.PRINTFPSEVENT, 1000)

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.is_running = False
            elif event.type == self.PRINTFPSEVENT:
                print(str(int(self.clock.get_fps())) + " FPS")
            self.state[self.current_state].handle_events(event)

    def update(self):
        self.state[self.current_state].update()

    def draw(self):
        self.state[self.current_state].draw()

    def new_game(self, level="resources/levels/Level1.txt"):
        self.state[self.current_state].update()
        self.state[self.current_state].draw()

        self.player = Player(self)
        self.object_handler = ObjectHandler()
        self.object_renderer = ObjectRenderer(self)
        self.map = Map(self)

        self.raycasting = RayCasting(self)
        self.sound = Sound()
        self.weapon = Weapon(self)
        self.map.get_map(level)
        self.pathfinding = PathFinding(self)
        self.object_handler.load_map(self)
        self.state["Loading"].game_ready = True

    def run(self):
        while self.is_running:
            self.check_events()
            self.update()
            self.draw()
        pg.quit()
        sys.exit()

    def set_state(self, state):
        self.current_state = state
        self.state[self.current_state].on_set()


if __name__ == '__main__':
    game = Game()
    game.run()
