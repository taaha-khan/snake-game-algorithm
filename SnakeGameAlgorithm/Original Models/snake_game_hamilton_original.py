# Hamlitonian Cycle and Shortcut AI File

# Importing important imports
import turtle
import random
import time

# Speed Delays
delay = 0.05
aldelay = 0.02

xlength = 300
ylength = 300

# AI High Score: 786
score = 0
high_score = 786

# Initializing Screen
wn = turtle.Screen()
wn.bgcolor('light blue')
wn.tracer(0)
wn.title("Snake Game - Hamilton")
wn.setup(width = 700, height = 700)

# Screen Registering Shapes
wn.register_shape('small square', ((-9,9),(9,9),(9,-9),(-9,-9)))

# Possible Nodes in Array Grid
xs = []
ys = []
for i in range(-xlength,ylength - 1):
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


# Reads Gridlines into a list
mx = []
my = []
for coor in range(-xlength + 20, ylength - 10):
    if coor % 10 == 0:
        mx.append(coor)
        my.append(coor)
ycount = 0
xcount = 0
grid_coordinates = []
for x in mx:
    for y in my:
        if ycount % 4 == 0 and xcount % 4 == 0:
            grid_coordinates.append((x,y))
        ycount += 1
    xcount += 1

# Drawing borders
border = turtle.Turtle()
border.speed(0)
border.ht()
border.pu()
border.width(4)
border.goto(-xlength,-ylength)
border.color('red')
border.pd()
for wall in range(4):
    border.forward(xlength * 2)
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


# Dark Background <Optional>
dark_background = True
if dark_background:
    wn.bgcolor('black')
    head.color('green')
    head.shape('square')
    food.shape('circle')
    pen.color('red')


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



algorithm_running = False

# GENERATING HAMITONIAN CYCLE --------------------------------------------------------------------------

def tup():
    t.direction = 'up'
    if t.ycor() + 20 > xlength: t.sety(xlength - 10)
    else: t.sety(t.ycor() + 20)
def tdown():
    t.direction = 'down'
    if t.ycor() - 20 < -xlength: t.sety(-xlength + 10)
    else: t.sety(t.ycor() - 20)
def tleft():
    t.direction = 'left'
    if t.xcor() - 20 < -xlength: t.setx(-xlength + 10)
    else: t.setx(t.xcor() - 20)
def tright():
    t.direction = 'right'
    if t.xcor() + 20 > xlength: t.setx(xlength - 10)
    else: t.setx(t.xcor() + 20)

# Initializing Pens
t = turtle.Turtle()
t.direction = 'up'
t.speed(0)
t.width(2)
t.ht()
t.penup()
origin = (xlength - 290,ylength - 290)
t.setposition(origin)
t.pendown()
t.shape('square')
t.color('red')

p = turtle.Turtle()
p.speed(0)
p.width(3)
p.penup()
p.pendown()
p.shape('circle')
p.ht()
p.color('blue')
p.pu()

# MST PRIM ---------------------------------------

# Initializing main lists and position
forest = []
walls = []
position = random.choice(grid_coordinates)
position = grid_coordinates[20]
forest.append(position)
# Continues until forest includes all nodes
while len(forest) < len(grid_coordinates):
    # Finding a random node that has neighbors
    random.shuffle(forest)
    for pos in forest:
        adjacent = []
        above = (pos[0], pos[1] + 40); below = (pos[0], pos[1] - 40)
        onright = (pos[0] + 40, pos[1]); onleft = (pos[0] - 40, pos[1])
        if above not in forest and above[1] < ylength: adjacent.append(above)
        if below not in forest and below[1] > -ylength: adjacent.append(below)
        if onright not in forest and onright[0] < xlength: adjacent.append(onright)
        if onleft not in forest and onleft[0] > -xlength: adjacent.append(onleft)
        if len(adjacent) >= 1:
            position = pos
            break
    # Getting a random adjacent block from node
    direction = random.choice(adjacent)
    p.penup(); p.goto(position)
    p.pendown(); p.goto(direction)
    onex = position[0]; oney = position[1]
    twox = direction[0]; twoy = direction[1]
    # Defining traverse walls
    if onex > twox and oney == twoy:
        walls.append((onex - 10, oney))
        walls.append((onex - 30, oney))
    elif onex < twox and oney == twoy:
        walls.append((onex + 10, oney))
        walls.append((onex + 30, oney))
    elif oney > twoy and onex == twox:
        walls.append((onex, oney - 10))
        walls.append((onex, oney - 30))
    elif oney < twoy and onex == twox:
        walls.append((onex, oney + 10))
        walls.append((onex, oney + 30))
    # Adding new value to forest and resetting position
    forest.append(direction)
    position = forest[random.randint(0, len(forest) - 1)]

