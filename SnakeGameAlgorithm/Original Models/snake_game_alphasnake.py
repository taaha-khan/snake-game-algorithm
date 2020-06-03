# AlphaSnake() Pathfinding AI File

# Importing important imports
import turtle
import random
import time

# Speed Delays
delay = 0.05
aldelay = 0.02

# AI High Score: 96
score = 0
high_score = 0

# Initializing Screen
wn = turtle.Screen()
wn.bgcolor('light blue')
wn.tracer(0)
wn.title('Snake Game - AlphaSnake()')
wn.setup(width = 700, height = 700)


# Screen Registering Shapes
wn.register_shape('small square', ((-9,9),(9,9),(9,-9),(-9,-9)))


# Possible Nodes in Array Grid
xs = []
ys = []
for i in range(-280,279):
    if i % 10 == 0:
        xs.append(i)
        ys.append(i)
coordinates = []
xcount = 0
ycount = 0
for x in range(len(xs)):
    for y in range(len(ys)):
        if xcount % 2 == 1 and ycount % 2 == 1:
            coordinates.append((xs[x], ys[y]))
        ycount += 1
    xcount += 1
possible_spots = []


# Drawing borders
border = turtle.Turtle()
border.speed(0)
border.ht()
border.pu()
border.width(2)
border.goto(-280,-280)
border.color('red')
border.pd()
for wall in range(4):
    border.forward(560)
    border.left(90)

# Initializing Snake player
head = turtle.Turtle()
head.speed(0)
head.width(18)
head.shape('square')
head.color('black')
head.pu()
head.goto(-10,-10)
head.direction = 'stop'

# Initializing Food
food = turtle.Turtle()
food.speed(0)
food.shape('circle')
food.color('red')
food.pu()
food.goto(-10,110)

segments = []

# Initializing Score
pen = turtle.Turtle()
pen.speed(0)
pen.color('black')
pen.pu()
pen.ht()
pen.goto(0,300)
pen.write('Score: 0  High Score: 0', align='center', font=('Courier', 24, "bold"))

# Player continuous movement
def move():
    if head.direction == 'up':
        head.sety(head.ycor() + 20)
    elif head.direction == 'down':
        head.sety(head.ycor() - 20)
    elif head.direction == 'right':
        head.setx(head.xcor() + 20)
    elif head.direction == 'left':
        head.setx(head.xcor() - 20)

# Player directional movement
def up():
    if head.direction != 'down':
        head.direction = 'up'
def down():
    if head.direction != 'up':
        head.direction = 'down'
def left():
    if head.direction != 'right':
        head.direction = 'left'
def right():
    if head.direction != 'left':
        head.direction = 'right'

"""
# Food chasing secondary game (Inverse Snake)
def fup():
  food.sety(food.ycor() + 20)
def fdown():
  if food.ycor() - 20 > -280:
    food.sety(food.ycor() - 20)
def fleft():
  if food.xcor() - 20 > -280:
    food.setx(food.xcor() - 20)
def fright():
  if food.xcor() + 20 < 280:
    food.setx(food.xcor() + 20)
"""


# AI SNAKE PLAYING ALGORITHMS ------------------------------------------------------
algorithm_running = False

