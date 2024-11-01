def pathToExit(maze, start):
    directions = {
        'N': (0, 1),  # Move north
        'S': (0, -1), # Move south
        'E': (1, 0),  # Move east
        'W': (-1, 0)  # Move west
    }

    # find the coordinates of 'r'
    exitPos = None
    for cord, tile in maze.items():
        if tile == 'r':
            exitPos = cord
            break

    # list with the starting position
    queue = [(start, [])]
    visited = set()
    visited.add(start)

    # bfs
    while queue:
        currentPos, path = queue.pop(0)  
        
        # check if we've reached the exit
        if currentPos == exitPos:
            return path  # Shortest path to the exit

        for direction, (dx, dy) in directions.items():
            newPos = (currentPos[0] + dx, currentPos[1] + dy)
            if newPos in maze and maze[newPos] != 'w' and newPos not in visited:
                visited.add(newPos)
                queue.append((newPos, path + [direction]))

    return None