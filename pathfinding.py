

def find_path(start_pos, target_pos, level_map):
    # Define all possible movement directions
    # Diagonal movement is also possible, but may result in a path that goes
    # through a wall, as walls are not checked separately on X and Y axes
    directions = [
        (-1,  0),
        ( 0, -1),
        ( 0,  1),
        ( 1,  0)
    ]

    # Pathfinding is performed on a grid, so truncate the decimal points
    # Also, positions need to be stored as tuples, as lists do not work in sets
    start_pos = (int(start_pos[0]), int(start_pos[1]))
    target_pos = (int(target_pos[0]), int(target_pos[1]))

    # Remember previously visited positions to avoid an infinite loop
    visited = set()

    queue = []
    # Start pathfinding from the target position so that the next step from the
    # starting position can be returned
    queue.append(target_pos)
    while len(queue) > 0:
        pos = queue.pop()

        visited.add(pos)

        for d in directions:
            next_pos = (pos[0] + d[0], pos[1] + d[1])

            # If the next position is the start, it means that the current
            # position is the next position from the start, and should be
            # returned
            # Make sure to return the position as an array
            if next_pos == start_pos:
                return [pos[0], pos[1]]

            if next_pos not in visited and not level_map.is_wall(next_pos[0], next_pos[1]):
                queue.append(next_pos)

    # No path was found
    return start_pos
