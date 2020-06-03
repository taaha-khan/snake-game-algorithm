import random, turtle, math
from grid import Grid

class HamiltonianCycle:

    """
    A Hamiltonian Cycle Generation algorithm using a Prim MST
    tree as a maze and traversing it to generate a cycle that
    passes through every point once

    - self.generateSpanningTree() -- Makes MST Prim Tree
    - self.traversePath() -- Runs through the maze turning left
    - self.generateHamiltonianCycle() -- Compiles run functions and returns cycle
    """

    def __init__(self, grid: Grid):
        
        # Model Variables
        self.grid = grid
        self.scl = grid.scl
        self.coordinates = Grid(grid.cols // 2, grid.rows // 2, grid.scl * 2)

        # MST Prim Variables
        self.forest = []
        self.walls = []
        self.edges = []

        # Maze Traverse
        self.cycle = []
    
    # MST Prim
    def generateSpanningTree(self):

        self.forest = []
        self.walls = []
        self.edges = []
        
        position = self.coordinates.randomPos()
        self.forest.append(position)

        while len(self.forest) < self.coordinates.length():

            position, adjacent = self.getRandomPrimNode()
            direction = random.choice(adjacent)

            edge = Edge(position, direction, self.scl)
            edge.getWallsBetweenNodes()

            for wall in edge.walls:
                self.walls.append(wall)

            self.forest.append(direction)
            self.edges.append(edge)
    

    # Traversing MST Prim Maze
    def traversePath(self):

        self.cycle = []
        runner = Runner(self.grid.randomPos(), self.walls, self.grid.cells, self.scl)
        
        while len(runner.traveled) < self.grid.length():

            up = [0, 1]; down = [0, -1]
            right = [1, 0]; left = [-1, 0]

            directions = [left, up, right, down]

            current = runner.strDirections.index(runner.dir)  # Straight
            nextOne = int(current) + 1  # Going Left
            if nextOne >= len(directions):
                nextOne = 0  # Wrapping Around
            prev = int(current) - 1  # Going Right
            
            if runner.canGo(directions[prev]):
                runner.directions[prev]()  # Left
            elif runner.canGo(directions[current]):
                runner.directions[current]() # Straight
            elif runner.canGo(directions[nextOne]):
                runner.directions[nextOne]()  # Right

            runner.traveled.append(runner.pos())
            self.cycle.append(runner.pos())

    # Compiling Hamiltonian Generation Algorithms
    def generateHamiltonianCycle(self):
        
        # Checking if an hCycle exists
        if self.grid.cols % 2 != 0 or self.grid.rows % 2 != 0:
            return None
        
        # Generating Hamiltonian Cycle
        self.generateSpanningTree()
        self.traversePath()

        # Making sure that hCycle has all nodes
        while True:
            complete = True
            if dist(self.cycle[1], self.cycle[-1]) > self.scl * 2:
                complete = False
            else:
                for cell in self.grid.cells:
                    if cell not in self.cycle:
                        complete = False
                        break
            if not complete:
                # Resetting the cycle until all nodes are in it
                self.generateSpanningTree()
                self.traversePath()
            elif complete:
                return self.cycle
    
    # Showing HCycle
    def show(self, animating = False, cycle = True, prim = True):
        self.pen = turtle.Turtle()
        self.pen.pu(); self.pen.ht()
        self.pen.goto(self.cycle[0])
        self.pen.color('red')
        self.pen.width(2)
        self.pen.pd()

        if prim:
            for edge in self.edges:
                edge.show(animating)
        
        if cycle:
            index = 0
            for pos in self.cycle:
                self.pen.color('red')
                self.pen.goto(pos)
                if animating:
                    self.pen.color('white')
                    self.pen.write(str(index), align='center', font=('Arial', 6, "bold"))  
                    index += 1
    
    # Hiding HCycle
    def clear(self):
        if self.pen: self.pen.clear()
        for edge in self.edges:
            edge.clearPen()
        
    # MST Prim Helper Function
    def getRandomPrimNode(self):

        random.shuffle(self.forest)

        for pos in self.forest:

            adjacent = []
            above = (pos[0], pos[1] + self.coordinates.scl)
            below = (pos[0], pos[1] - self.coordinates.scl)
            onright = (pos[0] + self.coordinates.scl, pos[1])
            onleft = (pos[0] - self.coordinates.scl, pos[1])

            neighbors = [above, below, onright, onleft]

            for val in neighbors:
                if val not in self.forest:
                    if val in self.coordinates.cells: 
                        adjacent.append(val)
            
            if len(adjacent) > 0:
                return pos, adjacent       

# Edge Class for MST Prim
class Edge:
    def __init__(self, node1: tuple, node2: tuple, scl: int):
        self.node1 = node1
        self.node2 = node2
        self.scl = scl
        self.sclh = scl / 2
        self.sclm = scl * 1.5
        self.walls = []
        self.pen = False
        self.directionToNode1 = [0, 0]
        self.directionToNode2 = [0, 0]


    def show(self, animating = False):
        self.pen = turtle.Turtle()
        self.pen.pu(); self.pen.ht()
        self.pen.color('blue')
        self.pen.goto(self.node1)
        self.pen.pendown()
        self.pen.goto(self.node2)
        self.pen.penup()
        for wall in self.walls:
            self.pen.goto(wall)
            self.pen.dot(5)
            if animating:
                self.pen.write('')
    
    def clearPen(self):
        if self.pen: self.pen.clear()
    
    # Getting Maze walls for Prim
    def getWallsBetweenNodes(self):

        xoff, yoff = self.getDirectionBetweenNodes()
        differences = [self.sclh, self.sclm]

        for wall in range(len(differences)):
            pos = list(self.node1)

            pos[0] += xoff * differences[wall]
            pos[1] += yoff * differences[wall]

            self.walls.append(tuple(pos))
        
        return self.walls

    # MST Edge Direction    
    def getDirectionBetweenNodes(self):

        xoff = self.node2[0] - self.node1[0]
        yoff = self.node2[1] - self.node1[1]

        if xoff != 0: xoff /= abs(xoff)
        elif yoff != 0: yoff /= abs(yoff)

        self.directionToNode2 = [xoff, yoff]
        self.directionToNode1 = [yoff, xoff]
        return self.directionToNode2


# Object to traverse the Prim MST Maze
class Runner:
    def __init__(self, pos: tuple, maze: list, grid: Grid, scl: int):

        # Position Variables
        self.x = pos[0]
        self.y = pos[1]
        self.dir = 'right'
        self.strDirections = ['left', 'up', 'right', 'down']
        self.directions = [self.left, self.up, self.right, self.down]
        
        # Scaling and Sizing Variables
        self.scl = scl
        self.sclh = scl / 2
        self.sclm = scl * 1.5

        # Environment Variables
        self.grid = grid
        self.maze = maze
        self.traveled = []
    

    def pos(self):
        return (self.x, self.y)

    def canGo(self, direction: list):
        scaled = direction[:]
        direction[0] *= self.scl; direction[1] *= self.scl
        if (self.x + direction[0], self.y + direction[1]) in self.grid:
            if (self.x + direction[0], self.y + direction[1]) not in self.traveled:
                if (self.x + scaled[0] * self.sclh, self.y + scaled[1] * self.sclh) not in self.maze:
                    return True
        return False

    # Movement Functions
    def up(self):
        self.y += self.scl
        self.dir = 'up'
    def down(self):
        self.y -= self.scl
        self.dir = 'down'
    def right(self):
        self.x += self.scl
        self.dir = 'right'
    def left(self):
        self.x -= self.scl
        self.dir = 'left'


def dist(pos1: tuple or list, pos2: tuple or list):
    x1, y1 = pos1; x2, y2 = pos2
    dist = abs(math.sqrt((x2 - x1)**2 + (y2 - y1)**2))
    return dist


    