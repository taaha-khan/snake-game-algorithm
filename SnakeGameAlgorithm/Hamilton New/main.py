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

# Main Run Class
class Game:

    # Initializing Variables
    def __init__(self):

        # Screen Sizes
        self.scl = 40   # Scale
        self.rows = 20  # Width
        self.cols = 30  # Height
        self.bord = 5   # Fold

        # Screen Sizes
        self.width = self.cols * self.scl
        self.height = self.rows * self.scl 
        self.sclh = self.scl / 2

        # Initializing Start Variables
        self.playSpeed = 1
        self.frame = 0
        self.runFrame = 0
        self.startTime = time.time()

        # Showing Screen Variables
        self.gettingFrameRate = False
        self.showingPath = False
        self.showingHCycle = False
        self.play = False

        # Calculated Algorithm Path
        self.path = []

        # Main Screen Setup
        self.window = turtle.Screen()
        self.window.setup(self.width + 50, self.height + 50)
        self.window.title("Snake Game Algorithme")
        self.window.bgcolor('#141414')
        self.window.tracer(0)

        # Registering Scaled Square Shape
        self.window.register_shape('scaled-square', (
            (-self.sclh + self.bord, self.sclh-self.bord), 
            (self.sclh - self.bord, self.sclh - self.bord), 
            (self.sclh - self.bord, -self.sclh + self.bord), 
            (-self.sclh + self.bord, -self.sclh + self.bord))
        )

        # Generating Arena Grid Map
        self.grid = Grid(self.cols, self.rows, self.scl)
        self.cells = self.grid.createGrid()
        self.grid.drawBorder('red')

        # Generating Hamiltonian Cycle
        self.hc = HamiltonianCycle(self.grid)
        self.hCycle = self.hc.generateHamiltonianCycle()
        self.grid.hCycle = self.hCycle
        self.grid.bord = self.bord

        # Creating Main Snake Object
        self.snake = Snake(self.grid)

        # Showing Algorithm Path Pen
        self.show = turtle.Turtle()
        self.show.pu(); self.show.ht()
        self.show.color('blue')
        self.show.width(4)

    # Speeding Up Run
    def speedUp(self):
        self.playSpeed = 10
    
    # Slowing Down Run
    def slowDown(self):
        self.playSpeed = 1
    
    # Showing Predicted Path
    def showPath(self):
        self.showingPath = not self.showingPath
        self.show.clear()
    
    # Pausing and Playing
    def pausePlay(self):
        self.play = not self.play

    # Showing and Hiding HamiltonianCycle
    def showHCycle(self):
        self.showingHCycle = not self.showingHCycle
        if self.showingHCycle:
            self.hc.show(False, True, False) 
        else: self.hc.clear()
    
    # Manual Gameplay Keybindings
    def manualGameplay(self):
        self.clearManualMovement()
        self.window.listen()
        self.window.onkey(self.snake.up, "Up")
        self.window.onkey(self.snake.down, "Down")
        self.window.onkey(self.snake.left, "Left")
        self.window.onkey(self.snake.right, "Right")
        time.sleep(0.05)

    # Clearing mutiple movements per Frame
    def clearManualMovement(self):
        self.window.onkey(None, "Up")
        self.window.onkey(None, "Down")
        self.window.onkey(None, "Left")
        self.window.onkey(None, "Right")
    
    # Getting Frame Rate
    def frameRate(self):
        self.gettingFrameRate = not self.gettingFrameRate
    
    # Main Simulation Keybindings
    def setMainKeybindings(self):
        self.window.listen()
        self.window.onkeypress(self.speedUp, 'space')
        self.window.onkeyrelease(self.slowDown, 'space')
        self.window.onkey(self.showPath, 'p')
        self.window.onkey(self.pausePlay, 's')
        self.window.onkey(self.frameRate, 'f')
        self.window.onkey(self.showHCycle, 'h')

    # Main Compiling Run Function
    def run(self):

        # Setting the Keybindings
        self.setMainKeybindings()

        # Main Run Loop
        while True:

            # Updating Screen
            self.window.update()

            # Showing predicted Path
            if self.showingPath and self.path:
                self.show.clear()
                self.show.pu()
                self.show.goto(self.path[0])
                self.show.pd()
                for node in self.path:
                    self.show.goto(node)
            
            # Pausing and Playing
            if self.play: continue

            # Speed loop
            for _ in range(self.playSpeed):
                
                # Frame Counting
                self.frame += 1
                self.runFrame += 1

                # Frame Rate Calculator
                self.currentTime = time.time()
                if self.currentTime - self.startTime >= 1:
                    if self.gettingFrameRate:
                        print(f'FPS: {self.runFrame}')
                    self.runFrame = 0
                    self.startTime = time.time()
                    self.gettingFrameRate = False

                # Algorithms

                # self.path = self.snake.getPathFromAstar()
                # self.path = self.snake.pathShortcutHamilton()
                self.path = self.snake.shortcutHamilton()

                # Updating and Showing Snake
                self.snake.run()

                # Resetting Snake
                if self.snake.dead:
                    self.snake = Snake(self.grid)
                
                # Updating Score in Title
                self.window.title(f"Snake Game Algorithm  -  Score: {self.snake.drawnLength}")

                # Manually Playing
                # self.manualGameplay()
        
        # Ending Program
        self.window.mainloop()

# Main Function
def main():
    game = Game()
    game.run()

# Executing Program
if __name__ == '__main__':
    main()
