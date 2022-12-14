from object_handler import *
from object_renderer import *
from pathfinding import *
from player import *
from raycasting import *
from sound import *
from states.game import GameState
from states.intro import IntroState
from states.loading import LoadingState
from states.lose import LoseState
from states.pause import PauseState
from states.win import WinState
from weapon import *


class Game:
    def __init__(self):
        pg.init()

        self.screen = pg.display.set_mode(RES)
        self.clock = pg.time.Clock()

        self.object_handler = ObjectHandler()
        self.object_renderer = ObjectRenderer(self)
        self.map_lists = ["Level1", "Level2", "Level3", "Level4"]
        # self.map_lists = ["T_Level1", "T_Level2", "T_Level3"]

        self.state = {
            "Intro": IntroState(self),
            "Loading": LoadingState(self),
            "Game": GameState(self),
            "Pause": PauseState(self),
            "Win": WinState(self),
            "Game over": LoseState(self)
        }
        self.current_state = "Intro"

        # self.PRINTFPSEVENT = pg.USEREVENT + 1
        # pg.time.set_timer(self.PRINTFPSEVENT, 1000)

        self.hit_flash_ms = HIT_FLASH_MS

    def __del__(self):
        pg.quit()

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.is_running = False
            # elif event.type == self.PRINTFPSEVENT:
            #    print(str(int(self.clock.get_fps())) + " FPS")
            self.state[self.current_state].handle_events(event)

    def update(self):
        self.dt = self.clock.tick(FPS)

        self.state[self.current_state].update(self.dt)

    def draw(self):
        self.state[self.current_state].draw()

        if self.hit_flash_ms < HIT_FLASH_MS:
            surface = pg.Surface((RES[0], RES[1]), pg.SRCALPHA)
            surface.fill(HIT_FLASH_COLOR)
            self.screen.blit(surface, (0, 0))

            self.hit_flash_ms = self.hit_flash_ms + self.dt

        pg.display.flip()

    def new_game(self, level):
        self.state[self.current_state].update(0)
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

    def run(self):
        self.is_running = True

        while self.is_running:
            self.handle_events()
            self.update()
            self.draw()

    @property
    def current_state(self):
        return self._current_state

    @current_state.setter
    def current_state(self, current_state):
        self._current_state = current_state
        self.state[self._current_state].on_set()
