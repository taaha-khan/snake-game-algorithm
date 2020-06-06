# Importing Important Imports
import turtle, math
import random, time

# File Imports
from grid import Grid
from snake import Snake
from HamiltonianCycle import HamiltonianCycle

# Scaling Sizes
scl  = 40   # Scale
rows = 20   # Height
cols = 30   # Width

# Screen Sizes
width = cols * scl
height = rows * scl
sclh = scl / 2

# Main Variables
speed = 1; run = 0
showingPath = False
path = False
start = time.time()

# Main Screen Setup
wn = turtle.Screen()
wn.setup(width + 50, height + 50)
wn.title('Snake Game Algorithm')
wn.bgcolor('#141414')
wn.tracer(0)

# Registering Scaled Square Shape
wn.register_shape('scaled-square', ((-sclh+2, sclh-2), (sclh-2, sclh-2), (sclh-2, -sclh+2), (-sclh+2, -sclh+2)))

# Generating Arena Grid Map
grid = Grid(cols, rows, scl)
cells = grid.createGrid()
grid.drawBorder('red')

# Generating Hamiltonian Cycle
hc = HamiltonianCycle(grid)
hCycle = hc.generateHamiltonianCycle()

# Creating Main Snake
snake = Snake(grid, hCycle)

# Speed Functions
def speedUp():
    global speed
    speed = 10
def slowDown():
    global speed
    speed = 1

# Showing Predicted Path Function
def showPath():
    global showingPath
    showingPath = not showingPath
    show.clear()

# Manual Gameplay Keybindings
def manualGameplay():
    wn.listen()
    wn.onkey(snake.up, 'Up')
    wn.onkey(snake.down, 'Down')
    wn.onkey(snake.left, 'Left')
    wn.onkey(snake.right, 'Right')
    time.sleep(0.05)

# Framerate Calculator
def frameRate():
    global run, start
    end = time.time()
    if end - start >= 1:
        print(f"FPS: {run}")
        run = 0
        start = time.time()
 
# Main Keybindings
wn.listen()
wn.onkeypress(speedUp, 'space')
wn.onkeyrelease(slowDown, 'space')
wn.onkey(showPath, 'p')

# Showing predicted path pen
show = turtle.Turtle()
show.pu(); show.ht()
show.color('blue'); show.width(3)

# Main Run Loop
while True:

    # Updating Screen
    wn.update()

    # Speed loop
    for play in range(speed):

        # Frame Count
        run += 1

        # Algorithms
        # path = snake.getPathFromAstar()
        path = snake.shortcutHamilton()

        # Showing predicted path
        if showingPath and path:
            show.clear()
            show.pu(); show.goto(path[0]); show.pd()
            for node in path:
                show.goto(node)

        # Updating Snake
        snake.run()

        # Manual Game Ending
        if snake.dead:
            snake = Snake(grid, path)

        # Updating Score in Title
        wn.title(f'Snake Game Algorithm  -  Score: {snake.drawnLength}')

        # Runtime Functions
        # manualGameplay()
        # frameRate()

# Ending Program
wn.mainloop()
