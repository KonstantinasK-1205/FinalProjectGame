import math


def resolve_collision(x, y, dx, dy, tilemap, radius):
    # Margin is used to push the player away from a wall and prevent the
    # collision from persisting due to rounding or floating point error
    margin = 0.001

    new_x = x + dx
    new_y = y + dy

    collided = None

    # First handle motion and collision in the X axis
    if new_x < x:
        if tilemap.is_wall(new_x - radius, y - radius):
            collided = tilemap.get_wall(new_x - radius, y - radius)
            new_x = math.ceil(new_x - radius) + radius + margin
        elif tilemap.is_wall(new_x - radius, y + radius):
            collided = tilemap.get_wall(new_x - radius, y + radius)
            new_x = math.ceil(new_x - radius) + radius + margin
    elif new_x > x:
        if tilemap.is_wall(new_x + radius, y - radius):
            collided = tilemap.get_wall(new_x + radius, y - radius)
            new_x = math.floor(new_x + radius) - radius - margin
        elif tilemap.is_wall(new_x + radius, y + radius):
            collided = tilemap.get_wall(new_x + radius, y + radius)
            new_x = math.floor(new_x + radius) - radius - margin

    # Next handle motion and collision in the Y axis
    if new_y < y:
        if tilemap.is_wall(new_x - radius, new_y - radius):
            collided = tilemap.get_wall(new_x - radius, new_y - radius)
            new_y = math.ceil(new_y - radius) + radius + margin
        elif tilemap.is_wall(new_x + radius, new_y - radius):
            collided = tilemap.get_wall(new_x + radius, new_y - radius)
            new_y = math.ceil(new_y - radius) + radius + margin
    elif new_y > y:
        if tilemap.is_wall(new_x - radius, new_y + radius):
            collided = tilemap.get_wall(new_x - radius, new_y + radius)
            new_y = math.floor(new_y + radius) - radius - margin
        elif tilemap.is_wall(new_x + radius, new_y + radius):
            collided = tilemap.get_wall(new_x + radius, new_y + radius)
            new_y = math.floor(new_y + radius) - radius - margin

    return CollisionResult(new_x, new_y, collided)


class CollisionResult:
    def __init__(self, x, y, collided):
        self.x = x
        self.y = y
        self.collided = collided
