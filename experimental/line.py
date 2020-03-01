import math
import os
import random
import sys
import time
import signal

from pynput import keyboard

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import clear, sign, Vector, WIDTH, HEIGHT
Key = keyboard.Key

class InputHandler:
    def __init__(self):
        self.listener = keyboard.Listener(
            on_press=self.on_press_mapper,
            on_release=lambda f: None
        )
        self.x = 28
        self.y = 40
        
    def on_press_mapper(self, key):
        name = ''
        if type(key) is keyboard._win32.KeyCode:
            name = key.char
        elif type(key) is Key:
            name = key.name
        else:
            raise Exception(f'Unknown key: {key}, type:{type(key)}')
        name = str(name)
        self.on_press(name)

    def on_press(self, key):
        key = key.lower()
        d = 1
        if key == 'esc':
            os.kill(os.getpid(), signal.SIGINT)
        elif key == 'right':
            self.x += d
        elif key == 'left':
            self.x -= d
        elif key == 'up':
            self.y -= d
        elif key == 'down':
            self.y += d
        else:
            return

        clear()
        LineGen.get_line_points(Vector(30, 25), Vector(self.x, self.y))
  
    def start(self):
        self.listener.start()
    
class LineGen:
    @staticmethod
    def get_line_points(point_a: Vector, point_b: Vector):
        points = []
        grid = [list(['.']*WIDTH) for _ in range(HEIGHT)]
        
        point_b.x = min(WIDTH-3, max(0, point_b.x))
        point_b.y = min(HEIGHT-3, max(0, point_b.y))

        x1, y1 = point_a.x, point_a.x
        x2, y2 = point_b.x, point_b.y

        grid[y1][x1] = 'A'
        grid[y2][x2] = 'B'

        if y1 == y2: # horizontal line
            for x in range(min(x1, x2), max(x1, x2)):
                grid[y1][x] = '>'
                points.append(Vector(x, y1))
            print()
        elif x1 == x2: # vertical line
            for y in range(min(y1, y2), max(y1, y2)):
                grid[y][x1] = '^'
                points.append(Vector(x1, y))
            print()
        else:
            slope = (y2 - y1) / (x2 - x1)
            s = sign(slope)
            b = int(y2 - slope*x2)
            if abs(slope) < 1: # predominantly horizontal
                for x in range(min(x1, x2), max(x1, x2)):
                    y_curr = slope*x + b
                    y_next = slope*(x+s) + b
                    hyp = math.hypot(1, y_next-y_curr)
                    if x == 9:
                        print(y_curr, y_next, hyp)
                    if hyp > 1:
                        grid[int(y_curr)][x] = '#'
                        points.append(Vector(x, int(y_curr)))
                    # grid[int(y_curr+s)][x] = 'h'
            elif abs(slope) > 1: # predominantly vertical
                for y in range(min(y1, y2), max(y1, y2)):
                    x_curr = (y - b)/slope
                    x_next = (y+s - b)/slope
                    hyp = math.hypot(1, x_next-x_curr)
                    if y == 3:
                        print(x_curr, x_next, hyp)
                    if hyp > 1:
                        grid[y][int(x_curr)] = '#'
                        points.append(Vector(int(x_curr), y))
                    # grid[y+s][int(x_curr+s)] = 'v'
            else: # diagonal
                for x in range(min(x1, x2), max(x1, x2)+1):
                    y = int(slope*x + b)
                    grid[y][x] = 'd'
            print(f'B:({x2},{y2}), dy/dx:{slope}, b:{b}')

        print('\n'.join(''.join(row) for row in grid))

        return points

if __name__ == '__main__':
    WIDTH, HEIGHT = 65, 52
    input_handler = InputHandler()
    input_handler.start()
    clear()
    LineGen.get_line_points(Vector(30, 25), Vector(28, 40))

time.sleep(9999)
