import gui
import copy


class LeftPanel(gui.VBox):
    def __init__(self, game):
        super().__init__(game)

        self.flexible = (False, True)
        self.size = (211, 0)

        self.game.renderer.load_texture_from_file("resources/icons/editor/paint.png")
        self.game.renderer.load_texture_from_file("resources/icons/editor/select.png")
        self.game.renderer.load_texture_from_file("resources/icons/editor/erase.png")

        # Init toolbar
        toolbar_spacer = gui.Component(self.game)
        toolbar_spacer.background_color = (0, 0, 0)

        toolbar_select = gui.Button(self.game)
        toolbar_select.flexible = (True, True)
        toolbar_select.size = (0, 0)
        toolbar_select.font = game.unscaled_fonts[1]
        toolbar_select.background_color = (0, 0, 0)
        toolbar_select.background_texture = "resources/icons/editor/select.png"
        toolbar_select.function = self.handle_select_tool

        toolbar_paint = gui.Button(self.game)
        toolbar_paint.flexible = (True, True)
        toolbar_paint.size = (0, 0)
        toolbar_paint.font = game.unscaled_fonts[1]
        toolbar_paint.background_color = (0, 0, 0)
        toolbar_paint.background_texture = "resources/icons/editor/paint.png"
        toolbar_paint.function = self.handle_paint_tool

        toolbar = gui.HBox(self.game)
        toolbar.flexible = (True, False)
        toolbar.size = (0, 40)
        toolbar.background_color = (0, 0, 0)
        toolbar.add(copy.copy(toolbar_spacer))
        toolbar.add(toolbar_select)
        toolbar.add(toolbar_paint)
        toolbar.add(copy.copy(toolbar_spacer))
        self.add(toolbar)

        # Init pickers
        entities_text = gui.Button(self.game)
        entities_text.flexible = (True, False)
        entities_text.size = (0, 40)
        entities_text.font = game.unscaled_fonts[1]
        entities_text.string = "Entities"
        entities_text.function = self.toggle_entities
        self.add(entities_text)

        self.entities_grid = gui.GridBox(self.game)
        self.entities_grid.background_color = (0, 0, 0)
        self.entities_grid.rows = 4
        self.init_entities()

        self.entities_scrollbar = gui.VScrollbar(self.game)
        self.entities_scrollbar.flexible = (False, True)
        self.entities_scrollbar.size = (20, 0)
        self.entities_scrollbar.min_value = 0
        self.entities_scrollbar.max_value = len(self.entities_grid.children) / 4
        self.entities_scrollbar.step = 3
        self.entities_scrollbar.value = 0
        self.entities_scrollbar.slider_height = 50

        self.entities_hbox = gui.HBox(self.game)
        self.entities_hbox.flexible = (True, True)
        self.entities_hbox.add(self.entities_grid)
        self.entities_hbox.add(self.entities_scrollbar)

        self.add(self.entities_hbox)

        wall_text = gui.Button(self.game)
        wall_text.flexible = (True, False)
        wall_text.size = (0, 40)
        wall_text.font = game.unscaled_fonts[1]
        wall_text.string = "Walls"
        wall_text.function = self.toggle_walls
        self.add(wall_text)

        self.wall_grid = gui.GridBox(self.game)
        self.wall_grid.background_color = (0, 0, 0)
        self.wall_grid.rows = 4
        self.init_walls()
        self.add(self.wall_grid)

        floor_text = gui.Button(self.game)
        floor_text.flexible = (True, False)
        floor_text.size = (0, 40)
        floor_text.font = game.unscaled_fonts[1]
        floor_text.string = "Floors"
        floor_text.function = self.toggle_floors
        self.add(floor_text)

        self.floor_grid = gui.GridBox(self.game)
        self.floor_grid.background_color = (0, 0, 0)
        self.floor_grid.rows = 4
        self.init_floors()
        self.add(self.floor_grid)

        self.selected_tool = "select"
        self.selected_brush = ""

    def init_entities(self):
        items = [
            ("entity:erase", "Erase Entity", "resources/icons/editor/erase.png"),
            ("entity:O", "Player", "resources/icons/editor/player.png"),
            ("entity:Z", "Zombie", "resources/sprites/npc/Zombie/idle.png"),
            ("entity:X", "Soldier", "resources/sprites/npc/Soldier/idle.png"),
            ("entity:C", "Pinky", "resources/sprites/npc/Pinky/idle.png"),
            ("entity:V", "Lost Soul", "resources/sprites/npc/LostSoul/idle.png"),
            ("entity:B", "Reaper", "resources/sprites/npc/Reaper/idle.png"),
            ("entity:N", "Battlelord", "resources/sprites/npc/Battlelord/idle.png"),
            ("entity:q", "Health Pickup", "resources/sprites/pickups/health.png"),
            ("entity:w", "Armor Pickup", "resources/sprites/pickups/armor.png"),
            ("entity:a", "Pitchfork Pickup", "resources/sprites/pickups/special/corpse_pitchfork.png"),
            ("entity:s", "Revolver Pickup", "resources/sprites/weapon/revolver/icon.png"),
            ("entity:d", "Double Shotgun Pickup", "resources/sprites/weapon/double_shotgun/icon.png"),
            ("entity:f", "Automatic Rifle Pickup", "resources/sprites/weapon/automatic_rifle/icon.png"),
            ("entity:S", "Revolver Ammo", "resources/sprites/pickups/ammo/Revolver.png"),
            ("entity:D", "Shotgun Ammo", "resources/sprites/pickups/ammo/Double Shotgun.png"),
            ("entity:F", "Rifle Ammo", "resources/sprites/pickups/ammo/Automatic Rifle.png"),
            ("entity:!", "Tree", "resources/sprites/environment/tree0.png"),
            ("entity:@", "Big Torch", "resources/sprites/environment/TorchBig/0.png"),
            ("entity:#", "Small Torch", "resources/sprites/environment/TorchSmall/0.png"),
            ("entity:*", "Corpse", "resources/sprites/environment/corpse0.png"),
            ("entity:-", "Bonus Level", "resources/sprites/pickups/misc/silver_card.png"),
            ("entity:]", "Level Change Chunk", "resources/icons/editor/level_change.png"),
            ("entity:[", "Breakable Wall", "resources/textures/crack.png"),
            ("entity:,", "Zombie Spawn", "resources/sprites/pickups/ammo/pistol.png")
        ]

        self.init_grid(self.entities_grid, items)

    def init_walls(self):
        items = [
            ("wall:0", "Erase Wall", "resources/icons/editor/erase.png")
        ]
        for i in range(1, 7):
            items.append((
                "wall:" + str(i),
                "Wall " + str(i),
                "resources/textures/desert/wall_" + str(i) + ".jpg"
            ))

        self.init_grid(self.wall_grid, items)

    def init_floors(self):
        items = [
            ("floor:0", "Erase Floor", "resources/icons/editor/erase.png"),
        ]
        for i in range(1, 3):
            items.append((
                "floor:" + str(i),
                "Floor " + str(i),
                "resources/textures/desert/floor_" + str(i) + ".jpg"
            ))

        self.init_grid(self.floor_grid, items)

    def init_grid(self, grid, items):
        grid.children = []
        for i in items:
            self.game.renderer.load_texture_from_file(i[2])

            tooltip = gui.Text(self.game)
            tooltip.background_color = (32, 32, 32, 192)
            tooltip.font = self.game.unscaled_fonts[2]
            tooltip.string = i[1]
            tooltip.centered = (False, False)
            tooltip.visible = False

            button = gui.Button(self.game)
            button.background_color = (0, 0, 0)
            button.background_texture = i[2]
            button.function = self.handle_select
            button.user_data = i[0]
            button.tooltip = tooltip

            grid.add(button)

    def toggle_entities(self, component):
        self.entities_hbox.visible = not self.entities_hbox.visible
        self.layout()

    def toggle_walls(self, component):
        self.wall_grid.visible = not self.wall_grid.visible
        self.layout()

    def toggle_floors(self, component):
        self.floor_grid.visible = not self.floor_grid.visible
        self.layout()

    def handle_select(self, component):
        self.selected_brush = component.user_data

    def handle_select_tool(self, component):
        self.selected_tool = "select"

    def handle_paint_tool(self, component):
        self.selected_tool = "paint"

    def update(self):
        super().update()

        self.entities_grid.row_offset = self.entities_scrollbar.value
        self.entities_grid.layout()
