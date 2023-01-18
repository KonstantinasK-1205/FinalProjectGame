import gui


class RightPanel(gui.VBox):
    def __init__(self, game):
        super().__init__(game)

        self.flexible = (False, True)
        self.size = (211, 0)

        layer_text = gui.Text(self.game)
        layer_text.font = game.unscaled_fonts[1]
        layer_text.string = "Layers"
        layer_text.flexible = (True, False)
        layer_text.size = (0, 40)

        self.layer_grid_button = gui.Button(self.game)
        self.layer_grid_button.background_color = (0, 64, 0)
        self.layer_grid_button.font = game.unscaled_fonts[1]
        self.layer_grid_button.string = "Grid"
        self.layer_grid_button.flexible = (True, False)
        self.layer_grid_button.size = (0, 40)
        self.layer_grid_button.function = self.onclick_layer_grid

        self.layer_entities_button = gui.Button(self.game)
        self.layer_entities_button.background_color = (0, 64, 0)
        self.layer_entities_button.font = game.unscaled_fonts[1]
        self.layer_entities_button.string = "Entities"
        self.layer_entities_button.flexible = (True, False)
        self.layer_entities_button.size = (0, 40)
        self.layer_entities_button.function = self.onclick_layer_entities

        self.layer_walls_button = gui.Button(self.game)
        self.layer_walls_button.background_color = (0, 64, 0)
        self.layer_walls_button.font = game.unscaled_fonts[1]
        self.layer_walls_button.string = "Walls"
        self.layer_walls_button.flexible = (True, False)
        self.layer_walls_button.size = (0, 40)
        self.layer_walls_button.function = self.onclick_layer_walls

        self.layer_floors_button = gui.Button(self.game)
        self.layer_floors_button.background_color = (0, 64, 0)
        self.layer_floors_button.font = game.unscaled_fonts[1]
        self.layer_floors_button.string = "Floors"
        self.layer_floors_button.flexible = (True, False)
        self.layer_floors_button.size = (0, 40)
        self.layer_floors_button.function = self.onclick_layer_floors

        self.add(layer_text)
        self.add(self.layer_grid_button)
        self.add(self.layer_entities_button)
        self.add(self.layer_walls_button)
        self.add(self.layer_floors_button)

        self.layer_grid = True
        self.layer_entities = True
        self.layer_walls = True
        self.layer_floors = True

    def onclick_layer_grid(self, component):
        self.layer_grid = not self.layer_grid
        if self.layer_grid:
            self.layer_grid_button.background_color = (0, 64, 0)
        else:
            self.layer_grid_button.background_color = (0, 0, 0)

        self.game.current_state_obj.center_panel.gridbox.draw_grid = self.layer_grid

    def onclick_layer_entities(self, component):
        self.layer_entities = not self.layer_entities
        if self.layer_entities:
            self.layer_entities_button.background_color = (0, 64, 0)
        else:
            self.layer_entities_button.background_color = (0, 0, 0)

        self.game.current_state_obj.center_panel.update_gridbox(self.layer_entities, self.layer_walls, self.layer_floors)

    def onclick_layer_walls(self, component):
        self.layer_walls = not self.layer_walls
        if self.layer_walls:
            self.layer_walls_button.background_color = (0, 64, 0)
        else:
            self.layer_walls_button.background_color = (0, 0, 0)

        self.game.current_state_obj.center_panel.update_gridbox(self.layer_entities, self.layer_walls, self.layer_floors)

    def onclick_layer_floors(self, component):
        self.layer_floors = not self.layer_floors
        if self.layer_floors:
            self.layer_floors_button.background_color = (0, 64, 0)
        else:
            self.layer_floors_button.background_color = (0, 0, 0)

        self.game.current_state_obj.center_panel.update_gridbox(self.layer_entities, self.layer_walls, self.layer_floors)
