from States.State import *


class IntroState(State):
    def __init__(self, game):
        super().__init__(game)
        self.title_surface = create_text_surface(self.font, "Welcome To Die!")
        self.continue_surface = create_text_surface(self.font, "Press mouse to continue")

    @staticmethod
    def on_set():
        return None

    def handle_events(self, event):
        if event.type == pg.KEYUP:
            if event.key == pg.K_RETURN or event.key == pg.K_SPACE:
                self.game.set_state("Loading")
                self.game.new_game("resources/levels/" + self.game.map_lists[0] + ".txt")
        if event.type == pg.MOUSEBUTTONUP and event.button == 1:
            self.game.set_state("Loading")
            self.game.new_game("resources/levels/" + self.game.map_lists[0] + ".txt")

    @staticmethod
    def update():
        return None

    def draw(self):
        pg.draw.rect(self.screen, (44, 44, 44), pg.Rect(0, 0, RES[0], RES[1]))
        self.screen.blit(self.title_surface[0], (self.title_surface[1][0],
                                                 self.title_surface[1][1] - self.title_surface[0].get_height()))
        self.screen.blit(self.continue_surface[0], (self.continue_surface[1][0], self.continue_surface[1][1]))
        pg.display.flip()
