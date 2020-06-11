import random, turtle

# Grid Object
class Grid:

    # Main Variables for Grid
    def __init__(self, cols: int, rows: int, scl: int):
        self.cols = cols
        self.rows = rows
        self.cells = []
        self.size = cols * rows
        self.width = cols * scl
        self.height = rows * scl
        self.scl = scl
        self.cellPositions = {}
    
    # Drawing Grid Border
    def drawBorder(self, color: str):
        self.pen = turtle.Turtle()
        self.pen.pu(); self.pen.ht()
        self.pen.color(color)
        self.pen.goto(-self.width / 2 - 2, -self.height / 2 - 2)
        self.pen.width(3); self.pen.pd()
        self.pen.goto(self.width / 2 + 2, -self.height / 2 - 2)
        self.pen.goto(self.width / 2 + 2, self.height / 2 + 2)
        self.pen.goto(-self.width / 2 - 2, self.height / 2 + 2)
        self.pen.goto(-self.width / 2 - 2, -self.height / 2 - 2)
        self.pen.pu()
    
    # Showing grid cells
    def show(self, color: str):
        if len(self.cells) == 0:
            self.createGrid()
        self.pen = turtle.Turtle()
        self.pen.pu(); self.pen.ht()
        self.pen.color(color)
        for cell in self.cells:
            self.pen.goto(cell)
            self.pen.dot(10)

    # Generating grid from top right to bottom left
    def createGrid(self):
        self.cells = []
        for y in range(self.rows):
            for x in range(self.cols):
                sx = (x - self.cols / 2) * self.scl + (self.scl / 2)
                sy = -((y - self.rows / 2) * self.scl + (self.scl / 2))
                position = (sx, sy)
                self.cells.append(position)
                self.cellPositions[str(position)] = self.cells[-1]
        return self.cells
    
    # Getting Center node from grid
    def center(self):
        if len(self.cells) == 0:
            self.createGrid()
        index = len(self.cells) // 2
        return self.cells[index + (self.cols // 2)]

    # Getting random position in grid
    def randomPos(self):
        if len(self.cells) == 0:
            self.createGrid()
        return random.choice(self.cells)
    
    # Getting length of grid
    def length(self):
        return len(self.cells)

# Mapping values from values
def Map(value: float, leftMin: float, leftMax: float, rightMin: float, rightMax: float):
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin
    valueScaled = float(value - leftMin) / float(leftSpan)
    return rightMin + (valueScaled * rightSpan)
