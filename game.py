from object_handler import *
from hud.hud_manager import *
from map import *
from pathfinding import *
from player import *
from renderer.renderer import *
from sound import *
from sprites.sprite_manager import *
from states.game import GameState
from states.intro import IntroState
from states.menu import MenuState
from states.options import OptionsState
from states.loading import LoadingState
from states.lose import LoseState
from states.win import WinState
from weapons.weapon import Weapon


class Game:
    def __init__(self):
        pg.init()
        pg.display.set_mode((WIDTH, HEIGHT), pg.RESIZABLE | pg.OPENGL | pg.DOUBLEBUF, vsync=VSYNC)
        pg.display.set_caption("Final Project")
        pg.display.set_icon(pg.image.load("logo.png"))

        # Init variables
        self.font = None
        self.font_small = None
        self.font_smaller = None
        self.show_fps = True
        self.running = False

        # Needs to be initialized, otherwise will crash on resize before new game
        self.player = None
        self.pathfinding = None
        self.weapon = None

        self.clock = pg.time.Clock()
        self.renderer = Renderer(self)
        self.sprite_manager = SpriteManager(self)
        self.object_handler = ObjectHandler(self)
        self.player = Player(self)
        self.hud = Hud(self)
        self.map = Map(self)
        self.sound = Sound()

        self.starting_map = "T_Level1"
        self.current_map = "T_Level1"

        self.init_fonts()

        self.state = {
            "Intro": IntroState(self),
            "Menu": MenuState(self),
            "Options": OptionsState(self),
            "Loading": LoadingState(self),
            "Game": GameState(self),
            "Win": WinState(self),
            "Game over": LoseState(self)
        }
        self.current_state = "Intro"
        self.map_started_to_change = 0
        self.dt = 0

    def __del__(self):
        pg.quit()

    def init_fonts(self):
        self.font = pg.font.Font("resources/fonts/Font.ttf", int(36 / 720 * self.height))
        self.font_small = pg.font.Font("resources/fonts/Font.ttf", int(24 / 720 * self.height))
        self.font_smaller = pg.font.Font("resources/fonts/Font.ttf", int(18 / 720 * self.height))

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            elif event.type == pg.WINDOWSIZECHANGED:
                self.init_fonts()
                if hasattr(self.player, "health"):
                    self.hud.on_resize()
                if hasattr(self.weapon, "reset_weapon_pos"):
                    self.weapon.reset_weapon_pos()

            self.state[self.current_state].handle_events(event)

    def update(self):
        self.dt = self.clock.tick()
        self.state[self.current_state].update()

    def draw(self):
        self.state[self.current_state].draw()
        self.renderer.draw_queued()
        pg.display.flip()

    def new_game(self, level):
        self.player = Player(self)
        self.weapon = Weapon(self)
        self.object_handler = ObjectHandler(self)

        self.map = Map(self)
        self.map.get_map(level)
        self.player.on_level_change()
        self.weapon.save_weapon_info()

        self.pathfinding = PathFinding(self)
        self.hud.level_change(self.player.health, self.player.armor)

    def next_level(self, level):
        self.map_started_to_change = pg.time.get_ticks()
        self.object_handler = ObjectHandler(self)

        self.map = Map(self)
        self.map.get_map(level)
        self.current_map = level
        self.player.on_level_change()
        self.weapon.save_weapon_info()

        self.pathfinding = PathFinding(self)
        self.hud.level_change(self.player.health, self.player.armor)

        print(pg.time.get_ticks() - self.map_started_to_change)

    def restart_level(self, level):
        self.object_handler = ObjectHandler(self)

        self.map = Map(self)
        self.map.get_map(level)
        self.player.load_player_stats()
        self.weapon.load_weapon_info()

        self.pathfinding = PathFinding(self)
        self.hud.level_change(self.player.health, self.player.armor)

    def run(self):
        self.running = True

        while self.running:
            self.handle_events()
            self.update()
            self.draw()

    @property
    def current_state_obj(self):
        return self.state[self.current_state]

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
