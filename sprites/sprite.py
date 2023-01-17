import math


class Sprite:
    def __init__(self, game, pos=None, size=None):
        # Variables to other objects
        self.game = game
        self.player = game.player
        self.sprite_manager = game.sprite_manager

        # Position and size variables
        self.pos = [0, 0, 0] if pos is None else pos
        self.size = [0, 0] if size is None else size

        # Path to sprite and delete variable
        self.sprite = None
        self.delete = False

    def update(self):
        pass

    def draw(self):
        self.game.renderer.draw_sprite(self.pos, self.size, self.sprite)

    # Calculate distance between sprite and passed object position
    def distance_from(self, other):
        return math.dist(self.pos, other.pos)

    # Returns grid (int) position
    @property
    def grid_pos(self):
        return [int(self.pos[0]),  # X Position
                int(self.pos[1]),  # Y Position
                int(self.pos[2])]  # Z Position

    # Returns exact (float) position
    @property
    def exact_pos(self):
        return self.pos

    # Returns exact (float) position on X axis
    @property
    def pos_x(self):
        return self.pos[0]

    # Returns exact (float) position on Y axis
    @property
    def pos_y(self):
        return self.pos[1]

    # Returns exact (float) position on Z axis
    @property
    def pos_z(self):
        return self.pos[2]

    # Returns sprite (image) width
    @property
    def width(self):
        return self.size[0]

    # Returns sprite (image) height
    @property
    def height(self):
        return self.size[1]
