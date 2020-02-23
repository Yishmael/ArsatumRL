class Pane:
    def __init__(self, x, h):
        self.x = x
        self.h = h
        if h == 0:
            self.h = 999
        
    def apply_on(self, display):
        max_x = len(display[0])
        for i in range(self.x, max_x):
            self.h = min(self.h, len(display))
            for j in range(0, self.h):
                display[j][i] = ' '
                if i in [self.x, max_x-1]:
                    display[j][i] = '|'
                if j in [0, self.h-1]:
                    if display[j][i] == '|':
                        display[j][i] = '*'
                    else:
                        display[j][i] = '-'