wn.update()

# MAZE TRAVERSE ---------------------------------------
maze = walls
traveled = []
# Defining safe traveling
def can_left(maze, traveled):
    if (t.xcor() - 10, t.ycor()) not in maze and (t.xcor() - 20, t.ycor()) not in traveled and t.xcor() - 20 > -xlength: return True
    return False
def can_up(maze, traveled):
    if (t.xcor(), t.ycor() + 10) not in maze and (t.xcor(), t.ycor() + 20) not in traveled and t.ycor() + 20 < ylength: return True
    return False
def can_right(maze, traveled):
    if (t.xcor() + 10, t.ycor()) not in maze and (t.xcor() + 20, t.ycor()) not in traveled and t.xcor() + 20 < xlength: return True
    return False
def can_down(maze, traveled):
    if (t.xcor(), t.ycor() - 10) not in maze and (t.xcor(), t.ycor() - 20) not in traveled and t.ycor() - 20 > -ylength: return True
    return False
x = 0
# Main MST traverse
while len(traveled) < len(coordinates):
    if t.direction == 'up':
        if can_left(maze, traveled): tleft()
        elif can_up(maze, traveled): tup()
        elif can_right(maze, traveled): tright()
    elif t.direction == 'right':
        if can_up(maze, traveled): tup()
        elif can_right(maze, traveled): tright()
        elif can_down(maze, traveled): tdown()
    elif t.direction == 'left':
        if can_down(maze, traveled): tdown()
        elif can_left(maze, traveled): tleft()
        elif can_up(maze, traveled): tup()
    elif t.direction == 'down':
        if can_right(maze, traveled): tright()
        elif can_down(maze, traveled): tdown()
        elif can_left(maze, traveled): tleft()
    traveled.append(t.pos())
    t.color('white')
    # t.write(str(x), align='center', font=('Arial', 6, "bold"))  
    t.color('red'); x += 1
p.clear(); t.clear()
path = traveled

# ------------------------------------------------------------------------------------------------------------------

wn.update(); head.goto(path[0])
run = 0

# AI SNAKE PLAYING ALGORITHM ---------------------------------------------------------------------------------------

