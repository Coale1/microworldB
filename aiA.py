# NAME(S): Cole Adams, Odin York
#
# APPROACH: [WRITE AN OVERVIEW OF YOUR APPROACH HERE.]
#     Please use multiple lines (< ~80-100 char) for you approach write-up.
#     Keep it readable. In other words, don't write
#     the whole damned thing on one super long line.
#
#     Going to start with what we had for project 1. There's now a random amount of goals so the bots will have to search
#     the whole map before going to the exit. For now I will treat teleporteor tiles as ground tiles for the search algorithm.
#     Hopefully if both bots use the same visted set and memory dir it just works and doesn't cause problems. One major problem
#     I see is how do the bots know when they've search the whole map.

#     In-code comments DO NOT count as a description of
#     your approach.

import random
import BFS

class AI:
    def __init__(self, max_turns):
        """
        Called once before the sim starts. You may use this function
        to initialize any data or data structures you need.
        """
        self.visited = set()  
        self.pathStack = []
        self.directions = ['N', 'S', 'E', 'W']
        self.dirCords = {
            'N': (0, 1),
            'S': (0, -1),
            'E': (1, 0),
            'W': (-1, 0),
        }
        self.curPos = (0, 0)
        self.memory = {}
        self.goals = ["0","1","2","3","4","5","6","7","8","9"]
        self.turnNum = 0

    def update(self, percepts, msg):
        """
        PERCEPTS:
        Called each turn. Parameter "percepts" is a dictionary containing
        nine entries with the following keys: X, N, NE, E, SE, S, SW, W, NW.
        Each entry's value is a single character giving the contents of the
        map cell in that direction. X gives the contents of the cell the agent
        is in.

        COMMAND:
        This function must return one of the following commands as a string:
        N, E, S, W, U

        N moves the agent north on the map (i.e. up)
        E moves the agent east
        S moves the agent south
        W moves the agent west
        U uses/activates the contents of the cell if it is useable. For
        example, stairs (o, b, y, p) will not move the agent automatically
        to the corresponding hex. The agent must 'U' the cell once in it
        to be transported.

        The same goes for goal hexes (0, 1, 2, 3, 4, 5, 6, 7, 8, 9).
        """
        #improve so it detects 'r' anywhere in it's line of sight (It should now, see below)
        if percepts['X'][0] in self.goals:
            return 'U', 'lol'

        self.visited.add(self.curPos)

        # memorization - Use memory and a* or smth to go to exit once map is explored
        for dir in percepts:
            idk = (self.curPos[0], self.curPos[1])  # Store current position
            for tile in percepts[dir]:
                if dir == 'X':
                    self.memory[idk] = tile
                else:
                    idk = (self.curPos[0] + self.dirCords[dir][0],
                           self.curPos[1] + self.dirCords[dir][1])
                    if idk in self.memory:
                        break
                    self.memory[idk] = tile

        print(self.memory)

        # Detection for r and goals in any direction
        for direction in ['N', 'S', 'E', 'W']:    
            index = next((i for i, char in enumerate(percepts[direction]) if char in self.goals), None)
            if index is not None:
                moveToGoal = direction
                for _ in range(index):
                    self.curPos = (
                    self.curPos[0] + self.dirCords[moveToGoal][0],
                    self.curPos[1] + self.dirCords[moveToGoal][1]
                    )
                self.turnNum += 1
                return moveToGoal, "lol"
            
        if 'r' in self.memory.items():
            exitPath = BFS.pathToExit(self.memory, self.curPos)
            if len(exitPath) + self.turnNum >= 1000:
                nextDir = exitPath.pop()
                self.curPos = (self.curPos[0] + self.dirCords[nextDir][0],
                               self.curPos[1] + self.dirCords[nextDir][1])      
                self.turnNum += 1
                return nextDir, "lol" 


        # Explore unexplored g cells
        for direction in self.directions:
            # Allow movement to 'g' (ground) or 'r' (exit)
            if percepts[direction][0] == 'g' or percepts[direction][0] == 'r':
                newPos = (self.curPos[0] + self.dirCords[direction][0],
                          self.curPos[1] + self.dirCords[direction][1])
                if newPos not in self.visited:
                    self.pathStack.append(direction)  # Add to stack for backtracking
                    self.curPos = newPos
                    self.turnNum += 1
                    return direction, "lol"

        # backtracking when no new cells to explore
        if self.pathStack:
            lastDir = self.pathStack.pop()
            reverseDir = {'N': 'S', 'S': 'N', 'E': 'W', 'W': 'E'}
            reverseMove = reverseDir[lastDir]
            self.curPos = (self.curPos[0] + self.dirCords[reverseMove][0],
                           self.curPos[1] + self.dirCords[reverseMove][1])
            self.turnNum += 1
            return reverseMove, "lol"

        # Default move if nothing else (shouldn't be reached often)
        self.turnNum += 1
        return 'N'
