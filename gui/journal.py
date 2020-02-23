from .pane import Pane
from item import Item

class Journal(Pane):
    def __init__(self, world):
        super(Journal, self).__init__(30, 10)
        self.world = world
        self.line_length = 30
        self.text = ''

    def apply_on(self, display):
        super().apply_on(display)
        left = self.x + 2
        title = 'Journal'
        display[1][left:left+len(title)] = list(title)

        for idx, line in enumerate(self.text.split('\n')):
            if len(line) > self.line_length:
                line = line[:self.line_length-2] + '..'
            else:
                line = line[:self.line_length]
            if idx == len(self.text.split('\n')) - 1:
                line += '|'
            display[2+idx][left:left+len(line)] = list(line)
            if idx > self.h - 6:
                break
        text = 'Press [esc] to close.'
        display[self.h-2][left:left+len(text)] = list(text)
    
    def recv_key(self, key):
        if key == 'enter':
            self.text += '\n'
        elif key == 'space':
            self.text += ' '
        elif key == 'backspace':
            self.text = self.text[:-1]
        elif len(key) == 1:
            self.text += key