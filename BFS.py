from collections import deque

def pathToExit(maze, start):
    directions = {
        'N': (-1, 0),  # Move north
        'S': (1, 0),   # Move south
        'E': (0, 1),   # Move east
        'W': (0, -1)   # Move west
    }

    # find cord of 'r'
    exitPos = None
    for cord, tile in maze.items():
        if tile == 'r':
            exitPos = cord
            break

    # queue with the starting position
    queue = deque([(start, [])])
    visited = set()
    visited.add(start)

    # bfs
    while queue:
        currentPos, path = queue.popleft()
        
        # check if we've reached the exit
        if currentPos == exitPos:
            return path  # Shortest path to the exit
        for direction, (dx, dy) in directions.items():
            newPos = (currentPos[0] + dx, currentPos[1] + dy)
            if newPos in maze and maze[newPos] != 'w' and newPos not in visited:
                visited.add(newPos)
                queue.append((newPos, path + [direction]))

    return None