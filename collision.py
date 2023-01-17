import math


def resolve_collision(pos, dx, dy, tilemap, radius):
    # Margin is used to push the player away from a wall and prevent the
    # collision from persisting due to rounding or floating point error
    margin = 0.001

    new_pos = [pos[0] + dx, pos[1] + dy, pos[2]]

    collided = None

    # First handle motion and collision in the X axis
    if new_pos[0] < pos[0]:

        if tilemap.is_wall(new_pos[0] - radius, pos[1] - radius):
            collided = tilemap.get_wall(new_pos[0] - radius, pos[1] - radius)
            new_pos[0] = math.ceil(new_pos[0] - radius) + radius + margin

        elif tilemap.is_wall(new_pos[0] - radius, pos[1] + radius):
            collided = tilemap.get_wall(new_pos[0] - radius, pos[1] + radius)
            new_pos[0] = math.ceil(new_pos[0] - radius) + radius + margin

    elif new_pos[0] > pos[0]:
        if tilemap.is_wall(new_pos[0] + radius, pos[1] - radius):
            collided = tilemap.get_wall(new_pos[0] + radius, pos[1] - radius)
            new_pos[0] = math.floor(new_pos[0] + radius) - radius - margin

        elif tilemap.is_wall(new_pos[0] + radius, pos[1] + radius):
            collided = tilemap.get_wall(new_pos[0] + radius, pos[1] + radius)
            new_pos[0] = math.floor(new_pos[0] + radius) - radius - margin

    # Next handle motion and collision in the Y axis
    if new_pos[1] < pos[1]:
        if tilemap.is_wall(new_pos[0] - radius, new_pos[1] - radius):
            collided = tilemap.get_wall(new_pos[0] - radius, new_pos[1] - radius)
            new_pos[1] = math.ceil(new_pos[1] - radius) + radius + margin

        elif tilemap.is_wall(new_pos[0] + radius, new_pos[1] - radius):
            collided = tilemap.get_wall(new_pos[0] + radius, new_pos[1] - radius)
            new_pos[1] = math.ceil(new_pos[1] - radius) + radius + margin

    elif new_pos[1] > pos[1]:
        if tilemap.is_wall(new_pos[0] - radius, new_pos[1] + radius):
            collided = tilemap.get_wall(new_pos[0] - radius, new_pos[1] + radius)
            new_pos[1] = math.floor(new_pos[1] + radius) - radius - margin

        elif tilemap.is_wall(new_pos[0] + radius, new_pos[1] + radius):
            collided = tilemap.get_wall(new_pos[0] + radius, new_pos[1] + radius)
            new_pos[1] = math.floor(new_pos[1] + radius) - radius - margin

    return new_pos, collided
