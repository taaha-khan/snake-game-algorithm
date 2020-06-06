import math, random
from grid import Grid
import turtle


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

    t = turtle.Turtle()
    t.speed(0)
    t.pu(); t.ht()
    t.color('blue')

    # t.clear()
    # getAmountAvailableNodes(start, grid, walls, t)

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

        movedWalls = walls[:]
        if layer[str(current)] > 4:
            if len(walls) - layer[str(current)] > 0:
                for i in range(layer[str(current)] - 4):
                    movedWalls.pop()
            else: movedWalls.clear()
            movedWalls = [current] + constructPath(current, parent) + movedWalls
        # if getAmountAvailableNodes(current, grid, movedWalls, t):
        #     continue

        neighbors = getNeighbors(current, movedWalls, grid)
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

def getNeighbors(node, walls, grid):
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



def getAmountAvailableNodes(pos: tuple, grid: Grid, walls: list, t):

    t.clear()

    totalNeighbors = [pos]
    checkedNodes = []

    nodesChecked = 0

    while not allValues(checkedNodes, totalNeighbors):
        
        current = random.choice(totalNeighbors)
        while current in checkedNodes:
            current = random.choice(totalNeighbors)

        checkedNodes.append(current)

        neighbors = getNeighbors(current, walls, grid)
        for neighbor in neighbors:
            if neighbor not in checkedNodes:
                if neighbor not in totalNeighbors:
                    totalNeighbors.append(neighbor)
                    nodesChecked += 1
                    
                    t.goto(neighbor); t.dot(10)
                    # t.write('')  # Hacky Updating Screen
        
        if len(totalNeighbors) - 1 >= 0.75 * grid.length():
            t.write('')
            print("MORE THAN 75")
            t.clear()
            return True

    t.write('')
    print("NOT MORE")
    return len(totalNeighbors) - 1


def allValues(list1: list, list2: list):
    amountSame = 0
    for val in list1:
        if val in list2:
            amountSame += 1
    if amountSame == len(list2): return True
    return False
