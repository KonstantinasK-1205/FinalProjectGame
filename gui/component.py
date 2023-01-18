import pygame as pg


class Component:
    def __init__(self, game):
        self.game = game
        self.parent = None
        self.children = []
        self.position = (0, 0)
        self.size = (0, 0)
        self.flexible = (True, True)
        self.background_color = (32, 32, 32)
        self.background_texture = None
        self.visible = True
        self.active = True
        self.tooltip = None
        self.user_data = None

    def add(self, component):
        component.parent = self
        self.children.append(component)

    def handle_event(self,event):
        if not self.visible or not self.active:
            return

        if self.tooltip and event.type == pg.MOUSEMOTION:
            if event.pos[0] >= self.position[0] and event.pos[0] < (self.position[0] + self.size[0]) and \
               event.pos[1] >= self.position[1] and event.pos[1] < (self.position[1] + self.size[1]):
                self.tooltip.visible = True
                # Offset the tooltip by a bit to not overlap the cursor
                self.tooltip.position = (event.pos[0] + 10, event.pos[1] + 15)
            else:
                self.tooltip.visible = False

        for c in self.children:
            if c.position[0] + c.size[0] - 1 < self.position[0] or \
               c.position[1] + c.size[1] - 1 < self.position[1] or \
               c.position[0] + c.size[0] - 1 > self.position[0] + self.size[0] or \
               c.position[1] + c.size[1] - 1 > self.position[1] + self.size[1]:
                continue

            c.handle_event(event)

        if self.tooltip:
            self.tooltip.handle_event(event)

    def update(self):
        if not self.visible:
            return

        for c in self.children:
            if c.position[0] + c.size[0] - 1 < self.position[0] or \
               c.position[1] + c.size[1] - 1 < self.position[1] or \
               c.position[0] + c.size[0] - 1 > self.position[0] + self.size[0] or \
               c.position[1] + c.size[1] - 1 > self.position[1] + self.size[1]:
                continue

            c.update()

        if self.tooltip:
            self.tooltip.update()

    def draw(self):
        if not self.visible:
            return

        if self.background_texture:
            self.game.renderer.draw_rect(
                self.position[0],
                self.position[1],
                self.size[0],
                self.size[1],
                self.background_texture
            )
        else:
            self.game.renderer.draw_rect(
                self.position[0],
                self.position[1],
                self.size[0],
                self.size[1],
                color=self.background_color
            )

        for c in self.children:
            if c.position[0] + c.size[0] - 1 < self.position[0] or \
               c.position[1] + c.size[1] - 1 < self.position[1] or \
               c.position[0] + c.size[0] - 1 > self.position[0] + self.size[0] or \
               c.position[1] + c.size[1] - 1 > self.position[1] + self.size[1]:
                continue

            c.draw()

    def draw_tooltips(self):
        for c in self.children:
            c.draw_tooltips()

        if self.tooltip:
            self.tooltip.draw()

    def layout(self):
        pass
