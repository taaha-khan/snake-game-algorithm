import math
from grid import Grid

def Astar(start: tuple, end: tuple, walls: list, grid: Grid):
    Infinity = math.inf

    open_list = []
    closed_list = []

    open_list.append(start)
    parent = {str(start):None}

    f = {str(start):0}  # Distance to Start
    g = {str(start):0}  # Distance to End
    h = {str(start):0}  # g + f

    layer = {str(start):0}  # Movement of the snake

    while len(open_list) > 0:

        least = Infinity
        current = None
        for node in open_list:
            if f[str(node)] < least:
                least = f[str(node)]
                current = node
       
        if current == end:
            return constructPath(current, parent)
        
        open_list.remove(current)
        closed_list.append(current)

        gScore = g[str(current)] + grid.scl
        gScoreBest = False

        w = walls[:]
        if len(w) - layer[str(current)] >= 0:
            for _ in range(layer[str(current)]):
                w.remove(w[-1])
        elif len(w) - layer[str(current)] < 0: w.clear()

        neighbors = getNeighbors(current, w, start, end, grid)
        for n in neighbors:

            if n not in closed_list:
                if n not in open_list:
                    open_list.append(n)
                    parent[str(n)] = current

                    gScoreBest = True
                    h[str(n)] = heuristic(n, end)

                elif gScore < g[str(n)]:
                    gScoreBest = True
                
                if gScoreBest:
                    g[str(n)] = gScore
                    h[str(n)] = heuristic(n, end)
                    f[str(n)] = g[str(n)] + h[str(n)]

                    p = parent[str(n)]
                    layer[str(n)] = layer[str(p)] + 1

    return False

def getNeighbors(node, walls, start, end, grid):
    above = (node[0], node[1] + grid.scl)
    below = (node[0], node[1] - grid.scl)
    onright = (node[0] + grid.scl, node[1])
    onleft = (node[0] - grid.scl, node[1])

    possible = [above, below, onright, onleft]
    neighbors = []

    for n in possible:
        if isSafe(n, walls, grid): 
            neighbors.append(n)

    return neighbors

def isSafe(node, walls, grid):
    if node not in walls and node in grid.cells:
        return True
    return False

def constructPath(node, parent):
    path = []
    path.append(node)
    while parent[str(node)] != None:
        node = parent[str(node)]
        path.append(node)
    path.reverse()
    return path

def heuristic(pos1, pos2):
    x1, y1 = pos1; x2, y2 = pos2

    dist = abs(x1 - x2) + abs(y1 - y2)  # Change Distance
    dist = abs(math.sqrt((x2 - x1)**2 + (y2 - y1)**2))  # Euclidian Distance

    return dist
