import math
import os
import sys


WIDTH, HEIGHT = 65, 15
# WIDTH, HEIGHT = 165, 40

def get_icon(name):
    if 'You' in name:
        return '@'
    elif 'white rat' in name:
        return 'r'
    elif 'coyote' in name:
        return 'C'
    elif 'cave bat' in name:
        return 'b'
    elif 'stick' in name:
        return '/'
    elif 'torch' in name:
        return '/'
    elif 'flask' in name or 'potion' in name:
        return '!'
    elif 'scroll' in name:
        return '?'
    elif 'meal' in name:
        return '%'
    elif 'sweater' in name or 'barrel top' in name:
        return '['
    elif 'puddle' in name:
        return '~'
    elif 'glass shard' in name:
        return ','
    elif 'cloud' in name:
        return '*'
    else:
        return '('

def within_bounds(x, y):
    return 0 <= x < WIDTH and 0 <= y < HEIGHT

class Loader:
    @staticmethod
    def load_grid(filename):
        if os.getcwd().endswith('arsatum'):
            path = f'zones/{filename}'
        else:
            path = f'../zones/{filename}'
        with open(path) as f:
            return [list(line) for line in f.read().split('\n')]

class Vector:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
    def __iter__(self):
        return iter((self.x, self.y))
    # def __getitem__(self, idx):
    #     if idx == 0:
    #         return self.x
    #     elif idx == 1:
    #         return self.y
    def __eq__(self, other):
        if type(other) is Vector:
            return self.x == other.x and self.y == other.y
        return self.x == other[0] and self.y == other[1]
    def __repr__(self):
        return f'Vector({self.x}, {self.y})'

def clear():
    if 'idlelib' in sys.modules:
        print('\n'*10)
    else:
        os.system('cls')

def sign(n):
    return -1 if n < 0 else 1 if n > 0 else 0

def get_direction(start, end):
    return Vector(sign(end[0]-start[0]), sign(end[1]-start[1]))

def distance_between(o1, o2):
    return abs(o1.x - o2.x) + abs(o1.y - o2.y) - \
        min(abs(o1.x - o2.x), abs(o1.y - o2.y))

def distance_between_points(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1]) - \
        min(abs(p1[0] - p2[0]), abs(p1[1] - p2[1]))

def get_dir(key):
    if key == 'home':
        return (-1, -1)
    elif key == 'up':
        return (0, -1)
    elif key == 'page_up':
        return (1, -1)
    elif key == 'left':
        return (-1, 0)
    elif key == 'right':
        return (1, 0)
    elif key == 'end':
        return (-1, 1)
    elif key == 'down':
        return (0, 1)
    elif key == 'page_down':
        return (1, 1)

class Vision:
    def __init__(self, display):
        self.display = display
        self.points = []

    def add_source(self, center, radius):
        center = Vector(center[0], center[1])
        if radius == 1:        
            for y in range(HEIGHT):
                for x in range(WIDTH):
                    if abs(x - center.x) <= 1:
                        if abs(y - center.y) <= 1:
                            if abs(y - center.y) <= 1:
                                self.points.append(Vector(x, y))
        elif radius == 2:
            for y in range(HEIGHT):
                for x in range(WIDTH):
                    dist = math.hypot(x-center.x, y-center.y)
                    if dist <= radius:
                        self.points.append(Vector(x, y))
        elif radius == 3:
            for y in range(HEIGHT):
                for x in range(WIDTH):
                    if y == center.y:
                        if abs(x-center.x) <= 3:
                            self.points.append(Vector(x, y))
                    elif x == center.x:
                        if abs(y-center.y) <= 2:
                            self.points.append(Vector(x, y))
                    else:
                        if abs(x-center.x) <= 2 and abs(y-center.y) <= 1:
                            self.points.append(Vector(x, y))
        else:
            for y in range(HEIGHT):
                for x in range(WIDTH):
                    if math.hypot(x - center.x, (y - center.y)*1.3) <= radius:
                        self.points.append(Vector(x, y))

    def add_line(self, source, target):
        for point in get_line_points(Vector(source.x, source.y), Vector(target.x, target.y)):
            self.points.append(point)
                        
    def apply(self):
        old_display = list(list(row) for row in self.display)
        for y in range(HEIGHT):
            for x in range(WIDTH):
                self.display[y][x] = ' '
        for point in self.points:
            x, y = point.x, point.y
            self.display[y][x] = old_display[y][x]
            
    def reset(self):
        self.points.clear()
    
# TODO fix line missing when points are close to each other
def get_line_points(point_a: Vector, point_b: Vector):
    points = []
    grid = [list(['.']*WIDTH) for _ in range(HEIGHT)]
    
    point_b.x = min(WIDTH-3, max(0, point_b.x))
    point_b.y = min(HEIGHT-3, max(0, point_b.y))

    x1, y1 = point_a.x, point_a.y
    x2, y2 = point_b.x, point_b.y

    grid[y1][x1] = 'A'
    grid[y2][x2] = 'B'

    if y1 == y2: # horizontal line
        for x in range(min(x1, x2), max(x1, x2)):
            grid[y1][x] = '>'
            points.append(Vector(x, y1))
        # print()
    elif x1 == x2: # vertical line
        for y in range(min(y1, y2), max(y1, y2)):
            grid[y][x1] = '^'
            points.append(Vector(x1, y))
        # print()
    else:
        slope = (y2 - y1) / (x2 - x1)
        s = sign(slope)
        b = int(y2 - slope*x2)
        if abs(slope) < 1: # predominantly horizontal
            for x in range(min(x1, x2), max(x1, x2)):
                y_curr = slope*x + b
                y_next = slope*(x+s) + b
                hyp = math.hypot(1, y_next-y_curr)
                # if x == 9:
                #     print(y_curr, y_next, hyp)
                if hyp > 1:
                    grid[int(y_curr)][x] = '#'
                    points.append(Vector(x, int(y_curr)))
                # grid[int(y_curr+s)][x] = 'h'
        elif abs(slope) > 1: # predominantly vertical
            for y in range(min(y1, y2), max(y1, y2)):
                x_curr = (y - b)/slope
                x_next = (y+s - b)/slope
                hyp = math.hypot(1, x_next-x_curr)
                # if y == 3:
                #     print(x_curr, x_next, hyp)
                if hyp > 1:
                    grid[y][int(x_curr)] = '#'
                    points.append(Vector(int(x_curr), y))
                # grid[y+s][int(x_curr+s)] = 'v'
        else: # diagonal
            for x in range(min(x1, x2), max(x1, x2)+1):
                y = int(slope*x + b)
                grid[y][x] = 'd'
        # print(f'B:({x2},{y2}), dy/dx:{slope}, b:{b}')

    # print('\n'.join(''.join(row) for row in grid))

    return points