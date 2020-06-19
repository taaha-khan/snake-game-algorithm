"""
 __ __ __ __ __ __ __ __ __ __ __ __ __ __ __
|                                            |
|   © Taaha Khan 2020                        |
|   All Rights Reserved                      |
|   "Snake Game Algorithm" - V 7.1.0         |
|   This is a Snake Game playing algorithm   |
|   that generates a Hamiltonian Cycle       |
|   through a grid and uses shortcuts        |
|   to efficiently find a path to the food   |
|__ __ __ __ __ __ __ __ __ __ __ __ __ __ __|

"""

# Importing Important Imports
import turtle, math
import random, time

# File Imports
from grid import Grid
from snake import Snake
from cycle import HamiltonianCycle

# Scaling Sizes
scl  = 40   # Scale
rows = 20   # Height
cols = 30   # Width
bord = 5    # Fold

# Screen Sizes
width = cols * scl
height = rows * scl
sclh = scl / 2

# Main Variables
speed = 1; run = 0
showingPath = False
showingHCycle = False
play = False; path = []
start = time.time()

# Main Screen Setup
wn = turtle.Screen()
wn.setup(width + 50, height + 50)
wn.title('Snake Game Algorithm')
wn.bgcolor('#141414')
wn.tracer(0)

# Registering Scaled Square Shape
wn.register_shape('scaled-square', ((-sclh+bord, sclh-bord), (sclh-bord, sclh-bord), (sclh-bord, -sclh+bord), (-sclh+bord, -sclh+bord)))

# Generating Arena Grid Map
grid = Grid(cols, rows, scl)
cells = grid.createGrid()
grid.drawBorder('red')

# Generating Hamiltonian Cycle
hc = HamiltonianCycle(grid)
hCycle = hc.generateHamiltonianCycle()
grid.hCycle = hCycle
grid.bord = bord

# Creating Main Snake
snake = Snake(grid)

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

# Pause and Play
def pausePlay():
    global play
    play = not play

# Showing and Hiding HCycle
def showHCycle():
    global showingHCycle
    showingHCycle = not showingHCycle
    if showingHCycle:
        hc.show(False, True, False)
    else: hc.clear()

# Manual Gameplay Keybindings
def manualGameplay():
    clearKeybindings()
    wn.listen()
    wn.onkey(snake.up, 'Up')
    wn.onkey(snake.down, 'Down')
    wn.onkey(snake.left, 'Left')
    wn.onkey(snake.right, 'Right')
    time.sleep(0.05)

# Clearing multiple movements
def clearKeybindings():
    wn.onkey(None, 'Up')
    wn.onkey(None, 'Down')
    wn.onkey(None, 'Left')
    wn.onkey(None, 'Right')

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
wn.onkey(pausePlay, 's')
wn.onkey(showHCycle, 'h')
wn.onkey(frameRate, 'f')

# Showing predicted path pen
show = turtle.Turtle()
show.pu(); show.ht()
show.color('blue'); show.width(4)

# Main Run Loop
while True:

    # Updating Screen
    wn.update()

    # Showing predicted path
    if showingPath and path:
        show.clear()
        show.pu(); show.goto(path[0]); show.pd()
        for node in path:
            show.goto(node)
    
    # Pausing and Playing
    if play: continue

    # Speed loop
    for frame in range(speed):

        # Frame Count
        run += 1

        # Algorithms ------------------------

        # path = snake.getPathFromAstar()
        # path = snake.pathShortcutHamilton()
        path = snake.shortcutHamilton()

        # Updating Snake
        snake.run()

        # Manual Game Ending
        if snake.dead:
            snake = Snake(grid)

        # Updating Score in Title                     
        wn.title(f'Snake Game Algorithm  -  Score: {snake.drawnLength}')

        # Runtime Functions
        # manualGameplay()

# Ending Program
wn.mainloop()