# A* Pathfinding AI File

# Importing important imports
import turtle
import random
import time

# Speed Delays
delay = 0.07
aldelay = 0.02

# AI High Score: 96
score = 0
high_score = 0

# Initializing Screen
wn = turtle.Screen()
wn.bgcolor('light blue')
wn.tracer(0)
wn.title('Snake Game - A*')
wn.setup(width = 700, height = 700)

# To show projected A* Path
show_path = False

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
border.pu()

t = turtle.Turtle()
t.speed(0)
t.color('red')
t.ht(); t.pu()

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



# AI SNAKE PLAYING ALGORITHMS ------------------------------------------------------
algorithm_running = False

def astar(start, destination, segment_positions):
  
    # Initialization of main containers
    open_list = []
    closed_list = []
    parent = {}

    open_list.append(start)
    parent[str(start)] = None

    layer = {str(start):0}

    # Core Loop
    while len(open_list) > 0:

        # Finding closest item in [open_list] to destination
        least = 1000
        current = ()
        for item in open_list:
            if destination.distance(item) < least:
                least = destination.distance(item)
                current = item

        # Checking if destination has been found
        if current == destination.position():
            parent[str(destination.position())] = parent[str(current)]
            final_path = construct_path(destination.position(), parent)
            return final_path
        
        # Switching current to [closed_list]
        open_list.remove(current)
        closed_list.append(current)

        moved_walls = segment_positions[:]
        if len(moved_walls) - layer[str(current)] >= 0:
            for _ in range(layer[str(current)]):
                moved_walls.remove(moved_walls[-1])
        else: moved_walls = []
        
        # Finding neighbors of current and adding them to [open_list]
        neighboring = neighbors(current, moved_walls)
        for neighbor in neighboring:
            if neighbor not in closed_list:
                if neighbor not in open_list:
                    open_list.append(neighbor)
                    parent[str(neighbor)] = str(current)
                    layer[str(neighbor)] = layer[str(parent[str(neighbor)])] + 1

    return False  # No path found

def neighbors(node, walls):
    neighboring = []
    above = (node[0], node[1] + 20)
    below = (node[0], node[1] - 20)
    onright = (node[0] + 20, node[1])
    onleft = (node[0] - 20, node[1])
    wall_positions = walls[:]
    if above not in wall_positions and above[1] < 290: neighboring.append(above)
    if below not in wall_positions and below[1] > -290: neighboring.append(below)
    if onright not in wall_positions and onright[0] < 290: neighboring.append(onright)
    if onleft not in wall_positions and onleft[0] > -290: neighboring.append(onleft)
    return neighboring

def convert_tuple(input_str):
    str_list = []
    for i in range(len(input_str)): str_list.append(input_str[i])
    str_list.remove('('); str_list.remove(')')
    comma = str_list.index(',')
    str_list.remove(',')
    first = str_list[:comma]; last = str_list[comma:]
    first_number = ''; last_number = ''
    for i in range(len(first)): first_number += first[i]
    for i in range(len(last)): last_number += last[i]
    final = (float(first_number), float(last_number))
    return final

def construct_path(node, dict):
    path = []
    path.append(node)
    while dict[str(node)] is not None:
        node = dict[str(node)]
        path.append(convert_tuple(node))
    path.reverse()
    path.remove(path[0])
    return path

def runAstar(path):
    global algorithm_running, i, segment_positions
    algorithm_running = True

    if path != False:
        head.goto(path[i])
        if i + 1 <= len(path) - 1: i += 1
        else: i = 0
    else: 
        wn.exitonclick()
        wn.mainloop()
        
        
# ----------------------------------------------------------------------------------

# Keyboard Bindings (For manual gameplay)
wn.listen()
wn.onkey(up, 'Up')
wn.onkey(down, 'Down')
wn.onkey(left, 'Left')
wn.onkey(right, 'Right')


# Dark Theme <Optional>
dark_background = True
if dark_background:
    wn.bgcolor('black')
    head.color('green')
    pen.color('red')

segment_positions = []
path = astar(head.pos(), food, segment_positions)


i = 0

# Main Game Loop
while True:
    wn.update()

    # Checking Segment positions
    segment_positions = []
    for seg in segments: segment_positions.append(seg.pos())
    
    
    # AI Algorithms
    if path != False:
        runAstar(path)
   

    # If food gets eaten
    if head.pos() == food.pos():

        # Adds a new segment to snake
        new_segment = turtle.Turtle()
        new_segment.speed(0)
        new_segment.width(19)
        new_segment.shape('small square')
        new_segment.color('green')
        new_segment.pu()
        segment_positions.append(new_segment.pos())
        segments.append(new_segment)
        
        # Replacing food to spot that the snake is not on
        seg_pos = segment_positions[:]
        seg_pos.append(head.pos())
        new_position = random.choice(coordinates)
        while new_position in seg_pos:
            new_position = random.choice(coordinates)
        food.goto(new_position)

        # Score and delays
        delay -= 0.0005
        aldelay -= 0.0005

        score+=1
        if score > high_score: high_score = score
        pen.clear()
        pen.write('Score: '+str(score)+'  High Score: '+str(high_score), align='center', font=('Courier', 24, "bold")) 

        path = []
        path = astar(head.pos(), food, segment_positions)
        if path == False:
            runAstar(path)
        if show_path:
            t.clear()
            t.pu()
            t.width(4)
            t.goto(path[0])
            t.pd()
            for x in path:
                t.goto(x)
        
        i = 0
        

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
    if head.pos() in segment_positions or (head.xcor() >= 280 or head.xcor() <= -280 or head.ycor() >= 280 or head.ycor() <= -280) or path == False:

        # Scores and delays
        score = 0
        pen.clear()
        pen.write('Score: '+str(score)+'  High Score: '+str(high_score), align='center', font=('Courier', 24, "bold"))

        delay = 0.09
        aldelay = 0.02

        # Resetting positions
        time.sleep(1)
        head.pu()
        head.goto(-10,-10)
        head.direction = 'stop'

        for segment in segments:
            segment.clear()
            segment.pu()
            segment.goto(1000,1000)
            segments = []

        path = []
        path = astar(head.pos(), food, segment_positions)
        i = 0
        


    # Delays for canceling out lag
    if algorithm_running == False: time.sleep(delay)

input('Final End Script: ')
