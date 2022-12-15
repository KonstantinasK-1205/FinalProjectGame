from states.state import *


class IntroState(State):
    def __init__(self, game):
        super().__init__(game)

        self.title_text = "Welcome to Final Project!"
        self.text.append("")
        self.text.append("You must kill all enemies to proceed to the next level.")
        self.text.append("Press Space or Left Mouse Button to start!")
        self.update_state_text()

    def on_set(self):
        pass

    def handle_events(self, event):
        if event.type == pg.KEYUP:
            if event.key == pg.K_RETURN or event.key == pg.K_SPACE:
                self.game.current_state = "Loading"
                self.game.new_game("resources/levels/" + self.game.map_lists[0] + ".txt")
        if event.type == pg.MOUSEBUTTONUP and event.button == 1:
            self.game.current_state = "Loading"
            self.game.new_game("resources/levels/" + self.game.map_lists[0] + ".txt")

    def update(self, dt):
        pass

    def draw(self):
        pg.draw.rect(self.screen, (44, 44, 44), pg.Rect(0, 0, RES[0], RES[1]))
        self.draw_state_text()
