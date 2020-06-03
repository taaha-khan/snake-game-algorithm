# Importing Important Imports
import turtle, math
import random, time

# File Imports
from grid import Grid
from snake import Snake
from HamiltonianCycle import HamiltonianCycle

# Screen Sizes
scl  = 30   # Scale
rows = 20   # Height
cols = 30   # Width

width = cols * scl
height = rows * scl
sclh = scl / 2
speed = 1
run = 0

# Main Screen Setup
wn = turtle.Screen()
wn.setup(width + 50, height + 50)
wn.title('Snake Game Algorithm')
wn.bgcolor('#141414')
wn.tracer(0)

wn.register_shape('scaled-square', ((-sclh+2, sclh-2), (sclh-2, sclh-2), (sclh-2, -sclh+2), (-sclh+2, -sclh+2)))

# Generating Arena Grid Map
grid = Grid(cols, rows, scl)
cells = grid.createGrid()
grid.drawBorder('red')

# Generating Hamiltonian Cycle
hc = HamiltonianCycle(grid)
path = hc.generateHamiltonianCycle()

snake = Snake(grid, path)

start = time.time()

def speedUp():
    global speed
    speed = 10
def slowDown():
    global speed
    speed = 1

def manualGameplay():
    wn.listen()
    wn.onkey(snake.up, 'Up')
    wn.onkey(snake.down, 'Down')
    wn.onkey(snake.left, 'Left')
    wn.onkey(snake.right, 'Right')
    time.sleep(0.05)

def frameRate():
    global run, start
    end = time.time()
    if end - start >= 1:
        print(f"FPS: {run}")
        run = 0
        start = time.time()
 

wn.listen()
wn.onkeypress(speedUp, 'space')
wn.onkeyrelease(slowDown, 'space')



while True:

    wn.update()

    for s in range(speed):

        run += 1

        # snake.getPathFromAstar()
        snake.shortcutHamilton()

        snake.run()

        if snake.dead:
            snake = Snake(grid, path)

        wn.title(f'Snake Game Algorithm  -  Score: {snake.drawnLength}')

        # manualGameplay()
        # frameRate()



wn.mainloop()
