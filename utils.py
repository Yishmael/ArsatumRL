import math
import os
import sys

WIDTH, HEIGHT = 65, 12
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
        return ''
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

def apply_fov(player, display, radius=1):
    if radius == 1:        
        for y in range(len(display)):
            for x in range(len(display[0])):
                if abs(x - player.x) > 1:
                    if abs(x - player.x) > 1:
                        display[y][x] = ' '
                if abs(y - player.y) > 1:
                    if abs(y - player.y) > 1:
                        display[y][x] = ' '
    elif radius == 2:
        for y in range(len(display)):
            for x in range(len(display[0])):
                dist = math.hypot(x-player.x, y-player.y)
                if dist > radius:
                    display[y][x] = ' '
    elif radius == 3:
        for y in range(len(display)):
            for x in range(len(display[0])):
                if y == player.y:
                    if abs(x-player.x) > 3:
                        display[y][x] = ' '
                elif x == player.x:
                    if abs(y-player.y) > 2:
                        display[y][x] = ' '
                else:
                    if abs(x-player.x) > 2 or abs(y-player.y) > 1:
                        display[y][x] = ' '