#AUTOR = GUSTAVO ANDRÉ


class Grid:
    def __init__(self, width,height, scl):
        self.scl = scl
        self.grid=[]
        self.personalize = False

        for x in range(width/self.scl):
            self.grid.append([])            
            for y in range(height/self.scl):  
                
                self.grid[x].append( [int(x*scl), int(y*scl)])
                
    def update(self):
        if(click):
            x = int(mouseX/self.scl)
            y = int(mouseY/self.scl)
            self.grid[x][y] = [None, None]
            self.personalize = True
                    
    def show(self):
        for x in range(len(self.grid)):
            for y in range(len(self.grid[0])):
                if(None in self.grid[x][y]):
                    fill(0)
                    xx = int(x * self.scl)+self.scl/2
                    yy = int(y * self.scl)+self.scl/2
                    ellipse(xx,yy,self.scl/2,self.scl/2)
                    
                    
class Knot:
    def __init__(self, x,y, grid,previous = None):
        self.x = x
        self.y = y
        self.previous = previous
        self.Grid = grid
        self.grid = grid.grid
        self.scl = grid.scl
        
    def addKnot(self, list_open, list_close):
        paths = []
        operation = [-1,0,1]
        for x in operation:
            for y in operation:
                vector = Knot(self.x+x, self.y+y, self.Grid, previous=self)
                _, itemInOpen = itemInArray(list_open, vector)
                _, itemInClose = itemInArray(list_close, vector)
                if(
                   vector.x > -1 and vector.x < len(self.grid) and
                   vector.y > -1 and vector.y < len(self.grid[-1]) and
                   not itemInOpen and
                   not itemInClose and
                   None not in self.grid[vector.x][vector.y]
                ):
                    paths.append(vector)
                
        return paths
    
    def show(self):
        noStroke()        
        rect(self.grid[self.x][self.y][0], self.grid[self.x][self.y][1], self.scl, self.scl)



def heuristic(a, b):
    return int(dist(a.x, a.y, b.x, b.y))
                                             
def calc_path(knot, end):
    path = []    
    
    current = knot 
    value = heuristic(knot, end)
    
    path.append(current)
    
    while(current.previous != None):
        current = current.previous        
        path.append(current)

    value += len(path)
    
    if len(path) > 1:
        return (path, value)
    else:
        return ([knot], 1000)

def calc_better_path(knots, end):
    smaller = 100000
    selected = None
    for knot in knots: 
        path, value = calc_path(knot, end)
        if(value <= smaller):
            smaller = value
            selected = path          

    return selected if selected else []

def itemInArray(arr, elm):
    for item in arr:
        if(elm.x == item.x and elm.y == item.y):
            return (arr.index(item), True)
        
    return (-1, False)
                                                                                                                                                                                            
#### class's
scl = 400/25                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         
grid = Grid(400,400,scl)

#### variable

end = Knot(len(grid.grid)-1, len(grid.grid[-1])-1, grid)

#### array
better_path = []
list_open = []
list_close = []

#### event pressed ####
click = False
runner = False


#### commands
origin = Knot(0,0,grid)
list_open.append(Knot(0,0,grid))

def setup():
    
    size(400,400)
    
    
def grid_random():
    for x in range(len(grid.grid)):
        for y in range(len(grid.grid[-1])):
            if(x == origin.x and y == origin.y or x == end.x and y == end.y): continue
            else:
                if(random(0,1) <= 0.4):
                    grid.grid[x][y] = [None, None]
    
def draw():
    global frame, better_path, list_open, runner
    background(255,20)
    ##print(len(list_open))

    if(not runner):
        #if(not grid.personalize): grid_random()
        # grid.update()
        grid_random()
        runner = True
        
    else:
        
        _, endInClose = itemInArray(list_open, end)
        if(not endInClose):
            knots = calc_better_path(list_open, end)
            for item in knots:
                id, condiction = itemInArray(list_open, item)
                if(condiction):
                    list_open.pop(id)        
            if(len(knots) > 0):
                selected = knots[0]
                list_close.append(selected)
                paths = selected.addKnot(list_open, list_close)
                
                if(len(paths) > 0):
                    for k in paths:
                        list_open.append(k)
            else:
                print("no solution")
                noLoop()
            
                

        else:
            print("DONE!")
            better_path = calc_better_path(list_open, end)
            
    for k in list_open:

        fill(0,255,0)
        k.show()
        
    for k in list_close:

        fill(0,0,255)
        k.show()
    fill(255,244,0)
    end.show()
    grid.show()    
    
    if(len(better_path) > 0):
        noFill();
        stroke(255, 0, 200);
        strokeWeight(scl / 2);
        beginShape();
        
        for k in better_path:
            vertex(k.x * scl + scl / 2, k.y * scl + scl / 2);
            
        endShape()
        noLoop()
    

    
    
def mouseClicked():
    global click
    click = not click

    
def keyTyped():
    global runner
    if(key == ' '):
        runner = True    
