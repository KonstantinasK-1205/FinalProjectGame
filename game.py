from object_handler import *
from hud.hud_manager import *
from map import *
from player import *
from renderer.renderer import *
from sound import *
from sprites.sprite_manager import *
from states.game import GameState
from states.menu import MenuState
from states.options import OptionsState
from states.loading import LoadingState
from states.lose import LoseState
from states.win import WinState
from states.controls import ControlsState
from states.video_options import VideoOptionsState
from states.audio_options import AudioOptionsState
from states.editor import EditorState
from weapons.weapon import Weapon
from settings_manager import *


class Game:
    def __init__(self):
        # Initialize the settings manager first as it may be needed for window
        # and other object initialization
        self.settings_manager = SettingsManager()
        self.settings_manager.load()

        pg.init()
        fullscreen = pg.FULLSCREEN if self.settings_manager.settings["fullscreen"] else 0
        pg.display.set_mode(
            (
                self.settings_manager.settings["width"],
                self.settings_manager.settings["height"]
            ),
            fullscreen | pg.RESIZABLE | pg.OPENGL | pg.DOUBLEBUF,
            vsync=self.settings_manager.settings["vsync"]
        )
        pg.display.set_caption("Final Project")
        pg.display.set_icon(pg.image.load("resources/icons/game_icon.png"))

        # Init variables
        self.fonts = [None] * 3
        self.unscaled_fonts = [
            pg.font.Font("resources/fonts/font.ttf", 36),
            pg.font.Font("resources/fonts/font.ttf", 24),
            pg.font.Font("resources/fonts/font.ttf", 18)
        ]
        self.running = False

        # Needs to be initialized, otherwise will crash on resize before new game
        self.player = None
        self.weapon = None

        self.clock = pg.time.Clock()
        self.renderer = Renderer(self)
        self.sprite_manager = SpriteManager(self)
        self.object_handler = ObjectHandler(self)
        self.player = Player(self)
        self.hud = Hud(self)
        self.map = Map(self)
        self.sound = Sound(self)

        self.starting_map = "Level1"
        self.current_map = "Level1"

        self.init_fonts()

        self.state = {
            "Menu": MenuState(self),
            "Options": OptionsState(self),
            "Loading": LoadingState(self),
            "Game": GameState(self),
            "Win": WinState(self),
            "Lose": LoseState(self),
            "Controls": ControlsState(self),
            "VideoOptions": VideoOptionsState(self),
            "AudioOptions": AudioOptionsState(self),
            "Editor": EditorState(self)
        }
        self.current_state = "Menu"
        self.map_started_to_change = 0
        self.dt = 0

    def __del__(self):
        pg.quit()

    def init_fonts(self):
        self.fonts[0] = pg.font.Font("resources/fonts/font.ttf", int(36 / 720 * self.height))
        self.fonts[1] = pg.font.Font("resources/fonts/font.ttf", int(24 / 720 * self.height))
        self.fonts[2] = pg.font.Font("resources/fonts/font.ttf", int(18 / 720 * self.height))

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

            self.state[self.current_state].handle_event(event)

    def update(self):
        self.dt = self.clock.tick()
        self.state[self.current_state].update()

    def draw(self):
        self.state[self.current_state].draw()
        self.renderer.draw_queued()
        pg.display.flip()

    def new_game(self, level_filename):
        self.player = Player(self)
        self.weapon = Weapon(self)
        self.object_handler = ObjectHandler(self)

        self.map.load(level_filename)
        self.player.on_level_change()
        self.weapon.save_weapon_info()

        self.hud.level_change(self.player.health, self.player.armor)
        self.object_handler.update_npc_list()

    def next_level(self, level_filename):
        self.map_started_to_change = pg.time.get_ticks()
        self.object_handler = ObjectHandler(self)

        self.map.load(level_filename)
        self.current_map = level_filename
        self.player.on_level_change()
        self.weapon.save_weapon_info()

        self.hud.level_change(self.player.health, self.player.armor)
        self.object_handler.update_npc_list()

        print("Map: " + str(self.current_map) + ", loaded in: " + str(
            pg.time.get_ticks() - self.map_started_to_change) + "ms.")

    def restart_level(self, level_filename):
        self.object_handler = ObjectHandler(self)

        self.map.load(level_filename)
        self.player.load_player_stats()
        self.weapon.load_weapon_info()

        self.hud.level_change(self.player.health, self.player.armor)
        self.object_handler.update_npc_list()

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
