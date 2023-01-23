import gui
import pygame as pg


class CenterPanel(gui.VBox):
    def __init__(self, game):
        super().__init__(game)

        self.hbox = gui.HBox(self.game)

        self.gridbox = gui.GridBox(self.game)
        self.gridbox.background_color = (0, 0, 0)
        self.gridbox.rows = self.game.map.width
        self.hbox.add(self.gridbox)

        self.vscrollbar = gui.VScrollbar(self.game)
        self.vscrollbar.size = (20, 0)
        self.vscrollbar.flexible = (False, True)
        self.vscrollbar.min_value = -5
        self.vscrollbar.max_value = self.game.map.height + 5
        self.vscrollbar.value = 0
        self.hbox.add(self.vscrollbar)

        self.hscrollbar = gui.HScrollbar(self.game)
        self.hscrollbar.size = (0, 20)
        self.hscrollbar.flexible = (True, False)
        self.hscrollbar.min_value = -5
        self.hscrollbar.max_value = self.game.map.width + 5
        self.hscrollbar.value = 0

        self.add(self.hbox)        
        self.add(self.hscrollbar)

        self.layout()

        self.dragging = False
        self.drawing = False
        self.mouse_on_press = (0, 0)
        self.value_on_press = (0, 0)
        self.mouse_cur = (0, 0)
        self.cursor_pos = (0, 0)

    def handle_event(self, event):
        super().handle_event(event)

        if event.type == pg.MOUSEBUTTONDOWN:
            # Check against the position of the gridbox to avoid enabling
            # drawing or dragging if the user clicks on the scrollbars
            if event.pos[0] >= self.gridbox.position[0] and event.pos[0] < (self.gridbox.position[0] + self.gridbox.size[0]) and \
               event.pos[1] >= self.gridbox.position[1] and event.pos[1] < (self.gridbox.position[1] + self.gridbox.size[1]):
                if event.button == 1:
                    self.drawing = True
                elif event.button == 3 and not self.dragging:
                    self.mouse_on_press = (event.pos[0], event.pos[1])
                    self.value_on_press = (self.hscrollbar.value, self.vscrollbar.value)
                    self.dragging = True
        elif event.type == pg.MOUSEBUTTONUP:
            if event.button == 1:
                self.drawing = False
            elif event.button == 3:
                self.dragging = False
        elif event.type == pg.WINDOWFOCUSLOST:
            self.dragging = False
            self.drawing = False

    def update(self):
        super().update()

        self.mouse_cur = pg.mouse.get_pos()
        self.cursor_pos = (
            max(0, min(self.game.map.width, int(int(self.hscrollbar.value) + (self.mouse_cur[0] - self.position[0]) / self.gridbox.tile_size[0]))),
            max(0, min(self.game.map.height, int(int(self.vscrollbar.value) + (self.mouse_cur[1] - self.position[1]) / self.gridbox.tile_size[1])))
        )

        if self.drawing:
            lp = self.game.current_state_obj.left_panel
            if lp.selected_tool == "paint" and ":" in lp.selected_brush:
                brush = lp.selected_brush.split(":")
                if brush[0] == "wall":
                    self.game.map.set_wall(self.cursor_pos[0], self.cursor_pos[1], int(brush[1]))
                elif brush[0] == "floor":
                    self.game.map.set_floor(self.cursor_pos[0], self.cursor_pos[1], int(brush[1]))
                elif brush[0] == "entity":
                    if brush[1] == "erase":
                        self.game.map.set_entity(self.cursor_pos[0], self.cursor_pos[1], "")
                    else:
                        self.game.map.set_entity(self.cursor_pos[0], self.cursor_pos[1], brush[1])
                self.update_gridbox()

        if self.dragging:
            sensitivity = 0.1
            rel_x = (self.mouse_cur[0] - self.mouse_on_press[0]) * sensitivity
            rel_y = (self.mouse_cur[1] - self.mouse_on_press[1]) * sensitivity

            self.hscrollbar.value = min(self.hscrollbar.max_value, max(self.hscrollbar.min_value, self.value_on_press[0] + rel_x))
            self.vscrollbar.value = min(self.vscrollbar.max_value, max(self.vscrollbar.min_value, self.value_on_press[1] + rel_y))

        self.hscrollbar.max_value = self.game.map.width - int(self.gridbox.size[0] / self.gridbox.tile_size[0]) + 5
        if self.hscrollbar.max_value - self.hscrollbar.min_value == 0:
            self.hscrollbar.max_value = self.hscrollbar.min_value + 1

        self.vscrollbar.max_value = self.game.map.height - int(self.gridbox.size[1] / self.gridbox.tile_size[1]) + 5
        if self.vscrollbar.max_value - self.vscrollbar.min_value == 0:
            self.vscrollbar.max_value = self.vscrollbar.min_value + 1

        self.gridbox.column_offset = self.hscrollbar.value
        self.gridbox.row_offset = self.vscrollbar.value
        self.gridbox.layout()

    def update_gridbox(self):
        self.gridbox.rows = self.game.map.width
        items = {
            "e": "resources/icons/editor/erase.png",
            "O": "resources/icons/editor/player.png",
            "Z": "resources/sprites/npc/Zombie/idle.png",
            "X": "resources/sprites/npc/Soldier/idle.png",
            "C": "resources/sprites/npc/Pinky/idle.png",
            "V": "resources/sprites/npc/LostSoul/idle.png",
            "B": "resources/sprites/npc/Reaper/idle.png",
            "N": "resources/sprites/npc/Battlelord/idle.png",
            "q": "resources/sprites/pickups/health.png",
            "w": "resources/sprites/pickups/armor.png",
            "a": "resources/sprites/pickups/special/corpse_pitchfork.png",
            "s": "resources/sprites/weapon/revolver/icon.png",
            "d": "resources/sprites/weapon/double_shotgun/icon.png",
            "f": "resources/sprites/weapon/automatic_rifle/icon.png",
            "S": "resources/sprites/pickups/ammo/Revolver.png",
            "D": "resources/sprites/pickups/ammo/Double Shotgun.png",
            "F": "resources/sprites/pickups/ammo/Automatic Rifle.png",
            "!": "resources/sprites/environment/tree0.png",
            "@": "resources/sprites/environment/TorchBig/0.png",
            "#": "resources/sprites/environment/TorchSmall/0.png",
            "*": "resources/sprites/environment/corpse0.png",
            "-": "resources/sprites/pickups/misc/silver_card.png",
            "]": "resources/icons/editor/level_change.png",
            "[": "resources/textures/crack.png",
            ",": "resources/sprites/pickups/ammo/pistol.png"
        }

        rp = self.game.current_state_obj.right_panel
        draw_entities = rp.layer_entities
        draw_walls = rp.layer_walls
        draw_floors = rp.layer_floors

        self.gridbox.children = []
        for i in range(self.game.map.width * self.game.map.height):
            tile = gui.Component(self.game)
            
            wall = self.game.map.walls[i]
            floor = self.game.map.floors[i]
            entity = self.game.map.entities[i]

            if entity in items and draw_entities:
                tile.background_texture = items[entity]
            elif wall > 0 and draw_walls:
                tile.background_texture = "resources/textures/desert/wall_" + str(wall) + ".jpg"
            elif floor > 0 and draw_floors:
                tile.background_texture = "resources/textures/desert/floor_" + str(floor) + ".jpg"
            else:
                tile.background_color = (32, 0, 0)
            self.gridbox.add(tile)