def AlphaSnake(body_pos): # Pathfinding Algorithm

    # Resetting to algorithm specifications
    global algorithm_running
    algorithm_running = True

    # Checking 2 blocks ahead of projected move
    def safe(tuple, body_pos):
        onright = (tuple[0] + 20, tuple[1])
        onleft = (tuple[0] - 20, tuple[1])
        above = (tuple[0], tuple[1] + 20)
        below = (tuple[0], tuple[1] - 20)
        if (onright in body_pos or onright == head.pos() or onright[0] > 280) and (onleft in body_pos or onleft == head.pos() or onleft[0] < -280) and (above in body_pos or above == head.pos() or above[1] > 280) and (below in body_pos or below == head.pos() or below[1] < -280): return False
        return True

    # Finding all possible movement squares
    move_list = []
    if (head.xcor() + 20, head.ycor()) not in body_pos and head.xcor() + 20 < 280 and safe((head.xcor() + 20, head.ycor()), body_pos): move_list.append('right')
    if (head.xcor() - 20, head.ycor()) not in body_pos and head.xcor() - 20 > -280 and safe((head.xcor() - 20, head.ycor()), body_pos): move_list.append('left')
    if (head.xcor(), head.ycor() + 20) not in body_pos and head.ycor() + 20 < 280 and safe((head.xcor(), head.ycor() + 20), body_pos) : move_list.append('up')
    if (head.xcor(), head.ycor() - 20) not in body_pos and head.ycor() - 20 > -280 and safe((head.xcor(), head.ycor() - 20), body_pos): move_list.append('down')
    
    # Initializing Comparison items
    least = 1000
    direction = ''

    # Finds possible moves -> Shortest Distance -> Fastest Direction
    if 'right' in move_list:
        if food.distance((head.xcor() + 20,head.ycor())) < least:
            least = food.distance((head.xcor() + 20,head.ycor()))
            direction = 'right'
    if 'left' in move_list:
        if food.distance((head.xcor() - 20,head.ycor())) < least:
            least = food.distance((head.xcor() - 20,head.ycor()))
            direction = 'left'
    if 'up' in move_list:
        if food.distance((head.xcor(),head.ycor() + 20)) < least:
            least = food.distance((head.xcor(),head.ycor() + 20))
            direction = 'up'
    if 'down' in move_list:
        if food.distance((head.xcor(),head.ycor() - 20)) < least:
            least = food.distance((head.xcor(),head.ycor() - 20))
            direction = 'down'
    
    # Traveling to best calculated direction
    if direction == 'down': down()
    elif direction == 'up': up()
    elif direction == 'right': right()
    elif direction == 'left': left()

# ----------------------------------------------------------------------------------

# Keyboard Bindings (For manual gameplay)

wn.listen()

wn.onkey(up, 'w')
wn.onkey(down, 's')
wn.onkey(left, 'a')
wn.onkey(right, 'd')

wn.onkey(up, 'Up')
wn.onkey(down, 'Down')
wn.onkey(left, 'Left')
wn.onkey(right, 'Right')

# For secondary Inverse Snake game
# wn.onkey(fup, 'up')
# wn.onkey(fdown, 'down')
# wn.onkey(fleft, 'left')
# wn.onkey(fright, 'right')


# Dark Background <Optional>
dark_background = True
if dark_background:
    wn.bgcolor('black')
    head.color('green')
    pen.color('red')



# Main Game Loop
while True:

    wn.update()

    # Checking Segment positions
    segment_positions = []
    for seg in segments: segment_positions.append(seg.pos())
    
    
    # AI Algorithms
    AlphaSnake(segment_positions)


    # If food gets eaten
    if head.distance(food) < 20:

        # Adds a new segment to snake
        new_segment = turtle.Turtle()
        new_segment.speed(0)
        new_segment.width(19)
        new_segment.shape('small square')
        new_segment.color('green')
        new_segment.pu()
        segments.append(new_segment)
        
        # Replacing food to spot that the snake is not on
        seg_pos = segment_positions[:]
        seg_pos.append(head.pos())
        seg_pos.append(segments[len(segments) - 1].pos())
        new_position = random.choice(coordinates)
        while new_position in seg_pos:
            new_position = random.choice(coordinates)
        food.goto(new_position)
        

        # Score and delays
        delay -= 0.0001
        aldelay -= 0.0001

        score+=1
        if score > high_score: high_score = score
        pen.clear()
        pen.write('Score: '+str(score)+'  High Score: '+str(high_score), align='center', font=('Courier', 24, "bold"))  


    # Moving Body Segments
    for index in range(len(segments)-1, 0, -1):
        segments[index].clear()
        x = segments[index-1].xcor()
        y = segments[index-1].ycor()
        segments[index].goto(x,y)
        if index != len(segments) - 1:
            segments[index].pd()
    if len(segments) > 0:
        segments[0].clear()
        x = head.xcor()
        y = head.ycor()
        segments[0].goto(x,y)
        if len(segments) != 1:
            segments[0].pd()
    

    # Continuous movement
    move()
    
    
    # Checking if head hits body or walls (Dies)
    if head.pos() in segment_positions or head.pos() not in coordinates:

        # Scores and delays
        score = 0
        pen.clear()
        pen.write('Score: '+str(score)+'  High Score: '+str(high_score), align='center', font=('Courier', 24, "bold"))

        delay = 0.05
        aldelay = 0.02

        # Resetting positions
        time.sleep(0.5)
        head.pu()
        head.goto(-10,-10)
        head.direction = 'stop'

        for segment in segments:
            segment.clear()
            segment.pu()
            segment.ht()
            segment.goto(1000,1000)
            segments = []


    # Delays for canceling out lag
    if algorithm_running == False: time.sleep(delay)

wn.mainloop()