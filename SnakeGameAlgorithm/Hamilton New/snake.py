# Imports
import turtle, random
from grid import Grid
from astar import Astar

# Main Snake Object
class Snake:

    # Initializing Snake
    def __init__(self, grid: Grid):

        # Variables
        self.body = []
        self.body_positions = []
        self.dead = False
        self.won = False
        self.speed = grid.scl

        # Environment Variables
        self.grid = grid
        self.cycle = grid.hCycle
        self.cyclePath = None

        # A* Variables
        self.getNextAstarPath = False
        self.astarPath = None
        self.gettingAstarPath = False

        # Internal Measurements
        self.frame = 0
        self.gainFromFood = 4

        # Growth Measurements
        self.growthLength = self.gainFromFood
        self.drawnLength = 0

        # Snake Head
        self.directions = ['up', 'down', 'left', 'right']
        self.head = turtle.Turtle()
        self.head.pu()
        self.head.shape('scaled-square')
        self.color = '#009600'
        self.head.color(self.color)
        self.head.width(self.speed - (self.grid.bord * 2) + 1)
        self.head.origin = self.grid.center()
        self.head.goto(self.head.origin)
        self.head.dir = 'right'

        # Snake Food
        self.food = turtle.Turtle()
        self.food.pu()
        self.food.shape('scaled-square')
        self.food.color('red')
        self.setFoodPos()
    
    # Snake Movement
    def up(self):
        if self.head.dir != 'down':
            self.head.dir = 'up'
    def down(self):
        if self.head.dir != 'up':
            self.head.dir = 'down'
    def left(self):
        if self.head.dir != 'right':
            self.head.dir = 'left'
    def right(self):
        if self.head.dir != 'left':
            self.head.dir = 'right'

    # Moving Snake Head and Checking Food
    def update(self):

        # Snake Border
        self.head.clear()
        if len(self.body) > 0:
            self.head.pd()

        # Snake Directional Movement
        if self.head.dir == 'up':
            self.head.sety(self.head.ycor() + self.speed)
        elif self.head.dir == 'down':
            self.head.sety(self.head.ycor() - self.speed)
        elif self.head.dir == 'left':
            self.head.setx(self.head.xcor() - self.speed)
        elif self.head.dir == 'right':
            self.head.setx(self.head.xcor() + self.speed)
        
        # Checking Wall Hits
        if self.head.pos() not in self.grid.cells:
            self.die()
        
        # Getting all Snake Body Positions
        self.getBodyPositions()

        if len(self.body) >= self.grid.size - 2:
            self.won = True

        # Checking if Snake got to Food
        if self.head.pos() == self.food.pos():
            self.setFoodPos()
            self.growthLength += self.gainFromFood

            if self.gettingAstarPath:
                self.getNextAstarPath = True
            
        
        # Adding Body Segments from gain variable
        if self.growthLength > 0:
            if len(self.body) > 0:
                self.body[-1].pd()
            self.addSegment()
            self.growthLength -= 1
            self.drawnLength += 1
        
        # Snake internal clock
        self.frame += 1
    
    # Set Food Position to a Spot that the body is not on
    def setFoodPos(self):
        position = self.grid.randomPos()
        # Repeating until a viable spot is found
        while position in self.getBodyPositions() or position == self.head.pos():
            position = self.grid.randomPos()
        # Setting Food Position
        self.food.goto(position)
    
    # Moving Snake Body Segments
    def move(self):
        # Running through Snake Body Backwards
        for index in range(len(self.body)-1, 0, -1):
            self.body[index].clear()
            self.body[index].st()
            # Moving body segment
            x = self.body[index-1].xcor()
            y = self.body[index-1].ycor()
            self.body[index].goto(x,y)
            if index != len(self.body) - 1:
                self.body[index].pd()
        # Moving First body Segment
        if len(self.body) > 0:
            self.body[0].clear()
            self.body[0].st()
            # Moving to head positions
            x = self.head.xcor()
            y = self.head.ycor()
            self.body[0].goto(x,y)
            if len(self.body) > 1:
                self.body[0].pd()
    
    # Adding a Segment
    def addSegment(self):
        # Generating new segment
        new_segment = turtle.Turtle()
        new_segment.speed(0)
        new_segment.width(self.speed - (self.grid.bord * 2) + 1)
        new_segment.ht()
        new_segment.shape('scaled-square')
        new_segment.color(self.color)
        new_segment.pu()
        new_segment.goto(self.head.pos())
        # Adding the new segment to the body
        self.body.append(new_segment)

    # Checking if the head collides with any part of the tail  
    def checkCollisionWithBody(self):
        if self.head.pos() in self.body_positions:
            self.die()

    # Checking Collision with position in predicted walls
    def checkCollision(self, pos, walls):
        if pos in walls or pos not in self.grid.cells:
            return True
        return False
    
    # Getting All positions of snake body
    def getBodyPositions(self):
        positions = []
        for seg in self.body:
            positions.append(seg.pos())
        self.body_positions = positions
        return positions

    # Compiling all functions into one run function
    def run(self):
        # Only Move if the game is not won or lost
        if not self.won and not self.dead:
            self.move()   # Moving Body Segments
            self.update()   # Moving Head
            self.checkCollisionWithBody()  # Checking if Dead

    # Hiding Snake
    def hide(self):
        self.head.ht()
        self.head.clear()
        self.food.ht()
        for seg in self.body:
            seg.clear(); seg.ht()
    
    # Showing Snake
    def show(self):
        self.head.st(); self.food.st()
        for seg in self.body: seg.st()
    
    # Destroying Snake
    def die(self):
        self.dead = True
        self.hide()
        del self


    # ALGORITHMS ----------------------------------------------------------------------------------------------
    
    # Moving to a node
    def toward(self, pos):
        x, y = pos
        if x == self.head.xcor() and y > self.head.ycor(): self.up()
        elif x == self.head.xcor() and y < self.head.ycor(): self.down()
        elif x > self.head.xcor() and y == self.head.ycor(): self.right()
        elif x < self.head.xcor() and y == self.head.ycor(): self.left()

    # A* Compiling Algorithm
    def getPathFromAstar(self):
        self.gettingAstarPath = True
        if self.astarPath == None or self.getNextAstarPath:
            self.astarPath = Astar(self.head.pos(), self.food.pos(), self.getBodyPositions(), self.grid)
            self.getNextAstarPath = False
        try: self.toward(self.astarPath[self.astarPath.index(self.head.pos()) + 1])
        except: ValueError
        return self.astarPath

    # Path Distance from nodes
    def pathDistance(self, pos1, pos2):
        if pos1 < pos2:
            return pos2 - pos1 - 1
        return pos2 - pos1 - 1 + self.grid.size
    
    # Calculating Path From Head to food
    def getPathFromShortcutHamilton(self):

        layer = 0
        path = [self.getNextMoveFromShortcut(self.head.pos())]

        while path[-1] != self.food.pos():
            layer += 1
            nextNode = self.getNextMoveFromShortcut(path[-1], layer, path)
            path.append(nextNode)
    
        return path
    
    # Main Movement Function for Shortcut Algorithm
    def pathShortcutHamilton(self):
        self.cyclePath = self.getPathFromShortcutHamilton()
        self.toward(self.cyclePath[0])
        return self.cyclePath
    
    # Only Calculating One Block Ahead
    def shortcutHamilton(self):
        node = self.getNextMoveFromShortcut(self.head.pos())
        self.toward(node); return [node]

    def getNextMoveFromShortcut(self, pos, layer = 1, pathSoFar = []):

        # Predicting Body Movement with shortcut
        walls = self.getBodyPositions(); x, y = pos
        if len(walls) - layer > 0:
            for _ in range(layer):
                walls.remove(walls[-1])
        else: walls.clear()
        walls = [pos] + pathSoFar + walls

        # Getting Main Distances
        pathNumber = self.cycle.index(pos)
        distanceToFood = self.pathDistance(pathNumber, self.cycle.index(self.food.pos()))
        if len(self.body) > 0:
            distanceToTail = self.pathDistance(pathNumber, self.cycle.index(walls[-1]))
        else: distanceToTail = float('inf')

        # Calculating Available Cutting Amounts
        cuttingAmountAvailable = distanceToTail - self.drawnLength - self.gainFromFood - self.growthLength
        emptySquaresOnBoard = self.grid.size - self.drawnLength - self.growthLength - 1
        if self.drawnLength >= self.grid.size * 0.5:
            cuttingAmountAvailable = 0  # Disabling Shortcuts
        elif distanceToFood < distanceToTail:
            cuttingAmountAvailable -= (self.gainFromFood + self.growthLength)
            if (distanceToTail - distanceToFood) * 4 > emptySquaresOnBoard:
                cuttingAmountAvailable -= (self.gainFromFood + self.growthLength)

        # Normalizing Cutting Amounts
        cuttingAmountDesired = distanceToFood
        if cuttingAmountDesired < cuttingAmountAvailable:
            cuttingAmountAvailable = cuttingAmountDesired
        if cuttingAmountAvailable < 0:
            cuttingAmountAvailable = 0
        
        # Directions
        above = (x, y + self.speed)
        below = (x, y - self.speed)
        onleft = (x - self.speed, y)
        onright = (x + self.speed, y)

        # Checking if Direction is safe
        canGoRight = not self.checkCollision(onright, walls)
        canGoLeft = not self.checkCollision(onleft, walls)
        canGoUp = not self.checkCollision(above, walls)
        canGoDown = not self.checkCollision(below, walls)

        # Safety Lookup Table
        canGo = {
            above: canGoUp,
            below: canGoDown,
            onright: canGoRight,
            onleft: canGoLeft
        }

        # Main Comparison Items
        bestDir = ()
        bestDist = -1

        # Possible Directions
        goList = [above, below, onleft, onright]

        # Looking for optimal node to travel to
        for node in goList:
            if canGo[node]:
                dist = self.pathDistance(pathNumber, self.cycle.index(node))
                if dist <= cuttingAmountAvailable and dist > bestDist:
                    bestDir = node
                    bestDist = dist

        # Return Best Direction
        if bestDist >= 0:
            return bestDir
        
        # Should not reach here -------------------

        print(random.random())
        
        # Returning viable node
        for node in goList:
            if canGo[node]:
                return node
        return above