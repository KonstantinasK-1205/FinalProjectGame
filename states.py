import pygame as pg
from settings import *

rgb_colors = {
    "White": (255, 255, 255),
    "Red": (255, 0, 0),
    "Green": (0, 255, 0),
    "Blue": (0, 0, 255),
    "Black": (0, 0, 0),
}


def center_surface(surface):
    return (RES[0] - surface.get_width()) / 2, (RES[1] - surface.get_height()) / 2


def create_text_surface(font, string, color='White', centered=True):
    position = (0, 0)
    if color not in rgb_colors:
        color = 'White'
    surface = font.render(string, True, rgb_colors[color])

    if centered:
        position = center_surface(surface)
    return [surface, position]


class State:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.font = pg.font.Font("resources/fonts/Font.ttf", 48)

    def update(self):
        return None

    def draw(self):
        return None


class IntroState(State):
    def __init__(self, game):
        super().__init__(game)
        self.title_surface = create_text_surface(self.font, "Welcome To Die")
        self.continue_surface = create_text_surface(self.font, "Press mouse to continue")

    def handle_events(self, event):
        if event.type == pg.KEYUP:
            if event.key == pg.K_RETURN or event.key == pg.K_SPACE:
                self.game.current_state = "Loading"
                self.game.new_game("resources/levels/" + self.game.map_lists[0] + ".txt")
        if event.type == pg.MOUSEBUTTONUP and event.button == 1:
            self.game.current_state = "Loading"
            self.game.new_game("resources/levels/" + self.game.map_lists[0] + ".txt")

    def update(self):
        return None

    def draw(self):
        pg.draw.rect(self.screen, (44, 44, 44), pg.Rect(0, 0, RES[0], RES[1]))
        self.screen.blit(self.title_surface[0], (self.title_surface[1][0],
                                                 self.title_surface[1][1] - self.title_surface[0].get_height()))
        self.screen.blit(self.continue_surface[0], (self.continue_surface[1][0], self.continue_surface[1][1]))
        pg.display.flip()


class LoadingState(State):
    def __init__(self, game):
        super().__init__(game)
        self.game_ready = False
        self.level_surface = create_text_surface(self.font, str(self.game.map_lists[0]))

        self.loading_string = "Loading level"
        self.loading_surface = create_text_surface(self.font, self.loading_string)
        self.loading_screen_time = pg.time.get_ticks()

    def handle_events(self, event):
        if event.type == pg.KEYUP:
            if event.key == pg.K_RETURN or event.key == pg.K_SPACE:
                self.game_ready = False
                self.game.current_state = "Game"
        if event.type == pg.MOUSEBUTTONUP and event.button == 1:
            self.game_ready = False
            self.game.current_state = "Game"

    def update(self):
        current_tick = pg.time.get_ticks()
        if not self.game_ready and current_tick - self.loading_screen_time < 500:
            if self.loading_string.count('.') < 3:
                self.loading_string += "."
                self.loading_surface = create_text_surface(self.font, self.loading_string)

            else:
                self.loading_string = "Loading level"
                self.loading_surface = create_text_surface(self.font, self.loading_string)
            self.loading_screen_time = current_tick
        elif self.game_ready:
            self.loading_string = "Press mouse to continue"
            self.loading_surface = create_text_surface(self.font, self.loading_string)

    def draw(self):
        pg.draw.rect(self.screen, (44, 44, 44), pg.Rect(0, 0, RES[0], RES[1]))
        self.screen.blit(self.level_surface[0], (self.level_surface[1][0],
                                                 self.level_surface[1][1] - self.level_surface[0].get_height()))
        self.screen.blit(self.loading_surface[0], (self.loading_surface[1][0], self.loading_surface[1][1]))
        pg.display.flip()


class GameState(State):
    def __init__(self, game):
        super().__init__(game)

    def handle_events(self, event):
        self.game.player.handle_events(event)
        if event.type == pg.KEYUP:
            if event.key == pg.K_ESCAPE:
                self.game.current_state = "Pause"
                self.game.state[self.game.current_state].pause()

    def update(self):
        self.game.raycasting.update()
        self.game.object_handler.update()
        self.game.player.update()
        self.game.delta_time = self.game.clock.tick(FPS)

    def draw(self):
        self.game.object_renderer.draw()
        self.game.weapon.draw()
        pg.display.flip()


class PauseState(State):
    def __init__(self, game):
        super().__init__(game)
        self.pause_surface = create_text_surface(self.font, "Game Paused!")
        self.continue_surface = create_text_surface(self.font, "Press mouse to continue")

    def handle_events(self, event):
        if event.type == pg.KEYUP:
            if event.key == pg.K_RETURN or event.key == pg.K_SPACE or event.key == pg.K_ESCAPE:
                self.unpause()
                self.game.current_state = "Game"
        if event.type == pg.MOUSEBUTTONUP and event.button == 1:
            self.unpause()
            self.game.current_state = "Game"

    def update(self):
        return None

    def draw(self):
        pg.draw.rect(self.screen, (44, 44, 44), pg.Rect(0, 0, RES[0], RES[1]))
        self.screen.blit(self.pause_surface[0], (self.pause_surface[1][0],
                                              self.pause_surface[1][1] - self.pause_surface[0].get_height()))
        self.screen.blit(self.continue_surface[0], (self.continue_surface[1][0], self.continue_surface[1][1]))
        pg.display.flip()

    def pause(self):
        pg.mouse.set_visible(True)
        pg.event.set_grab(False)

    def unpause(self):
        pg.mouse.set_visible(False)
        pg.event.set_grab(True)


class WinState(State):
    def __init__(self, game):
        super().__init__(game)
        self.victory_image = pg.image.load('resources/textures/win.png').convert_alpha()
        self.victory_image = pg.transform.scale(self.victory_image, RES)

    def handle_events(self, event):
        if event.type == pg.KEYUP:
            if event.key == pg.K_RETURN or event.key == pg.K_SPACE:
                self.game.is_running = False
        if event.type == pg.MOUSEBUTTONUP and event.button == 1:
            self.game.is_running = False

    def update(self):
        return None

    def draw(self):
        self.screen.blit(self.victory_image, (0, 0))
        pg.display.flip()


class LoseState(State):
    def __init__(self, game):
        super().__init__(game)
        self.lose_image = pg.image.load('resources/textures/game_over.png').convert_alpha()
        self.lose_image = pg.transform.scale(self.lose_image, RES)

    def handle_events(self, event):
        if event.type == pg.KEYUP:
            if event.key == pg.K_RETURN or event.key == pg.K_SPACE:
                self.game.current_state = "Loading"
                self.game.new_game("resources/levels/" + self.game.map_lists[0] + ".txt")
            if event.key == pg.K_ESCAPE:
                self.game.is_running = False

        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            self.game.current_state = "Loading"
            self.game.new_game("resources/levels/" + self.game.map_lists[0] + ".txt")

    def update(self):
        return None

    def draw(self):
        self.screen.blit(self.lose_image, (0, 0))
        pg.display.flip()