def hamilton(path):

    global algorithm_running, run
    algorithm_running = True

    # Neighbors of head
    onup = (head.xcor(), head.ycor() + 20)
    ondown = (head.xcor(), head.ycor() - 20)
    onleft = (head.xcor() - 20, head.ycor())
    onright = (head.xcor() + 20, head.ycor())

    go_list = []
    
    # Paramaters of exclusion in ham-cycle
    def exclude(tuple):
        #if tuple in seg_pos: return False
        # See if body exists and not out of bounds
        if len(segments) > 0:  
            if tuple in path:
                # Indexes
                headIndex = path.index(head.pos())
                tailIndex = path.index(segments[len(segments) - 1].position())
                tupleIndex = path.index(tuple)
                if headIndex < tailIndex:  # If behind Tail
                    if tupleIndex > headIndex and tupleIndex < tailIndex:
                        return True
                    return False
                elif headIndex > tailIndex:  # If ahead of tail
                    if tupleIndex not in range(tailIndex, headIndex):
                        return True
                    return False
                return True
            return False
        return True
    
    # Appending safe spots
    if exclude(onup): go_list.append(onup)
    if exclude(ondown): go_list.append(ondown)
    if exclude(onleft): go_list.append(onleft)
    if exclude(onright): go_list.append(onright)

    # Comparison items
    direction = ()
    larIndex = float('-inf')

    # Main indexes
    headIndex = path.index(head.pos())
    foodIndex = path.index(food.pos())
    
    # Finding the most efficient spot
    if len(segments) < len(coordinates) * 0.6:  # Disabling shortcuts after 60%
        if headIndex <= foodIndex:  # If behind food
            for n in go_list:
                itemIndex = path.index(n)
                if itemIndex <= foodIndex:
                    if itemIndex > larIndex:
                        larIndex = itemIndex
                        direction = n
        elif headIndex > foodIndex:  # If ahead of food
            itemIndex = {}
            wrap = len(path)
            for n in go_list:
                itemIndex[str(n)] = path.index(n)
                if itemIndex[str(n)] < headIndex:
                    itemIndex[str(n)] += wrap
            # Wrapping around to find optimal path
            if foodIndex < headIndex:
                foodIndex += wrap
            # Finding direction
            for n in go_list:
                if itemIndex[str(n)] <= foodIndex:
                    if itemIndex[str(n)] > larIndex:
                        larIndex = itemIndex[str(n)]
                        direction = n
    else:  # Following ham-cycle exactly
        run = path.index(head.pos())
        if run + 1 < len(path): run += 1
        else: run = 0
        direction = path[run]
        if run % 3 == 0: wn.update()
    
    # Traveling to spot
    head.goto(direction)


# --------------------------------------------------------------------------------------------------------------------



speed = 1

def speedUp():
    global speed
    speed = 10
def slowDown():
    global speed
    speed = 1



# Keyboard Bindings (For manual gameplay)
wn.listen()

wn.onkey(up, 'Up')
wn.onkey(down, 'Down')
wn.onkey(left, 'Left')
wn.onkey(right, 'Right')

wn.onkeypress(speedUp, 'space')
wn.onkeyrelease(slowDown, 'space')

run = 0
won = False

# Main Game Loop
while True:
    
    # Updating Screen
    wn.update()

    for s in range(speed):

        # Checking Segment positions
        # segment_positions = []
        # for seg in segments: segment_positions.append(seg.pos())
        

        # AI Algorithm
        hamilton(path)



        # If food gets eaten
        if head.pos() == food.pos():
            segment_positions = []
            for seg in segments: segment_positions.append(seg.pos())
            
            # Adds a new segment to snake
            new_segment = turtle.Turtle()
            new_segment.speed(0)
            new_segment.width(19)
            new_segment.shape('small square')
            new_segment.color('green')
            new_segment.pu()
            segments.append(new_segment)
            segment_positions.append(new_segment.pos())
            
            # Replacing food to spot that the snake is not on
            seg_pos = segment_positions[:]
            seg_pos.append(head.pos())
            # seg_pos.append(segments[len(segments) - 1].pos())
            new_position = random.choice(coordinates)
            while new_position in seg_pos:
                new_position = random.choice(coordinates)
            food.goto(new_position)

            # Score and delays
            delay -= 0.0005
            aldelay -= 0.0005

            score += 1
            if score > high_score: high_score = score
            pen.clear()
            pen.write('Score: '+str(score)+'  High Score: '+str(high_score), align='center', font=('Courier', 24, "bold"))  

        
        if len(segments) == len(path): won = True; break


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
        if algorithm_running != True: move()
        
        """
        # Checking if head hits body or walls (Dies)
        if head.pos() in segment_positions or (head.xcor() >= 280 or head.xcor() <= -280 or head.ycor() >= 280 or head.ycor() <= -280):

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
        """

        # Delays for manual gameplay
        if not algorithm_running: time.sleep(delay)

wn.mainloop()