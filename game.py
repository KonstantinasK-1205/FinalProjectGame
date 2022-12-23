from object_handler import *
from hud import *
from pathfinding import *
from player import *
from renderer.renderer import *
from sound import *
from states.game import GameState
from states.intro import IntroState
from states.menu import MenuState
from states.options import OptionsState
from states.loading import LoadingState
from states.lose import LoseState
from states.pause import PauseState
from states.win import WinState
from weapons.weapon import Weapon


class Game:
    def __init__(self):
        pg.init()
        pg.display.set_mode((WIDTH, HEIGHT), pg.RESIZABLE | pg.OPENGL | pg.DOUBLEBUF, vsync=VSYNC)
        pg.display.set_caption("Final Project")
        pg.display.set_icon(pg.image.load("logo.png"))

        self.show_fps = PRINT_FPS

        self.running = False

        self.clock = pg.time.Clock()
        self.renderer = Renderer(self)
        self.object_handler = ObjectHandler(self)
        self.hud = Hud(self)
        self.map = Map(self)
        #self.map_lists = ["Level1", "Level2", "Level3", "Level4", "Level5", "Level6"]
        self.map_lists = ["Level6"]

        self.font = pg.font.Font("resources/fonts/Font.ttf", int(36 / 1280 * WIDTH))
        self.font_small = pg.font.Font("resources/fonts/Font.ttf", int(24 / 1280 * WIDTH))
        self.sound = Sound()

        self.state = {
            "Intro": IntroState(self),
            "Menu": MenuState(self),
            "Options": OptionsState(self),
            "Loading": LoadingState(self),
            "Game": GameState(self),
            "Pause": PauseState(self),
            "Win": WinState(self),
            "Game over": LoseState(self)
        }
        self.current_state = "Intro"

        self.hit_flash_ms = HIT_FLASH_MS

        self.dt = 0

    def __del__(self):
        pg.quit()

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            elif event.type == pg.VIDEORESIZE:
                self.font = pg.font.Font("resources/fonts/Font.ttf", int(36 / 1280 * event.w))
                self.font_small = pg.font.Font("resources/fonts/Font.ttf", int(24 / 1280 * event.w))

            self.state[self.current_state].handle_events(event)

    def update(self):
        self.dt = self.clock.tick()

        self.state[self.current_state].update()

        if self.hit_flash_ms < HIT_FLASH_MS:
            self.hit_flash_ms = self.hit_flash_ms + self.dt

    def draw(self):
        self.state[self.current_state].draw()

        if self.hit_flash_ms < HIT_FLASH_MS:
            self.renderer.draw_fullscreen_rect(color=HIT_FLASH_COLOR)

        self.renderer.draw_queued()
        pg.display.flip()

    def new_game(self, level):
        self.player = Player(self)
        self.object_handler = ObjectHandler(self)
        self.hud = Hud(self)
        self.map = Map(self)

        self.weapon = Weapon(self)
        self.map.get_map(level)
        self.pathfinding = PathFinding(self)

        self.renderer.draw_world = True

    def next_level(self, level):
        self.player.on_level_change()
        self.weapon.save_weapon_info()
        self.object_handler = ObjectHandler(self)
        self.map = Map(self)

        self.map.get_map(level)
        self.pathfinding = PathFinding(self)

    def restart_level(self, level):
        self.player.load_player_stats()
        self.weapon.load_weapon_info()

        self.object_handler = ObjectHandler(self)
        self.map = Map(self)

        self.map.get_map(level)
        self.pathfinding = PathFinding(self)


    def run(self):
        self.running = True

        while self.running:
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

    @property
    def width(self):
        return pg.display.get_window_size()[0]

    @property
    def height(self):
        return pg.display.get_window_size()[1]
