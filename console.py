import sys
import time

import curses


if 'idlelib' in sys.modules:
    sys.__stdout__ = open('stdout.txt', 'w')

class Console():
    def __init__(self):
        self.window = curses.initscr()
        curses.start_color()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_BLUE, curses.COLOR_WHITE)

        self.grid = []
        #[self.grid.append(['x']*65) for _ in range(30)]

        #curses.wrapper(main)
    
    def close(self):
        curses.endwin()
            
    def draw(self):
        #curses.start_color()
        # Clear screen
        if not self.window:
            return
        self.window.clear()
        #curses.echo()
        #curses.setsyx(10, 30)
        self.window.move(20, 15)
        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                self.window.addstr(i, j, self.grid[i][j], curses.color_pair(1))

        #self.window.refresh()

    def _set_tile(self, x, y, string, color=1):
        if not self.window:
            return
        self.grid[y][x] = string[0]
        self.window.addstr(y, x, string, curses.color_pair(color))
        self.window.refresh()

    def _set_grid(self, x, y, w, h, char, color=1):
        if not self.window:
            return
        for j in range(y, y + h):
            self.grid[j][x] = char
            self.window.addstr(0, 20, char, curses.color_pair(1))
            self.window.addstr(j, x, char*w, curses.color_pair(color))
        self.window.refresh()

    def update_display(self, display):
        if not self.grid:
            self.grid = [list(row) for row in display]
            #self.grid = []
            #[self.grid.append(['x']*65) for _ in range(30)]
            
        c = 0
        self.draw()
        for i in range(len(display)):
            for j in range(len(display[0])):
                if self.grid[i][j] != display[i][j]:
                    char = display[i][j]
                    self.grid[i][j] = char
                    self.window.addstr(i, j, char, curses.color_pair(2))
                    c += 1
        self.window.addstr(15, 0, 'count:'+str(c), curses.color_pair(2))
        self.window.move(16, 0)
        self.window.refresh()


def main(screen):
    pass
curses.wrapper(main)

if __name__ == '__main__':
    console = Console()

    #[console.grid.append(['x']*65) for _ in range(30)]
    for _ in range(50):
        console._set_grid(2, 2, 20, 20, '.', 1)
    for _ in range(2):
        time.sleep(1)
        
        for i in range(1, 5):
            console._set_tile(4, 2 + i%20, 'b', i)
            time.sleep(0.2)
        #console.draw()
        a = console.window.getkey()
        console._set_tile(0, 0, str(a), 4)